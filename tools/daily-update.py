#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Almalaeb V2 — التحديث اليومي للبيانات (ESPN public API — بلا مفتاح، بلا اشتراك).

المصدر: ESPN public API (site.api.espn.com + sports.core.api.espn.com).
يغطي الدوريات الأوروبية الخمسة (eng.1, esp.1, ita.1, ger.1, fra.1).
البطولة المغربية غير موجودة في ESPN إطلاقاً (mar.1 → 404) — تُدمج يدوياً من
data/botola-manual.json (انظر تعليمات التحديث اليدوي أسفل هذا الملف).

ما يفعله السكربت كل صباح (بتوقيت المغرب):
  1) يجلب مباريات اليوم + 4 أيام قادمة، ونتائج آخر 14 يوماً، من ESPN scoreboard.
  2) يجلب جدول كل دوري من سجلات الفرق (core API team record) — مرتب بالنقاط/فرق الأهداف.
  3) يجلب الهدافين (core API leaders) ويترجم الأسماء عبر data/player-names.json.
  4) يجلب تفاصيل كل نتيجة منتهية (إحصائيات + أحداث الأهداف + الملعب) من summary.
  5) يدمج البطولة من data/botola-manual.json.
  6) يتحقق من البيانات (عدد الصفوف، النقاط = 3×فوز + تعادل، لا قيم فارغة)،
     ثم يكتب data/leagues.json + data/fixtures.json بشكل ذري، ويعيد البناء
     عبر tools/build-v2.py.

قواعد السلامة (لا تُكسر أبداً):
  - لا يكتب رقماً لم يجلبه من ESPN أو من botola-manual.json.
  - عند فشل جلب أي دوري كامل: يخرج بخطأ (exit != 0) ويترك البيانات القديمة كما هي.
  - عند فشل تفاصيل مباراة واحدة (summary): تُحفظ النتيجة بلا إحصائيات + تحذير.
  - لا يخترع ترجمة عربية للاعب غير موجود في player-names.json: يعرض الاسم
    اللاتيني كما هو ويسجّل تحذيراً.

تعليمات التحديث اليدوي للبطولة (كل صباح، قبل تشغيل السكربت):
  افتح data/botola-manual.json وحدّث من جدول FRMF.ma (أو ويكيبيديا 2026–27
  Botola Pro المنقولة عن FRMF.ma): حقل updated (تاريخ اليوم)، والجدول الكامل
  (16 فريقاً)، والهدافين العشرة، ومباريات الجولة القادمة (التاريخ + التوقيت
  بتوقيت المغرب)، ونتائج الجولة الأخيرة. إن لم يتغير شيء، يكفي تحديث حقل
  updated. إن كان الملف أقدم من 3 أيام، يطبع السكربت تحذيراً واضحاً في الملخص.

التشغيل:
  cd ~/workspace/almalaeb-v2 && python3 tools/daily-update.py
  (الكـرون اليومي يُنشئه الوكيل الرئيسي — لا تُنشئه من هنا.)
"""
import json
import os
import re
import subprocess
import sys
import unicodedata
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
# توقيت المغرب: UTC+1 دائماً إلا في رمضان (UTC+0). تحذير: tzdata هذا الجهاز
# خاطئة للمغرب في 2026 (تعطي +00 في نونبر!) — لذلك لا نعتمد على ZoneInfo هنا.
# نوافذ رمضان (تقريبية — تُحدَّث سنوياً): 2026: 15 فبراير–22 مارس،
# 2027: 7 مارس–7 أبريل، 2028: 25 فبراير–27 مارس.
from datetime import timezone as _tz, timedelta as _td
_MOROCCO_PLUS1 = _tz(_td(hours=1))
_RAMADAN_UTC0 = [("2026-02-15", "2026-03-22"), ("2027-03-07", "2027-04-07"),
                 ("2028-02-25", "2028-03-27")]


def morocco_tz(d):
    iso = d.isoformat() if hasattr(d, "isoformat") else str(d)
    for a, b in _RAMADAN_UTC0:
        if a <= iso <= b:
            return _tz.utc
    return _MOROCCO_PLUS1


TZ = _MOROCCO_PLUS1
TODAY = datetime.now(_MOROCCO_PLUS1).date()
TODAY_ISO = TODAY.isoformat()
AR_MONTHS = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
             "يوليوز", "غشت", "شتنبر", "أكتوبر", "نونبر", "دجنبر"]
AR_WEEKDAYS = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]

LEAGUES = [
    {"id": "premier-league", "espn": "eng.1", "rows": 20},
    {"id": "la-liga",       "espn": "esp.1", "rows": 20},
    {"id": "serie-a",       "espn": "ita.1", "rows": 20},
    {"id": "bundesliga",    "espn": "ger.1", "rows": 18},
    {"id": "ligue-1",       "espn": "fra.1", "rows": 18},
]
BOTOLA_ID = "botola"
FIX_WINDOW_DAYS = 4      # اليوم + 4 أيام (يغطي عطلة نهاية الأسبوع)
RES_WINDOW_DAYS = 14     # نتائج آخر 14 يوماً (آخر جولة مكتملة)
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AlmalaebV2-daily/1.0"}
SITE = "https://site.api.espn.com/apis/site/v2/sports/soccer"
CORE = "https://sports.core.api.espn.com/v2/sports/soccer"

WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)
    print(f"  ⚠️  {msg}", file=sys.stderr)


def ar_date(iso):
    """2026-11-20 -> 'الجمعة 20 نونبر 2026' ; '20 نونبر' if short=True."""
    d = date.fromisoformat(iso) if isinstance(iso, str) else iso
    return f"{AR_WEEKDAYS[d.weekday()]} {d.day} {AR_MONTHS[d.month - 1]} {d.year}"


def ar_date_short(iso):
    d = date.fromisoformat(iso) if isinstance(iso, str) else iso
    return f"{d.day} {AR_MONTHS[d.month - 1]}"


def ar_range(d1, d2):
    """'21–23 نونبر 2026' أو '30 نونبر – 2 دجنبر 2026'."""
    a, b = date.fromisoformat(d1), date.fromisoformat(d2)
    if a.month == b.month and a.year == b.year:
        return f"{a.day}–{b.day} {AR_MONTHS[a.month - 1]} {a.year}"
    return f"{a.day} {AR_MONTHS[a.month - 1]} – {b.day} {AR_MONTHS[b.month - 1]} {b.year}"


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def https(u):
    return u.replace("http://", "https://")


# ------------------------------------------------------------------ maps ---
def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


LOGOS = load_json(os.path.join(DATA, "logos.json"))
PLAYER_NAMES = load_json(os.path.join(DATA, "player-names.json"))["names"]

STOP = {"fc", "afc", "acf", "ca", "as", "ac", "sc", "sv", "tsg", "rcd", "rc", "us",
        "cf", "cfc", "cd", "ud", "sd", "ss", "ssc", "losc", "estac", "sco", "fsv",
        "real", "club", "de", "la", "le", "di",
        "calcio", "fussball", "olympique", "stade", "ogc", "brestois",
        "alsace", "bc", "milano"}


def _norm(s):
    """تطبيع اسم فريق للمطابقة: إزالة التشكيل (Alavés→alaves)، أحرف صغيرة، حذف البادئات."""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return " ".join(t for t in s.split() if t not in STOP and not t.isdigit()).strip()


EN2AR = {}
EN2SLUG = {}
for _c in LOGOS["clubs"]:
    EN2AR[_norm(_c["en"])] = _c["ar"]
    EN2SLUG[_norm(_c["en"])] = _c["slug"]
# أسماء ESPN المختلفة جذرياً عن logos.json (Cologne=Köln، Hamburg=Hamburger…)
TEAM_ALIASES = {
    "cologne": "koln",
    "hamburg": "hamburger",
    "lyon": "lyonnais",
    "deportivo": "deportivo coruna",   # ESPN 'Deportivo' = ديبورتيفو لاكورونيا (وليس ألافيس)
    "internazionale": "inter milan",
    "inter": "inter milan",
    "mainz": "fsv mainz",
}
# حالات خاصة لا يطابقها التطبيع إطلاقاً
TEAM_AR_DIRECT = {"brest": "بريست"}
TEAM_SLUG_DIRECT = {"brest": "brest"}


def _resolve_team(espn_name):
    """اسم ESPN -> مفتاح التطبيع في logos.json (أو None)."""
    n = _norm(espn_name)
    if n in TEAM_AR_DIRECT:
        return None  # يُحلّ عبر TEAM_AR_DIRECT مباشرة
    if n in EN2AR:
        return n
    if n in TEAM_ALIASES and _norm(TEAM_ALIASES[n]) in EN2AR:
        return _norm(TEAM_ALIASES[n])
    # مطابقة جزئية وحيدة: الاسم المختصر جزء من اسم واحد فقط (athletic ⊂ athletic bilbao)
    cands = [k for k in EN2AR if k and n and (n in k or k in n)]
    if len(cands) == 1:
        return cands[0]
    return None


def team_ar(espn_name):
    n = _norm(espn_name)
    if n in TEAM_AR_DIRECT:
        return TEAM_AR_DIRECT[n]
    key = _resolve_team(espn_name)
    return EN2AR.get(key) if key else None


def team_slug(espn_name):
    n = _norm(espn_name)
    if n in TEAM_SLUG_DIRECT:
        return TEAM_SLUG_DIRECT[n]
    key = _resolve_team(espn_name)
    if key and key in EN2SLUG:
        return EN2SLUG[key]
    return re.sub(r"[^a-z0-9]+", "-", espn_name.lower()).strip("-")


def player_ar(latin_name):
    if latin_name in PLAYER_NAMES:
        return PLAYER_NAMES[latin_name]
    warn(f"لاعب بلا ترجمة عربية في data/player-names.json: {latin_name} — يُعرض باللاتينية")
    return latin_name


# الملاعب: الاسم الإنجليزي (ESPN) -> الاسم العربي المعروض (من بياناتنا الموثقة)
VENUES = {
    "Allianz Arena": "أليانز أرينا، ميونيخ",
    "Allianz Riviera": "أليانز ريفييرا، نيس",
    "Allianz Stadium": "أليانز ستاديوم، تورينو",
    "Anfield": "أنفيلد، ليفربول",
    "Stadio Olimpico": "الملعب الأولمبي، روما",
    "BayArena": "باي أرينا، ليفركوزن",
    "Borussia-Park": "بوروسيا بارك، مونشنغلادباخ",
    "San Siro": "سان سيرو، ميلانو",
    "San Mamés": "سان ماميس، بلباو",
    "St. James' Park": "سانت جيمس بارك، نيوكاسل",
    "Santiago Bernabéu": "سانتياغو برنابيو، مدريد",
    "Signal Iduna Park": "سيغنال إيدونا بارك، دورتموند",
    "Vitality Stadium": "فيتاليتي ستاديوم، بورنموث",
    "Villa Park": "فيلا بارك، برمنغهام",
    "Coventry Building Society Arena": "كوفنتري بيلدينغ سوسايتي أرينا، كوفنتري",
    "MKM Stadium": "ملعب MKM، هال",
    "WWK Arena": "ملعب WWK، أوغسبورغ",
    "Stadion An der Alten Försterei": "ملعب آلته فورستيري، برلين",
    "Stadio Artemio Franchi": "ملعب أرتيميو فرانكي، فلورنسا",
    "Etihad Stadium": "ملعب الاتحاد، مانشستر",
    "Stade Pierre-Mauroy": "ملعب بيير موروا، ليل",
    "Tottenham Hotspur Stadium": "ملعب توتنهام هوتسبير، لندن",
    "Gtech Community Stadium": "ملعب جيتك كوميونيتي، لندن",
    "Stadio Diego Armando Maradona": "ملعب دييغو أرماندو مارادونا، نابولي",
    "Gewiss Stadium": "ملعب غيويس، بيرغامو",
    "Stade de l'Aube": "ملعب لوب، تروا",
    "Stadio Luigi Ferraris": "ملعب لويجي فيراريس، جنوى",
    "MEWA Arena": "ملعب ميوا، ماينز",
    "Stade Vélodrome": "ملعب فيلودروم، مارسيليا",
    "Parc des Princes": "حديقة الأمراء، باريس",
    "Camp Nou": "كامب نو، برشلونة",
    "Emirates Stadium": "ملعب الإمارات، لندن",
    "Stamford Bridge": "ستامفورد بريدج، لندن",
    "London Stadium": "ملعب لندن",
    "Old Trafford": "أولد ترافورد، مانشستر",
    "Stadio Giuseppe Meazza": "سان سيرو، ميلانو",
    # ملاعب إضافية (من نتائج/مباريات نونبر 2026 — أسماء موثقة)
    "American Express Stadium": "ملعب أميكس، برايتون",
    "Balaidos": "بالايدوس، فيغو",
    "Craven Cottage": "كرافن كوتاج، لندن",
    "Decathlon Arena - Stade Pierre-Mauroy": "ملعب بيير موروا، ليل",
    "Deutsche Bank Park": "دويتشه بنك بارك، فرانكفورت",
    "El Sadar": "إل سادار، بامبلونا",
    "El Sardineros": "إل ساردينيرو، سانتاندير",
    "Elland Road": "إيلاند رود، ليدز",
    "Ennio Tardini": "ملعب إنيو تارديني، بارما",
    "Estadi Ciutat de València": "ملعب سيوتات دي فالنسيا، فالنسيا",
    "Estadio Coliseum": "ملعب كوليسيوم، خيتافي",
    "Estadio Martínez Valero": "ملعب مارتينيز فاليرو، إلتشي",
    "Estadio de Vallecas": "ملعب فاييكاس، مدريد",
    "Estadio de la Cerámica": "ملعب لا سيراميكا، فياريال",
    "Europa-Park Stadion": "ملعب أوروبا بارك، فرايبورغ",
    "Giuseppe Sinigaglia": "ملعب جوزيبي سينيغاليا، كومو",
    "Hill Dickinson Stadium": "ملعب هيل ديكنسون، ليفربول",
    "Home Deluxe Arena": "ملعب هوم ديلوكس أرينا، بادربورن",
    "La Rosaleda": "لا روزاليدا، مالقا",
    "MHPArena": "إم إتش بي أرينا، شتوتغارت",
    "Mapei Stadium": "ملعب مابي، ريجيو إميليا",
    "Mendizorrotza": "مينديزوروتزا، فيتوريا",
    "Mestalla Stadium": "ميستايا، فالنسيا",
    "New Balance Arena": "ملعب نيو بالانس أرينا، لايبزيغ",
    "Olimpico": "الملعب الأولمبي، روما",
    "Portman Road": "بورتمان رود، إيبسويتش",
    "PreZero Arena": "بريزيرو أرينا، سينسهايم",
    "RCDE Stadium": "ملعب آر سي دي إي، برشلونة",
    "Ramón Sánchez Pizjuán Stadium": "رامون سانشيز بيزخوان، إشبيلية",
    "Reale Arena": "ريالي أرينا، سان سيباستيان",
    "Red Bull Arena": "ريد بول أرينا، لايبزيغ",
    "Renato Dall'Ara": "ملعب ريناتو دالارا، بولونيا",
    "RheinEnergieStadion": "ملعب راين إنرجي، كولن",
    "Riyadh Air Metropolitano": "ملعب ميتروبوليتانو، مدريد",
    "Roazhon Park": "روازون بارك، رين",
    "Selhurst Park": "سيلهرست بارك، لندن",
    "Spotify Camp Nou": "كامب نو، برشلونة",
    "Stade Bollaert-Delelis": "ملعب بولارت ديليليس، لنس",
    "Stade Francis-Le Blé": "ملعب فرانسيس لو بليه، بريست",
    "Stade Jean Bouin": "ملعب جان بوان، باريس",
    "Stade Louis II": "ملعب لويس الثاني، موناكو",
    "Stade Marie-Marvingt": "ملعب ماري مارفينغ، لومان",
    "Stade Océane": "ملعب أوسيان، لوهافر",
    "Stade Raymond Kopa": "ملعب ريمون كوبا، أنجيه",
    "Stade de l'Abbé-Deschamps": "ملعب آبي ديشان، أوكسير",
    "Stade de la Meinau": "ملعب لامينو، ستراسبورغ",
    "Stade du Moustoir - Yves Allainmat": "ملعب موستوار، لوريان",
    "Stadio Olimpico Grande Torino": "الملعب الأولمبي الكبير، تورينو",
    "Stadio Pier Luigi Penzo": "ملعب بيير لويجي بينزو، البندقية",
    "Stadium Municipal de Toulouse": "الملعب البلدي، تولوز",
    "Stadium of Light": "ملعب النور، سندرلاند",
    "The City Ground": "سيتي غراوند، نوتنغهام",
    "The MKM Stadium": "ملعب MKM، هال",
    "U-Power Stadium": "ملعب يو باور، مونزا",
    "URSAPHARM-Arena an der Kaiserlinde": "ملعب أورسافارم أرينا، إلفرسبرغ",
    "Unipol Domus": "أونيبول دوموس، كالياري",
    "Veltins Arena": "فيلتينس أرينا، غيلسنكيرشن",
    "Volksparkstadion": "فولكسبارك شتاديون، هامبورغ",
    "Weserstadion": "فيزر شتاديون، بريمن",
}


def venue_ar(espn_venue):
    if not espn_venue:
        return "قيد التأكيد"
    if espn_venue in VENUES:
        return VENUES[espn_venue]
    low = espn_venue.lower()
    for k, v in VENUES.items():
        if k.lower() == low:
            return v
    return espn_venue


# حقوق البث في المغرب/الشرق الأوسط (معروفة وثابتة، ليست رقماً يُجلب يومياً)
CHANNEL_EU = "beIN Sports"
CHANNEL_BOTOLA = "Arryadia TNT"

# ------------------------------------------------------------- ESPN fetch --
def parse_event(ev, league_id, league_name):
    """حدث واحد من scoreboard -> قاموس مباراة في مخطط الموقع."""
    comp = ev["competitions"][0]
    cs = comp["competitors"]
    home = next(c for c in cs if c["homeAway"] == "home")
    away = next(c for c in cs if c["homeAway"] == "away")
    h_ar, a_ar = team_ar(home["team"]["displayName"]), team_ar(away["team"]["displayName"])
    if not h_ar or not a_ar:
        raise ValueError(f"فريق بلا اسم عربي: {home['team']['displayName']} / {away['team']['displayName']}")
    # التاريخ/الوقت بتوقيت المغرب (ESPN يعطي UTC؛ morocco_tz لأن tzdata الجهاز خاطئة)
    dt_utc = datetime.fromisoformat(ev["date"].replace("Z", "+00:00"))
    dt = dt_utc.astimezone(morocco_tz(dt_utc.date()))
    m = {
        "id": f"{team_slug(home['team']['displayName'])}-{team_slug(away['team']['displayName'])}-{dt.date().isoformat()}",
        "home": h_ar, "away": a_ar,
        "league": league_id, "league_name": league_name,
        "date": dt.date().isoformat(),
        "source": f"ESPN (site.api.espn.com) — {ar_date_short(dt.date().isoformat())} {dt.year}",
        "venue": venue_ar((comp.get("venue") or {}).get("fullName")),
        "channel": CHANNEL_EU,
    }
    st = comp["status"]["type"]
    state, completed = st.get("state"), st.get("completed", False)
    if completed:
        # منتهية — ESPN يستخدم STATUS_FULL_TIME (وليس STATUS_FINAL)
        m["home_goals"] = int(home.get("score", 0))
        m["away_goals"] = int(away.get("score", 0))
        m["status"] = "finished"
        m["espn_event_id"] = ev["id"]
    elif state == "in":
        m["home_goals"] = int(home.get("score", 0))
        m["away_goals"] = int(away.get("score", 0))
        m["status"] = "live"
        m["minute"] = comp["status"].get("displayClock", "").replace("'", "")
        m["espn_event_id"] = ev["id"]
    elif state == "pre":
        m["time"] = dt.strftime("%H:%M")
        m["status"] = "scheduled"
    else:
        # مؤجلة/ملغاة (STATUS_POSTPONED / STATUS_CANCELED…) — لا تُعرض كمباراة قادمة
        return None
    return m


def fetch_scoreboard_day(espn_code, day):
    url = f"{SITE}/{espn_code}/scoreboard?dates={day.strftime('%Y%m%d')}"
    return fetch(url).get("events", [])


def fetch_league_events(lg, old_league):
    """مباريات + نتائج + مباشر لدوري واحد في النوافذ المحددة."""
    days_fix = [TODAY + timedelta(days=i) for i in range(FIX_WINDOW_DAYS + 1)]
    days_res = [TODAY - timedelta(days=i) for i in range(1, RES_WINDOW_DAYS + 1)]
    events = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(fetch_scoreboard_day, lg["espn"], d): d
                for d in days_fix + days_res}
        for fut in as_completed(futs):
            try:
                events.extend(fut.result())
            except Exception as e:
                raise RuntimeError(f"فشل جلب scoreboard {lg['espn']} يوم {futs[fut]}: {e}")
    upcoming, results, live = [], [], []
    seen = set()
    for ev in events:
        try:
            m = parse_event(ev, lg["id"], old_league["name"])
        except ValueError as e:
            warn(f"{lg['id']}: {e} — تُستبعد المباراة")
            continue
        if m is None:
            continue  # مؤجلة/ملغاة — لا تُعرض
        if m["id"] in seen:
            continue
        seen.add(m["id"])
        if m["status"] == "scheduled":
            upcoming.append(m)
        elif m["status"] == "finished":
            results.append(m)
        elif m["status"] == "live":
            live.append(m)
    upcoming.sort(key=lambda x: (x["date"], x.get("time", "")))
    results.sort(key=lambda x: (x["date"]), reverse=True)
    return upcoming, results, live


def fetch_standings(lg):
    """الجدول من سجلات الفرق (core API) — مرتب بالنقاط ثم فرق الأهداف ثم الأهداف."""
    teams = fetch(f"{CORE}/leagues/{lg['espn']}/seasons/2026/teams?lang=en&region=us&limit=30")["items"]

    def one(t):
        tid = t["$ref"].split("/teams/")[1].split("?")[0]
        team = fetch(f"{CORE}/leagues/{lg['espn']}/seasons/2026/teams/{tid}?lang=en&region=us")
        rec = fetch(https(team["record"]["$ref"]))
        item = rec["items"][0]
        st = {s["name"]: s["value"] for s in item["stats"]}
        ar = team_ar(team["displayName"])
        if not ar:
            raise ValueError(f"فريق بلا اسم عربي في الجدول: {team['displayName']}")
        return {"team": ar, "p": int(st["gamesPlayed"]), "w": int(st.get("wins", 0)),
                "d": int(st["ties"]), "l": int(st["losses"]),
                "gf": int(st["pointsFor"]), "ga": int(st["pointsAgainst"]),
                "gd": int(st["pointDifferential"]), "pts": int(st["points"])}

    with ThreadPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(one, teams))
    rows.sort(key=lambda r: (-r["pts"], -r["gd"], -r["gf"], -r["w"]))
    for i, r in enumerate(rows, 1):
        r2 = {"pos": i}
        r2.update(r)
        rows[i - 1] = r2
    if len(rows) != lg["rows"]:
        raise RuntimeError(f"جدول {lg['id']}: {len(rows)} صفاً بدل {lg['rows']}")
    return rows


def fetch_scorers(lg):
    """الهدافون العشرة من core API leaders (يُحلّ $ref اللاعب والفريق)."""
    data = fetch(f"{CORE}/leagues/{lg['espn']}/seasons/2026/types/1/leaders?lang=en&region=us")
    leaders = None
    for cat in data.get("categories", []):
        if cat.get("name") == "goals":
            leaders = cat.get("leaders", [])
            break
    if not leaders:
        raise RuntimeError(f"لا قائمة هدافين من ESPN لـ {lg['id']}")
    def one(ld):
        ath = fetch(https(ld["athlete"]["$ref"]))
        team = fetch(https(ld["team"]["$ref"]))
        team_name = team_ar(team["displayName"])
        if not team_name:
            warn(f"{lg['id']}: فريق هداف بلا اسم عربي: {team['displayName']}")
            return None
        full = ath.get("fullName") or ath.get("displayName")
        return {"player": player_ar(full), "team": team_name,
                "goals": int(ld["value"])}
    with ThreadPoolExecutor(max_workers=8) as ex:
        out = [x for x in ex.map(one, leaders[:10]) if x]
    out.sort(key=lambda s: -s["goals"])
    return out[:10]


def fetch_match_details(lg_espn, match):
    """تفاصيل نتيجة منتهية: إحصائيات + أحداث الأهداف/البطاقات + الملعب + الحكم."""
    try:
        s = fetch(f"{SITE}/{lg_espn}/summary?event={match['espn_event_id']}")
    except Exception as e:
        warn(f"تعذّر جلب تفاصيل {match['home']} × {match['away']}: {e}")
        return
    stats = {}
    try:
        for side, key in ((0, "home"), (1, "away")):
            team_stats = s["boxscore"]["teams"][side]["statistics"]
            d = {x["name"]: x.get("displayValue") for x in team_stats}
            def num(name):
                v = d.get(name)
                if v is None:
                    return None
                return int(float(str(v).replace("%", "")))
            stats[f"possession_{key}"] = num("possessionPct")
            stats[f"shots_{key}"] = num("totalShots")
            stats[f"shots_on_target_{key}"] = num("shotsOnTarget")
            stats[f"corners_{key}"] = num("wonCorners")
        if all(v is not None for v in stats.values()):
            stats["source"] = f"ESPN (site.api.espn.com) — {ar_date_short(match['date'])} {match['date'][:4]}"
            match["stats"] = stats
    except Exception as e:
        warn(f"إحصائيات ناقصة لـ {match['home']} × {match['away']}: {e}")
    try:
        venue = (s.get("gameInfo") or {}).get("venue", {})
        if venue.get("fullName"):
            match["venue"] = venue_ar(venue["fullName"])
        officials = s.get("officials") or []
        if officials:
            match["referee"] = officials[0].get("displayName", "قيد التحقق")
    except Exception:
        pass
    try:
        evs = []
        for ke in s.get("keyEvents", []) or []:
            # الهدف = scoringPlay (علم ESPN نفسه) — أنواعه متعددة: goal،
            # goal---header، goal---penalty، penalty---scored…
            if not ke.get("scoringPlay"):
                continue
            parts = ke.get("participants") or []
            name = ""
            if parts:
                name = ((parts[0].get("athlete") or {}).get("displayName") or "")
            team_name = team_ar((ke.get("team") or {}).get("displayName", "")) or ""
            minute = (ke.get("clock") or {}).get("displayValue", "").replace("'", "")
            evs.append({"minute": minute,
                        "team": team_name,
                        "player": player_ar(name) if name else "",
                        "type": "هدف"})  # كل أنواع الأهداف (goal / goal---header / goal---penalty…)
        if evs:
            match["events"] = evs
    except Exception as e:
        warn(f"أحداث ناقصة لـ {match['home']} × {match['away']}: {e}")


# ------------------------------------------------------------------ Botola --
def load_botola(old_league):
    """يدمج البطولة من data/botola-manual.json؛ عند أي مشكلة يُبقي القديم + تحذير."""
    path = os.path.join(DATA, "botola-manual.json")
    try:
        manual = load_json(path)
    except Exception as e:
        warn(f"botola-manual.json غير مقروء ({e}) — تُبقى بيانات البطولة القديمة")
        return old_league, [], []
    upd = manual.get("updated", "")
    try:
        age = (TODAY - date.fromisoformat(upd)).days
        if age > 3:
            warn(f"بيانات البطولة اليدوية قديمة ({upd} — منذ {age} أيام) — حدّث data/botola-manual.json")
    except Exception:
        warn("حقل updated في botola-manual.json غير صالح")
    if len(manual.get("table", [])) != 16 or len(manual.get("scorers", [])) != 10:
        warn("botola-manual.json ناقص (الجدول 16 / الهدافون 10) — تُبقى بيانات البطولة القديمة")
        return old_league, [], []
    league = dict(old_league)
    league["table"] = manual["table"]
    league["scorers"] = manual["scorers"]
    league["round"] = manual.get("round", old_league.get("round", ""))
    league["next_round"] = manual.get("next_round", old_league.get("next_round", ""))
    league["source"] = manual.get("source", old_league.get("source", ""))
    league["meta"] = (f"جدول ترتيب البطولة الاحترافية المغربية 2026-27: "
                      f"{manual['table'][0]['team']} متصدر بـ{manual['table'][0]['pts']} نقطة، "
                      f"{manual['table'][1]['team']} {manual['table'][1]['pts']}، "
                      f"{manual['table'][2]['team']} {manual['table'][2]['pts']} — "
                      f"{manual['scorers'][0]['player']} هداف البطولة بـ{manual['scorers'][0]['goals']} أهداف، "
                      f"مباريات {manual.get('next_round', '')} والنتائج.")
    fx = manual.get("fixtures", []) or []
    res = manual.get("results", []) or []
    for m in fx + res:
        m.setdefault("channel", CHANNEL_BOTOLA)
        m.setdefault("source", f"FRMF.ma / ويكيبيديا — {upd}")
    return league, fx, res

# -------------------------------------------------------------- validation --
def validate(leagues, fixtures):
    errs = []
    if len(leagues) != 6:
        errs.append(f"الدوريات: {len(leagues)} بدل 6")
    expected_rows = {"premier-league": 20, "la-liga": 20, "serie-a": 20,
                     "bundesliga": 18, "ligue-1": 18, "botola": 16}
    for lg in leagues:
        n = expected_rows.get(lg["id"])
        if len(lg.get("table", [])) != n:
            errs.append(f"{lg['id']}: الجدول {len(lg.get('table', []))} صفاً بدل {n}")
        for r in lg.get("table", []):
            expect_pts = 3 * r["w"] + r["d"] - r.get("deduction", 0)
            if r["pts"] != expect_pts:
                errs.append(f"{lg['id']} {r['team']}: النقاط {r['pts']} ≠ 3×{r['w']}+{r['d']}-خصم{r.get('deduction', 0)}")
            if r["p"] != r["w"] + r["d"] + r["l"] or r["gd"] != r["gf"] - r["ga"]:
                errs.append(f"{lg['id']} {r['team']}: حسابات الجدول غير متسقة")
            if any(v is None for v in r.values()):
                errs.append(f"{lg['id']} {r['team']}: قيمة فارغة في الجدول")
        if len(lg.get("scorers", [])) != 10:
            errs.append(f"{lg['id']}: الهدافون {len(lg.get('scorers', []))} بدل 10")
        for s in lg.get("scorers", []):
            if not s.get("player") or not s.get("team") or not s.get("goals"):
                errs.append(f"{lg['id']}: هداف ناقص: {s}")
    ids = set()
    for m in fixtures["upcoming"] + fixtures["results"] + fixtures["live"]:
        for k in ("home", "away", "league", "date"):
            if not m.get(k):
                errs.append(f"مباراة ناقصة {k}: {m.get('id')}")
        if m["id"] in ids:
            errs.append(f"مباراة مكررة: {m['id']}")
        ids.add(m["id"])
    for m in fixtures["upcoming"]:
        if not m.get("time"):
            errs.append(f"مباراة قادمة بلا توقيت: {m['id']}")
    for m in fixtures["results"]:
        if m.get("home_goals") is None or m.get("away_goals") is None:
            errs.append(f"نتيجة بلا أهداف: {m['id']}")
    if errs:
        raise RuntimeError("فشل التحقق:\n  - " + "\n  - ".join(errs))


# -------------------------------------------------------------------- main --
def main():
    old_leagues = load_json(os.path.join(DATA, "leagues.json"))
    old_fx = load_json(os.path.join(DATA, "fixtures.json"))
    old_by_id = {l["id"]: l for l in old_leagues["leagues"]}
    new_leagues = []
    all_upcoming, all_results, all_live = [], [], []
    changes = []

    for lg in LEAGUES:
        old = old_by_id[lg["id"]]
        print(f"[{lg['id']}] جلب المباريات والنتائج من ESPN…")
        upcoming, results, live = fetch_league_events(lg, old)
        print(f"[{lg['id']}] جلب الجدول (سجلات الفرق)…")
        table = fetch_standings(lg)
        print(f"[{lg['id']}] جلب الهدافين…")
        scorers = fetch_scorers(lg)
        # تفاصيل النتائج (إحصائيات + أحداث) — فشل الواحدة لا يوقف التشغيل
        espn_code = lg["espn"]
        with ThreadPoolExecutor(max_workers=8) as ex:
            list(ex.map(lambda m: fetch_match_details(espn_code, m), results))
        for m in results + upcoming + live:
            m.pop("espn_event_id", None)
        # الجولة: عدد المباريات الملعوبة / الجولة القادمة من تواريخ المباريات
        played = max(r["p"] for r in table)
        lg_fx = [m for m in upcoming if m["league"] == lg["id"]]
        if lg_fx:
            d1, d2 = lg_fx[0]["date"], lg_fx[-1]["date"]
            next_round = f"الجولة {played + 1} — {ar_range(d1, d2)}"
        else:
            next_round = f"الجولة {played + 1} — التاريخ قيد التأكيد"
        top = table[:3]
        meta = (f"جدول ترتيب {old['name']} 2026-27: {top[0]['team']} في الصدارة "
                f"بـ{top[0]['pts']} نقطة، {top[1]['team']} {top[1]['pts']}، "
                f"{top[2]['team']} {top[2]['pts']} — {scorers[0]['player']} هداف الدوري "
                f"بـ{scorers[0]['goals']} أهداف، مباريات {next_round} والنتائج.")
        new_leagues.append({
            "id": lg["id"], "name": old["name"], "short": old["short"],
            "country": old["country"], "season": old.get("season", "2026-27"),
            "round": f"الجولة {played}",
            "next_round": next_round,
            "source": f"ESPN (site.api.espn.com + sports.core.api.espn.com) — {ar_date(TODAY_ISO)} — الهدافون: ESPN",
            "table": table, "scorers": scorers, "meta": meta,
        })
        all_upcoming += upcoming
        all_results += results
        all_live += live
        # ملخص التغييرات مقابل القديم
        old_top = [(r["team"], r["pts"]) for r in old["table"][:3]]
        new_top = [(r["team"], r["pts"]) for r in table[:3]]
        if old_top != new_top:
            changes.append(f"{lg['id']}: الصدارة {old_top} ← {new_top}")
        old_sc = [(s["player"], s["goals"]) for s in old["scorers"][:3]]
        new_sc = [(s["player"], s["goals"]) for s in scorers[:3]]
        if old_sc != new_sc:
            changes.append(f"{lg['id']}: الهدافون {old_sc} ← {new_sc}")

    # البطولة (يدوي)
    print("[botola] دمج البيانات اليدوية…")
    bot_league, bot_fx, bot_res = load_botola(old_by_id[BOTOLA_ID])
    new_leagues.append(bot_league)
    all_upcoming += [m for m in bot_fx if m.get("status") != "finished"]
    all_results += [m for m in bot_fx if m.get("status") == "finished"] + bot_res

    # ترتيب الدوريات كما في الموقع
    order = ["premier-league", "la-liga", "serie-a", "bundesliga", "ligue-1", "botola"]
    new_leagues.sort(key=lambda l: order.index(l["id"]))
    all_upcoming.sort(key=lambda x: (x["date"], x.get("time", "")))
    all_results.sort(key=lambda x: x["date"], reverse=True)
    tomorrow = (TODAY + timedelta(days=1)).isoformat()
    today_fx = [m for m in all_upcoming if m["date"] == TODAY_ISO]
    tomorrow_fx = [m for m in all_upcoming if m["date"] == tomorrow]
    next_day = all_upcoming[0]["date"] if all_upcoming else None
    if today_fx:
        note = (f"{ar_date(TODAY_ISO)}: {len(today_fx)} مباراة اليوم في الدوريات الستة. "
                f"الأوقات بتوقيت المغرب (UTC+1).")
    elif next_day:
        note = (f"{ar_date(TODAY_ISO)}: لا مباريات اليوم في الدوريات الستة. "
                f"العودة {ar_date(next_day)} ({len([m for m in all_upcoming if m['date'] == next_day])} مباريات). "
                f"الأوقات بتوقيت المغرب (UTC+1).")
    else:
        note = f"{ar_date(TODAY_ISO)}: لا مباريات قادمة مسجلة. الأوقات بتوقيت المغرب (UTC+1)."

    new_leagues_doc = {
        "updated": TODAY_ISO,
        "leagues": new_leagues,
        "note": f"الجداول الكاملة موثقة لكل دوري (آخر تحقق {ar_date(TODAY_ISO)}). المصدر: ESPN + FRMF.ma للبطولة.",
    }
    new_fx_doc = {
        "updated": TODAY_ISO,
        "today_date": TODAY_ISO,
        "tomorrow_date": tomorrow,
        "note": note,
        "live": all_live,
        "today": today_fx,
        "tomorrow": tomorrow_fx,
        "upcoming": all_upcoming,
        "results": all_results[:60],
    }
    validate(new_leagues, new_fx_doc)

    # كتابة ذرية + إعادة البناء (مع استرجاع النسخ القديمة عند فشل البناء)
    backups = {}
    for name in ("leagues.json", "fixtures.json"):
        p = os.path.join(DATA, name)
        backups[name] = open(p, encoding="utf-8").read()
    try:
        for name, doc in (("leagues.json", new_leagues_doc), ("fixtures.json", new_fx_doc)):
            tmp = os.path.join(DATA, f".{name}.tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(doc, f, ensure_ascii=False, indent=2)
            os.replace(tmp, os.path.join(DATA, name))
        print("إعادة البناء: python3 tools/build-v2.py …")
        r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build-v2.py")],
                           cwd=ROOT, capture_output=True, text=True, timeout=600)
        if r.returncode != 0:
            raise RuntimeError(f"فشل البناء:\n{r.stdout}\n{r.stderr}")
    except Exception:
        for name, content in backups.items():
            with open(os.path.join(DATA, name), "w", encoding="utf-8") as f:
                f.write(content)
        raise

    # ------------------------------------------------------------- summary --
    print()
    print(f"✅ التحديث اليومي اكتمل — {ar_date(TODAY_ISO)}")
    print(f"   المصدر: ESPN public API (بلا مفتاح) + البطولة يدوياً (data/botola-manual.json)")
    print(f"   مباريات اليوم: {len(today_fx)} | غداً: {len(tomorrow_fx)} | "
          f"قادمة ({FIX_WINDOW_DAYS + 1} أيام): {len(all_upcoming)} | "
          f"نتائج (آخر {RES_WINDOW_DAYS} يوماً): {len(new_fx_doc['results'])} | مباشرة الآن: {len(all_live)}")
    print(f"   نتائج بإحصائيات: {sum(1 for m in new_fx_doc['results'] if m.get('stats'))} | "
          f"بأحداث أهداف: {sum(1 for m in new_fx_doc['results'] if m.get('events'))}")
    if changes:
        print("   تغييرات عن أمس:")
        for c in changes:
            print(f"   - {c}")
    else:
        print("   لا تغيير في الصدارة ولا في أول 3 هدافين عن أمس.")
    if WARNINGS:
        print(f"   تحذيرات ({len(WARNINGS)}):")
        for w in WARNINGS:
            print(f"   - {w}")
    else:
        print("   بلا تحذيرات.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ فشل التحديث اليومي — البيانات القديمة لم تُمس:\n{e}", file=sys.stderr)
        sys.exit(1)
