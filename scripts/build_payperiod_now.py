"""Build /tools/what-pay-period-is-it (federal pay period lookup, leave years 2026-2028).
Run from repo root: PYTHONPATH=scripts python3 scripts/build_payperiod_now.py"""
import json
from fed_dates import periods, HOL, D
from tax_common import page

YEARS = (2026, 2027, 2028)
P = {y: periods(y) for y in YEARS}
data = json.dumps({str(y): [[n, s.isoformat(), e.isoformat(), d.isoformat(), o.isoformat()] for n, s, e, d, o in P[y]] for y in YEARS})

f = lambda d: f"{d.strftime('%a')}, {d.strftime('%b')} {d.day}, {d.year}"
sh = lambda d: f"{d.strftime('%b')} {d.day}"


def note(dep, off):
    out = []
    if dep.weekday() == 1:
        out.append(f'{HOL[dep.fromordinal(dep.toordinal() - 1)]} moves the deposit to Tuesday')
    if off in HOL:
        out.append(f'Official pay date is {HOL[off]}')
    return '; '.join(out)


rows26 = ''.join(f'<tr><td>{n}</td><td>{sh(s)} – {sh(e)}{", " + str(e.year) if e.year != 2026 else ""}</td><td>{f(d)}</td><td>{note(d, o)}</td></tr>' for n, s, e, d, o in P[2026])
# stable worked examples for the FAQ
ex = []
for day in (D(2026, 12, 1), D(2027, 3, 15), D(2027, 7, 4)):
    for y in YEARS:
        for n, s, e, d, o in P[y]:
            if s <= day <= e:
                ex.append((day, y, n, (day - s).days + 1, d))
ex_txt = '; '.join(f'{sh(a)}, {a.year} is pay period {n} of leave year {y} (day {k} of 14), paid by NFC on {sh(d)}{", " + str(d.year) if d.year != a.year else ""}' for a, y, n, k, d in ex)

calc = """<div class="mc-calculator"><h2>Pay period for any date</h2>
<label class="mc-field"><span>Date</span><input id="ppD" type="date" min="2026-01-11" max="2029-01-06"></label>
<button class="mc-button" data-action="pp">Show pay period</button>
<div class="mc-result tp-res" id="ppR" aria-live="polite">Pick a date.</div>
<h3 class="tp-wide" style="margin:14px 0 0">Next NFC paydays</h3>
<div class="mc-result tp-res" id="ppN"></div></div>"""

script = """<script>(()=>{const Y=__D__,$=id=>document.getElementById(id);
const p=s=>{const[a,b,c]=s.split('-').map(Number);return new Date(a,b-1,c,12)},iso=d=>d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
const fm=s=>p(s).toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric',year:'numeric'}),days=(a,b)=>Math.round((p(b)-p(a))/864e5);
const all=Object.entries(Y).flatMap(([y,L])=>L.map(r=>({y,n:r[0],s:r[1],e:r[2],d:r[3],o:r[4]})));
function run(){const v=$('ppD').value;if(!v)return;const x=all.find(r=>v>=r.s&&v<=r.e);
if(!x){$('ppR').innerHTML='Pick a date between Jan 11, 2026 and Jan 6, 2029.';return}
const k=days(x.s,v)+1,left=days(v,x.e),tot=Y[x.y].length,rem=tot-x.n;
let t='<p class="tp-big"><strong>Pay period '+x.n+'</strong> of '+tot+', leave year '+x.y+'</p>';
t+='<div class="tp-scroll"><table class="tp-table"><tbody><tr><td>Day of pay period</td><td class="n">Day '+k+' of 14 (week '+(k<=7?1:2)+')</td></tr><tr><td>Pay period dates</td><td class="n">'+fm(x.s)+' – '+fm(x.e)+'</td></tr>'+
'<tr><td>Days left in this pay period</td><td class="n">'+left+'</td></tr><tr><td>NFC deposit for this pay period</td><td class="n"><b>'+fm(x.d)+'</b></td></tr><tr><td>Official pay date</td><td class="n">'+fm(x.o)+'</td></tr>'+
'<tr><td>Pay periods left in leave year '+x.y+'</td><td class="n">'+rem+'</td></tr></tbody></table></div>';
$('ppR').innerHTML=t;
const up=all.filter(r=>r.d>=v).slice(0,4);$('ppN').innerHTML='<div class="tp-scroll"><table class="tp-table"><tbody>'+up.map((r,i)=>'<tr><td>'+fm(r.d)+'</td><td>PP '+r.n+' ('+r.y+')</td><td class="n">'+(days(v,r.d)===0?'today':'in '+days(v,r.d)+' days')+'</td></tr>').join('')+'</tbody></table></div><p class="tp-note">NFC deposit dates. Most banks post federal pay on the deposit date.</p>'}
document.addEventListener('DOMContentLoaded',()=>{const t=iso(new Date());$('ppD').value=(t>='2026-01-11'&&t<='2029-01-06')?t:'2027-01-10';$('ppD').addEventListener('input',run);document.querySelectorAll('[data-action="pp"]').forEach(b=>b.addEventListener('click',run));run()})})();</script>"""
script = script.replace('__D__', data)

ly = lambda y: f"{f(P[y][0][1])} to {f(P[y][-1][2])}"
body = f"""
<header><p class="mc-kicker mc-dark">How it works</p><h2>What pay period is it today?</h2>
<p class="tp-answer">The calculator shows today's federal pay period as soon as the page loads. Federal pay periods are 14 days long, run Sunday to Saturday, and are numbered 1 to 26 from the start of each leave year.</p>
<p>For example: {ex_txt}.</p></header>

<section><h2>Federal leave years at a glance</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Leave year</th><th>Dates</th><th>Pay periods</th></tr></thead><tbody>
<tr><td>2026</td><td>{ly(2026)}</td><td>26</td></tr><tr><td>2027</td><td>{ly(2027)}</td><td>26</td></tr><tr><td>2028</td><td>{ly(2028)}</td><td>26</td></tr></tbody></table></div>
<p>Each leave year starts with the first full biweekly pay period of the calendar year, so it begins in early January and ends in early January of the next year. See the <a href="/tools/federal-pay-periods-2027">full NFC pay period calendar for 2027</a> for every 2027 date and the use-or-lose leave deadline.</p></section>

<section><h2>How to work out the pay period number yourself</h2>
<ol><li>Find the start of the leave year: Sunday, January 11, 2026; Sunday, January 10, 2027; or Sunday, January 9, 2028.</li>
<li>Count the days from that Sunday to your date.</li>
<li>Divide by 14, drop the remainder and add 1. That is the pay period number. The remainder plus 1 is the day of the pay period (days 1 to 7 are week 1).</li></ol>
<p>Example: December 1, 2026 is 324 days after January 11, 2026. 324 ÷ 14 = 23 remainder 2, so it is pay period 24, day 3.</p></section>

<section><h2>2026 federal pay period calendar</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>PP</th><th>Pay period</th><th>NFC deposit</th><th>Notes</th></tr></thead><tbody>{rows26}</tbody></table></div>
<p class="tp-note">NFC deposits settle on the second Monday after the pay period ends, or Tuesday when that Monday is a federal holiday. Agencies paid by DFAS, the Interior Business Center or GSA use the same pay periods but may pay on a different day. Sources: <a href="https://www.opm.gov/policy-data-oversight/pay-leave/leave-administration/fact-sheets/leave-year-beginning-and-ending-dates" rel="noopener" target="_blank">OPM leave year dates</a>, <a href="https://www.nfc.usda.gov/Publications/Forms/pay_period_calendar.php" rel="noopener" target="_blank">NFC pay period calendars</a>, <a href="https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/" rel="noopener" target="_blank">OPM federal holidays</a>.</p></section>
<nav class="mc-related-links" aria-label="Related tools"><h2>Related calculators</h2><a href="/tools/federal-pay-periods-2027">NFC pay period calendar 2027</a><a href="/tools/federal-holidays-2027">Federal holidays 2027</a><a href="/tools/military-pay-dates-2027">Military pay dates 2027</a><a href="/tools/payday-calendar-2027">2027 payday calendar</a><a href="/tools/long-weekends-2027">Long weekends 2027</a><a href="/tools/us-paycheck-calculator">US paycheck calculator</a><a href="/tools/pay-period-converter">Pay period converter</a></nav>"""

faqs = [("What pay period is it right now?", "Open this page and the calculator shows today's federal pay period, the day of the period, and the next NFC payday. Pay periods are numbered 1 to 26 within each leave year."),
        ("What pay period is December 2026?", "December 2026 covers the end of pay period 23 (Nov 15 to 28), pay period 24 (Nov 29 to Dec 12), pay period 25 (Dec 13 to 26) and the start of pay period 26 (Dec 27, 2026 to Jan 9, 2027)."),
        ("When does pay period 1 of 2027 start?", "Sunday, January 10, 2027. Leave year 2026 ends on Saturday, January 9, 2027 with pay period 26."),
        ("How many pay periods are left in 2026?", "Leave year 2026 has 26 pay periods ending January 9, 2027. The calculator shows how many remain from any date you choose."),
        ("Is it a pay week this week?", "For NFC-paid employees, pay is deposited on the Monday of the second week after a pay period ends. The next paydays are listed in the calculator."),
        ("Do all federal agencies use the same pay periods?", "Yes. Executive branch agencies use the same biweekly pay periods and leave year. The pay date can differ by payroll provider (NFC, DFAS, IBC or GSA).")]

page('what-pay-period-is-it', 'What Pay Period Is It? Federal Pay Period Today | ToolPinch',
     "See today's federal pay period number, the day of the period, days left, and the next NFC payday. Covers leave years 2026, 2027 and 2028.",
     'What Pay Period Is It?', 'Federal pay periods 2026–2028',
     "Today's federal pay period, its dates, and your next NFC payday, plus any date from January 2026 to January 2029.",
     ['Updates to today', 'NFC paydays', 'No signup'], calc, body, faqs, script)
