/* الملعب V2 — بيانات احتياطية موثقة (18 نونبر 2026)، تُستخدم فقط إذا تعذّر تحميل data/*.json */
const FALLBACK = {
  "leagues": [
    {
      "id": "premier-league",
      "name": "الدوري الإنجليزي الممتاز",
      "short": "البريميرليغ",
      "country": "إنجلترا",
      "season": "2026-27",
      "round": "الجولة 10",
      "next_round": "الجولة 11 — 21–23 نونبر 2026",
      "source": "kickofflens.com (تحديث 18 نونبر 2026 02:22 UTC) + مطابقة مع thestatsapi.com وnbcsports.com",
      "table": [
        {
          "pos": 1,
          "team": "آرسنال",
          "p": 10,
          "w": 9,
          "d": 0,
          "l": 1,
          "gf": 15,
          "ga": 5,
          "gd": 10,
          "pts": 27
        },
        {
          "pos": 2,
          "team": "برايتون",
          "p": 10,
          "w": 7,
          "d": 1,
          "l": 2,
          "gf": null,
          "ga": null,
          "gd": 19,
          "pts": 22
        },
        {
          "pos": 3,
          "team": "مانشستر سيتي",
          "p": 10,
          "w": 7,
          "d": 0,
          "l": 3,
          "gf": 21,
          "ga": 13,
          "gd": 8,
          "pts": 21
        },
        {
          "pos": 4,
          "team": "ليفربول",
          "p": 10,
          "w": 5,
          "d": 3,
          "l": 2,
          "gf": null,
          "ga": null,
          "gd": 4,
          "pts": 18
        },
        {
          "pos": 5,
          "team": "تشيلسي",
          "p": 10,
          "w": 5,
          "d": 1,
          "l": 4,
          "gf": null,
          "ga": null,
          "gd": 3,
          "pts": 16
        }
      ],
      "scorers": [
        {
          "player": "إيرلينغ هالاند",
          "team": "مانشستر سيتي",
          "goals": 9
        },
        {
          "player": "ألكسندر إيزاك",
          "team": "ليفربول",
          "goals": 7
        },
        {
          "player": "تيرنو باري",
          "team": "—",
          "goals": 6
        },
        {
          "player": "نيكولاس جاكسون",
          "team": "—",
          "goals": 6
        }
      ],
      "meta": "جدول ترتيب الدوري الإنجليزي الممتاز 2026-27: آرسنال في الصدارة بـ27 نقطة، برايتون 22، مانشستر سيتي 21 — الهدافون، مباريات الجولة 11 (21–23 نونبر) والنتائج."
    },
    {
      "id": "la-liga",
      "name": "الدوري الإسباني",
      "short": "الليغا",
      "country": "إسبانيا",
      "season": "2026-27",
      "round": "الجولة 12",
      "next_round": "الجولة 13 — 20–23 نونبر 2026",
      "source": "kickofflens.com (18 نونبر 2026) + مطابقة مع laligatable.co وthestatsapi.com",
      "table": [
        {
          "pos": 1,
          "team": "برشلونة",
          "p": 12,
          "w": 11,
          "d": 0,
          "l": 1,
          "gf": 48,
          "ga": 13,
          "gd": 35,
          "pts": 33
        },
        {
          "pos": 2,
          "team": "ريال مدريد",
          "p": 12,
          "w": 10,
          "d": 0,
          "l": 2,
          "gf": 31,
          "ga": 10,
          "gd": 21,
          "pts": 30
        },
        {
          "pos": 3,
          "team": "أتلتيكو مدريد",
          "p": 12,
          "w": 9,
          "d": 1,
          "l": 2,
          "gf": null,
          "ga": null,
          "gd": 13,
          "pts": 28
        },
        {
          "pos": 4,
          "team": "ريال بيتيس",
          "p": 12,
          "w": 8,
          "d": 2,
          "l": 2,
          "gf": null,
          "ga": null,
          "gd": 5,
          "pts": 26
        },
        {
          "pos": 5,
          "team": "ريال سوسيداد",
          "p": 12,
          "w": 7,
          "d": 1,
          "l": 4,
          "gf": null,
          "ga": null,
          "gd": 1,
          "pts": 22
        }
      ],
      "scorers": [
        {
          "player": "رافينيا",
          "team": "برشلونة",
          "goals": 15
        },
        {
          "player": "كيليان مبابي",
          "team": "ريال مدريد",
          "goals": 13
        },
        {
          "player": "لامين يامال",
          "team": "برشلونة",
          "goals": 10
        }
      ],
      "meta": "جدول ترتيب الدوري الإسباني 2026-27: برشلونة متصدر بـ33 نقطة، ريال مدريد 30، أتلتيكو 28 — رافينيا هداف الليغا بـ15 هدفاً، مباريات الجولة 13 والنتائج."
    },
    {
      "id": "serie-a",
      "name": "الدوري الإيطالي",
      "short": "الكالتشيو",
      "country": "إيطاليا",
      "season": "2026-27",
      "round": "الجولة 11",
      "next_round": "الجولة 12 — 21–23 نونبر 2026",
      "source": "kickofflens.com (18 نونبر 2026) + مطابقة مع oddalerts.com",
      "table": [
        {
          "pos": 1,
          "team": "لاتسيو",
          "p": 11,
          "w": 9,
          "d": 2,
          "l": 0,
          "gf": null,
          "ga": null,
          "gd": 16,
          "pts": 29
        },
        {
          "pos": 2,
          "team": "إنتر ميلان",
          "p": 11,
          "w": 9,
          "d": 1,
          "l": 1,
          "gf": null,
          "ga": null,
          "gd": 15,
          "pts": 28
        },
        {
          "pos": 3,
          "team": "روما",
          "p": 11,
          "w": 8,
          "d": 3,
          "l": 0,
          "gf": null,
          "ga": null,
          "gd": 21,
          "pts": 27
        },
        {
          "pos": 4,
          "team": "ميلان",
          "p": 11,
          "w": 7,
          "d": 3,
          "l": 1,
          "gf": null,
          "ga": null,
          "gd": 10,
          "pts": 24
        },
        {
          "pos": 5,
          "team": "كومو",
          "p": 11,
          "w": 7,
          "d": 2,
          "l": 2,
          "gf": null,
          "ga": null,
          "gd": 8,
          "pts": 23
        }
      ],
      "scorers": [
        {
          "player": "غوستافو فاريلا",
          "team": "—",
          "goals": 9
        },
        {
          "player": "أنتونيو رايموندو",
          "team": "—",
          "goals": 8
        },
        {
          "player": "دونييل مالين",
          "team": "—",
          "goals": 8
        },
        {
          "player": "نيكولا كرستوفيتش",
          "team": "—",
          "goals": 7
        }
      ],
      "meta": "جدول ترتيب الدوري الإيطالي 2026-27: لاتسيو في الصدارة بـ29 نقطة، إنتر 28، روما 27 — الهدافون، مباريات الجولة 12 (21–23 نونبر) والنتائج."
    },
    {
      "id": "bundesliga",
      "name": "الدوري الألماني",
      "short": "البوندسليغا",
      "country": "ألمانيا",
      "season": "2026-27",
      "round": "الجولة 9",
      "next_round": "الجولة 10 — 20–22 نونبر 2026",
      "source": "kickofflens.com (18 نونبر 2026) + مطابقة مع oddalerts.com وchief-scout.com",
      "table": [
        {
          "pos": 1,
          "team": "بايرن ميونيخ",
          "p": 9,
          "w": 6,
          "d": 3,
          "l": 0,
          "gf": 29,
          "ga": 9,
          "gd": 20,
          "pts": 21
        },
        {
          "pos": 2,
          "team": "بوروسيا دورتموند",
          "p": 9,
          "w": 6,
          "d": 3,
          "l": 0,
          "gf": 16,
          "ga": 7,
          "gd": 9,
          "pts": 21
        },
        {
          "pos": 3,
          "team": "فرايبورغ",
          "p": 9,
          "w": 6,
          "d": 1,
          "l": 2,
          "gf": null,
          "ga": null,
          "gd": 10,
          "pts": 19
        },
        {
          "pos": 4,
          "team": "لايبزيغ",
          "p": 9,
          "w": 6,
          "d": 0,
          "l": 3,
          "gf": null,
          "ga": null,
          "gd": 14,
          "pts": 18
        },
        {
          "pos": 5,
          "team": "باير ليفركوزن",
          "p": 9,
          "w": 5,
          "d": 1,
          "l": 3,
          "gf": null,
          "ga": null,
          "gd": 3,
          "pts": 16
        }
      ],
      "scorers": [
        {
          "player": "نيكلاس فولكروغ",
          "team": "—",
          "goals": 9
        },
        {
          "player": "باتريك شيك",
          "team": "—",
          "goals": 8
        },
        {
          "player": "مايكل أوليز",
          "team": "—",
          "goals": 6
        }
      ],
      "meta": "جدول ترتيب الدوري الألماني 2026-27: بايرن ميونيخ ودورتموند متساويان بـ21 نقطة، فرايبورغ 19 — الهدافون، مباريات الجولة 10 (20–22 نونبر) والنتائج."
    },
    {
      "id": "ligue-1",
      "name": "الدوري الفرنسي",
      "short": "الليغ 1",
      "country": "فرنسا",
      "season": "2026-27",
      "round": "الجولة 10",
      "next_round": "الجولة 11 — 20–22 نونبر 2026",
      "source": "kickofflens.com (18 نونبر 2026) + مطابقة مع oddalerts.com",
      "table": [
        {
          "pos": 1,
          "team": "باريس سان جيرمان",
          "p": 10,
          "w": 7,
          "d": 2,
          "l": 1,
          "gf": null,
          "ga": null,
          "gd": 12,
          "pts": 23
        },
        {
          "pos": 2,
          "team": "ليل",
          "p": 10,
          "w": 6,
          "d": 3,
          "l": 1,
          "gf": null,
          "ga": null,
          "gd": 7,
          "pts": 21
        },
        {
          "pos": 3,
          "team": "باريس إف سي",
          "p": 10,
          "w": 6,
          "d": 2,
          "l": 2,
          "gf": null,
          "ga": null,
          "gd": 7,
          "pts": 20
        },
        {
          "pos": 4,
          "team": "مارسيليا",
          "p": 10,
          "w": 6,
          "d": 0,
          "l": 4,
          "gf": null,
          "ga": null,
          "gd": 8,
          "pts": 18
        },
        {
          "pos": 5,
          "team": "ليون",
          "p": 10,
          "w": 5,
          "d": 2,
          "l": 3,
          "gf": null,
          "ga": null,
          "gd": 6,
          "pts": 17
        }
      ],
      "scorers": [
        {
          "player": "لاسين سينايوكو",
          "team": "—",
          "goals": 9
        },
        {
          "player": "إستيبان لوبول",
          "team": "—",
          "goals": 7
        },
        {
          "player": "أمين غويري",
          "team": "—",
          "goals": 6
        },
        {
          "player": "إلي واهي",
          "team": "—",
          "goals": 6
        }
      ],
      "meta": "جدول ترتيب الدوري الفرنسي 2026-27: باريس سان جيرمان متصدر بـ23 نقطة، ليل 21، باريس إف سي 20 — الهدافون، مباريات الجولة 11 (20–22 نونبر) والنتائج."
    },
    {
      "id": "botola",
      "name": "البطولة الاحترافية المغربية",
      "short": "البطولة",
      "country": "المغرب",
      "season": "2026-27",
      "round": "الجولة 7",
      "next_round": "الجولة 8 — التاريخ قيد التأكيد",
      "source": "le360.ma (09 نونبر 2026) + pitchlabstats.com (جدول 08 نونبر 2026) — المركز 3 غير موثق",
      "table": [
        {
          "pos": 1,
          "team": "الكوكب المراكشي",
          "p": 7,
          "w": 5,
          "d": 1,
          "l": 1,
          "gf": 10,
          "ga": 6,
          "gd": 4,
          "pts": 16
        },
        {
          "pos": 2,
          "team": "النادي المكناسي",
          "p": null,
          "w": null,
          "d": null,
          "l": null,
          "gf": null,
          "ga": null,
          "gd": null,
          "pts": 14
        },
        {
          "pos": 3,
          "team": "— قيد التحقق —",
          "p": null,
          "w": null,
          "d": null,
          "l": null,
          "gf": null,
          "ga": null,
          "gd": null,
          "pts": null,
          "placeholder": true
        },
        {
          "pos": 4,
          "team": "الجيش الملكي",
          "p": 6,
          "w": 3,
          "d": 2,
          "l": 1,
          "gf": 9,
          "ga": 5,
          "gd": 4,
          "pts": 11
        },
        {
          "pos": 5,
          "team": "الوداد الرياضي",
          "p": null,
          "w": null,
          "d": null,
          "l": null,
          "gf": null,
          "ga": null,
          "gd": null,
          "pts": 11
        },
        {
          "pos": 6,
          "team": "المغرب الفاسي",
          "p": 7,
          "w": 3,
          "d": 2,
          "l": 2,
          "gf": 6,
          "ga": 5,
          "gd": 1,
          "pts": 11
        }
      ],
      "scorers": [],
      "meta": "جدول ترتيب البطولة الاحترافية المغربية 2026-27: الكوكب المراكشي متصدر بـ16 نقطة، النادي المكناسي 14، الجيش الملكي 11 — مباريات الجولة 8 والنتائج."
    }
  ],
  "fixtures": {
    "live": [],
    "today": [],
    "tomorrow": [],
    "upcoming": [
      {
        "id": "bayern-koln-2026-11-20",
        "home": "بايرن ميونيخ",
        "away": "كولن",
        "league": "bundesliga",
        "league_name": "الدوري الألماني",
        "date": "2026-11-20",
        "time": "20:30",
        "status": "scheduled",
        "source": "kickofflens.com + football.mib.news (19:30 UTC)"
      },
      {
        "id": "athletic-espanyol-2026-11-20",
        "home": "أتلتيك بلباو",
        "away": "إسبانيول",
        "league": "la-liga",
        "league_name": "الدوري الإسباني",
        "date": "2026-11-20",
        "time": "21:00",
        "status": "scheduled",
        "source": "kickofflens.com + football.mib.news (20:00 UTC)"
      },
      {
        "id": "troyes-lehavre-2026-11-20",
        "home": "تروا",
        "away": "لوهافر",
        "league": "ligue-1",
        "league_name": "الدوري الفرنسي",
        "date": "2026-11-20",
        "time": "20:45",
        "status": "scheduled",
        "source": "vavel.com (14:45 ET = 19:45 UTC) + football.mib.news"
      },
      {
        "id": "man-city-fulham-2026-11-21",
        "home": "مانشستر سيتي",
        "away": "فولهام",
        "league": "premier-league",
        "league_name": "الدوري الإنجليزي",
        "date": "2026-11-21",
        "time": "13:30",
        "status": "scheduled",
        "source": "premierleague.com + nbcsports.com (12:30 UK)"
      },
      {
        "id": "aston-villa-sunderland-2026-11-21",
        "home": "أستون فيلا",
        "away": "سندرلاند",
        "league": "premier-league",
        "league_name": "الدوري الإنجليزي",
        "date": "2026-11-21",
        "time": "16:00",
        "status": "scheduled",
        "source": "premierleague.com (15:00 UK)"
      },
      {
        "id": "bournemouth-nottingham-2026-11-21",
        "home": "بورنموث",
        "away": "نوتينغهام فورست",
        "league": "premier-league",
        "league_name": "الدوري الإنجليزي",
        "date": "2026-11-21",
        "time": "16:00",
        "status": "scheduled",
        "source": "premierleague.com (15:00 UK)"
      },
      {
        "id": "coventry-crystal-palace-2026-11-21",
        "home": "كوفنتري سيتي",
        "away": "كريستال بالاس",
        "league": "premier-league",
        "league_name": "الدوري الإنجليزي",
        "date": "2026-11-21",
        "time": "16:00",
        "status": "scheduled",
        "source": "livescore.in + premierleague.com (15:00 UK)"
      },
      {
        "id": "tottenham-ipswich-2026-11-21",
        "home": "توتنهام",
        "away": "إيبسويتش تاون",
        "league": "premier-league",
        "league_name": "الدوري الإنجليزي",
        "date": "2026-11-21",
        "time": "16:00",
        "status": "scheduled",
        "source": "livescore.in + premierleague.com (15:00 UK)"
      },
      {
        "id": "newcastle-arsenal-2026-11-21",
        "home": "نيوكاسل يونايتد",
        "away": "آرسنال",
        "league": "premier-league",
        "league_name": "الدوري الإنجليزي",
        "date": "2026-11-21",
        "time": "18:30",
        "status": "scheduled",
        "source": "premierleague.com + nbcsports.com (17:30 UK)"
      },
      {
        "id": "real-madrid-celta-2026-11-21",
        "home": "ريال مدريد",
        "away": "سيلتا فيغو",
        "league": "la-liga",
        "league_name": "الدوري الإسباني",
        "date": "2026-11-21",
        "time": null,
        "status": "scheduled",
        "source": "laligatable.co (المباراة المقبلة لريال مدريد — التوقيت قيد التأكيد)"
      },
      {
        "id": "union-leipzig-2026-11-21",
        "home": "يونيون برلين",
        "away": "لايبزيغ",
        "league": "bundesliga",
        "league_name": "الدوري الألماني",
        "date": "2026-11-21",
        "time": "15:30",
        "status": "scheduled",
        "source": "fcstats.com (09:30 ET = 15:30 CET)"
      },
      {
        "id": "leverkusen-paderborn-2026-11-21",
        "home": "باير ليفركوزن",
        "away": "بادربورن",
        "league": "bundesliga",
        "league_name": "الدوري الألماني",
        "date": "2026-11-21",
        "time": "15:30",
        "status": "scheduled",
        "source": "fcstats.com (09:30 ET = 15:30 CET)"
      },
      {
        "id": "gladbach-dortmund-2026-11-21",
        "home": "بوروسيا مونشنغلادباخ",
        "away": "بوروسيا دورتموند",
        "league": "bundesliga",
        "league_name": "الدوري الألماني",
        "date": "2026-11-21",
        "time": "15:30",
        "status": "scheduled",
        "source": "fcstats.com (09:30 ET = 15:30 CET)"
      },
      {
        "id": "augsburg-mainz-2026-11-21",
        "home": "أوغسبورغ",
        "away": "ماينز",
        "league": "bundesliga",
        "league_name": "الدوري الألماني",
        "date": "2026-11-21",
        "time": "15:30",
        "status": "scheduled",
        "source": "fcstats.com (09:30 ET = 15:30 CET)"
      },
      {
        "id": "nice-psg-2026-11-21",
        "home": "نيس",
        "away": "باريس سان جيرمان",
        "league": "ligue-1",
        "league_name": "الدوري الفرنسي",
        "date": "2026-11-21",
        "time": "17:15",
        "status": "scheduled",
        "source": "vavel.com (11:15 ET = 16:15 UTC)"
      },
      {
        "id": "lille-lyon-2026-11-21",
        "home": "ليل",
        "away": "ليون",
        "league": "ligue-1",
        "league_name": "الدوري الفرنسي",
        "date": "2026-11-21",
        "time": "20:45",
        "status": "scheduled",
        "source": "vavel.com (14:45 ET = 19:45 UTC)"
      },
      {
        "id": "hull-brighton-2026-11-22",
        "home": "هال سيتي",
        "away": "برايتون",
        "league": "premier-league",
        "league_name": "الدوري الإنجليزي",
        "date": "2026-11-22",
        "time": "15:00",
        "status": "scheduled",
        "source": "livescore.in (06:00 PT = 14:00 UTC)"
      },
      {
        "id": "liverpool-manutd-2026-11-22",
        "home": "ليفربول",
        "away": "مانشستر يونايتد",
        "league": "premier-league",
        "league_name": "الدوري الإنجليزي",
        "date": "2026-11-22",
        "time": "18:30",
        "status": "scheduled",
        "source": "premierleague.com + nbcsports.com (16:30 UK)"
      },
      {
        "id": "barcelona-villarreal-2026-11-22",
        "home": "برشلونة",
        "away": "فياريال",
        "league": "la-liga",
        "league_name": "الدوري الإسباني",
        "date": "2026-11-22",
        "time": null,
        "status": "scheduled",
        "source": "laligatable.co (المباراة المقبلة لبرشلونة — التوقيت قيد التأكيد)"
      },
      {
        "id": "atalanta-inter-2026-11-22",
        "home": "أتالانتا",
        "away": "إنتر ميلان",
        "league": "serie-a",
        "league_name": "الدوري الإيطالي",
        "date": "2026-11-22",
        "time": null,
        "status": "scheduled",
        "source": "showupandplay.com (عطلة نهاية الأسبوع 21–23 نونبر — اليوم الدقيق قيد التأكيد)",
        "date_label": "21–23 نونبر 2026"
      },
      {
        "id": "juventus-venezia-2026-11-22",
        "home": "يوفنتوس",
        "away": "فينيزيا",
        "league": "serie-a",
        "league_name": "الدوري الإيطالي",
        "date": "2026-11-22",
        "time": null,
        "status": "scheduled",
        "source": "منشور فيسبوك FAFG (عطلة نهاية الأسبوع 21–23 نونبر — اليوم الدقيق قيد التأكيد)",
        "date_label": "21–23 نونبر 2026"
      },
      {
        "id": "brentford-everton-2026-11-23",
        "home": "برينتفورد",
        "away": "إيفرتون",
        "league": "premier-league",
        "league_name": "الدوري الإنجليزي",
        "date": "2026-11-23",
        "time": "21:00",
        "status": "scheduled",
        "source": "livescore.in (12:00 PT = 20:00 UTC)"
      }
    ],
    "results": [
      {
        "id": "mainz-bayern-2026-11-08",
        "home": "ماينز",
        "away": "بايرن ميونيخ",
        "home_goals": 1,
        "away_goals": 2,
        "league": "bundesliga",
        "league_name": "الدوري الألماني",
        "date": "2026-11-08",
        "status": "finished",
        "source": "showupandplay.com (تقرير 08 نونبر 2026)"
      },
      {
        "id": "dortmund-elversberg-2026-11-08",
        "home": "بوروسيا دورتموند",
        "away": "إلفرسبرغ",
        "home_goals": 2,
        "away_goals": 1,
        "league": "bundesliga",
        "league_name": "الدوري الألماني",
        "date": "2026-11-08",
        "status": "finished",
        "source": "showupandplay.com (تقرير 08 نونبر 2026)"
      },
      {
        "id": "napoli-lazio-2026-11-08",
        "home": "نابولي",
        "away": "لاتسيو",
        "home_goals": 1,
        "away_goals": 1,
        "league": "serie-a",
        "league_name": "الدوري الإيطالي",
        "date": "2026-11-08",
        "status": "finished",
        "source": "showupandplay.com (تقرير 08 نونبر 2026)"
      },
      {
        "id": "inter-como-2026-11-08",
        "home": "إنتر ميلان",
        "away": "كومو",
        "home_goals": 2,
        "away_goals": 0,
        "league": "serie-a",
        "league_name": "الدوري الإيطالي",
        "date": "2026-11-08",
        "status": "finished",
        "source": "showupandplay.com (تقرير 08 نونبر 2026)"
      },
      {
        "id": "roma-sassuolo-2026-11-08",
        "home": "روما",
        "away": "ساسولو",
        "home_goals": 3,
        "away_goals": 0,
        "league": "serie-a",
        "league_name": "الدوري الإيطالي",
        "date": "2026-11-08",
        "status": "finished",
        "source": "showupandplay.com (تقرير 08 نونبر 2026)"
      },
      {
        "id": "genoa-milan-2026-11-08",
        "home": "جنوى",
        "away": "ميلان",
        "home_goals": 1,
        "away_goals": 2,
        "league": "serie-a",
        "league_name": "الدوري الإيطالي",
        "date": "2026-11-08",
        "status": "finished",
        "source": "showupandplay.com (تقرير 08 نونبر 2026)"
      },
      {
        "id": "fiorentina-juventus-2026-11-08",
        "home": "فيورنتينا",
        "away": "يوفنتوس",
        "home_goals": 2,
        "away_goals": 2,
        "league": "serie-a",
        "league_name": "الدوري الإيطالي",
        "date": "2026-11-08",
        "status": "finished",
        "source": "showupandplay.com (تقرير 08 نونبر 2026)"
      }
    ]
  }
};
