"""Build /tools/pakistan-salary-tax-calculator (tax year 2027 = FY 2026-27)."""
import json
from tax_common import page, related, BT_JS

TY27 = [[600000, .01], [1200000, .11], [2200000, .20], [3200000, .25], [4100000, .29], [5600000, .32], [7000000, .35]]
TY26 = [[600000, .01], [1200000, .11], [2200000, .23], [3200000, .30], [4100000, .35]]


def bt(x, b):
    t = 0
    for i, (lo, r) in enumerate(b):
        hi = b[i + 1][0] if i + 1 < len(b) else 1e18
        if x > lo:
            t += (min(x, hi) - lo) * r
    return t


def ty26(x):
    t = bt(x, TY26)
    return t * 1.09 if x > 10000000 else t


# fixed amounts published in the Finance Act schedule
for at, fixed in [(1200000, 6000), (2200000, 116000), (3200000, 316000), (4100000, 541000), (5600000, 976000), (7000000, 1424000)]:
    assert round(bt(at, TY27)) == fixed, (at, bt(at, TY27))
for at, fixed in [(2200000, 116000), (3200000, 346000), (4100000, 616000)]:
    assert round(bt(at, TY26)) == fixed
m = lambda x: 'Rs ' + f"{x:,.0f}"
ex = []
for mo in (50000, 75000, 100000, 150000, 200000, 250000, 300000, 400000, 500000, 750000, 1000000):
    a = mo * 12
    t, o = bt(a, TY27), ty26(a)
    ex.append((mo, t, o))
    print(mo, round(t / 12), round(o / 12))
ex_html = ''.join(f'<tr><td>{m(mo)}</td><td class="n"><b>{m(t/12)}</b></td><td class="n">{m(mo-t/12)}</td><td class="n">{m(o/12)}</td><td class="n">{m((o-t)/12)}</td></tr>' for mo, t, o in ex)
slab27 = [("Up to Rs 600,000", "0%"), ("Rs 600,001 – 1,200,000", "1% of the amount over Rs 600,000"),
          ("Rs 1,200,001 – 2,200,000", "Rs 6,000 + 11% over Rs 1,200,000"), ("Rs 2,200,001 – 3,200,000", "Rs 116,000 + 20% over Rs 2,200,000"),
          ("Rs 3,200,001 – 4,100,000", "Rs 316,000 + 25% over Rs 3,200,000"), ("Rs 4,100,001 – 5,600,000", "Rs 541,000 + 29% over Rs 4,100,000"),
          ("Rs 5,600,001 – 7,000,000", "Rs 976,000 + 32% over Rs 5,600,000"), ("Above Rs 7,000,000", "Rs 1,424,000 + 35% over Rs 7,000,000")]
slab_html = ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in slab27)
data = json.dumps({'A': TY27, 'B': TY26})

calc = """<div class="mc-calculator"><h2>Your tax year 2027 salary tax</h2>
<label class="mc-field"><span>Salary (Rs)</span><input id="pSal" type="number" min="0" step="1000" value="150000"></label>
<label class="mc-field"><span>Salary is</span><select id="pPer"><option value="12">Per month</option><option value="1">Per year</option></select></label>
<button class="mc-button" data-action="pk-tax">Calculate</button>
<div class="mc-result tp-res" id="pResult" aria-live="polite">Enter your salary to see your income tax.</div></div>"""

script = """<script>(()=>{const D=__D__,$=id=>document.getElementById(id);""" + BT_JS + """
const fmt=x=>'Rs '+Math.round(x).toLocaleString('en-PK');
function run(){const a=Math.max(0,+$('pSal').value||0)*(+$('pPer').value),t=BT(a,D.A),o=BT(a,D.B)*(a>1e7?1.09:1),mo=a/12;
let h='<p class="tp-big"><strong>'+fmt(t/12)+'</strong> income tax per month</p>';
h+='<div class="tp-scroll"><table class="tp-table"><thead><tr><th></th><th class="n">Monthly</th><th class="n">Yearly</th></tr></thead><tbody>'+
'<tr><td>Gross salary</td><td class="n">'+fmt(mo)+'</td><td class="n">'+fmt(a)+'</td></tr>'+
'<tr><td>Income tax (tax year 2027)</td><td class="n">−'+fmt(t/12)+'</td><td class="n">−'+fmt(t)+'</td></tr>'+
'<tr class="tot"><td>Salary after tax</td><td class="n">'+fmt(mo-t/12)+'</td><td class="n">'+fmt(a-t)+'</td></tr></tbody></table></div>';
h+='<p>Effective tax rate <b>'+(a?(100*t/a).toFixed(2):'0.00')+'%</b>. Last year (tax year 2026) the tax on this salary was '+fmt(o/12)+' a month, so you '+(o>t?'save <b>'+fmt((o-t)/12)+'</b> a month ('+fmt(o-t)+' a year).':'pay the same.')+'</p>';
h+='<p class="tp-note">Salaried individuals (salary over 75% of taxable income). EOBI, provident fund and other deductions by your employer are not included.</p>';$('pResult').innerHTML=h}
document.addEventListener('DOMContentLoaded',()=>{['pSal','pPer'].forEach(id=>$(id).addEventListener('input',run));
document.querySelectorAll('[data-action="pk-tax"]').forEach(b=>b.addEventListener('click',run));run()})})();</script>""".replace('__D__', data)

t150 = bt(1800000, TY27); t300 = bt(3600000, TY27); o300 = ty26(3600000)
script = script.replace('__D__', data)
body = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>How much tax is deducted from salary in Pakistan in 2026–27?</h2>
<p class="tp-answer">Annual salary up to <strong>Rs 600,000</strong> (Rs 50,000 a month) is tax-free. Above that, rates rise from 1% to 35% under the Finance Act 2026, which applies to tax year 2027 (1 July 2026 to 30 June 2027).
On <strong>Rs 150,000 a month</strong> the tax is <strong>{m(t150/12)}</strong> a month, the same as last year; on <strong>Rs 300,000 a month</strong> it is <strong>{m(t300/12)}</strong>, down from {m(o300/12)} in tax year 2026.</p>
<p>The budget cut the rates for the Rs 2.2 million to Rs 4.1 million bands, added new 29% and 32% bands, and abolished the 9% surcharge on salaried income above Rs 10 million.</p></header>

<section><h2>Salary tax slabs for tax year 2027</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Annual taxable salary</th><th>Tax</th></tr></thead><tbody>{slab_html}</tbody></table></div>
<p class="tp-note">For individuals whose salary is more than 75% of taxable income. Non-salaried individuals and AOPs have a separate, higher schedule.</p></section>

<section><h2>Monthly tax by salary</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Monthly salary</th><th class="n">Tax per month (2026–27)</th><th class="n">Take-home</th><th class="n">Tax per month (2025–26)</th><th class="n">Monthly saving</th></tr></thead><tbody>{ex_html}</tbody></table></div></section>

<section><h2>What changed from last year</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Annual salary</th><th class="n">Tax year 2026</th><th class="n">Tax year 2027</th></tr></thead><tbody>
<tr><td>Up to Rs 1.2 million</td><td class="n">0% / 1%</td><td class="n">0% / 1% (unchanged)</td></tr>
<tr><td>Rs 1.2 – 2.2 million</td><td class="n">11%</td><td class="n">11% (unchanged)</td></tr>
<tr><td>Rs 2.2 – 3.2 million</td><td class="n">23%</td><td class="n">20%</td></tr>
<tr><td>Rs 3.2 – 4.1 million</td><td class="n">30%</td><td class="n">25%</td></tr>
<tr><td>Rs 4.1 – 5.6 million</td><td class="n">35%</td><td class="n">29%</td></tr>
<tr><td>Rs 5.6 – 7.0 million</td><td class="n">35%</td><td class="n">32%</td></tr>
<tr><td>Above Rs 7.0 million</td><td class="n">35%</td><td class="n">35%</td></tr>
<tr><td>Surcharge above Rs 10 million</td><td class="n">9% of tax</td><td class="n">Abolished</td></tr></tbody></table></div></section>

<section><h2>How it works and sources</h2>
<p>Employers deduct tax every month under section 149 of the Income Tax Ordinance, 2001 by working out the tax on your expected annual salary and dividing it over the remaining months.
The calculator applies the slabs to gross taxable salary. Tax-exempt allowances, such as some medical allowances, reduce taxable salary; contributions to approved pension funds and Zakat can earn credits or deductions that are not included here.</p>
<p>Slabs from the Finance Act 2026 (enacted 27 June 2026), as reported by
<a href="https://propakistani.pk/2026/06/12/heres-how-much-tax-youll-be-paying-after-revised-tax-slabs/" rel="noopener" target="_blank">ProPakistani</a> and
<a href="https://paktaxcalculator.pk/commentary-after-budget-2026-27/" rel="noopener" target="_blank">PakTaxCalculator commentary</a>, with the fixed amounts checked against the schedule.
See the <a href="https://www.fbr.gov.pk/" rel="noopener" target="_blank">Federal Board of Revenue</a> for the official text.</p></section>
{related('pakistan-salary-tax-calculator', [('/tools/salary-to-hourly-calculator', 'Salary to hourly'), ('/tools/percentage-calculator', 'Percentage calculator')])}"""

f = lambda mo: (bt(mo * 12, TY27) / 12)
faqs = [
    ("What is the tax-free salary limit in Pakistan for 2026–27?", "Rs 600,000 a year, or Rs 50,000 a month. It is unchanged from last year."),
    ("How much tax on a Rs 100,000 monthly salary?", f"{m(f(100000))} a month in tax year 2027 ({m(f(100000)*12)} a year)."),
    ("How much tax on a Rs 200,000 monthly salary?", f"{m(f(200000))} a month in tax year 2027, down from {m(ty26(2400000)/12)} last year."),
    ("How much tax on a Rs 300,000 monthly salary?", f"{m(f(300000))} a month in tax year 2027, down from {m(ty26(3600000)/12)} last year."),
    ("Was the surcharge on salaried income removed?", "Yes. The Finance Act 2026 abolished the 9% surcharge that applied to salaried individuals earning more than Rs 10 million a year."),
    ("What is tax year 2027?", "In Pakistan the tax year is named after the year in which it ends, so tax year 2027 runs from 1 July 2026 to 30 June 2027 (fiscal year 2026–27)."),
    ("What is the highest salary tax rate?", "35%, on annual salary above Rs 7 million, with a fixed amount of Rs 1,424,000 on the first Rs 7 million."),
]

page('pakistan-salary-tax-calculator', 'Salary Tax Calculator Pakistan 2026–27 (Tax Year 2027) | ToolPinch',
     'Calculate monthly income tax on salary in Pakistan for 2026–27 using the Finance Act 2026 slabs. Compare with last year and see your take-home pay.',
     'Pakistan Salary Tax Calculator 2026–27', 'Tax year 2027 · Finance Act 2026',
     'Find the monthly income tax on your salary under the new 2026–27 slabs, your take-home pay, and how much you save compared with last year.',
     ['Finance Act 2026 slabs', 'Compare with 2025–26', 'No signup'], calc, body, faqs, script)
