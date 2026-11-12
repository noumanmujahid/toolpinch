"""Build /tools/2027-tax-brackets (IRS Rev. Proc. 2026-35)."""
import json
from tax_common import page, related, BT_JS

F = lambda b: [[t, r / 100] for t, r in b]
Y27 = {'single': (F([[0,10],[12800,12],[52025,22],[109125,24],[208325,32],[264550,35],[661375,37]]), 16600),
       'married': (F([[0,10],[25600,12],[104050,22],[218250,24],[416650,32],[529100,35],[793650,37]]), 33200),
       'hoh': (F([[0,10],[18250,12],[69650,22],[109100,24],[208300,32],[264550,35],[661350,37]]), 24925),
       'mfs': (F([[0,10],[12800,12],[52025,22],[109125,24],[208325,32],[264550,35],[396825,37]]), 16600)}
Y26 = {'single': (F([[0,10],[12400,12],[50400,22],[105700,24],[201775,32],[256225,35],[640600,37]]), 16100),
       'married': (F([[0,10],[24800,12],[100800,22],[211400,24],[403550,32],[512450,35],[768700,37]]), 32200),
       'hoh': (F([[0,10],[17700,12],[67450,22],[105700,24],[201750,32],[256200,35],[640600,37]]), 24150),
       'mfs': (F([[0,10],[12400,12],[50400,22],[105700,24],[201775,32],[256225,35],[384350,37]]), 16100)}
NAMES = {'single': 'Single', 'married': 'Married filing jointly', 'hoh': 'Head of household', 'mfs': 'Married filing separately'}


def bt(x, b):
    t = 0
    for i, (lo, r) in enumerate(b):
        hi = b[i + 1][0] if i + 1 < len(b) else 1e18
        if x > lo:
            t += (min(x, hi) - lo) * r
    return t


def tax(gross, st, yr):
    b, sd = yr[st]
    return bt(max(0, gross - sd), b)


m = lambda x: f"${int(x + 0.5):,}"
# check: single $75,000 in 2027: taxable 58,400 -> 1,280 + 0.12*(52,025-12,800)=4,707 + 0.22*(58,400-52,025)=1,402.50 -> 7,389.50
assert round(tax(75000, 'single', Y27), 2) == 7389.50
ex = []
for g, st in [(40000, 'single'), (60000, 'single'), (75000, 'single'), (100000, 'single'), (150000, 'single'), (100000, 'married'), (150000, 'married'), (250000, 'married'), (80000, 'hoh')]:
    a, b_ = tax(g, st, Y26), tax(g, st, Y27)
    ex.append((g, st, a, b_))
    print(g, st, round(a), round(b_), round(a - b_))
ex_html = ''.join(f'<tr><td>{m(g)}</td><td>{NAMES[st]}</td><td class="n">{m(a)}</td><td class="n">{m(b_)}</td><td class="n"><b>{m(a-b_)}</b></td><td class="n">{100*b_/g:.1f}%</td></tr>' for g, st, a, b_ in ex)


def btable(st):
    b = Y27[st][0]
    rows = ''
    for i, (lo, r) in enumerate(b):
        hi = b[i + 1][0] if i + 1 < len(b) else None
        cum = bt(lo, b)
        rng = f'{m(lo)} – {m(hi)}' if hi else f'Over {m(lo)}'
        rows += f'<tr><td class="n">{r*100:g}%</td><td>{rng}</td><td>{m(cum)} + {r*100:g}% of the amount over {m(lo)}</td></tr>' if lo else f'<tr><td class="n">{r*100:g}%</td><td>{rng}</td><td>10% of taxable income</td></tr>'
    return f'<div class="tp-scroll"><table class="tp-table"><thead><tr><th class="n">Rate</th><th>Taxable income</th><th>Tax owed</th></tr></thead><tbody>{rows}</tbody></table></div>'


data = json.dumps({'A': Y27, 'B': Y26})
calc = """<div class="mc-calculator"><h2>Your 2027 federal income tax</h2>
<label class="mc-field"><span>Gross income for 2027 ($)</span><input id="bInc" type="number" min="0" step="100" value="75000"></label>
<label class="mc-field"><span>Filing status</span><select id="bSt"><option value="single">Single</option><option value="married">Married filing jointly</option><option value="hoh">Head of household</option><option value="mfs">Married filing separately</option></select></label>
<label class="mc-field"><span>Pre-tax deductions (401(k), HSA) ($)</span><input id="bPre" type="number" min="0" step="100" value="0"></label>
<button class="mc-button" data-action="b27">Calculate</button>
<div class="mc-result tp-res" id="bResult" aria-live="polite">Enter your income to see your 2027 tax.</div></div>"""

script = """<script>(()=>{const D=__D__,$=id=>document.getElementById(id);""" + BT_JS + """
const fmt=x=>x.toLocaleString('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0});
function run(){const g=Math.max(0,+$('bInc').value||0),st=$('bSt').value,pre=Math.min(g,Math.max(0,+$('bPre').value||0)),a=D.A[st],b=D.B[st];
const ti=Math.max(0,g-pre-a[1]),t=BT(ti,a[0]),ti6=Math.max(0,g-pre-b[1]),t6=BT(ti6,b[0]);let mr=0;a[0].forEach(x=>{if(ti>x[0])mr=x[1]});
let h='<p class="tp-big"><strong>'+fmt(t)+'</strong> federal income tax for 2027</p><div class="tp-scroll"><table class="tp-table"><tbody>'+
'<tr><td>Gross income</td><td class="n">'+fmt(g)+'</td></tr>'+(pre?'<tr><td>Pre-tax deductions</td><td class="n">−'+fmt(pre)+'</td></tr>':'')+
'<tr><td>Standard deduction</td><td class="n">−'+fmt(a[1])+'</td></tr><tr><td>Taxable income</td><td class="n">'+fmt(ti)+'</td></tr>'+
'<tr class="tot"><td>Federal income tax</td><td class="n">'+fmt(t)+'</td></tr><tr><td>Marginal tax rate (top bracket)</td><td class="n">'+(mr*100)+'%</td></tr>'+
'<tr><td>Effective tax rate (of gross income)</td><td class="n">'+(g?(100*t/g).toFixed(2):'0.00')+'%</td></tr></tbody></table></div>';
h+='<p>Same income in 2026: '+fmt(t6)+'. '+(t6>t?'You pay <b>'+fmt(t6-t)+' less</b> in 2027 because of inflation adjustments.':'No change.')+'</p>';
h+='<p class="tp-note">Before credits such as the child tax credit. Excludes Social Security and Medicare tax and state tax.</p>';$('bResult').innerHTML=h}
document.addEventListener('DOMContentLoaded',()=>{['bInc','bSt','bPre'].forEach(id=>$(id).addEventListener('input',run));document.querySelectorAll('[data-action="b27"]').forEach(x=>x.addEventListener('click',run));run()})})();</script>"""
script = script.replace('__D__', data)

t75 = tax(75000, 'single', Y27)
body = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>What are the 2027 tax brackets?</h2>
<p class="tp-answer">The seven rates stay at <strong>10%, 12%, 22%, 24%, 32%, 35% and 37%</strong>, but every bracket is about 3.2% wider than in 2026.
The standard deduction rises to <strong>$16,600</strong> for single filers, <strong>$33,200</strong> for married couples filing jointly and <strong>$24,925</strong> for heads of household.
A single filer earning $75,000 owes about <strong>{m(t75)}</strong> in federal income tax for 2027, {m(tax(75000,'single',Y26)-t75)} less than for the same income in 2026.</p>
<p>These apply to income earned from January 1 to December 31, 2027, reported on returns filed in early 2028. The IRS published them on November 5, 2026 in Revenue Procedure 2026-35.</p></header>

<section><h2>2027 federal income tax brackets</h2><div class="mc-example-grid">
<div><h3>Single</h3>{btable('single')}</div>
<div><h3>Married filing jointly</h3>{btable('married')}</div>
<div><h3>Head of household</h3>{btable('hoh')}</div>
<div><h3>Married filing separately</h3>{btable('mfs')}</div></div></section>

<section><h2>2027 vs 2026: what changes</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Item</th><th class="n">2026</th><th class="n">2027</th></tr></thead><tbody>
<tr><td>Standard deduction, single</td><td class="n">$16,100</td><td class="n">$16,600</td></tr>
<tr><td>Standard deduction, married filing jointly</td><td class="n">$32,200</td><td class="n">$33,200</td></tr>
<tr><td>Standard deduction, head of household</td><td class="n">$24,150</td><td class="n">$24,925</td></tr>
<tr><td>12% bracket starts (single)</td><td class="n">$12,400</td><td class="n">$12,800</td></tr>
<tr><td>22% bracket starts (single)</td><td class="n">$50,400</td><td class="n">$52,025</td></tr>
<tr><td>24% bracket starts (single)</td><td class="n">$105,700</td><td class="n">$109,125</td></tr>
<tr><td>37% bracket starts (single)</td><td class="n">$640,600</td><td class="n">$661,375</td></tr>
<tr><td>Child tax credit (maximum)</td><td class="n">$2,200</td><td class="n">$2,300</td></tr>
<tr><td>Annual gift tax exclusion</td><td class="n">$19,000</td><td class="n">$20,000</td></tr>
<tr><td>Health FSA contribution limit</td><td class="n">$3,400</td><td class="n">$3,500</td></tr></tbody></table></div></section>

<section><h2>Same income, less tax: 2026 vs 2027</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Income</th><th>Status</th><th class="n">2026 tax</th><th class="n">2027 tax</th><th class="n">Saving</th><th class="n">2027 effective rate</th></tr></thead><tbody>{ex_html}</tbody></table></div>
<p class="tp-note">Standard deduction, no other deductions or credits. If your pay rises with inflation, your tax will rise too; the adjustment stops inflation alone from pushing you into a higher bracket.</p></section>

<section><h2>How tax brackets work</h2><p>The US uses a <strong>progressive</strong> system: each rate applies only to the slice of taxable income inside its band. Moving into the 22% bracket does not make all your income taxed at 22%.
For a single filer with $58,400 of taxable income in 2027: the first $12,800 is taxed at 10% ($1,280), the next $39,225 at 12% ($4,707), and the last $6,375 at 22% ($1,402.50). Total {m(t75)}, an effective rate of {100*t75/58400:.1f}% of taxable income.</p>
<p><strong>Marginal rate</strong> is the rate on your next dollar of income; <strong>effective rate</strong> is total tax divided by income. Pre-tax 401(k), 403(b), traditional IRA and HSA contributions reduce taxable income, so they save tax at your marginal rate.</p></section>

<section><h2>Other 2027 amounts</h2><ul>
<li>Alternative minimum tax exemption: $93,000 (unmarried), $144,700 (married filing jointly).</li>
<li>Estate tax basic exclusion: $15,480,000.</li>
<li>Maximum earned income tax credit: $8,496 with three or more qualifying children.</li>
<li>HSA contribution limit: $4,500 self-only, $9,000 family.</li></ul>
<p>The 2027 401(k) and IRA contribution limits are announced separately by the IRS and had not been published when this page was updated.</p>
<p>Source: <a href="https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2027-taxpayers-continue-to-benefit-from-the-working-families-tax-cuts" rel="noopener" target="_blank">IRS news release IR-2026-133</a> (Rev. Proc. 2026-35, November 5, 2026). 2026 figures from Rev. Proc. 2025-32.</p></section>
{related('2027-tax-brackets')}"""

faqs = [
    ("What are the 2027 federal tax brackets for single filers?", "10% up to $12,800 of taxable income, 12% up to $52,025, 22% up to $109,125, 24% up to $208,325, 32% up to $264,550, 35% up to $661,375 and 37% above."),
    ("What are the 2027 tax brackets for married filing jointly?", "10% up to $25,600, 12% up to $104,050, 22% up to $218,250, 24% up to $416,650, 32% up to $529,100, 35% up to $793,650 and 37% above."),
    ("What is the 2027 standard deduction?", "$16,600 for single filers and married filing separately, $33,200 for married couples filing jointly and $24,925 for heads of household."),
    ("When do the 2027 tax brackets apply?", "To income earned in calendar year 2027, reported on the tax return filed in early 2028. Income earned in 2026 uses the 2026 brackets on the return filed in early 2027."),
    ("Did tax rates change for 2027?", "No. The seven rates stay the same; only the income thresholds and the standard deduction rise with inflation."),
    ("Will I pay less tax in 2027?", f"If your income stays the same, yes, slightly. A single filer earning $75,000 pays about {m(tax(75000,'single',Y26)-t75)} less federal income tax in 2027 than in 2026."),
    ("What is my marginal tax rate?", "The rate of the highest bracket your taxable income reaches. It applies only to income in that bracket, not to all of your income."),
]

page('2027-tax-brackets', '2027 Tax Brackets and Standard Deduction (IRS Official) + Calculator | ToolPinch',
     'Official 2027 federal tax brackets for single, married and head of household, the $16,600 standard deduction, and a calculator comparing your 2027 tax with 2026.',
     '2027 Federal Tax Brackets', 'IRS Rev. Proc. 2026-35 · Published Nov 5, 2026',
     'See the official 2027 income tax brackets and standard deduction, and calculate how much federal tax you will owe on 2027 income.',
     ['Official IRS figures', 'All filing statuses', 'No signup'], calc, body, faqs, script)
