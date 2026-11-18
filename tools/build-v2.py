# -*- coding: utf-8 -*-
"""Almalaeb V2 builder — rebuilds ~/workspace/almalaeb-v2 from V1 data + VERIFIED data only.
Run: python3 tools/build-v2.py  (from inside almalaeb-v2/)
Every number in data/ below was verified 2026-11-18 from the sources listed
in REPORT.md. Anything unverified is an explicit placeholder, never invented.
"""
import json, os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V1 = os.path.expanduser("~/workspace/almalaeb")
CHECKED = "2026-11-18"

# ---------------------------------------------------------------- data ---
# Tables: TOP 5 ONLY — verified 2026-11-18 (KickoffLens, updated 02:22 UTC,
# cross-checked TheStatsAPI / NBC Sports / laligatable.co).
# gf/ga only where verified; gd always verified. None = not verified.
def row(pos, team, p, w, d, l, gd, pts, gf=None, ga=None):
    return {"pos": pos, "team": team, "p": p, "w": w, "d": d, "l": l,
            "gf": gf, "ga": ga, "gd": gd, "pts": pts}

LEAGUES = [
 {"id": "premier-league", "name": "الدوري الإنجليزي الممتاز", "short": "البريميرليغ",
  "country": "إنجلترا", "season": "2026-27", "round": "الجولة 10",
  "next_round": "الجولة 11 — 21–23 نونبر 2026",
  "source": "kickofflens.com (تحديث 18 نونبر 2026 02:22 UTC) + مطابقة مع thestatsapi.com وnbcsports.com",
  "table": [
   row(1, "آرسنال", 10, 9, 0, 1, 10, 27, 15, 5),
   row(2, "برايتون", 10, 7, 1, 2, 19, 22),
   row(3, "مانشستر سيتي", 10, 7, 0, 3, 8, 21, 21, 13),
   row(4, "ليفربول", 10, 5, 3, 2, 4, 18),
   row(5, "تشيلسي", 10, 5, 1, 4, 3, 16)],
  "scorers": [
   {"player": "إيرلينغ هالاند", "team": "مانشستر سيتي", "goals": 9},
   {"player": "ألكسندر إيزاك", "team": "ليفربول", "goals": 7},
   {"player": "تيرنو باري", "team": "—", "goals": 6},
   {"player": "نيكولاس جاكسون", "team": "—", "goals": 6}],
  "meta": "جدول ترتيب الدوري الإنجليزي الممتاز 2026-27: آرسنال في الصدارة بـ27 نقطة، برايتون 22، مانشستر سيتي 21 — الهدافون، مباريات الجولة 11 (21–23 نونبر) والنتائج."},
 {"id": "la-liga", "name": "الدوري الإسباني", "short": "الليغا",
  "country": "إسبانيا", "season": "2026-27", "round": "الجولة 12",
  "next_round": "الجولة 13 — 20–23 نونبر 2026",
  "source": "kickofflens.com (18 نونبر 2026) + مطابقة مع laligatable.co وthestatsapi.com",
  "table": [
   row(1, "برشلونة", 12, 11, 0, 1, 35, 33, 48, 13),
   row(2, "ريال مدريد", 12, 10, 0, 2, 21, 30, 31, 10),
   row(3, "أتلتيكو مدريد", 12, 9, 1, 2, 13, 28),
   row(4, "ريال بيتيس", 12, 8, 2, 2, 5, 26),
   row(5, "ريال سوسيداد", 12, 7, 1, 4, 1, 22)],
  "scorers": [
   {"player": "رافينيا", "team": "برشلونة", "goals": 15},
   {"player": "كيليان مبابي", "team": "ريال مدريد", "goals": 13},
   {"player": "لامين يامال", "team": "برشلونة", "goals": 10}],
  "meta": "جدول ترتيب الدوري الإسباني 2026-27: برشلونة متصدر بـ33 نقطة، ريال مدريد 30، أتلتيكو 28 — رافينيا هداف الليغا بـ15 هدفاً، مباريات الجولة 13 والنتائج."},
 {"id": "serie-a", "name": "الدوري الإيطالي", "short": "الكالتشيو",
  "country": "إيطاليا", "season": "2026-27", "round": "الجولة 11",
  "next_round": "الجولة 12 — 21–23 نونبر 2026",
  "source": "kickofflens.com (18 نونبر 2026) + مطابقة مع oddalerts.com",
  "table": [
   row(1, "لاتسيو", 11, 9, 2, 0, 16, 29),
   row(2, "إنتر ميلان", 11, 9, 1, 1, 15, 28),
   row(3, "روما", 11, 8, 3, 0, 21, 27),
   row(4, "ميلان", 11, 7, 3, 1, 10, 24),
   row(5, "كومو", 11, 7, 2, 2, 8, 23)],
  "scorers": [
   {"player": "غوستافو فاريلا", "team": "—", "goals": 9},
   {"player": "أنتونيو رايموندو", "team": "—", "goals": 8},
   {"player": "دونييل مالين", "team": "—", "goals": 8},
   {"player": "نيكولا كرستوفيتش", "team": "—", "goals": 7}],
  "meta": "جدول ترتيب الدوري الإيطالي 2026-27: لاتسيو في الصدارة بـ29 نقطة، إنتر 28، روما 27 — الهدافون، مباريات الجولة 12 (21–23 نونبر) والنتائج."},
 {"id": "bundesliga", "name": "الدوري الألماني", "short": "البوندسليغا",
  "country": "ألمانيا", "season": "2026-27", "round": "الجولة 9",
  "next_round": "الجولة 10 — 20–22 نونبر 2026",
  "source": "kickofflens.com (18 نونبر 2026) + مطابقة مع oddalerts.com وchief-scout.com",
  "table": [
   row(1, "بايرن ميونيخ", 9, 6, 3, 0, 20, 21, 29, 9),
   row(2, "بوروسيا دورتموند", 9, 6, 3, 0, 9, 21, 16, 7),
   row(3, "فرايبورغ", 9, 6, 1, 2, 10, 19),
   row(4, "لايبزيغ", 9, 6, 0, 3, 14, 18),
   row(5, "باير ليفركوزن", 9, 5, 1, 3, 3, 16)],
  "scorers": [
   {"player": "نيكلاس فولكروغ", "team": "—", "goals": 9},
   {"player": "باتريك شيك", "team": "—", "goals": 8},
   {"player": "مايكل أوليز", "team": "—", "goals": 6}],
  "meta": "جدول ترتيب الدوري الألماني 2026-27: بايرن ميونيخ ودورتموند متساويان بـ21 نقطة، فرايبورغ 19 — الهدافون، مباريات الجولة 10 (20–22 نونبر) والنتائج."},
 {"id": "ligue-1", "name": "الدوري الفرنسي", "short": "الليغ 1",
  "country": "فرنسا", "season": "2026-27", "round": "الجولة 10",
  "next_round": "الجولة 11 — 20–22 نونبر 2026",
  "source": "kickofflens.com (18 نونبر 2026) + مطابقة مع oddalerts.com",
  "table": [
   row(1, "باريس سان جيرمان", 10, 7, 2, 1, 12, 23),
   row(2, "ليل", 10, 6, 3, 1, 7, 21),
   row(3, "باريس إف سي", 10, 6, 2, 2, 7, 20),
   row(4, "مارسيليا", 10, 6, 0, 4, 8, 18),
   row(5, "ليون", 10, 5, 2, 3, 6, 17)],
  "scorers": [
   {"player": "لاسين سينايوكو", "team": "—", "goals": 9},
   {"player": "إستيبان لوبول", "team": "—", "goals": 7},
   {"player": "أمين غويري", "team": "—", "goals": 6},
   {"player": "إلي واهي", "team": "—", "goals": 6}],
  "meta": "جدول ترتيب الدوري الفرنسي 2026-27: باريس سان جيرمان متصدر بـ23 نقطة، ليل 21، باريس إف سي 20 — الهدافون، مباريات الجولة 11 (20–22 نونبر) والنتائج."},
 {"id": "botola", "name": "البطولة الاحترافية المغربية", "short": "البطولة",
  "country": "المغرب", "season": "2026-27", "round": "الجولة 7",
  "next_round": "الجولة 8 — التاريخ قيد التأكيد",
  "source": "le360.ma (09 نونبر 2026) + pitchlabstats.com (جدول 08 نونبر 2026) — المركز 3 غير موثق",
  "table": [
   row(1, "الكوكب المراكشي", 7, 5, 1, 1, 4, 16, 10, 6),
   row(2, "النادي المكناسي", None, None, None, None, None, 14),
   {"pos": 3, "team": "— قيد التحقق —", "p": None, "w": None, "d": None,
    "l": None, "gf": None, "ga": None, "gd": None, "pts": None, "placeholder": True},
   row(4, "الجيش الملكي", 6, 3, 2, 1, 4, 11, 9, 5),
   row(5, "الوداد الرياضي", None, None, None, None, None, 11),
   row(6, "المغرب الفاسي", 7, 3, 2, 2, 1, 11, 6, 5)],
  "scorers": [],
  "meta": "جدول ترتيب البطولة الاحترافية المغربية 2026-27: الكوكب المراكشي متصدر بـ16 نقطة، النادي المكناسي 14، الجيش الملكي 11 — مباريات الجولة 8 والنتائج."},
]

# Fixtures — times are Morocco time (UTC+1). time=None = time not verified.
def fx(fid, home, away, league, league_name, date, time, source, date_label=None):
    d = {"id": fid, "home": home, "away": away, "league": league,
         "league_name": league_name, "date": date, "time": time,
         "status": "scheduled", "source": source}
    if date_label:
        d["date_label"] = date_label
    return d

UPCOMING = [
 # Friday 20 Nov 2026
 fx("bayern-koln-2026-11-20", "بايرن ميونيخ", "كولن", "bundesliga", "الدوري الألماني",
    "2026-11-20", "20:30", "kickofflens.com + football.mib.news (19:30 UTC)"),
 fx("athletic-espanyol-2026-11-20", "أتلتيك بلباو", "إسبانيول", "la-liga", "الدوري الإسباني",
    "2026-11-20", "21:00", "kickofflens.com + football.mib.news (20:00 UTC)"),
 fx("troyes-lehavre-2026-11-20", "تروا", "لوهافر", "ligue-1", "الدوري الفرنسي",
    "2026-11-20", "20:45", "vavel.com (14:45 ET = 19:45 UTC) + football.mib.news"),
 # Saturday 21 Nov 2026 — Premier League MW11 (UK times +1h = Morocco)
 fx("man-city-fulham-2026-11-21", "مانشستر سيتي", "فولهام", "premier-league", "الدوري الإنجليزي",
    "2026-11-21", "13:30", "premierleague.com + nbcsports.com (12:30 UK)"),
 fx("aston-villa-sunderland-2026-11-21", "أستون فيلا", "سندرلاند", "premier-league", "الدوري الإنجليزي",
    "2026-11-21", "16:00", "premierleague.com (15:00 UK)"),
 fx("bournemouth-nottingham-2026-11-21", "بورنموث", "نوتينغهام فورست", "premier-league", "الدوري الإنجليزي",
    "2026-11-21", "16:00", "premierleague.com (15:00 UK)"),
 fx("coventry-crystal-palace-2026-11-21", "كوفنتري سيتي", "كريستال بالاس", "premier-league", "الدوري الإنجليزي",
    "2026-11-21", "16:00", "livescore.in + premierleague.com (15:00 UK)"),
 fx("tottenham-ipswich-2026-11-21", "توتنهام", "إيبسويتش تاون", "premier-league", "الدوري الإنجليزي",
    "2026-11-21", "16:00", "livescore.in + premierleague.com (15:00 UK)"),
 fx("newcastle-arsenal-2026-11-21", "نيوكاسل يونايتد", "آرسنال", "premier-league", "الدوري الإنجليزي",
    "2026-11-21", "18:30", "premierleague.com + nbcsports.com (17:30 UK)"),
 # Saturday 21 Nov — other leagues
 fx("real-madrid-celta-2026-11-21", "ريال مدريد", "سيلتا فيغو", "la-liga", "الدوري الإسباني",
    "2026-11-21", None, "laligatable.co (المباراة المقبلة لريال مدريد — التوقيت قيد التأكيد)"),
 fx("union-leipzig-2026-11-21", "يونيون برلين", "لايبزيغ", "bundesliga", "الدوري الألماني",
    "2026-11-21", "15:30", "fcstats.com (09:30 ET = 15:30 CET)"),
 fx("leverkusen-paderborn-2026-11-21", "باير ليفركوزن", "بادربورن", "bundesliga", "الدوري الألماني",
    "2026-11-21", "15:30", "fcstats.com (09:30 ET = 15:30 CET)"),
 fx("gladbach-dortmund-2026-11-21", "بوروسيا مونشنغلادباخ", "بوروسيا دورتموند", "bundesliga", "الدوري الألماني",
    "2026-11-21", "15:30", "fcstats.com (09:30 ET = 15:30 CET)"),
 fx("augsburg-mainz-2026-11-21", "أوغسبورغ", "ماينز", "bundesliga", "الدوري الألماني",
    "2026-11-21", "15:30", "fcstats.com (09:30 ET = 15:30 CET)"),
 fx("nice-psg-2026-11-21", "نيس", "باريس سان جيرمان", "ligue-1", "الدوري الفرنسي",
    "2026-11-21", "17:15", "vavel.com (11:15 ET = 16:15 UTC)"),
 fx("lille-lyon-2026-11-21", "ليل", "ليون", "ligue-1", "الدوري الفرنسي",
    "2026-11-21", "20:45", "vavel.com (14:45 ET = 19:45 UTC)"),
 # Sunday 22 Nov 2026
 fx("hull-brighton-2026-11-22", "هال سيتي", "برايتون", "premier-league", "الدوري الإنجليزي",
    "2026-11-22", "15:00", "livescore.in (06:00 PT = 14:00 UTC)"),
 fx("liverpool-manutd-2026-11-22", "ليفربول", "مانشستر يونايتد", "premier-league", "الدوري الإنجليزي",
    "2026-11-22", "18:30", "premierleague.com + nbcsports.com (16:30 UK)"),
 fx("barcelona-villarreal-2026-11-22", "برشلونة", "فياريال", "la-liga", "الدوري الإسباني",
    "2026-11-22", None, "laligatable.co (المباراة المقبلة لبرشلونة — التوقيت قيد التأكيد)"),
 fx("atalanta-inter-2026-11-22", "أتالانتا", "إنتر ميلان", "serie-a", "الدوري الإيطالي",
    "2026-11-22", None, "showupandplay.com (عطلة نهاية الأسبوع 21–23 نونبر — اليوم الدقيق قيد التأكيد)",
    date_label="21–23 نونبر 2026"),
 fx("juventus-venezia-2026-11-22", "يوفنتوس", "فينيزيا", "serie-a", "الدوري الإيطالي",
    "2026-11-22", None, "منشور فيسبوك FAFG (عطلة نهاية الأسبوع 21–23 نونبر — اليوم الدقيق قيد التأكيد)",
    date_label="21–23 نونبر 2026"),
 # Monday 23 Nov 2026
 fx("brentford-everton-2026-11-23", "برينتفورد", "إيفرتون", "premier-league", "الدوري الإنجليزي",
    "2026-11-23", "21:00", "livescore.in (12:00 PT = 20:00 UTC)"),
]

# Last verified results: final weekend before the international break (7–8 Nov 2026).
# Day-per-match NOT individually verified — grouped as one weekend, source noted.
RESULTS = [
 {"id": "mainz-bayern-2026-11-08", "home": "ماينز", "away": "بايرن ميونيخ",
  "home_goals": 1, "away_goals": 2, "league": "bundesliga", "league_name": "الدوري الألماني",
  "date": "2026-11-08", "status": "finished", "source": "showupandplay.com (تقرير 08 نونبر 2026)"},
 {"id": "dortmund-elversberg-2026-11-08", "home": "بوروسيا دورتموند", "away": "إلفرسبرغ",
  "home_goals": 2, "away_goals": 1, "league": "bundesliga", "league_name": "الدوري الألماني",
  "date": "2026-11-08", "status": "finished", "source": "showupandplay.com (تقرير 08 نونبر 2026)"},
 {"id": "napoli-lazio-2026-11-08", "home": "نابولي", "away": "لاتسيو",
  "home_goals": 1, "away_goals": 1, "league": "serie-a", "league_name": "الدوري الإيطالي",
  "date": "2026-11-08", "status": "finished", "source": "showupandplay.com (تقرير 08 نونبر 2026)"},
 {"id": "inter-como-2026-11-08", "home": "إنتر ميلان", "away": "كومو",
  "home_goals": 2, "away_goals": 0, "league": "serie-a", "league_name": "الدوري الإيطالي",
  "date": "2026-11-08", "status": "finished", "source": "showupandplay.com (تقرير 08 نونبر 2026)"},
 {"id": "roma-sassuolo-2026-11-08", "home": "روما", "away": "ساسولو",
  "home_goals": 3, "away_goals": 0, "league": "serie-a", "league_name": "الدوري الإيطالي",
  "date": "2026-11-08", "status": "finished", "source": "showupandplay.com (تقرير 08 نونبر 2026)"},
 {"id": "genoa-milan-2026-11-08", "home": "جنوى", "away": "ميلان",
  "home_goals": 1, "away_goals": 2, "league": "serie-a", "league_name": "الدوري الإيطالي",
  "date": "2026-11-08", "status": "finished", "source": "showupandplay.com (تقرير 08 نونبر 2026)"},
 {"id": "fiorentina-juventus-2026-11-08", "home": "فيورنتينا", "away": "يوفنتوس",
  "home_goals": 2, "away_goals": 2, "league": "serie-a", "league_name": "الدوري الإيطالي",
  "date": "2026-11-08", "status": "finished", "source": "showupandplay.com (تقرير 08 نونبر 2026)"},
]

ALLOWED = ["premier-league", "la-liga", "serie-a", "bundesliga", "ligue-1", "botola"]
LEAGUE_BY_ID = {l["id"]: l for l in LEAGUES}

def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def dump(path, obj):
    w(path, json.dumps(obj, ensure_ascii=False, indent=2) + "\n")

# ------------------------------------------------------------- CSS add ---
CSS_ADD = """
/* ---------- الملعب V2: إضافات ---------- */
.cpa-slot {
  border: 1.5px dashed var(--gold); border-radius: 12px; background: #171208;
  color: var(--muted); text-align: center; padding: 18px 14px; margin: 22px 0;
  font-size: .88rem;
}
.cpa-slot b { color: var(--gold); display: block; font-size: .95rem; margin-bottom: 4px; }
.cpa-slot small { display: block; margin-top: 6px; font-size: .75rem; }
.data-note {
  background: #0d1424; border: 1px solid var(--border); border-right: 3px solid var(--accent);
  border-radius: 10px; padding: 10px 14px; color: var(--muted); font-size: .82rem; margin: 14px 0;
}
.data-note b { color: var(--text); }
.league-chips { display: flex; gap: 8px; flex-wrap: wrap; padding: 14px 0 4px; }
.league-chips a {
  background: var(--card); border: 1px solid var(--border); color: var(--text);
  padding: 8px 16px; border-radius: 30px; font-weight: 700; font-size: .88rem;
}
.league-chips a:hover { border-color: var(--accent); color: var(--accent); }
.date-strip { display: flex; gap: 10px; flex-wrap: wrap; margin: 16px 0; }
.date-strip .day {
  flex: 1; min-width: 150px; background: var(--card); border: 1px solid var(--border);
  border-radius: 12px; padding: 12px 14px; text-align: center;
}
.date-strip .day b { display: block; font-size: 1rem; }
.date-strip .day span { color: var(--muted); font-size: .82rem; }
.date-strip .day.next { border-color: var(--accent); }
.date-strip .day.next b { color: var(--accent); }
.match-link { display: block; }
.match-link:hover .match-row { border-color: var(--accent); }
.match-row .date-lbl { font-size: .78rem; color: var(--muted); white-space: nowrap; }
.placeholder-box {
  background: var(--card); border: 1px dashed var(--border); border-radius: 12px;
  padding: 22px; text-align: center; color: var(--muted);
}
.verified-tag {
  display: inline-block; background: rgba(34,224,122,.15); color: var(--accent);
  border: 1px solid rgba(34,224,122,.4); font-size: .72rem; font-weight: 700;
  padding: 2px 10px; border-radius: 20px;
}
.stat-row { display: grid; grid-template-columns: 44px 1fr 44px; align-items: center; gap: 10px; margin-bottom: 10px; font-size: .88rem; }
.stat-bar { height: 8px; background: #0b0f1c; border-radius: 6px; overflow: hidden; display: flex; }
.stat-bar i { display: block; height: 100%; }
.stat-bar i.h { background: var(--accent); }
.stat-bar i.a { background: var(--blue); margin-inline-start: auto; }
.timeline { list-style: none; }
.timeline li { padding: 10px 4px; border-bottom: 1px solid var(--border); font-size: .92rem; }
.timeline li:last-child { border-bottom: none; }
.timeline .min { color: var(--gold); font-weight: 800; margin-inline-end: 8px; }
.scoreboard {
  background: linear-gradient(135deg, #14264a, #0e2b1a); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 26px 18px; text-align: center; margin: 18px 0;
}
.scoreboard .teams { display: flex; align-items: center; justify-content: center; gap: 18px; flex-wrap: wrap; }
.scoreboard .team-name { font-size: 1.25rem; font-weight: 800; }
.scoreboard .big-score { font-size: 2.4rem; font-weight: 800; background: #0b0f1c; border: 1px solid var(--border); border-radius: 12px; padding: 6px 22px; }
.scoreboard .status { color: var(--muted); margin-top: 10px; font-size: .9rem; }
.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
@media (max-width: 760px) { .detail-grid { grid-template-columns: 1fr; } }
"""

# -------------------------------------------------------------- JS ------
MAIN_JS = r"""/* الملعب V2 — main.js: فلتر صارم: 6 دوريات فقط، بلا محاكاة، بلا مسابقات أخرى */
(function () {
  "use strict";
  var ALLOWED_IDS = ["premier-league", "la-liga", "serie-a", "bundesliga", "ligue-1", "botola"];
  var ALLOWED_NAMES = ["الدوري الإنجليزي", "الدوري الإسباني", "الدوري الإيطالي",
    "الدوري الألماني", "الدوري الفرنسي", "البطولة الاحترافية المغربية", "البطولة المغربية"];
  window.MALAEB_ALLOWED = ALLOWED_IDS;
  window.isAllowedLeague = function (m) {
    if (!m) return false;
    if (m.league && ALLOWED_IDS.indexOf(m.league) !== -1) return true;
    if (m.league_name && ALLOWED_NAMES.indexOf(m.league_name) !== -1) return true;
    return false;
  };
  function onlyAllowed(list) { return (list || []).filter(window.isAllowedLeague); }

  async function loadJSON(path) {
    try { const r = await fetch(path); if (!r.ok) throw new Error("http " + r.status); return await r.json(); }
    catch (e) { return null; }
  }
  window.MalaebData = {
    async leagues() {
      const d = await loadJSON("data/leagues.json");
      if (d && d.leagues) return d;
      return { leagues: FALLBACK.leagues, updated: "نسخة احتياطية — آخر تحقق 2026-11-18" };
    },
    async fixtures() {
      const d = await loadJSON("data/fixtures.json");
      if (d) return d;
      return FALLBACK.fixtures;
    },
    async news() {
      const d = await loadJSON("data/news.json");
      if (d && d.articles) return d.articles;
      return [];
    }
  };

  document.addEventListener("DOMContentLoaded", function () {
    const btn = document.querySelector(".menu-btn");
    const nav = document.querySelector(".main-nav");
    if (btn && nav) btn.addEventListener("click", () => nav.classList.toggle("open"));
    document.querySelectorAll(".js-year").forEach(el => { el.textContent = new Date().getFullYear(); });
    document.querySelectorAll(".newsletter form").forEach(form => {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        const input = form.querySelector('input[type="email"]');
        const note = form.parentElement.querySelector(".form-note");
        const val = (input.value || "").trim();
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) {
          if (note) { note.textContent = "المرجو إدخال بريد إلكتروني صحيح."; note.style.color = "#ff4d5e"; }
          return;
        }
        if (note) { note.textContent = "شكراً! تم تسجيل اشتراكك بنجاح. ⚽"; note.style.color = "#22e07a"; }
        input.value = "";
      });
    });
    const closeAd = document.querySelector(".close-ad");
    if (closeAd) closeAd.addEventListener("click", () => {
      document.querySelector(".anchored-ad").style.display = "none";
    });
  });

  /* الشريط المتحرك: الدوريات الستة فقط — لا دوريات غامضة */
  window.renderTicker = async function (elId) {
    const el = document.getElementById(elId);
    if (!el) return;
    const fx = await window.MalaebData.fixtures();
    const items = [];
    onlyAllowed(fx.live || []).forEach(m => {
      items.push(`<span class="ticker-item"><span class="live-dot">● مباشر ${m.minute}'</span> <b>${m.home} ${m.home_goals} - ${m.away_goals} ${m.away}</b></span>`);
    });
    onlyAllowed(fx.upcoming || []).slice(0, 8).forEach(m => {
      items.push(`<span class="ticker-item">${m.home} × ${m.away} <b>${m.date_label || m.date} ${m.time || ""}</b></span>`);
    });
    el.innerHTML = items.join("") || "<span class='ticker-item'>لا توجد مباريات مبرمجة في الدوريات الستة حالياً</span>";
  };

  window.posClass = function (pos, leagueId) {
    if (pos <= 4) return "pos-ucl";
    if (leagueId === "botola") return pos >= 15 ? "pos-rel" : "";
    if (pos >= 18) return "pos-rel";
    return "";
  };

  function cell(v) { return (v === undefined || v === null || v === "") ? "—" : v; }
  function gdTxt(r) {
    if (r.gd !== undefined && r.gd !== null) return (r.gd > 0 ? "+" : "") + r.gd;
    if (r.gf !== null && r.gf !== undefined && r.ga !== null && r.ga !== undefined) {
      const gd = r.gf - r.ga; return (gd > 0 ? "+" : "") + gd;
    }
    return "—";
  }
  window.standingsTableHTML = function (league, limit) {
    const rows = (limit ? league.table.slice(0, limit) : league.table).map(r => {
      if (r.placeholder) return `<tr><td>${r.pos}</td><td class="team" style="color:var(--muted)">${r.team}</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td><b>—</b></td></tr>`;
      return `<tr class="${window.posClass(r.pos, league.id)}">
        <td>${r.pos}</td><td class="team">${r.team}</td><td>${cell(r.p)}</td>
        <td>${cell(r.w)}</td><td>${cell(r.d)}</td><td>${cell(r.l)}</td>
        <td>${gdTxt(r)}</td><td><b>${cell(r.pts)}</b></td></tr>`;
    }).join("");
    return `<div class="table-wrap"><table class="standings">
      <thead><tr><th>#</th><th>الفريق</th><th>لعب</th><th>فاز</th><th>تعادل</th><th>خسر</th><th>فرق</th><th>نقاط</th></tr></thead>
      <tbody>${rows}</tbody></table></div>`;
  };

  window.matchRowHTML = function (m) {
    const isLive = m.status === "live";
    const isFin = m.status === "finished";
    const score = isLive || isFin
      ? `<span class="score${isLive ? " live" : ""}">${m.home_goals} - ${m.away_goals}</span>`
      : `<span class="score">${m.time || "—"}</span>`;
    const time = isLive
      ? `<span class="time"><span class="live-dot">● مباشر</span> ${m.minute}'</span>`
      : `<span class="time">${m.date_label || m.date || ""} ${m.time || ""}</span>`;
    const inner = `<div class="match-row">
      <span class="lg">${m.league_name || ""}</span>
      <span class="team">${m.home}</span>${score}<span class="team away">${m.away}</span>${time}
    </div>`;
    return m.id ? `<a class="match-link" href="match.html?id=${m.id}">${inner}</a>` : inner;
  };
})();
"""

MATCHES_JS = r"""/* الملعب V2 — matches.js: تبويبات حقيقية من data/fixtures.json فقط. بلا محاكاة. */
(function () {
  "use strict";
  let FX = null, currentTab = "today";
  function $(id) { return document.getElementById(id); }
  function emptyMsg(txt) {
    return `<p style="color:var(--muted);text-align:center;padding:26px 0">${txt}</p>`;
  }
  function listHTML(list) {
    const ok = (list || []).filter(window.isAllowedLeague);
    return ok.length ? ok.map(window.matchRowHTML).join("") : null;
  }
  function render() {
    const box = $("matches-box");
    if (!box || !FX) return;
    let html = "";
    if (currentTab === "today") {
      html = listHTML(FX.today) || emptyMsg("لا توجد مباريات اليوم (الأربعاء 18 نونبر 2026) في الدوريات الستة — فترة التوقف الدولي. العودة الجمعة 20 نونبر.");
    } else if (currentTab === "tomorrow") {
      html = listHTML(FX.tomorrow) || emptyMsg("لا توجد مباريات غداً (الخميس 19 نونبر 2026) في الدوريات الستة — التوقف الدولي مستمر. العودة الجمعة 20 نونبر.");
    } else if (currentTab === "friday") {
      const fri = (FX.upcoming || []).filter(m => m.date === "2026-11-20");
      html = listHTML(fri) || emptyMsg("لا توجد مباريات مبرمجة يوم الجمعة 20 نونبر.");
    } else if (currentTab === "upcoming") {
      html = listHTML(FX.upcoming) || emptyMsg("لا توجد مباريات قادمة مسجلة.");
    } else {
      const r = FX.results || [];
      html = r.length ? listHTML(r) : emptyMsg("لا توجد نتائج مسجلة.");
      if (r.length) html = `<p class="data-note">آخر جولة قبل التوقف الدولي (عطلة نهاية الأسبوع 7–8 نونبر 2026) — المصدر: showupandplay.com، تقرير 08 نونبر 2026. اليوم الدقيق لكل مباراة غير موثق فردياً.</p>` + html;
    }
    box.innerHTML = html;
  }
  document.addEventListener("DOMContentLoaded", async function () {
    FX = await window.MalaebData.fixtures();
    render();
    document.querySelectorAll(".tabs button").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".tabs button").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        currentTab = btn.dataset.tab;
        render();
      });
    });
  });
})();
"""

STANDINGS_JS = r"""/* الملعب V2 — standings.js: 6 دوريات فقط */
(function () {
  "use strict";
  const ORDER = ["premier-league", "la-liga", "serie-a", "bundesliga", "ligue-1", "botola"];
  let DATA = null, current = "premier-league";
  function leagueById(id) { return DATA.leagues.find(l => l.id === id) || DATA.leagues[0]; }
  function renderSelector() {
    const box = document.getElementById("league-select");
    if (!box) return;
    box.innerHTML = ORDER.map(id => leagueById(id)).filter(Boolean).map(l =>
      `<button data-l="${l.id}" class="${l.id === current ? "active" : ""}">${l.name}</button>`).join("");
    box.querySelectorAll("button").forEach(b => b.addEventListener("click", () => {
      current = b.dataset.l;
      box.querySelectorAll("button").forEach(x => x.classList.remove("active"));
      b.classList.add("active");
      renderLeague();
    }));
  }
  function renderLeague() {
    const l = leagueById(current);
    const title = document.getElementById("league-title");
    if (title) title.innerHTML = `${l.name} <small style="color:var(--muted);font-size:.85rem">موسم ${l.season || "2026-27"} — ${l.round || ""}</small>`;
    const tw = document.getElementById("table-wrap");
    if (tw) tw.innerHTML = window.standingsTableHTML(l)
      + `<p class="data-note"><b>المصدر:</b> ${l.source || "—"} — <b>آخر تحقق:</b> ${DATA.updated || ""}. الجدول المعروض هو أول 5 مراكز موثقة فقط؛ الجدول الكامل (20 فريقاً) قيد التحقق من مصدر رسمي.</p>`;
    const sc = document.getElementById("scorers");
    if (sc) {
      const list = (l.scorers || []).slice(0, 8);
      sc.innerHTML = list.length ? list.map((s, i) => `
        <div class="scorer"><span class="rank">${i + 1}</span>
        <span class="info"><b>${s.player}</b><span>${s.team}</span></span>
        <span class="goals">${s.goals}</span></div>`).join("")
        : `<div class="placeholder-box">لا توجد قائمة هدافين موثقة لهذا الدوري بعد — تُضاف فور التحقق من مصدر رسمي.</div>`;
    }
    const upd = document.getElementById("data-updated");
    if (upd && DATA.updated) upd.textContent = "آخر تحديث: " + DATA.updated;
  }
  document.addEventListener("DOMContentLoaded", async function () {
    DATA = await window.MalaebData.leagues();
    renderSelector();
    renderLeague();
  });
})();
"""

HOME_JS = r"""/* الملعب V2 — home.js: الرئيسية تُبقي رسالة التوقف الدولي (Hero ثابت في HTML) */
(function () {
  "use strict";
  function newsCard(a) {
    return `<a href="news/${a.slug}.html" class="news-card">
      <div class="news-thumb">${a.emoji}</div>
      <div class="news-body">
        <div class="news-meta"><span class="cat">${a.category}</span><span>${a.date}</span></div>
        <h3>${a.title}</h3><p>${a.excerpt}</p>
      </div></a>`;
  }
  document.addEventListener("DOMContentLoaded", async function () {
    window.renderTicker("ticker-track");
    try {
      const articles = await window.MalaebData.news();
      if (articles.length) {
        document.querySelector("#home-news").innerHTML = articles.slice(0, 6).map(newsCard).join("");
      }
    } catch (e) {}
    try {
      const fx = await window.MalaebData.fixtures();
      const up = (fx.upcoming || []).filter(window.isAllowedLeague).slice(0, 6);
      document.querySelector("#home-matches").innerHTML = up.length
        ? up.map(window.matchRowHTML).join("")
        : `<p style="color:var(--muted)">لا توجد مباريات مبرمجة حالياً.</p>`;
    } catch (e) {}
    try {
      const data = await window.MalaebData.leagues();
      const pick = ["premier-league", "la-liga", "botola"]
        .map(id => data.leagues.find(l => l.id === id)).filter(Boolean);
      document.querySelector("#home-tables").innerHTML = pick.map(l => `
        <div>
          <div class="section-head" style="margin-bottom:10px">
            <h2 style="font-size:1.05rem">${l.name}</h2>
            <a class="more" href="league-${l.id}.html">الجدول الكامل ←</a>
          </div>
          ${window.standingsTableHTML(l, 5)}
          <p style="color:var(--muted);font-size:.78rem;margin-top:6px">أول 5 مراكز موثقة — آخر تحقق: ${data.updated || ""}</p>
        </div>`).join("");
    } catch (e) {}
  });
})();
"""

MATCH_JS = r"""/* الملعب V2 — match.js: صفحة تفاصيل المباراة (?id=) — بيانات موثقة فقط، والباقي Placeholder صريح */
(function () {
  "use strict";
  function q(name) { return new URLSearchParams(location.search).get(name); }
  function esc(s) { return String(s == null ? "" : s); }
  document.addEventListener("DOMContentLoaded", async function () {
    window.renderTicker("ticker-track");
    const id = q("id");
    const box = document.getElementById("match-detail");
    if (!box) return;
    const fx = await window.MalaebData.fixtures();
    const all = [].concat(fx.live || [], fx.today || [], fx.tomorrow || [], fx.upcoming || [], fx.results || []);
    const m = all.find(x => x.id === id);
    if (!m) {
      box.innerHTML = `<div class="placeholder-box"><h2 style="margin-bottom:8px">المباراة غير موجودة</h2><p>الرابط غير صحيح أو المباراة غير مدرجة في الدوريات الستة. <a href="matches.html" style="color:var(--accent)">← العودة إلى المباريات</a></p></div>`;
      return;
    }
    const isFin = m.status === "finished";
    const score = isFin ? `${m.home_goals} - ${m.away_goals}` : (m.time || "—");
    const status = isFin ? "انتهت" : `مباراة قادمة — ${m.date_label || m.date} ${m.time ? "• " + m.time + " بتوقيت المغرب" : "• التوقيت قيد التأكيد"}`;
    document.title = `${m.home} × ${m.away} | الملعب`;
    const h1 = document.getElementById("match-h1");
    if (h1) h1.textContent = `${m.home} × ${m.away}`;
    box.innerHTML = `
    <div class="scoreboard">
      <div class="teams"><span class="team-name">${esc(m.home)}</span>
      <span class="big-score">${score}</span>
      <span class="team-name">${esc(m.away)}</span></div>
      <div class="status">${m.league_name} • ${status}</div>
      <div class="status" style="font-size:.8rem">المصدر: ${esc(m.source || "—")} — آخر تحقق: 18 نونبر 2026</div>
    </div>
    <div class="detail-grid">
      <section class="section" style="padding-top:0">
        <div class="section-head"><h2>أحداث المباراة</h2></div>
        <div class="placeholder-box">لا توجد أحداث موثقة بعد لهذه المباراة (أهداف، بطاقات، تبديلات).<br>تُضاف الأحداث لحظة بلحظة بعد انطلاق المباراة وربط مصدر بيانات حي.</div>
      </section>
      <section class="section" style="padding-top:0">
        <div class="section-head"><h2>إحصائيات المباراة</h2></div>
        <div class="placeholder-box">الاستحواذ، التسديدات، الركنيات، الأخطاء…<br>غير موثقة بعد — تُعرض هنا بعد توفر مصدر إحصائيات حي.</div>
      </section>
      <section class="section" style="padding-top:0">
        <div class="section-head"><h2>التشكيلتان</h2></div>
        <div class="placeholder-box">التشكيلتان الرسميتان غير موثقتين بعد — تُنشران قبل انطلاق المباراة بساعة من مصدر رسمي.</div>
      </section>
      <section class="section" style="padding-top:0">
        <div class="section-head"><h2>المواجهات المباشرة</h2></div>
        <div class="placeholder-box">سجل المواجهات المباشرة بين الفريقين غير موثق بعد — يُضاف من مصدر رسمي.</div>
      </section>
    </div>
    <div class="cpa-slot"><b>مساحة إعلانية — CPA (Placeholder)</b>تُضاف هنا عروض موثوقة بعد اختيارها — بدون نوافذ منبثقة.<small>لا يوجد أي عرض حي أو رابط خارجي في هذه المساحة حالياً.</small></div>
    <p><a href="matches.html" style="color:var(--accent);font-weight:700">← العودة إلى كل المباريات</a></p>`;
  });
})();
"""

# ---------------------------------------------------------- templates ---
BASE = "https://almalaeb.example.com"
ICON = """<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚽</text></svg>">"""
FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">"""

def header(active=""):
    def a(page, label):
        return f'<li><a href="{page}" class="active">{label}</a></li>' if page == active else f'<li><a href="{page}">{label}</a></li>'
    return f"""<header class="site-header">
  <div class="container header-inner">
    <a href="index.html" class="logo"><span class="ball">⚽</span><span>الملعب<small>AL MALAEB</small></span></a>
    <button class="menu-btn" aria-label="القائمة">☰</button>
    <nav class="main-nav"><ul>
      {a("index.html", "الرئيسية")}{a("matches.html", "المباريات")}{a("standings.html", "الترتيب")}{a("news.html", "الأخبار")}
    </ul></nav>
  </div>
</header>"""

CHIPS = """<div class="container"><div class="league-chips">
<a href="league-premier-league.html">🏴󐁧󐁢󐁥󐁮󐁧󐁿 الدوري الإنجليزي</a>
<a href="league-la-liga.html">🇪🇸 الدوري الإسباني</a>
<a href="league-serie-a.html">🇮🇹 الدوري الإيطالي</a>
<a href="league-bundesliga.html">🇩🇪 الدوري الألماني</a>
<a href="league-ligue-1.html">🇫🇷 الدوري الفرنسي</a>
<a href="league-botola.html">🇲🇦 البطولة المغربية</a>
</div></div>"""

TICKER = """<div class="ticker-wrap"><div class="container ticker">
  <span class="ticker-label">مباشر</span>
  <div class="ticker-track" id="ticker-track"><span class="ticker-item">جارٍ التحميل…</span></div>
</div></div>"""

CPA_SLOT = """<div class="cpa-slot"><b>مساحة إعلانية — CPA (Placeholder)</b>تُضاف هنا عروض موثوقة بعد اختيارها — بدون نوافذ منبثقة وبدون روابط مراهنات.<small>لا يوجد أي عرض حي أو رابط خارجي في هذه المساحة حالياً.</small></div>"""

AD_LEADER = """<div class="container"><div class="ad-slot"><div class="ad-leaderboard">مساحة إعلانية — Leaderboard 970×250</div></div></div>"""

def footer():
    return """<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <h4>⚽ الملعب</h4>
        <p style="color:var(--muted);font-size:.9rem">موقعك المغربي لمتابعة كرة القدم: نتائج مباشرة، جداول الترتيب، وآخر الأخبار من الدوريات الأوروبية الخمسة الكبرى والبطولة المغربية.</p>
      </div>
      <div>
        <h4>أقسام الموقع</h4>
        <ul>
          <li><a href="matches.html">مباريات اليوم</a></li>
          <li><a href="standings.html">جداول الترتيب</a></li>
          <li><a href="news.html">آخر الأخبار</a></li>
          <li><a href="league-botola.html">البطولة المغربية</a></li>
        </ul>
      </div>
      <div>
        <h4>معلومات</h4>
        <ul>
          <li><a href="about.html">من نحن</a></li>
          <li><a href="contact.html">اتصل بنا</a></li>
          <li><a href="privacy.html">سياسة الخصوصية</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span class="js-year">2026</span> الملعب — جميع الحقوق محفوظة.</span>
      <span>البيانات لأغراض إخبارية — آخر تحديث: 18 نونبر 2026</span>
    </div>
  </div>
</footer>
<div class="anchored-ad"><span>مساحة إعلانية للهواتف</span><button class="close-ad">✕</button></div>"""

def table_html(league, limit=None):
    rows = league["table"][:limit] if limit else league["table"]
    out = []
    for r in rows:
        def c(v):
            return "—" if v is None else str(v)
        if r.get("placeholder"):
            out.append(f'<tr><td>{r["pos"]}</td><td class="team" style="color:var(--muted)">{r["team"]}</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td><b>—</b></td></tr>')
            continue
        gd = r["gd"]
        gd_txt = ("+" if gd and gd > 0 else "") + str(gd) if gd is not None else "—"
        cls = "pos-ucl" if r["pos"] <= 4 else ("pos-rel" if (league["id"] == "botola" and r["pos"] >= 15) or (league["id"] != "botola" and r["pos"] >= 18) else "")
        out.append(f'<tr class="{cls}"><td>{r["pos"]}</td><td class="team">{r["team"]}</td><td>{c(r["p"])}</td><td>{c(r["w"])}</td><td>{c(r["d"])}</td><td>{c(r["l"])}</td><td>{gd_txt}</td><td><b>{c(r["pts"])}</b></td></tr>')
    return ('<div class="table-wrap"><table class="standings">'
            '<thead><tr><th>#</th><th>الفريق</th><th>لعب</th><th>فاز</th><th>تعادل</th><th>خسر</th><th>فرق</th><th>نقاط</th></tr></thead>'
            f'<tbody>{"".join(out)}</tbody></table></div>')

def scorers_html(league):
    sc = league["scorers"]
    if not sc:
        return '<div class="placeholder-box">لا توجد قائمة هدافين موثقة لهذا الدوري بعد — تُضاف فور التحقق من مصدر رسمي.</div>'
    cards = "".join(
        f'<div class="scorer"><span class="rank">{i+1}</span><span class="info"><b>{s["player"]}</b><span>{s["team"]}</span></span><span class="goals">{s["goals"]}</span></div>'
        for i, s in enumerate(sc))
    return f'<div class="scorers">{cards}</div>'

def fixtures_list_html(matches):
    if not matches:
        return ""
    items = []
    for m in matches:
        score = f'{m["home_goals"]} - {m["away_goals"]}' if m["status"] == "finished" else (m.get("time") or "—")
        when = f'{m.get("date_label") or m["date"]} {m.get("time") or ""}'.strip()
        if m.get("time") is None:
            when += " — التوقيت قيد التأكيد"
        inner = (f'<div class="match-row"><span class="lg">{m["league_name"]}</span>'
                 f'<span class="team">{m["home"]}</span><span class="score">{score}</span>'
                 f'<span class="team away">{m["away"]}</span><span class="time">{when}</span></div>')
        items.append(f'<a class="match-link" href="match.html?id={m["id"]}">{inner}</a>' if m.get("id") else inner)
    return f'<div class="match-list">{"".join(items)}</div>'

def patch(path, pairs):
    with open(path, encoding="utf-8") as f:
        s = f.read()
    for old, new in pairs:
        # idempotent: skip if the replacement is already in place
        if old in s and new not in s:
            s = s.replace(old, new)
    w(path, s)

# ------------------------------------------------------------- build -----
def main():
    # ---- data files (verified only) ----
    dump(os.path.join(ROOT, "data/leagues.json"),
         {"updated": CHECKED, "leagues": LEAGUES,
          "note": "أول 5 مراكز موثقة فقط لكل دوري (آخر تحقق 2026-11-18). الجدول الكامل قيد التحقق."})
    dump(os.path.join(ROOT, "data/fixtures.json"),
         {"updated": CHECKED,
          "note": "18 و19 نونبر 2026: لا مباريات في الدوريات الستة (توقف دولي). العودة الجمعة 20 نونبر. الأوقات بتوقيت المغرب (UTC+1).",
          "live": [], "today": [], "tomorrow": [],
          "upcoming": UPCOMING, "results": RESULTS})
    with open(os.path.join(V1, "data/news.json"), encoding="utf-8") as f:
        news = json.load(f)
    news["articles"] = [a for a in news["articles"] if a.get("category") != "دوري أبطال أوروبا"]
    dump(os.path.join(ROOT, "data/news.json"), news)

    # ---- CSS ----
    css = os.path.join(ROOT, "assets/css/style.css")
    with open(css, encoding="utf-8") as f:
        s = f.read()
    if "الملعب V2" not in s:
        w(css, s + CSS_ADD)

    # ---- JS ----
    w(os.path.join(ROOT, "assets/js/main.js"), MAIN_JS)
    w(os.path.join(ROOT, "assets/js/matches.js"), MATCHES_JS)
    w(os.path.join(ROOT, "assets/js/standings.js"), STANDINGS_JS)
    w(os.path.join(ROOT, "assets/js/home.js"), HOME_JS)
    w(os.path.join(ROOT, "assets/js/match.js"), MATCH_JS)
    fb = {"leagues": LEAGUES,
          "fixtures": {"live": [], "today": [], "tomorrow": [], "upcoming": UPCOMING, "results": RESULTS}}
    w(os.path.join(ROOT, "assets/js/data-fallback.js"),
        "/* الملعب V2 — بيانات احتياطية موثقة (18 نونبر 2026)، تُستخدم فقط إذا تعذّر تحميل data/*.json */\n"
        "const FALLBACK = " + json.dumps(fb, ensure_ascii=False, indent=2) + ";\n")

    # ---- index.html (fresh) ----
    index = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>الملعب | مباريات اليوم، نتائج مباشرة، ترتيب الدوريات وآخر الأخبار</title>
<meta name="description" content="الملعب — مباريات اليوم والنتائج المباشرة، جداول ترتيب الدوري الإنجليزي والإسباني والإيطالي والألماني والفرنسي والبطولة المغربية، وآخر الأخبار بالعربية. آخر تحديث: 18 نونبر 2026.">
<meta property="og:title" content="الملعب | نتائج مباشرة وأخبار كرة القدم">
<meta property="og:description" content="مباريات اليوم، ترتيب الدوريات الخمسة الكبرى والبطولة المغربية، وآخر الأخبار.">
<meta property="og:type" content="website">
<meta property="og:locale" content="ar_MA">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebSite","name":"الملعب","alternateName":"Al Malaeb","inLanguage":"ar","description":"موقع عربي لمتابعة مباريات ونتائج وترتيب الدوريات الأوروبية الخمسة الكبرى والبطولة المغربية."}}</script>
{FONTS}
{ICON}
</head>
<body>
{header("index.html")}
{CHIPS}
{AD_LEADER}
{TICKER}
<main class="container">
  <section class="hero" id="hero"><div class="hero-card"><div class="hero-content">
    <span class="tag">⏸️ فترة التوقف الدولي</span>
    <h1>مباريات اليوم: لا مباريات في الدوريات الستة</h1>
    <p>الأربعاء 18 نونبر 2026 — الدوريات الخمسة الكبرى والبطولة المغربية في فترة التوقف الدولي. العودة يوم الجمعة 20 نونبر: بايرن ميونيخ × كولن، أتلتيك بلباو × إسبانيول، تروا × لوهافر — ثم الجولة الكاملة يوم السبت 21 نونبر، أبرزها نيوكاسل × آرسنال وليفربول × مانشستر يونايتد يوم الأحد.</p>
    <a class="btn" href="matches.html">شاهد مباريات الجمعة والسبت ←</a>
  </div></div></section>

  <div class="date-strip">
    <div class="day"><b>اليوم — الأربعاء 18 نونبر</b><span>لا مباريات في الدوريات الستة (توقف دولي)</span></div>
    <div class="day"><b>غداً — الخميس 19 نونبر</b><span>لا مباريات في الدوريات الستة (توقف دولي)</span></div>
    <div class="day next"><b>الجمعة 20 نونبر</b><span>3 مباريات — عودة الدوريات</span></div>
  </div>

  <section class="section">
    <div class="section-head"><h2>المباريات القادمة</h2><a class="more" href="matches.html">كل المباريات ←</a></div>
    <div class="match-list" id="home-matches"><p style="color:var(--muted)">جارٍ التحميل…</p></div>
    <p class="data-note"><b>مصادر المباريات:</b> premierleague.com وnbcsports.com وlaligatable.co وvavel.com وfcstats.com وfootball.mib.news — آخر تحقق: 18 نونبر 2026. الأوقات بتوقيت المغرب (UTC+1).</p>
  </section>

  {CPA_SLOT}

  <section class="section">
    <div class="section-head"><h2>آخر الأخبار</h2><a class="more" href="news.html">كل الأخبار ←</a></div>
    <div class="news-grid" id="home-news"></div>
    <p style="color:var(--muted);font-size:.82rem">الأخبار أرشيف بتاريخ نشرها (شتنبر 2026) — الأرقام الحالية تجدها في صفحات الترتيب والمباريات.</p>
  </section>

  <section class="section">
    <div class="section-head"><h2>جداول الترتيب — أول 5 مراكز موثقة</h2><a class="more" href="standings.html">الجداول الكاملة ←</a></div>
    <div class="news-grid" id="home-tables" style="grid-template-columns:repeat(auto-fill,minmax(300px,1fr))"></div>
  </section>

  <section class="newsletter">
    <h2>📬 النشرة البريدية للملعب</h2>
    <p>توصل بأهم الأخبار والنتائج كل صباح — مجاناً وبدون إزعاج.</p>
    <form><input type="email" placeholder="بريدك الإلكتروني" required><button class="btn" type="submit">اشترك</button></form>
    <div class="form-note"></div>
  </section>
</main>
{footer()}
<script src="assets/js/data-fallback.js"></script>
<script src="assets/js/main.js"></script>
<script src="assets/js/home.js"></script>
</body>
</html>"""
    w(os.path.join(ROOT, "index.html"), index)

    # ---- matches.html (fresh) ----
    matches = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>مباريات اليوم والنتائج المباشرة | الملعب</title>
<meta name="description" content="مباريات اليوم وغداً والقادمة والنتائج من الدوريات الخمسة الكبرى والبطولة المغربية. اليوم 18 نونبر 2026: توقف دولي، والعودة الجمعة 20 نونبر — مانشستر سيتي × فولهام ونيوكاسل × آرسنال يوم السبت 21 نونبر.">
<meta property="og:title" content="مباريات اليوم — نتائج مباشرة | الملعب">
<meta property="og:locale" content="ar_MA">
{FONTS}
{ICON}
</head>
<body>
{header("matches.html")}
{CHIPS}
{AD_LEADER}
{TICKER}
<main class="container">
  <section class="section">
    <div class="section-head"><h1 style="font-size:1.6rem">⚽ مباريات الدوريات الستة</h1></div>
    <p class="data-note"><b>اليوم الأربعاء 18 نونبر 2026:</b> لا توجد مباريات في الدوري الإنجليزي والإسباني والإيطالي والألماني والفرنسي والبطولة المغربية — فترة التوقف الدولي (9–17 نونبر للدوري الإنجليزي). العودة: الجمعة 20 نونبر. الأوقات بتوقيت المغرب (UTC+1).</p>
    <div class="tabs">
      <button data-tab="today" class="active">📅 اليوم 18 نونبر</button>
      <button data-tab="tomorrow">📅 غداً 19 نونبر</button>
      <button data-tab="friday">⏭️ الجمعة 20 نونبر</button>
      <button data-tab="upcoming">🗓️ كل القادمة</button>
      <button data-tab="results">✅ النتائج الأخيرة</button>
    </div>
    <div id="matches-box"><p style="color:var(--muted);text-align:center">جارٍ التحميل…</p></div>
    {CPA_SLOT}
    <p style="color:var(--muted);font-size:.78rem;margin-top:14px">💡 النتائج المباشرة تظهر هنا فقط من مصدر بيانات حي موثوق. حالياً لا يوجد مصدر حي مربوط (API-Football موقوف) — الصفحة تعرض المباريات المبرمجة الموثقة والنتائج الأخيرة فقط، بدون محاكاة.</p>
  </section>
</main>
{footer()}
<script src="assets/js/data-fallback.js"></script>
<script src="assets/js/main.js"></script>
<script src="assets/js/matches.js"></script>
<script>document.addEventListener("DOMContentLoaded",()=>window.renderTicker("ticker-track"));</script>
</body>
</html>"""
    w(os.path.join(ROOT, "matches.html"), matches)

    # ---- match.html (fresh template) ----
    match = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>تفاصيل المباراة | الملعب</title>
<meta name="description" content="تفاصيل المباراة: النتيجة، الأحداث، الإحصائيات، التشكيلتان والمواجهات المباشرة — الملعب.">
<meta property="og:title" content="تفاصيل المباراة | الملعب">
<meta property="og:locale" content="ar_MA">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SportsEvent","name":"مانشستر سيتي × فولهام","sport":"كرة القدم","startDate":"2026-11-21T12:30:00Z","location":{{"@type":"Place","name":"ملعب الاتحاد","address":"مانشستر، إنجلترا"}},"homeTeam":{{"@type":"SportsTeam","name":"مانشستر سيتي"}},"awayTeam":{{"@type":"SportsTeam","name":"فولهام"}},"competitor":[{{"@type":"SportsTeam","name":"مانشستر سيتي"}},{{"@type":"SportsTeam","name":"فولهام"}}]}}</script>
{FONTS}
{ICON}
</head>
<body>
{header("")}
{CHIPS}
{TICKER}
<main class="container">
  <section class="section">
    <h1 id="match-h1" style="font-size:1.6rem">تفاصيل المباراة</h1>
    <div id="match-detail"><p style="color:var(--muted)">جارٍ التحميل…</p></div>
  </section>
</main>
{footer()}
<script src="assets/js/data-fallback.js"></script>
<script src="assets/js/main.js"></script>
<script src="assets/js/match.js"></script>
</body>
</html>"""
    w(os.path.join(ROOT, "match.html"), match)

    # ---- league pages (fresh, static SEO content) ----
    cat_by_league = {"premier-league": "الدوري الإنجليزي", "la-liga": "الدوري الإسباني",
                     "ligue-1": "الدوري الفرنسي", "botola": "البطولة المغربية"}
    for l in LEAGUES:
        lg_fx = [m for m in UPCOMING if m["league"] == l["id"]]
        fx_html = fixtures_list_html(lg_fx) if lg_fx else \
            '<div class="placeholder-box">برنامج مباريات هذا الدوري القادمة لم يُنشر بعد بشكل موثق — قيد التحقق من مصدر رسمي.</div>'
        lg_news = [a for a in news["articles"] if a.get("category") == cat_by_league.get(l["id"], "")]
        if lg_news:
            news_html = '<div class="news-grid">' + "".join(
                f'<a href="news/{a["slug"]}.html" class="news-card"><div class="news-thumb">{a["emoji"]}</div>'
                f'<div class="news-body"><div class="news-meta"><span class="cat">{a["category"]}</span><span>{a["date"]}</span></div>'
                f'<h3>{a["title"]}</h3><p>{a["excerpt"]}</p></div></a>'
                for a in lg_news) + "</div>"
        else:
            news_html = '<div class="placeholder-box">لا توجد أخبار منشورة عن هذا الدوري بعد في أرشيف الموقع.</div>'
        page = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{l["name"]} | الملعب</title>
<meta name="description" content="{l["meta"]}">
<meta property="og:title" content="{l["name"]} | الملعب">
<meta property="og:description" content="{l["meta"]}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ar_MA">
{FONTS}
{ICON}
</head>
<body>
{header("standings.html")}
{CHIPS}
{AD_LEADER}
{TICKER}
<main class="container page" style="max-width:1100px">
  <h1>{l["name"]} <small style="color:var(--muted);font-size:1rem">— موسم {l["season"]} • {l["round"]}</small></h1>
  <p class="data-note"><span class="verified-tag">✓ موثق</span> <b>المصدر:</b> {l["source"]} — <b>آخر تحقق:</b> 18 نونبر 2026. الجدول المعروض هو أول 5 مراكز موثقة فقط؛ الجدول الكامل (20 فريقاً) قيد التحقق من مصدر رسمي.</p>
  <section class="section" style="padding-top:6px">
    <div class="section-head"><h2>جدول الترتيب</h2><span style="color:var(--muted);font-size:.82rem">{l["next_round"]}</span></div>
    {table_html(l)}
  </section>
  <section class="section">
    <div class="section-head"><h2>هدّافو الدوري</h2></div>
    {scorers_html(l)}
  </section>
  <section class="section">
    <div class="section-head"><h2>مباريات ونتائج</h2><a class="more" href="matches.html">كل المباريات ←</a></div>
    {fx_html}
  </section>
  {CPA_SLOT}
  <section class="section">
    <div class="section-head"><h2>أخبار {l["short"]}</h2><a class="more" href="news.html">كل الأخبار ←</a></div>
    {news_html}
  </section>
</main>
{footer()}
<script src="assets/js/data-fallback.js"></script>
<script src="assets/js/main.js"></script>
<script>document.addEventListener("DOMContentLoaded",()=>window.renderTicker("ticker-track"));</script>
</body>
</html>"""
        w(os.path.join(ROOT, f"league-{l['id']}.html"), page)

    # ---- patches to copied pages ----
    patch(os.path.join(ROOT, "standings.html"), [
        ('<meta name="description" content="جداول الترتيب الكاملة: الدوري الإنجليزي، الإسباني، الإيطالي، الألماني، الفرنسي، دوري أبطال أوروبا والبطولة المغربية — مع هدافي كل دوري.">',
         '<meta name="description" content="جداول ترتيب الدوريات الخمسة الكبرى والبطولة المغربية 2026-27 — أول 5 مراكز موثقة لكل دوري (آخر تحقق 18 نونبر 2026) مع هدافي كل دوري.">'),
        ('<title>جداول ترتيب الدوريات الأوروبية والبطولة المغربية | الملعب</title>',
         '<title>جداول ترتيب الدوريات الخمسة الكبرى والبطولة المغربية | الملعب</title>'),
        ('آخر تحديث: 20 شتنبر 2026', 'آخر تحديث: 18 نونبر 2026'),
        ('<div class="scorers" id="scorers"></div>\n  </section>',
         '<div class="scorers" id="scorers"></div>\n  </section>\n  ' + CPA_SLOT),
    ])
    patch(os.path.join(ROOT, "news.html"), [
        ('<meta name="description" content="آخر أخبار كرة القدم: الدوريات الأوروبية الخمسة الكبرى، دوري أبطال أوروبا، المنتخب المغربي والبطولة الاحترافية — تغطية يومية بالعربية.">',
         '<meta name="description" content="آخر أخبار كرة القدم: الدوريات الأوروبية الخمسة الكبرى، المنتخب المغربي والبطولة الاحترافية — تغطية يومية بالعربية.">'),
        ('      <button data-cat="دوري أبطال أوروبا">دوري الأبطال</button>\n', ''),
        ('آخر تحديث: 20 شتنبر 2026', 'آخر تحديث: 18 نونبر 2026'),
        ('    <div class="section-head"><h2>📰 آخر الأخبار</h2></div>',
         '    <div class="section-head"><h2>📰 آخر الأخبار</h2></div>\n    <p class="data-note">الأخبار أرشيف بتاريخ نشرها (شتنبر 2026) — الأرقام والترتيب الحاليان في صفحات الترتيب والمباريات.</p>'),
        ('    <!-- AdSense: in-feed -->\n    <div class="ad-slot"><div class="ad-infeed">مساحة إعلانية داخل المحتوى — In-feed</div></div>',
         '    <!-- AdSense: in-feed -->\n    <div class="ad-slot"><div class="ad-infeed">مساحة إعلانية داخل المحتوى — In-feed</div></div>\n    ' + CPA_SLOT),
    ])
    patch(os.path.join(ROOT, "about.html"), [
        ('للدوريات الأوروبية الخمسة الكبرى، دوري أبطال أوروبا، والبطولة الاحترافية المغربية.',
         'للدوريات الأوروبية الخمسة الكبرى والبطولة الاحترافية المغربية.'),
        ('  <p>نعتمد على مزودي بيانات رياضية معتمدين (مثل API-Football) لتحديث النتائج والجداول تلقائياً، بينما يُحرَّر المحتوى الخبري من طرف فريق التحرير بناءً على مصادر صحفية موثوقة. لا ننشر شائعات على أنها حقائق: أي خبر غير مؤكد يُذكر بصيغة واضحة.</p>',
         '  <p>نعتمد على مصادر رياضية موثوقة ومتاحة للعموم لتحديث النتائج والجداول، ونذكر مصدر كل رقم وتاريخ التحقق منه. لا ننشر شائعات على أنها حقائق: أي خبر غير مؤكد يُذكر بصيغة واضحة.</p>'),
        ('آخر تحديث: 20 شتنبر 2026', 'آخر تحديث: 18 نونبر 2026'),
    ])
    for f in ["contact.html", "privacy.html"]:
        patch(os.path.join(ROOT, f), [('آخر تحديث: 20 شتنبر 2026', 'آخر تحديث: 18 نونبر 2026')])
    # news articles: footer date + CPA placeholder in sidebar
    for name in os.listdir(os.path.join(ROOT, "news")):
        p = os.path.join(ROOT, "news", name)
        patch(p, [
            ('آخر تحديث: 20 شتنبر 2026', 'آخر تحديث: 18 نونبر 2026'),
            ('<div class="ad-rect">مساحة إعلانية<br>300 × 250</div>',
             '<div class="ad-rect">مساحة إعلانية<br>300 × 250</div>\n      <div class="cpa-slot" style="position:static"><b>مساحة إعلانية — CPA (Placeholder)</b>تُضاف هنا عروض موثوقة بعد اختيارها.<small>لا يوجد أي عرض حي حالياً.</small></div>'),
        ])

    # ---- sitemap / robots / render.yaml ----
    urls = ["index.html", "matches.html", "match.html", "standings.html", "news.html",
            "about.html", "contact.html", "privacy.html"] + \
           [f"league-{l['id']}.html" for l in LEAGUES] + \
           [f"news/{a['slug']}.html" for a in news["articles"]]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'] + \
         [f'  <url><loc>{BASE}/{u}</loc><lastmod>2026-11-18</lastmod></url>' for u in urls] + \
         ['</urlset>']
    w(os.path.join(ROOT, "sitemap.xml"), "\n".join(sm) + "\n")
    w(os.path.join(ROOT, "robots.txt"),
        "User-agent: *\nAllow: /\nDisallow: /tools/\n\n"
        f"Sitemap: {BASE}/sitemap.xml\n")
    w(os.path.join(ROOT, "render.yaml"),
        "services:\n  - type: web\n    name: almalaeb\n    env: static\n"
        "    buildCommand: \"\"\n    staticPublishPath: .\n")
    w(os.path.join(ROOT, "README.md"),
        "# الملعب V2\n\nموقع عربي ثابت (HTML/CSS/JS فقط) — الدوريات الستة فقط: الإنجليزي، الإسباني،\n"
        "الإيطالي، الألماني، الفرنسي + البطولة المغربية — 6 دوريات فقط.\n\n"
        "- البيانات في `data/*.json` — موثقة فقط (آخر تحقق 18 نونبر 2026)، انظر `REPORT.md`.\n"
        "- لا يوجد بوت ولا API-Football في V2 (الحساب موقوف) — التحديث اليومي يدوي أو عبر مصدر جديد.\n"
        "- النشر: موقع ثابت على Render — انظر `REPORT.md` (الخطوة التالية).\n"
        "- إعادة البناء: `python3 tools/build-v2.py` من داخل المجلد.\n")

if __name__ == "__main__":
    main()
    print("V2 built in", ROOT)
