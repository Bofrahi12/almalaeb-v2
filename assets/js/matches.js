/* الملعب V2 — matches.js: تبويبات حقيقية من data/fixtures.json فقط. بلا محاكاة. */
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
  /* تواريخ ديناميكية من data/fixtures.json (today_date/tomorrow_date) — بلا تواريخ مكتوبة */
  function dayLabel(iso) {
    if (!iso) return "";
    return new Date(iso + "T12:00:00").toLocaleDateString("ar-MA", {weekday: "long", day: "numeric", month: "long", year: "numeric"});
  }
  function shortDay(iso) {
    if (!iso) return "";
    return new Date(iso + "T12:00:00").toLocaleDateString("ar-MA", {day: "numeric", month: "long"});
  }
  function nextDay() {
    const up = (FX.upcoming || []);
    const t = FX.tomorrow_date || "";
    for (const m of up) { if (m.date > t) return m.date; }
    return null;
  }
  function relabelTabs() {
    document.querySelectorAll(".tabs button").forEach(btn => {
      const t = btn.dataset.tab;
      if (t === "today") btn.textContent = "📅 اليوم " + shortDay(FX.today_date);
      else if (t === "tomorrow") btn.textContent = "📅 غداً " + shortDay(FX.tomorrow_date);
      else if (t === "friday") { const nd = nextDay(); btn.textContent = nd ? "⏭️ " + dayLabel(nd) : "⏭️ القادمة"; }
    });
  }
  function render() {
    const box = $("matches-box");
    if (!box || !FX) return;
    let html = "";
    const nd = nextDay();
    const back = nd ? ` العودة ${dayLabel(nd)}.` : "";
    if (currentTab === "today") {
      html = listHTML(FX.today) || emptyMsg(`لا توجد مباريات اليوم (${dayLabel(FX.today_date)}) في الدوريات الستة.${back}`);
    } else if (currentTab === "tomorrow") {
      html = listHTML(FX.tomorrow) || emptyMsg(`لا توجد مباريات غداً (${dayLabel(FX.tomorrow_date)}) في الدوريات الستة.${back}`);
    } else if (currentTab === "friday") {
      const fri = (FX.upcoming || []).filter(m => nd && m.date === nd);
      html = listHTML(fri) || emptyMsg(nd ? `لا توجد مباريات مبرمجة يوم ${dayLabel(nd)}.` : "لا توجد مباريات قادمة مسجلة.");
    } else if (currentTab === "upcoming") {
      html = listHTML(FX.upcoming) || emptyMsg("لا توجد مباريات قادمة مسجلة.");
    } else {
      const r = FX.results || [];
      html = r.length ? listHTML(r) : emptyMsg("لا توجد نتائج مسجلة.");
      if (r.length) {
        const dates = r.map(m => m.date).sort();
        const range = dates[0] === dates[dates.length - 1] ? shortDay(dates[0]) : shortDay(dates[0]) + " – " + shortDay(dates[dates.length - 1]);
        html = `<p class="data-note">آخر النتائج (${range}) — المصدر: ESPN. الأوقات بتوقيت المغرب (UTC+1).</p>` + html;
      }
    }
    box.innerHTML = html;
  }
  document.addEventListener("DOMContentLoaded", async function () {
    await window.loadLogos();
    FX = await window.MalaebData.fixtures();
    render();
    relabelTabs();
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
