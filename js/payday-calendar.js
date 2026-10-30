(() => {
  'use strict';
  // US bank (Federal Reserve) holidays around 2027. Saturday holidays are not
  // observed by Reserve Banks; Sunday holidays move to Monday.
  const BANK_HOLIDAYS = {
    '2026-12-25': 'Christmas Day',
    '2027-01-01': "New Year's Day",
    '2027-01-18': 'Martin Luther King Jr. Day',
    '2027-02-15': "Washington's Birthday",
    '2027-05-31': 'Memorial Day',
    '2027-07-05': 'Independence Day (observed)',
    '2027-09-06': 'Labor Day',
    '2027-10-11': 'Columbus Day',
    '2027-11-11': 'Veterans Day',
    '2027-11-25': 'Thanksgiving Day',
    '2028-01-17': 'Martin Luther King Jr. Day'
  };
  const YEAR = 2027;
  const $ = id => document.getElementById(id);
  const iso = d => d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  const parse = s => { const [y, m, d] = s.split('-').map(Number); return new Date(y, m - 1, d, 12); };
  const addDays = (d, n) => { const x = new Date(d); x.setDate(x.getDate() + n); return x; };
  const isBusinessDay = d => d.getDay() !== 0 && d.getDay() !== 6 && !BANK_HOLIDAYS[iso(d)];
  const fmt = d => d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
  const monthName = m => new Date(YEAR, m, 1).toLocaleDateString('en-US', { month: 'long' });
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  function adjust(d, mode) {
    if (mode === 'none' || isBusinessDay(d)) return d;
    const step = mode === 'next' ? 1 : -1;
    let x = d;
    while (!isBusinessDay(x)) x = addDays(x, step);
    return x;
  }

  function scheduled(freq, anchor) {
    const out = [];
    if (freq === 'weekly' || freq === 'biweekly') {
      const step = freq === 'weekly' ? 7 : 14;
      const lo = new Date(YEAR - 1, 11, 1, 12), hi = new Date(YEAR + 1, 0, 31, 12);
      let d = new Date(anchor);
      while (d > lo) d = addDays(d, -step);
      while (d <= hi) { if (d >= lo) out.push(d); d = addDays(d, step); }
    } else {
      for (let y = YEAR - 1; y <= YEAR + 1; y++) {
        for (let m = 0; m < 12; m++) {
          const lastDay = new Date(y, m + 1, 0, 12);
          if (freq === 'semimonthly') out.push(new Date(y, m, 15, 12), lastDay);
          else if (freq === 'semimonthly-1-15') out.push(new Date(y, m, 1, 12), new Date(y, m, 15, 12));
          else out.push(lastDay);
        }
      }
    }
    return out;
  }

  function syncFields() {
    const freq = $('payFrequency').value;
    const anchored = freq === 'weekly' || freq === 'biweekly';
    $('anchorField').hidden = !anchored;
  }

  function run() {
    const freq = $('payFrequency').value;
    const mode = $('payAdjust').value;
    const anchorValue = $('payAnchor').value;
    const res = $('paydayResult');
    if ((freq === 'weekly' || freq === 'biweekly') && !anchorValue) {
      res.innerHTML = 'Enter any one of your real paydays to anchor the schedule.';
      return;
    }
    const anchor = anchorValue ? parse(anchorValue) : null;
    const rows = scheduled(freq, anchor).map(s => ({ s, p: adjust(s, mode) }))
      .filter(r => r.p.getFullYear() === YEAR)
      .sort((a, b) => a.p - b.p);
    const byMonth = Array.from({ length: 12 }, () => []);
    rows.forEach(r => byMonth[r.p.getMonth()].push(r));
    const normal = { weekly: 4, biweekly: 2, semimonthly: 2, 'semimonthly-1-15': 2, monthly: 1 }[freq];
    const extra = byMonth.map((r, i) => r.length > normal ? monthName(i) : null).filter(Boolean);
    const moved = rows.filter(r => iso(r.s) !== iso(r.p));
    const crossed = scheduled(freq, anchor).map(s => ({ s, p: adjust(s, mode) }))
      .filter(r => (r.s.getFullYear() === YEAR) !== (r.p.getFullYear() === YEAR));

    let html = '<p class="tp-big"><strong>' + rows.length + '</strong> paydays in ' + YEAR + '</p>';
    if (freq === 'biweekly' && rows.length === 27) html += '<p class="tp-flag">This is a 27-payday year. If pay is based on an annual salary divided by 26, the year will cost the employer one extra paycheck.</p>';
    if (freq === 'weekly' && rows.length === 53) html += '<p class="tp-flag">This is a 53-payday year for a weekly payroll.</p>';
    if (extra.length) html += '<p>Months with an extra paycheck: <strong>' + extra.join(', ') + '</strong>.</p>';
    if (crossed.length) html += '<p class="tp-note">' + crossed.map(r => 'The payday scheduled for ' + fmt(r.s) + ' moves to ' + fmt(r.p) + ', which changes the year it counts in.').join(' ') + '</p>';
    if (moved.length) html += '<p class="tp-note">' + moved.length + ' payday' + (moved.length > 1 ? 's were' : ' was') + ' moved off a weekend or bank holiday (marked *).</p>';
    html += '<div class="tp-months">';
    byMonth.forEach((list, i) => {
      html += '<div class="tp-month' + (list.length > normal ? ' tp-extra' : '') + '"><b>' + monthName(i) + ' <span>' + list.length + '</span></b>';
      list.forEach(r => {
        const note = iso(r.s) !== iso(r.p) ? ' title="Scheduled ' + esc(fmt(r.s)) + (BANK_HOLIDAYS[iso(r.s)] ? ', ' + esc(BANK_HOLIDAYS[iso(r.s)]) : '') + '"' : '';
        html += '<span' + note + '>' + r.p.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' }) + (note ? ' *' : '') + '</span>';
      });
      html += '</div>';
    });
    html += '</div>';
    res.innerHTML = html;
    lastRows = rows;
  }

  let lastRows = [];
  const freqLabel = () => $('payFrequency').selectedOptions[0].textContent;

  function download(name, type, text) {
    const url = URL.createObjectURL(new Blob([text], { type }));
    const a = document.createElement('a');
    a.href = url; a.download = name;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function exportIcs() {
    if (!lastRows.length) run();
    const stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+/, '');
    const lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//ToolPinch//Payday Calendar 2027//EN', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH'];
    lastRows.forEach((r, i) => {
      const day = iso(r.p).replace(/-/g, '');
      const next = iso(addDays(r.p, 1)).replace(/-/g, '');
      lines.push('BEGIN:VEVENT', 'UID:payday-' + day + '-' + i + '@toolpinch.com', 'DTSTAMP:' + stamp,
        'DTSTART;VALUE=DATE:' + day, 'DTEND;VALUE=DATE:' + next, 'SUMMARY:Payday',
        'DESCRIPTION:' + freqLabel().replace(/[,;]/g, ' ') + ' payday. Made with toolpinch.com/tools/payday-calendar-2027', 'TRANSP:TRANSPARENT', 'END:VEVENT');
    });
    lines.push('END:VCALENDAR');
    download('paydays-2027.ics', 'text/calendar', lines.join('\r\n') + '\r\n');
  }

  function exportCsv() {
    if (!lastRows.length) run();
    const out = ['Payday,Weekday,Scheduled date,Moved?'];
    lastRows.forEach(r => out.push([iso(r.p), r.p.toLocaleDateString('en-US', { weekday: 'long' }), iso(r.s), iso(r.s) !== iso(r.p) ? 'Yes' : 'No'].join(',')));
    download('paydays-2027.csv', 'text/csv', out.join('\n') + '\n');
  }

  document.addEventListener('DOMContentLoaded', () => {
    if (!$('payFrequency')) return;
    $('payFrequency').addEventListener('change', () => { syncFields(); run(); });
    $('payAnchor').addEventListener('change', run);
    $('payAdjust').addEventListener('change', run);
    document.querySelectorAll('[data-action="payday-2027"]').forEach(b => b.addEventListener('click', run));
    if ($('payIcs')) $('payIcs').addEventListener('click', exportIcs);
    if ($('payCsv')) $('payCsv').addEventListener('click', exportCsv);
    if ($('payPrint')) $('payPrint').addEventListener('click', () => window.print());
    syncFields();
    run();
  });
})();
