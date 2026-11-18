/* الملعب V2 — main.js: فلتر صارم: 6 دوريات فقط، بلا محاكاة، بلا مسابقات أخرى */
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

  /* الشعارات: ملفات محلية من data/logos.json — فريق بلا شعار يظهر نصاً فقط */
  window.MalaebLogos = { leagues: {}, byAr: {}, ready: false, promise: null };
  window.loadLogos = function () {
    if (window.MalaebLogos.promise) return window.MalaebLogos.promise;
    window.MalaebLogos.promise = (async function () {
      try {
        const d = await loadJSON("data/logos.json");
        if (d) {
          window.MalaebLogos.leagues = d.leagues || {};
          (d.clubs || []).forEach(c => { window.MalaebLogos.byAr[c.ar] = c.file; });
        }
      } catch (e) {}
      window.MalaebLogos.ready = true;
      return window.MalaebLogos;
    })();
    return window.MalaebLogos.promise;
  };
  window.logoFor = function (teamName) {
    if (!teamName || teamName === "—") return "";
    const f = window.MalaebLogos.byAr[teamName];
    if (!f) return "";
    const esc = String(teamName).replace(/"/g, "&quot;");
    return `<img class="team-logo" src="${f}" alt="شعار ${esc}" loading="lazy" onerror="this.remove()">`;
  };
  window.leagueLogoFor = function (leagueId) {
    const f = window.MalaebLogos.leagues[leagueId];
    if (!f) return "";
    return `<img class="league-logo" src="${f}" alt="شعار الدوري" loading="lazy" onerror="this.remove()">`;
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
    const liveCount = onlyAllowed(fx.live || []).length;
    const head = liveCount ? "" : "<span class='ticker-item'>لا مباريات مباشرة الآن — القادمة:</span>";
    el.innerHTML = head + (items.join("") || "<span class='ticker-item'>لا توجد مباريات مبرمجة في الدوريات الستة حالياً</span>");
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
        <td>${r.pos}</td><td class="team">${window.logoFor(r.team)}${r.team}</td><td>${cell(r.p)}</td>
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
    const badge = isLive
      ? `<span class="status-badge live">● مباشر ${m.minute || ""}'</span>`
      : isFin
        ? `<span class="status-badge finished">انتهت</span>`
        : `<span class="status-badge upcoming">لم تبدأ بعد</span>`;
    const time = isLive
      ? `<span class="time">${m.minute || ""}'</span>`
      : `<span class="time">${m.date_label || m.date || ""} ${m.time || ""}</span>`;
    const inner = `<div class="match-row">
      <span class="lg">${m.league_name || ""}${badge}</span>
      <span class="team">${window.logoFor(m.home)}${m.home}</span>${score}<span class="team away">${window.logoFor(m.away)}${m.away}</span>${time}
    </div>`;
    return m.id ? `<a class="match-link" href="match.html?id=${m.id}">${inner}</a>` : inner;
  };
})();
