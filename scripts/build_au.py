"""Build /tools/australia-take-home-pay-calculator (2026-27)."""
import json
from tax_common import page, related, BT_JS, RENDER_JS, PERIOD_SELECT

RES = [[18200, .15], [45000, .30], [135000, .37], [190000, .45]]
HELP = [69528, 129717, 186050]


def bt(x, b):
    t = 0
    for i, (lo, r) in enumerate(b):
        hi = b[i + 1][0] if i + 1 < len(b) else 1e18
        if x > lo:
            t += (min(x, hi) - lo) * r
    return t


def lito(ti):
    if ti <= 37500: return 700
    if ti <= 45000: return 700 - .05 * (ti - 37500)
    return max(0, 325 - .015 * (ti - 45000))


def medicare(ti):
    if ti <= 28011: return 0
    return min(.10 * (ti - 28011), .02 * ti)


def help_rep(ti):
    if ti <= HELP[0]: return 0
    if ti <= HELP[1]: return .15 * (ti - HELP[0])
    if ti <= HELP[2]: return 9028 + .17 * (ti - HELP[1])
    return .10 * ti


def calc_py(g, salsac=0, hd=False, med=True):
    ti = max(0, g - salsac)
    tax = max(0, bt(ti, RES) - lito(ti))
    ml = medicare(ti) if med else 0
    hp = help_rep(ti) if hd else 0
    return round(tax, 2), round(ml, 2), round(hp, 2)


# checks against the ATO table: tax on $45,000 = 4,020 (less LITO 325); on $135,000 = 31,020
assert round(bt(45000, RES)) == 4020 and round(bt(135000, RES)) == 31020 and round(bt(190000, RES)) == 51370
assert calc_py(80000) == (round(4020 + 35000 * .3, 2), 1600.0, 0)
m = lambda x: f"${x:,.0f}"
ex = [(g, calc_py(g)) for g in (40000, 50000, 60000, 70000, 80000, 90000, 100000, 120000, 150000, 200000)]
for g, r in ex:
    print(g, r, round(g - sum(r)))
ex_html = ''.join(f'<tr><td>{m(g)}</td><td class="n">{m(r[0])}</td><td class="n">{m(r[1])}</td><td class="n"><b>{m(g-sum(r))}</b></td><td class="n">{m((g-sum(r))/12)}</td><td class="n">{m((g-sum(r))/26)}</td><td class="n">{m(g*.12)}</td></tr>' for g, r in ex)
data = json.dumps({'R': RES, 'H': HELP})

calc = f"""<div class="mc-calculator"><h2>Your 2026–27 take-home pay</h2>
<label class="mc-field"><span>Annual salary before tax, excluding super ($)</span><input id="aGross" type="number" min="0" step="100" value="80000"></label>
<label class="mc-field"><span>Salary sacrifice to super ($ per year)</span><input id="aSac" type="number" min="0" step="100" value="0"></label>
<label class="mc-field"><span>HELP / HECS study debt</span><select id="aHelp"><option value="0">No</option><option value="1">Yes</option></select></label>
<label class="mc-field"><span>Medicare levy</span><select id="aMed"><option value="1">Pay 2% levy</option><option value="0">Exempt</option></select></label>
{PERIOD_SELECT}
<button class="mc-button" data-action="au-pay">Calculate</button>
<div class="mc-result tp-res" id="aResult" aria-live="polite">Enter your salary to see your take-home pay.</div></div>"""

script = """<script>(()=>{const D=__D__,$=id=>document.getElementById(id);""" + BT_JS + RENDER_JS + """
const fmt=x=>x.toLocaleString('en-AU',{style:'currency',currency:'AUD'});
const lito=t=>t<=37500?700:t<=45000?700-.05*(t-37500):Math.max(0,325-.015*(t-45000));
const hp=t=>t<=D.H[0]?0:t<=D.H[1]?.15*(t-D.H[0]):t<=D.H[2]?9028+.17*(t-D.H[1]):.1*t;
function run(){const g=Math.max(0,+$('aGross').value||0),sac=Math.min(g,Math.max(0,+$('aSac').value||0)),ti=g-sac;
const tax=Math.max(0,BT(ti,D.R)-lito(ti)),ml=$('aMed').value==='1'&&ti>28011?Math.min(.1*(ti-28011),.02*ti):0,h=$('aHelp').value==='1'?hp(ti):0;
const rows=[['Income tax',tax,1],['Medicare levy',ml,1]];if(h>0)rows.push(['HELP repayment',h,0]);if(sac>0)rows.push(['Salary sacrifice to super',sac,0]);
const net=g-rows.reduce((a,r)=>a+r[1],0);renderRes($('aResult'),g,rows,net,fmt,$('per').value);
$('aResult').insertAdjacentHTML('beforeend','<p class="tp-note">Your employer also pays super guarantee of '+fmt(Math.min(g,270830)*.12)+' a year (12%), on top of your salary. Low income tax offset applied: '+fmt(Math.min(lito(ti),BT(ti,D.R)))+'.</p>')}
document.addEventListener('DOMContentLoaded',()=>{['aGross','aSac','aHelp','aMed','per'].forEach(id=>$(id).addEventListener('input',run));
document.querySelectorAll('[data-action="au-pay"]').forEach(b=>b.addEventListener('click',run));run()})})();</script>""".replace('__D__', data)

r80 = calc_py(80000); n80 = 80000 - sum(r80)
script = script.replace('__D__', data)
body = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>How much tax do you pay in Australia in 2026–27?</h2>
<p class="tp-answer">Residents pay no tax on the first <strong>$18,200</strong>, then <strong>15%</strong> to $45,000, <strong>30%</strong> to $135,000, <strong>37%</strong> to $190,000 and <strong>45%</strong> above, plus the <strong>2% Medicare levy</strong>.
On an $80,000 salary you pay {m(r80[0])} tax and {m(r80[1])} Medicare levy and take home <strong>{m(n80)}</strong> a year ({m(n80/26)} a fortnight).</p>
<p>The lowest rate falls from 16% to <strong>15%</strong> on 1 July 2026, the first step of the tax cut legislated in 2025, and to 14% from 1 July 2027.</p></header>

<section><h2>Take-home pay by salary (2026–27)</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Salary</th><th class="n">Income tax</th><th class="n">Medicare</th><th class="n">Take-home / year</th><th class="n">Per month</th><th class="n">Per fortnight</th><th class="n">Employer super (12%)</th></tr></thead><tbody>{ex_html}</tbody></table></div>
<p class="tp-note">Resident for the full year, no HELP debt, low income tax offset applied.</p></section>

<section><h2>2026–27 resident tax rates</h2>
<table class="tp-table"><thead><tr><th>Taxable income</th><th>Tax on this income</th></tr></thead><tbody>
<tr><td>$0 – $18,200</td><td>Nil</td></tr><tr><td>$18,201 – $45,000</td><td>15c for each $1 over $18,200</td></tr>
<tr><td>$45,001 – $135,000</td><td>$4,020 plus 30c for each $1 over $45,000</td></tr><tr><td>$135,001 – $190,000</td><td>$31,020 plus 37c for each $1 over $135,000</td></tr>
<tr><td>$190,001 and over</td><td>$51,370 plus 45c for each $1 over $190,000</td></tr></tbody></table>
<p><strong>Low income tax offset (LITO):</strong> up to $700 for taxable income up to $37,500, reducing to nothing at $66,667. With LITO, a resident pays no income tax on about the first $22,866.</p>
<p><strong>Medicare levy:</strong> 2% of taxable income. Singles earning $28,011 or less pay nothing, with a phase-in up to $35,013. A Medicare levy surcharge of 1% to 1.5% applies to higher earners without private hospital cover (not included).</p></section>

<section><h2>HELP repayments for 2026–27</h2>
<table class="tp-table"><thead><tr><th>Repayment income</th><th>Repayment</th></tr></thead><tbody>
<tr><td>Up to $69,528</td><td>Nil</td></tr><tr><td>$69,529 – $129,717</td><td>15c for each $1 over $69,528</td></tr>
<tr><td>$129,718 – $186,050</td><td>$9,028 plus 17c for each $1 over $129,717</td></tr><tr><td>$186,051 and over</td><td>10% of total repayment income</td></tr></tbody></table>
<p>Since 2025–26, HELP repayments are worked out on the income above the threshold, not on your whole income.</p></section>

<section><h2>How the calculator works</h2>
<p>Taxable income is your salary minus salary sacrifice to super. Super guarantee is paid by your employer on top of your salary at 12% and is not deducted from your take-home pay.
The calculator assumes you are an Australian resident for tax purposes for the whole year with no other income, deductions or offsets. Working holiday makers and foreign residents pay different rates.</p>
<p>Sources: <a href="https://www.ato.gov.au/tax-rates-and-codes/tax-rates-australian-residents" rel="noopener" target="_blank">ATO tax rates for Australian residents</a>,
<a href="https://www.ato.gov.au/tax-rates-and-codes/study-and-training-support-loans-rates-and-repayment-thresholds" rel="noopener" target="_blank">ATO study and training loan repayment thresholds</a> and
<a href="https://www.pitcher.com.au/tax-facts-2026-27/" rel="noopener" target="_blank">Pitcher Partners Tax Facts 2026–27</a>.</p></section>
{related('australia-take-home-pay-calculator', [('/tools/salary-to-hourly-calculator', 'Salary to hourly'), ('/tools/pay-period-converter', 'Pay period converter')])}"""

r60, r100 = calc_py(60000), calc_py(100000)
faqs = [
    ("How much is $80,000 after tax in Australia?", f"{m(n80)} a year in 2026–27, or {m(n80/12)} a month and {m(n80/26)} a fortnight, after {m(r80[0])} income tax and {m(r80[1])} Medicare levy."),
    ("How much is $100,000 after tax in Australia?", f"{m(100000-sum(r100))} a year, or {m((100000-sum(r100))/26)} a fortnight, with no HELP debt."),
    ("How much is $60,000 after tax in Australia?", f"{m(60000-sum(r60))} a year, or {m((60000-sum(r60))/26)} a fortnight."),
    ("What are the tax rates for 2026–27?", "Nil up to $18,200, 15% to $45,000, 30% to $135,000, 37% to $190,000 and 45% above, plus the 2% Medicare levy."),
    ("What is the tax-free threshold?", "$18,200. With the low income tax offset, residents pay no income tax on about the first $22,866 of taxable income."),
    ("What is the super guarantee rate for 2026–27?", "12% of ordinary time earnings, paid by your employer on top of your salary, up to a maximum contribution base of $270,830 a year."),
    ("When do I start repaying HELP?", "When your repayment income is above $69,528 in 2026–27. You repay 15 cents for each dollar above that, rising to 17 cents above $129,717."),
    ("When does the 2026–27 financial year run?", "From 1 July 2026 to 30 June 2027."),
]

page('australia-take-home-pay-calculator', 'Australia Take-Home Pay Calculator 2026–27: Salary After Tax | ToolPinch',
     'Work out your 2026–27 take-home pay in Australia after income tax at the new 15% rate, Medicare levy and HELP repayments, with employer super shown.',
     'Australia Take-Home Pay Calculator 2026–27', 'Financial year 1 July 2026 to 30 June 2027',
     'See your salary after income tax, the Medicare levy and HELP repayments, per fortnight, month or year, using the 2026–27 rates.',
     ['ATO 2026–27 rates', 'HELP and super', 'No signup'], calc, body, faqs, script)
