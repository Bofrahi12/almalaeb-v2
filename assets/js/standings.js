/* الملعب V2 — standings.js: 6 دوريات فقط */
(function () {
  "use strict";
  const ORDER = ["premier-league", "la-liga", "serie-a", "bundesliga", "ligue-1", "botola"];
  let DATA = null, current = "premier-league";
  function leagueById(id) { return DATA.leagues.find(l => l.id === id) || DATA.leagues[0]; }
  function renderSelector() {
    const box = document.getElementById("league-select");
    if (!box) return;
    box.innerHTML = ORDER.map(id => leagueById(id)).filter(Boolean).map(l =>
      `<button data-l="${l.id}" class="${l.id === current ? "active" : ""}">${window.leagueLogoFor(l.id)}${l.name}</button>`).join("");
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
    if (title) title.innerHTML = `${window.leagueLogoFor(l.id)}${l.name} <small style="color:var(--muted);font-size:.85rem">موسم ${l.season || "2026-27"} — ${l.round || ""}</small>`;
    const tw = document.getElementById("table-wrap");
    if (tw) tw.innerHTML = window.standingsTableHTML(l)
      + `<p class="data-note"><b>المصدر:</b> ${l.source || "—"} — <b>آخر تحقق:</b> ${DATA.updated || ""}. الجدول الكامل موثق لكل دوري.</p>`;
    const sc = document.getElementById("scorers");
    if (sc) {
      const list = (l.scorers || []).slice(0, 8);
      sc.innerHTML = list.length ? list.map((s, i) => `
        <div class="scorer"><span class="rank">${i + 1}</span>
        <span class="info"><b>${s.player}</b><span>${window.logoFor(s.team)}${s.team}</span></span>
        <span class="goals">${s.goals}</span></div>`).join("")
        : `<div class="placeholder-box">لا توجد قائمة هدافين موثقة لهذا الدوري بعد — تُضاف فور التحقق من مصدر رسمي.</div>`;
    }
    const upd = document.getElementById("data-updated");
    if (upd && DATA.updated) upd.textContent = "آخر تحديث: " + DATA.updated;
  }
  document.addEventListener("DOMContentLoaded", async function () {
    await window.loadLogos();
    DATA = await window.MalaebData.leagues();
    renderSelector();
    renderLeague();
  });
})();
