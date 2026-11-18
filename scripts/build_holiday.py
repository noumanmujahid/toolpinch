"""Build /tools/holiday-pay-calculator. Run from repo root: PYTHONPATH=scripts python3 scripts/build_holiday.py"""
from tax_common import page


def calc_py(rate, reg, hol, mult, paid_off=0, credit=True):
    worked = reg + hol
    base = rate * worked
    prem = rate * (mult - 1) * hol
    ot_hrs = max(0, worked - 40)
    ot_extra = 0.5 * rate * ot_hrs
    if credit and mult >= 1.5:
        ot_extra = max(0, ot_extra - prem)
    off = rate * paid_off
    return dict(base=base, prem=prem, ot=ot_extra, off=off, total=base + prem + ot_extra + off, ot_hrs=ot_hrs)


r = calc_py(20, 32, 8, 1.5)
assert r['total'] == 880, r
r = calc_py(20, 40, 8, 1.5)
assert r['total'] == 1040, r
assert calc_py(20, 40, 8, 1.5, credit=False)['total'] == 1120
assert calc_py(20, 40, 8, 2.0)['total'] == 960 + 160          # premium 160 covers OT 80
assert calc_py(20, 32, 0, 1.5, paid_off=8)['total'] == 800
m = lambda x: f"${x:,.2f}"
EX = [('$18/hr, 8 hours on Thanksgiving, 32 other hours, time and a half', 18, 32, 8, 1.5),
      ('$22/hr, 10 hours on Christmas, 40 other hours, time and a half', 22, 40, 10, 1.5),
      ('$25/hr, 8 hours on New Year\'s Day, 32 other hours, double time', 25, 32, 8, 2.0),
      ('$16/hr, 8 hours on Thanksgiving, 40 other hours, no holiday premium', 16, 40, 8, 1.0)]
ex_html = ''.join(f'<tr><td>{lab}</td><td class="n">{m(calc_py(r_, a, b, mu)["total"])}</td><td class="n">{m(calc_py(r_, a, b, mu)["total"] - r_ * (a + b))}</td></tr>' for lab, r_, a, b, mu in EX)

calc = """<div class="mc-calculator"><h2>Your holiday week pay</h2>
<label class="mc-field"><span>Hourly rate ($)</span><input id="hR" type="number" min="0" step="0.01" value="20"></label>
<label class="mc-field"><span>Holiday pay rate</span><select id="hM"><option value="1">Regular rate (no premium)</option><option value="1.5" selected>Time and a half (1.5×)</option><option value="2">Double time (2×)</option><option value="2.5">Double time and a half (2.5×)</option></select></label>
<label class="mc-field"><span>Hours worked on the holiday</span><input id="hH" type="number" min="0" max="24" step="0.25" value="8"></label>
<label class="mc-field"><span>Other hours worked that week</span><input id="hO" type="number" min="0" max="120" step="0.25" value="32"></label>
<label class="mc-field"><span>Paid holiday hours not worked</span><input id="hP" type="number" min="0" max="40" step="0.25" value="0"></label>
<label class="mc-field"><span>Overtime policy</span><select id="hC"><option value="1">Holiday premium counts toward overtime (no pyramiding)</option><option value="0">Overtime paid on top of holiday premium</option></select></label>
<button class="mc-button" data-action="hol">Calculate</button>
<div class="mc-result tp-res" id="hRes" aria-live="polite">Enter your hours.</div></div>"""

script = """<script>(()=>{const $=id=>document.getElementById(id),v=id=>Math.max(0,+$(id).value||0),f=x=>x.toLocaleString('en-US',{style:'currency',currency:'USD'});
function run(){const r=v('hR'),mu=+$('hM').value,h=v('hH'),o=v('hO'),p=v('hP'),cr=$('hC').value==='1';
const w=h+o,base=r*w,prem=r*(mu-1)*h,otH=Math.max(0,w-40);let ot=.5*r*otH;const credited=cr&&mu>=1.5&&ot>0?Math.min(ot,prem):0;ot-=credited;const off=r*p,tot=base+prem+ot+off;
let t='<p class="tp-big"><strong>'+f(tot)+'</strong> gross pay for the week</p><div class="tp-scroll"><table class="tp-table"><tbody>'+
'<tr><td>'+w+' hours worked × '+f(r)+'</td><td class="n">'+f(base)+'</td></tr>'+(prem?'<tr><td>Holiday premium ('+h+' h × '+f(r*(mu-1))+')</td><td class="n">'+f(prem)+'</td></tr>':'')+
(otH?'<tr><td>Overtime premium ('+otH+' h over 40 × '+f(r/2)+')'+(credited?' after crediting '+f(credited)+' of holiday premium':'')+'</td><td class="n">'+f(ot)+'</td></tr>':'')+
(off?'<tr><td>Paid holiday not worked ('+p+' h)</td><td class="n">'+f(off)+'</td></tr>':'')+'<tr class="tot"><td>Total gross pay</td><td class="n">'+f(tot)+'</td></tr></tbody></table></div>';
t+='<p>Working the holiday adds <b>'+f(h*r*mu)+'</b> for those '+h+' hours, '+(mu>1?f(prem)+' more than at your regular rate.':'the same as a normal day.')+'</p>';
t+='<p class="tp-note">Gross pay before taxes. Federal law does not require holiday premium pay; check your employer\\'s policy or union contract.</p>';$('hRes').innerHTML=t}
document.addEventListener('DOMContentLoaded',()=>{['hR','hM','hH','hO','hP','hC'].forEach(i=>$(i).addEventListener('input',run));document.querySelectorAll('[data-action="hol"]').forEach(b=>b.addEventListener('click',run));run()})})();</script>"""

HOL = [("Thanksgiving", "Thu, Nov 26, 2026"), ("Christmas Day", "Fri, Dec 25, 2026"), ("New Year's Day", "Fri, Jan 1, 2027"),
       ("Martin Luther King Jr. Day", "Mon, Jan 18, 2027"), ("Presidents Day", "Mon, Feb 15, 2027"), ("Memorial Day", "Mon, May 31, 2027"),
       ("Juneteenth (observed)", "Fri, Jun 18, 2027"), ("Independence Day (observed)", "Mon, Jul 5, 2027"), ("Labor Day", "Mon, Sep 6, 2027"),
       ("Columbus Day", "Mon, Oct 11, 2027"), ("Veterans Day", "Thu, Nov 11, 2027"), ("Thanksgiving", "Thu, Nov 25, 2027"), ("Christmas (observed)", "Fri, Dec 24, 2027")]
hol_html = ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in HOL)

body = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>Do you get paid extra for working a holiday?</h2>
<p class="tp-answer">Only if your employer, contract or state requires it. <strong>Federal law does not require holiday pay</strong> or a premium for working Thanksgiving, Christmas or any other holiday. Many employers still pay <strong>time and a half</strong> or <strong>double time</strong>.
At $20 an hour, 8 hours on Thanksgiving at time and a half pays <strong>$240</strong> instead of $160.</p>
<p><strong>Thanksgiving 2026 is Thursday, November 26.</strong> Christmas Day and New Year's Day both fall on a Friday this year.</p></header>

<section><h2>Holiday pay examples</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Situation</th><th class="n">Weekly gross pay</th><th class="n">Extra from holiday and overtime</th></tr></thead><tbody>{ex_html}</tbody></table></div>
<p class="tp-note">Assumes holiday premium counts toward overtime, the most common policy.</p></section>

<section><h2>How holiday pay and overtime work together</h2>
<ul><li><strong>Overtime is based on hours actually worked.</strong> Under the Fair Labor Standards Act, non-exempt employees earn overtime for hours worked over 40 in a week. Hours you work on a holiday count; a paid holiday you take off does not.</li>
<li><strong>Holiday premiums can offset overtime.</strong> If your employer pays at least time and a half for holiday work, federal rules let that extra premium be credited toward overtime owed for the same week, so you are not paid "time and a half on time and a half." Some employers and union contracts pay both; the calculator lets you choose.</li>
<li><strong>Paid holidays off</strong> are usually paid at your regular rate and do not count toward the 40 hours.</li>
<li><strong>Salaried exempt employees</strong> generally receive their normal salary for a holiday week, whether or not they work the holiday.</li></ul></section>

<section><h2>State holiday pay laws</h2>
<p><strong>Rhode Island</strong> is the only state with a general holiday premium: covered employers must pay at least time and a half for work on Sundays and state holidays, including Thanksgiving and Christmas, with exemptions for some industries.
<strong>Massachusetts</strong> used to require a premium for retail work on Sundays and certain holidays, but it was phased out and ended in 2023. No other state requires holiday premium pay for private employers, although state overtime rules such as <a href="/tools/overtime-calculator-california">California's daily overtime</a> still apply on holidays.</p>
<p><strong>Federal government employees</strong> who work on a federal holiday receive holiday premium pay equal to their basic rate (double time) for non-overtime hours.</p></section>

<section><h2>US holidays coming up</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Holiday</th><th>Date</th></tr></thead><tbody>{hol_html}</tbody></table></div>
<p>Federal holidays falling on a Saturday are observed on the Friday before, and on a Sunday the Monday after. Private employers decide which holidays they pay; the most common are New Year's Day, Memorial Day, Independence Day, Labor Day, Thanksgiving and Christmas.</p>
<p>Sources: <a href="https://www.dol.gov/general/topic/workhours/holidays" rel="noopener" target="_blank">US Department of Labor: holidays</a>, <a href="https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/" rel="noopener" target="_blank">OPM federal holidays</a> and <a href="https://www.clockspot.com/research/holiday-pay-laws-by-state" rel="noopener" target="_blank">holiday pay laws by state</a>.</p></section>
<nav class="mc-related-links" aria-label="Related tools"><h2>Related calculators</h2><a href="/tools/overtime-calculator">Overtime calculator</a><a href="/tools/timesheet-calculator">Timesheet calculator</a><a href="/tools/us-paycheck-calculator">US paycheck calculator</a><a href="/tools/bonus-tax-calculator">Bonus tax calculator</a><a href="/tools/payday-calendar-2027">2027 payday calendar</a></nav>"""

faqs = [("Is holiday pay required by law?", "Not under federal law. The Fair Labor Standards Act does not require pay for holidays or a premium for working them. Rhode Island requires time and a half for many employers; otherwise it depends on your employer's policy or contract."),
        ("How much is time and a half on a holiday?", "Multiply your hourly rate by 1.5. At $20 an hour, holiday time and a half is $30 an hour, so an 8-hour shift pays $240."),
        ("Does holiday pay count toward overtime?", "Hours you actually work on a holiday count toward the 40-hour overtime threshold. Paid holiday hours you take off do not. A holiday premium of at least time and a half can be credited toward overtime owed in the same week."),
        ("When is Thanksgiving 2026?", "Thursday, November 26, 2026. Christmas Day is Friday, December 25, 2026, and New Year's Day is Friday, January 1, 2027."),
        ("Do part-time workers get holiday pay?", "Only if the employer's policy includes them. There is no federal requirement, and many employers limit paid holidays to full-time staff."),
        ("Do salaried employees get extra pay for working a holiday?", "Exempt salaried employees usually receive their normal salary regardless; extra pay or a substitute day off depends on company policy.")]

page('holiday-pay-calculator', 'Holiday Pay Calculator: Thanksgiving, Christmas Time and a Half and Double Time | ToolPinch',
     'Calculate holiday pay for Thanksgiving, Christmas and New Year with time and a half or double time, overtime over 40 hours, and paid holidays off. Includes state rules.',
     'Holiday Pay Calculator', 'Thanksgiving: Thu, Nov 26, 2026',
     'Work out your pay for a holiday week: holiday premium, overtime over 40 hours and paid holidays you take off.',
     ['Time and a half or double time', 'Overtime included', 'No signup'], calc, body, faqs, script)
