/* الملعب V2 — match.js: صفحة تفاصيل المباراة (?id=) — بيانات موثقة فقط، والباقي Placeholder صريح */
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
