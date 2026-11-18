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
    await window.loadLogos();
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
