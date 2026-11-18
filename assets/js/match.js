/* الملعب V2 — match.js: صفحة تفاصيل المباراة (?id=) — بيانات موثقة فقط، والباقي Placeholder صريح */
(function () {
  "use strict";
  function q(name) { return new URLSearchParams(location.search).get(name); }
  function esc(s) { return String(s == null ? "" : s); }
  document.addEventListener("DOMContentLoaded", async function () {
    window.renderTicker("ticker-track");
    await window.loadLogos();
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
    const infoVenue = m.venue || m.venue_note || "قيد التحقق";
    const infoRef = m.referee || "قيد التحقق";
    const infoChan = m.channel || "قيد التحقق";
    const infoTime = isFin ? "انتهت" : ((m.date_label || m.date || "") + (m.time ? " • " + m.time + " بتوقيت المغرب" : " • التوقيت قيد التأكيد"));
    function statBar(label, h, a) {
      const t = (h || 0) + (a || 0);
      const hp = t ? Math.round(100 * h / t) : 50;
      return `<div class="stat-row"><span><b>${h}</b></span><div><div style="text-align:center;font-size:.8rem;color:var(--muted)">${label}</div><div class="stat-bar"><i class="h" style="width:${hp}%"></i><i class="a" style="width:${100 - hp}%"></i></div></div><span style="text-align:left"><b>${a}</b></span></div>`;
    }
    const st = m.stats || null;
    const statsHTML = st ? (
      statBar("الاستحواذ %", st.possession_home, st.possession_away)
      + statBar("التسديدات", st.shots_home, st.shots_away)
      + statBar("التسديدات على المرمى", st.shots_on_target_home, st.shots_on_target_away)
      + statBar("الركنيات", st.corners_home, st.corners_away)
      + `<p style="color:var(--muted);font-size:.78rem;margin-top:10px">المصدر: ${esc(st.source || "—")}</p>`
    ) : `<div class="placeholder-box">الإحصائيات غير متوفرة بعد لهذه المباراة.<br>تُعرض هنا (الاستحواذ، التسديدات، الركنيات) فور توثيقها من مصدر رسمي.</div>`;
    box.innerHTML = `
    <div class="scoreboard">
      <div class="teams"><span class="team-name">${window.logoFor(m.home)}${esc(m.home)}</span>
      <span class="big-score">${score}</span>
      <span class="team-name">${window.logoFor(m.away)}${esc(m.away)}</span></div>
      <div class="status">${m.league_name} • ${status}</div>
      <div class="status" style="font-size:.8rem">المصدر: ${esc(m.source || "—")} — آخر تحقق: 18 نونبر 2026</div>
    </div>
    <div class="match-info">
      <span><span class="lbl">🏟️ الملعب:</span><b>${esc(infoVenue)}</b></span>
      <span><span class="lbl">الحكم:</span><b>${esc(infoRef)}</b></span>
      <span><span class="lbl">📺 القناة الناقلة:</span><b>${esc(infoChan)}</b></span>
      <span><span class="lbl">🕐 التوقيت:</span><b>${esc(infoTime)}</b></span>
    </div>
    <div class="match-tabs">
      <button data-mtab="events" class="active">الأحداث</button>
      <button data-mtab="stats">الإحصائيات</button>
      <button data-mtab="lineups">التشكيلة</button>
      <button data-mtab="h2h">المواجهات</button>
    </div>
    <div class="mtab-panel" data-panel="events">
      <div class="placeholder-box">لا توجد أحداث موثقة بعد لهذه المباراة (أهداف، بطاقات، تبديلات).<br>تُضاف الأحداث بعد توثيقها من مصدر رسمي.</div>
    </div>
    <div class="mtab-panel" data-panel="stats" style="display:none">${statsHTML}</div>
    <div class="mtab-panel" data-panel="lineups" style="display:none">
      <div class="placeholder-box">التشكيلتان الرسميتان غير موثقتين بعد — تُنشران قبل انطلاق المباراة بساعة من مصدر رسمي.</div>
    </div>
    <div class="mtab-panel" data-panel="h2h" style="display:none">
      <div class="placeholder-box">سجل المواجهات المباشرة بين الفريقين غير موثق بعد — يُضاف من مصدر رسمي.</div>
    </div>
    <p><a href="matches.html" style="color:var(--accent);font-weight:700">← العودة إلى كل المباريات</a></p>`;
    box.querySelectorAll(".match-tabs button").forEach(btn => {
      btn.addEventListener("click", () => {
        box.querySelectorAll(".match-tabs button").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        const tab = btn.dataset.mtab;
        box.querySelectorAll(".mtab-panel").forEach(p => { p.style.display = p.dataset.panel === tab ? "" : "none"; });
      });
    });
  });
})();
