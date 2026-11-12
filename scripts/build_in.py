"""Build /tools/india-income-tax-calculator (FY 2026-27, old vs new regime)."""
import json
from tax_common import page, related, BT_JS, PERIOD_SELECT

L = 100000
NEW = [[4*L, .05], [8*L, .10], [12*L, .15], [16*L, .20], [20*L, .25], [24*L, .30]]
OLD = {'u60': [[2.5*L, .05], [5*L, .20], [10*L, .30]], 's60': [[3*L, .05], [5*L, .20], [10*L, .30]], 's80': [[5*L, .20], [10*L, .30]]}


def bt(x, b):
    t = 0
    for i, (lo, r) in enumerate(b):
        hi = b[i + 1][0] if i + 1 < len(b) else 1e18
        if x > lo:
            t += (min(x, hi) - lo) * r
    return t


def surcharge(ti, tax, new):
    r = 0
    if ti > 50*L: r = .10
    if ti > 100*L: r = .15
    if ti > 200*L: r = .25
    if ti > 500*L and not new: r = .37
    return tax * r


def calc_new(g):
    ti = max(0, g - 75000)
    tax = bt(ti, NEW)
    if ti <= 12*L:
        tax = 0
    else:
        tax = min(tax, ti - 12*L)   # marginal relief
    sc = surcharge(ti, tax, True)
    return ti, tax, sc, (tax + sc) * .04


def calc_old(g, age='u60', ded=0):
    ti = max(0, g - 50000 - ded)
    tax = bt(ti, OLD[age])
    if ti <= 5*L:
        tax = max(0, tax - 12500)
    sc = surcharge(ti, tax, False)
    return ti, tax, sc, (tax + sc) * .04


assert calc_new(1275000)[1] == 0                          # ₹12.75 lakh salary: nil tax
t = calc_new(1300000)                                     # taxable 12.25L: slab tax 63,750 vs relief 25,000
assert t[1] == 25000, t
assert calc_new(2000000)[1] == bt(1925000, NEW) == 185000


def breakeven(g):
    tn = sum(calc_new(g)[1:])
    d = 0
    while sum(calc_old(g, 'u60', d)[1:]) > tn:
        d += 1000
    return d


BE = {g: breakeven(g) for g in (10*L, 15*L, 20*L, 25*L)}
print('breakeven', BE)
m = lambda x: '₹' + format_in(x)


def format_in(x):
    x = int(round(x))
    s = str(x)
    if len(s) <= 3: return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:]); head = head[:-2]
    if head: parts.insert(0, head)
    return ','.join(parts) + ',' + tail


assert format_in(1275000) == '12,75,000'
lk = lambda x: f'₹{x/L:.2f}'.rstrip('0').rstrip('.') + ' lakh'
ex = []
for g in (6*L, 8*L, 10*L, 12*L, 12.75*L, 15*L, 18*L, 20*L, 25*L, 30*L, 50*L):
    n = calc_new(g); o = calc_old(g, 'u60', 2*L)
    tn = n[1] + n[2] + n[3]; to = o[1] + o[2] + o[3]
    ex.append((g, tn, to))
    print(g, round(tn), round(to))
ex_html = ''.join(f'<tr><td>{m(g)}</td><td class="n"><b>{m(tn)}</b></td><td class="n">{m(to)}</td><td>{"New" if tn < to else ("Old" if to < tn else "Same")}</td><td class="n">{m((g-tn)/12)}</td></tr>' for g, tn, to in ex)
data = json.dumps({'N': NEW, 'O': OLD})

calc = f"""<div class="mc-calculator"><h2>Your FY 2026–27 tax</h2>
<label class="mc-field"><span>Annual gross salary (₹)</span><input id="iGross" type="number" min="0" step="1000" value="1500000"></label>
<label class="mc-field"><span>Age</span><select id="iAge"><option value="u60">Below 60</option><option value="s60">60 to 79</option><option value="s80">80 or above</option></select></label>
<label class="mc-field"><span>Employee PF (₹ per year)</span><input id="iPf" type="number" min="0" step="100" value="0"></label>
<label class="mc-field"><span>Professional tax (₹ per year)</span><input id="iPt" type="number" min="0" step="100" value="2500"></label>
<p class="tp-note" style="margin:4px 0 0"><b>Old regime deductions</b> (ignored in the new regime)</p>
<label class="mc-field"><span>80C investments excluding PF (₹)</span><input id="i80c" type="number" min="0" step="1000" value="0"></label>
<label class="mc-field"><span>80D health insurance (₹)</span><input id="i80d" type="number" min="0" step="1000" value="0"></label>
<label class="mc-field"><span>HRA exemption (₹)</span><input id="iHra" type="number" min="0" step="1000" value="0"></label>
<label class="mc-field"><span>Home loan interest, 24(b) (₹)</span><input id="iHl" type="number" min="0" step="1000" value="0"></label>
<label class="mc-field"><span>NPS 80CCD(1B) (₹)</span><input id="iNps" type="number" min="0" step="1000" value="0"></label>
<button class="mc-button" data-action="in-tax">Compare regimes</button>
<div class="mc-result tp-res" id="iResult" aria-live="polite">Enter your salary to compare the new and old regimes.</div></div>"""

script = """<script>(()=>{const D=__D__,$=id=>document.getElementById(id),L=1e5;""" + BT_JS + """
const fmt=x=>'₹'+Math.round(x).toLocaleString('en-IN'),v=id=>Math.max(0,+$(id).value||0);
const sur=(ti,t,nw)=>t*(ti>500*L&&!nw?.37:ti>200*L?.25:ti>100*L?.15:ti>50*L?.10:0);
function run(){const g=v('iGross'),age=$('iAge').value,pf=v('iPf'),pt=Math.min(2500,v('iPt'));
const tiN=Math.max(0,g-75000-pt);let tN=BT(tiN,D.N);tN=tiN<=12*L?0:Math.min(tN,tiN-12*L);const sN=sur(tiN,tN,true),cN=(tN+sN)*.04,totN=tN+sN+cN;
const ded=Math.min(150000,pf+v('i80c'))+Math.min(100000,v('i80d'))+v('iHra')+Math.min(200000,v('iHl'))+Math.min(50000,v('iNps'));
const tiO=Math.max(0,g-50000-pt-ded);let tO=BT(tiO,D.O[age]);if(tiO<=5*L)tO=Math.max(0,tO-12500);const sO=sur(tiO,tO,false),cO=(tO+sO)*.04,totO=tO+sO+cO;
const best=totN<=totO?'new':'old',save=Math.abs(totN-totO);
const col=(n,ti,t,s,c,tot)=>'<td class="n">'+fmt(ti)+'</td>';
let h='<p class="tp-big"><strong>'+fmt(Math.min(totN,totO))+'</strong> tax a year under the <b>'+best+' regime</b></p>';
h+='<p>'+(save<1?'Both regimes give the same tax.':'The '+best+' regime saves you <b>'+fmt(save)+'</b> a year.')+'</p>';
h+='<div class="tp-scroll"><table class="tp-table"><thead><tr><th></th><th class="n">New regime</th><th class="n">Old regime</th></tr></thead><tbody>'+
'<tr><td>Gross salary</td><td class="n">'+fmt(g)+'</td><td class="n">'+fmt(g)+'</td></tr>'+
'<tr><td>Standard deduction</td><td class="n">−'+fmt(Math.min(g,75000))+'</td><td class="n">−'+fmt(Math.min(g,50000))+'</td></tr>'+
'<tr><td>Professional tax</td><td class="n">−'+fmt(pt)+'</td><td class="n">−'+fmt(pt)+'</td></tr>'+
'<tr><td>Chapter VI-A, HRA and home loan</td><td class="n">—</td><td class="n">−'+fmt(ded)+'</td></tr>'+
'<tr><td>Taxable income</td><td class="n">'+fmt(tiN)+'</td><td class="n">'+fmt(tiO)+'</td></tr>'+
'<tr><td>Income tax (after 87A rebate)</td><td class="n">'+fmt(tN)+'</td><td class="n">'+fmt(tO)+'</td></tr>'+
'<tr><td>Surcharge</td><td class="n">'+fmt(sN)+'</td><td class="n">'+fmt(sO)+'</td></tr>'+
'<tr><td>Health and education cess (4%)</td><td class="n">'+fmt(cN)+'</td><td class="n">'+fmt(cO)+'</td></tr>'+
'<tr class="tot"><td>Total tax</td><td class="n">'+fmt(totN)+'</td><td class="n">'+fmt(totO)+'</td></tr>'+
'<tr><td>Monthly in-hand (after tax, PF, prof. tax)</td><td class="n">'+fmt((g-totN-pf-pt)/12)+'</td><td class="n">'+fmt((g-totO-pf-pt)/12)+'</td></tr></tbody></table></div>';
if(tiN>12*L&&tiN<12.75*L)h+='<p class="tp-note">Marginal relief applied: your new-regime tax is capped at the amount by which taxable income exceeds ₹12 lakh.</p>';
h+='<p class="tp-note">Effective tax rate: '+(g?(100*Math.min(totN,totO)/g).toFixed(1):'0.0')+'% of gross salary.</p>';$('iResult').innerHTML=h}
document.addEventListener('DOMContentLoaded',()=>{['iGross','iAge','iPf','iPt','i80c','i80d','iHra','iHl','iNps'].forEach(id=>$(id).addEventListener('input',run));
document.querySelectorAll('[data-action="in-tax"]').forEach(b=>b.addEventListener('click',run));run()})})();</script>""".replace('__D__', data)

script = script.replace('__D__', data)
body = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>How much income tax will I pay in FY 2026–27?</h2>
<p class="tp-answer">Under the <strong>new regime</strong> (the default), salaried people pay <strong>no tax on salary up to ₹12.75 lakh</strong>: the ₹75,000 standard deduction plus the Section 87A rebate cover the first ₹12 lakh of taxable income.
Above that, slabs run from 5% to 30%. The <strong>old regime</strong> has higher rates but allows deductions such as 80C, 80D, HRA and home loan interest.
Budget 2026 kept both regimes' slabs unchanged, and the new Income-tax Act, 2025 took effect on 1 April 2026 with the same rates.</p></header>

<section><h2>New regime vs old regime: tax by salary</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Gross salary</th><th class="n">New regime tax</th><th class="n">Old regime tax (₹2 lakh deductions)</th><th>Lower</th><th class="n">Monthly in-hand (new)</th></tr></thead><tbody>{ex_html}</tbody></table></div>
<p class="tp-note">Includes 4% cess and surcharge. Old regime assumes ₹2 lakh of deductions (for example ₹1.5 lakh 80C + ₹50,000 NPS). Age below 60, no professional tax or PF.</p></section>

<section><h2>Income tax slabs for FY 2026–27 (AY 2027–28)</h2><div class="mc-example-grid">
<div><h3>New regime (Section 115BAC)</h3><table class="tp-table"><tbody>
<tr><td>Up to ₹4,00,000</td><td class="n">Nil</td></tr><tr><td>₹4,00,001 – ₹8,00,000</td><td class="n">5%</td></tr><tr><td>₹8,00,001 – ₹12,00,000</td><td class="n">10%</td></tr>
<tr><td>₹12,00,001 – ₹16,00,000</td><td class="n">15%</td></tr><tr><td>₹16,00,001 – ₹20,00,000</td><td class="n">20%</td></tr><tr><td>₹20,00,001 – ₹24,00,000</td><td class="n">25%</td></tr><tr><td>Above ₹24,00,000</td><td class="n">30%</td></tr></tbody></table>
<p class="tp-note">Standard deduction ₹75,000. Rebate up to ₹60,000 if taxable income is ₹12 lakh or less, with marginal relief just above.</p></div>
<div><h3>Old regime (below 60)</h3><table class="tp-table"><tbody>
<tr><td>Up to ₹2,50,000</td><td class="n">Nil</td></tr><tr><td>₹2,50,001 – ₹5,00,000</td><td class="n">5%</td></tr><tr><td>₹5,00,001 – ₹10,00,000</td><td class="n">20%</td></tr><tr><td>Above ₹10,00,000</td><td class="n">30%</td></tr></tbody></table>
<p class="tp-note">Exemption limit ₹3 lakh for ages 60–79 and ₹5 lakh for 80+. Standard deduction ₹50,000. Rebate up to ₹12,500 if taxable income is ₹5 lakh or less.</p></div></div>
<p><strong>Surcharge</strong> on tax: 10% above ₹50 lakh, 15% above ₹1 crore, 25% above ₹2 crore (and 37% above ₹5 crore in the old regime only). <strong>Health and education cess</strong> of 4% applies to tax plus surcharge in both regimes.</p></section>

<section><h2>Which regime should you choose?</h2>
<p>The new regime is better for most salaried people, and for everyone with taxable income up to ₹12 lakh. The old regime only wins if your deductions are large: the old regime needs deductions of more than about {lk(BE[15*L])} at a ₹15 lakh salary, {lk(BE[20*L])} at ₹20 lakh and {lk(BE[25*L])} at ₹25 lakh to come out ahead, for example by combining full 80C, NPS, 80D, a large HRA exemption and home loan interest.
Salaried employees can switch regimes every year when filing the return; people with business income can switch back only once.</p></section>

<section><h2>How the calculator works</h2>
<p>New regime: taxable income = salary − ₹75,000 − professional tax. Old regime: taxable income = salary − ₹50,000 − professional tax − deductions, with 80C (including employee PF) capped at ₹1.5 lakh, 80D at ₹1 lakh, home loan interest at ₹2 lakh and 80CCD(1B) at ₹50,000.
Enter the HRA exemption you are eligible for; the calculator does not work it out from rent. Not included: employer NPS contributions under 80CCD(2), capital gains and other special-rate income, and marginal relief on surcharge.</p>
<p>Sources: <a href="https://www.incometax.gov.in/iec/foportal/help/individual/return-applicable-1" rel="noopener" target="_blank">Income Tax Department</a>,
<a href="https://www.indiabudget.gov.in/" rel="noopener" target="_blank">Union Budget</a> and the Finance Act, 2025 slabs carried into FY 2026–27.</p></section>
{related('india-income-tax-calculator', [('/tools/loan-amortization-calculator', 'Loan EMI calculator'), ('/tools/percentage-calculator', 'Percentage calculator')])}"""

n15 = calc_new(15*L); n20 = calc_new(20*L)
faqs = [
    ("Is income up to ₹12 lakh tax-free in FY 2026–27?", "Yes, under the new regime. Taxable income up to ₹12 lakh gets a full rebate under Section 87A, so salaried people pay no tax on a salary up to ₹12.75 lakh after the ₹75,000 standard deduction. The rebate does not apply to special-rate income such as capital gains."),
    ("How much tax on a ₹15 lakh salary?", f"{m(sum(n15[1:]))} under the new regime, including 4% cess (taxable income ₹14.25 lakh)."),
    ("How much tax on a ₹20 lakh salary?", f"{m(sum(n20[1:]))} under the new regime, including cess."),
    ("What are the new regime slabs for FY 2026–27?", "Nil up to ₹4 lakh, 5% from ₹4 to 8 lakh, 10% from ₹8 to 12 lakh, 15% from ₹12 to 16 lakh, 20% from ₹16 to 20 lakh, 25% from ₹20 to 24 lakh and 30% above ₹24 lakh."),
    ("Did Budget 2026 change the tax slabs?", "No. The slabs, the ₹75,000 standard deduction and the ₹12 lakh rebate limit in the new regime are the same as in FY 2025–26."),
    ("What is the standard deduction in the new regime?", "₹75,000 for salaried employees and pensioners. It is ₹50,000 in the old regime."),
    ("Which is better, the old or new tax regime?", "The new regime is better for most people. The old regime can be better if you claim large deductions such as full 80C, NPS, health insurance, HRA and home loan interest. Use the calculator to compare both with your own figures."),
    ("What is marginal relief in the new regime?", "If your taxable income is a little above ₹12 lakh, your tax is limited to the amount by which your income exceeds ₹12 lakh, so earning slightly more never leaves you with less after tax."),
]

page('india-income-tax-calculator', 'Income Tax Calculator India FY 2026–27: New vs Old Regime | ToolPinch',
     'Compare new and old regime income tax for FY 2026–27 (AY 2027–28). Slabs, ₹75,000 standard deduction, 87A rebate up to ₹12 lakh, surcharge and cess.',
     'India Income Tax Calculator FY 2026–27', 'FY 2026–27 · AY 2027–28',
     'Compare your tax under the new and old regimes, with the ₹12 lakh rebate, marginal relief, deductions, surcharge and cess, and see your monthly in-hand salary.',
     ['Budget 2026 slabs', 'Old vs new regime', 'No signup'], calc, body, faqs, script)
