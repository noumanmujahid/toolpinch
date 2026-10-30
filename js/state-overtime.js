(() => {
  'use strict';
  // State overtime calculator. Rules come from the data-rule attribute on #otState:
  //   ca   California: 1.5x over 8/day and over 40 regular hours/week, 2x over 12/day,
  //        7th consecutive day in the workweek: 1.5x first 8 hours, 2x after 8.
  //   flsa Weekly only: 1.5x over the weekly threshold (40, or 44 for NY residential employees).
  const $ = id => document.getElementById(id);
  const money = n => n.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
  const hrs = n => (Math.round(n * 100) / 100).toLocaleString('en-US', { maximumFractionDigits: 2 });
  const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

  function calc(rule, hours, weeklyLimit) {
    let reg = 0, ot = 0, dt = 0;
    if (rule === 'ca') {
      const seventh = hours.every(h => h > 0);
      hours.forEach((h, i) => {
        if (i === 6 && seventh) { ot += Math.min(h, 8); dt += Math.max(h - 8, 0); return; }
        reg += Math.min(h, 8); ot += Math.min(Math.max(h - 8, 0), 4); dt += Math.max(h - 12, 0);
      });
      const excess = Math.max(reg - 40, 0);
      reg -= excess; ot += excess;
    } else {
      const total = hours.reduce((a, b) => a + b, 0);
      reg = Math.min(total, weeklyLimit); ot = Math.max(total - weeklyLimit, 0);
    }
    return { reg, ot, dt };
  }

  function run() {
    const box = $('otState');
    if (!box) return;
    const rule = box.dataset.rule;
    const rate = Math.max(0, Number($('otRate').value) || 0);
    const hours = DAYS.map((d, i) => Math.min(24, Math.max(0, Number($('otDay' + i).value) || 0)));
    const live = $('otLiveIn') && $('otLiveIn').checked;
    const limit = live ? 44 : 40;
    const r = calc(rule, hours, limit);
    const total = hours.reduce((a, b) => a + b, 0);
    const pay = rate * (r.reg + 1.5 * r.ot + 2 * r.dt);
    const fed = calc('flsa', hours, 40);
    const fedPay = rate * (fed.reg + 1.5 * fed.ot);
    const premium = 0.5 * rate * Math.max(total - 40, 0);
    let h = '<p class="tp-big"><strong>' + money(pay) + '</strong> gross pay for ' + hrs(total) + ' hours</p>';
    h += '<p>Regular: ' + hrs(r.reg) + ' h × ' + money(rate) + ' = ' + money(rate * r.reg) + '<br>Overtime (1.5×): ' + hrs(r.ot) + ' h = ' + money(1.5 * rate * r.ot);
    if (rule === 'ca') h += '<br>Double time (2×): ' + hrs(r.dt) + ' h = ' + money(2 * rate * r.dt);
    h += '</p>';
    if (rule === 'ca' && Math.abs(pay - fedPay) > 0.004) h += '<p class="tp-note">Under federal rules alone (weekly overtime only) this week would pay ' + money(fedPay) + '. California daily overtime adds ' + money(pay - fedPay) + '.</p>';
    if (rule === 'ca' && hours.every(x => x > 0)) h += '<p class="tp-note">You worked all 7 days, so Sunday is paid under the seventh-day rule.</p>';
    if (live) h += '<p class="tp-note">Residential (live-in) employee: overtime starts after 44 hours.</p>';
    if (premium > 0) h += '<p class="tp-note">Overtime premium that may count toward the federal "no tax on overtime" deduction: about ' + money(premium) + ' (the extra half-time on hours over 40).</p>';
    $('otResult').innerHTML = h;
  }

  document.addEventListener('DOMContentLoaded', () => {
    if (!$('otState')) return;
    document.querySelectorAll('#otState input').forEach(i => i.addEventListener('input', run));
    document.querySelectorAll('[data-action="state-overtime"]').forEach(b => b.addEventListener('click', run));
    run();
  });
  window.ToolPinchStateOT = { calc };
})();
