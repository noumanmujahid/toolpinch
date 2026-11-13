"""Build /tools/uk-take-home-pay-calculator (2026/27)."""
import json
from tax_common import page, related, BT_JS, RENDER_JS, PERIOD_SELECT

PA, TAPER = 12570, 100000
RUK = [[0, .20], [37700, .40], [125140, .45]]                     # on taxable income (after allowance)
SCO = [[0, .19], [3967, .20], [16956, .21], [31092, .42], [62430, .45], [125140, .48]]
NI_PT, NI_UEL = 12570, 50270
SL = {'none': None, 'p1': (26900, .09), 'p2': (29385, .09), 'p4': (33795, .09), 'p5': (25000, .09)}
PGL = (21000, .06)


def bt(x, b):
    t = 0
    for i, (lo, r) in enumerate(b):
        hi = b[i + 1][0] if i + 1 < len(b) else 1e18
        if x > lo:
            t += (min(x, hi) - lo) * r
    return t


def calc_py(g, sco=False, pen=0, plan='none', pg=False):
    p = g * pen / 100
    ti_gross = g - p
    pa = max(0, PA - max(0, ti_gross - TAPER) / 2)
    tax = bt(max(0, ti_gross - pa), SCO if sco else RUK)
    ni = max(0, min(g, NI_UEL) - NI_PT) * .08 + max(0, g - NI_UEL) * .02
    sl = 0
    if SL[plan]:
        sl = max(0, g - SL[plan][0]) * SL[plan][1]
    if pg:
        sl += max(0, g - PGL[0]) * PGL[1]
    return round(tax, 2), round(ni, 2), round(sl, 2), round(p, 2)


# hand checks: £30,000 England: tax (30000-12570)*.2 = 3486; NI (30000-12570)*.08 = 1394.40
assert calc_py(30000) == (3486.0, 1394.4, 0, 0)
# £60,000: tax 37700*.2 + (60000-50270)*.4 = 7540 + 3892 = 11432; NI 37700*.08 + 9730*.02 = 3016 + 194.6
assert calc_py(60000)[:2] == (11432.0, 3210.6)
# £110,000: PA = 12570-5000 = 7570; taxable 102430: 7540 + (102430-37700)*.4 = 7540+25892 = 33432
assert calc_py(110000)[0] == 33432.0
m = lambda x: f"£{x:,.0f}"
ex = []
for g in (25000, 30000, 35000, 40000, 50000, 60000, 75000, 100000, 125000):
    e, s = calc_py(g), calc_py(g, True)
    ex.append((g, e, g - sum(e), s, g - sum(s)))
ex_html = ''.join(f'<tr><td>{m(g)}</td><td class="n">{m(e[0])}</td><td class="n">{m(e[1])}</td><td class="n"><b>{m(ne)}</b><br><small>{m(ne/12)}/mo</small></td><td class="n">{m(s[0])}</td><td class="n"><b>{m(ns)}</b><br><small>{m(ns/12)}/mo</small></td></tr>' for g, e, ne, s, ns in ex)
for r in ex:
    print(r[0], r[1], round(r[2]), r[3][0], round(r[4]))
data = json.dumps({'R': RUK, 'S': SCO, 'SL': SL, 'PG': PGL})

calc = f"""<div class="mc-calculator"><h2>Your 2026/27 take-home pay</h2>
<label class="mc-field"><span>Annual salary before tax (£)</span><input id="kGross" type="number" min="0" step="100" value="35000"></label>
<label class="mc-field"><span>Where you live</span><select id="kReg"><option value="ruk">England, Wales or Northern Ireland</option><option value="sco">Scotland</option></select></label>
<label class="mc-field"><span>Pension contribution (% of salary, before tax)</span><input id="kPen" type="number" min="0" max="100" step="0.5" value="5"></label>
<label class="mc-field"><span>Student loan</span><select id="kSL"><option value="none">None</option><option value="p1">Plan 1</option><option value="p2">Plan 2</option><option value="p4">Plan 4 (Scotland)</option><option value="p5">Plan 5</option></select></label>
<label class="mc-field"><span>Postgraduate loan</span><select id="kPG"><option value="0">No</option><option value="1">Yes</option></select></label>
{PERIOD_SELECT}
<button class="mc-button" data-action="uk-pay">Calculate</button>
<div class="mc-result tp-res" id="kResult" aria-live="polite">Enter your salary to see your take-home pay.</div></div>"""

script = """<script>(()=>{const D=__D__,$=id=>document.getElementById(id);""" + BT_JS + RENDER_JS + """
const fmt=x=>x.toLocaleString('en-GB',{style:'currency',currency:'GBP'});
function run(){const g=Math.max(0,+$('kGross').value||0),sco=$('kReg').value==='sco',p=g*Math.min(100,Math.max(0,+$('kPen').value||0))/100,ti=g-p;
const pa=Math.max(0,12570-Math.max(0,ti-100000)/2),tax=BT(Math.max(0,ti-pa),sco?D.S:D.R),ni=Math.max(0,Math.min(g,50270)-12570)*0.08+Math.max(0,g-50270)*0.02;
const pl=D.SL[$('kSL').value],sl=pl?Math.max(0,g-pl[0])*pl[1]:0,pg=$('kPG').value==='1'?Math.max(0,g-D.PG[0])*D.PG[1]:0;
const rows=[['Income tax',tax,1],['National Insurance',ni,0]];if(p>0)rows.push(['Pension',p,0]);if(sl>0)rows.push(['Student loan',sl,0]);if(pg>0)rows.push(['Postgraduate loan',pg,0]);
const net=g-rows.reduce((a,r)=>a+r[1],0);renderRes($('kResult'),g,rows,net,fmt,$('per').value);
$('kResult').insertAdjacentHTML('beforeend','<p class="tp-note">Personal Allowance used: '+fmt(pa)+(pa<12570?' (reduced by £1 for every £2 of income over £100,000)':'')+'. Tax code equivalent: '+(pa>=12570?'1257L':Math.floor(pa/10)+'L')+(sco?' (S prefix in Scotland)':'')+'.</p>')}
document.addEventListener('DOMContentLoaded',()=>{['kGross','kReg','kPen','kSL','kPG','per'].forEach(id=>$(id).addEventListener('input',run));
document.querySelectorAll('[data-action="uk-pay"]').forEach(b=>b.addEventListener('click',run));run()})})();</script>""".replace('__D__', data)

e35 = calc_py(35000)
script = script.replace('__D__', data)
body = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>How much tax will I pay in the UK in 2026/27?</h2>
<p class="tp-answer">The first <strong>£12,570</strong> is tax-free. In England, Wales and Northern Ireland you then pay <strong>20%</strong> up to £50,270, <strong>40%</strong> up to £125,140 and <strong>45%</strong> above.
National Insurance is <strong>8%</strong> on earnings between £12,570 and £50,270 and <strong>2%</strong> above.
On a £35,000 salary you pay {m(e35[0])} income tax and {m(e35[1])} National Insurance, and take home <strong>{m(35000-e35[0]-e35[1])}</strong> a year ({m((35000-e35[0]-e35[1])/12)} a month) before pension.</p>
<p>The rates and thresholds are unchanged from 2025/26: the government has frozen them until April 2031. The Autumn Budget on 28 October 2026 made no change to income tax or National Insurance on wages for 2026/27 or 2027/28.</p></header>

<section><h2>UK take-home pay by salary (2026/27)</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Salary</th><th class="n">Income tax (Eng/Wal/NI)</th><th class="n">NI</th><th class="n">Take-home (Eng/Wal/NI)</th><th class="n">Income tax (Scotland)</th><th class="n">Take-home (Scotland)</th></tr></thead><tbody>{ex_html}</tbody></table></div>
<p class="tp-note">No pension or student loan. Tax code 1257L.</p></section>

<section><h2>Income tax bands for 2026/27</h2><div class="mc-example-grid">
<div><h3>England, Wales and Northern Ireland</h3><table class="tp-table"><tbody>
<tr><td>Personal Allowance</td><td>Up to £12,570</td><td class="n">0%</td></tr><tr><td>Basic rate</td><td>£12,571 – £50,270</td><td class="n">20%</td></tr>
<tr><td>Higher rate</td><td>£50,271 – £125,140</td><td class="n">40%</td></tr><tr><td>Additional rate</td><td>Over £125,140</td><td class="n">45%</td></tr></tbody></table></div>
<div><h3>Scotland</h3><table class="tp-table"><tbody>
<tr><td>Personal Allowance</td><td>Up to £12,570</td><td class="n">0%</td></tr><tr><td>Starter</td><td>£12,571 – £16,537</td><td class="n">19%</td></tr>
<tr><td>Basic</td><td>£16,538 – £29,526</td><td class="n">20%</td></tr><tr><td>Intermediate</td><td>£29,527 – £43,662</td><td class="n">21%</td></tr>
<tr><td>Higher</td><td>£43,663 – £75,000</td><td class="n">42%</td></tr><tr><td>Advanced</td><td>£75,001 – £125,140</td><td class="n">45%</td></tr><tr><td>Top</td><td>Over £125,140</td><td class="n">48%</td></tr></tbody></table></div></div>
<p><strong>The £100,000 trap:</strong> the Personal Allowance falls by £1 for every £2 of income over £100,000 and disappears at £125,140. Income in that range is taxed at an effective <strong>60%</strong> (62% in Scotland, before NI).
Pension contributions reduce the income used for this test, which is why many people in this band pay extra into a pension.</p></section>

<section><h2>National Insurance and student loans</h2>
<p>Employees pay Class 1 National Insurance at <strong>8%</strong> on earnings between the Primary Threshold (£12,570, or £1,048 a month) and the Upper Earnings Limit (£50,270), and <strong>2%</strong> above. NI is the same in every part of the UK and is worked out on each pay period separately.</p>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Loan</th><th>Repay above</th><th class="n">Rate</th></tr></thead><tbody>
<tr><td>Plan 1</td><td>£26,900 a year</td><td class="n">9%</td></tr><tr><td>Plan 2</td><td>£29,385 a year</td><td class="n">9%</td></tr>
<tr><td>Plan 4 (Scotland)</td><td>£33,795 a year</td><td class="n">9%</td></tr><tr><td>Plan 5</td><td>£25,000 a year</td><td class="n">9%</td></tr>
<tr><td>Postgraduate loan</td><td>£21,000 a year</td><td class="n">6%</td></tr></tbody></table></div></section>

<section><h2>How the calculator works</h2>
<p>Pension contributions are treated as a net pay arrangement: they come off your salary before income tax but not before National Insurance. With salary sacrifice, NI would also be lower.
The calculator works on annual figures with a standard 1257L tax code and no other income, benefits in kind or Marriage Allowance. Your payslip can differ slightly because tax and NI are worked out each pay period.</p>
<p>Sources: <a href="https://www.gov.uk/government/publications/rates-and-allowances-income-tax/income-tax-rates-and-allowances-current-and-past" rel="noopener" target="_blank">HMRC income tax rates and allowances</a>,
<a href="https://www.gov.uk/scottish-income-tax" rel="noopener" target="_blank">Scottish Income Tax</a> and
<a href="https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2026-to-2027" rel="noopener" target="_blank">HMRC rates and thresholds for employers 2026 to 2027</a>.</p></section>
{related('uk-take-home-pay-calculator', [('/tools/salary-to-hourly-calculator', 'Salary to hourly'), ('/tools/pay-period-converter', 'Pay period converter')])}"""

e30, e50, e100 = calc_py(30000), calc_py(50000), calc_py(100000)
faqs = [
    ("How much is £30,000 after tax in the UK?", f"In England, Wales or Northern Ireland, {m(30000-sum(e30))} a year or {m((30000-sum(e30))/12)} a month in 2026/27, after {m(e30[0])} income tax and {m(e30[1])} National Insurance, with no pension or student loan."),
    ("How much is £50,000 after tax?", f"{m(50000-sum(e50))} a year or {m((50000-sum(e50))/12)} a month, after {m(e50[0])} income tax and {m(e50[1])} National Insurance."),
    ("How much is £100,000 after tax?", f"{m(100000-sum(e100))} a year or {m((100000-sum(e100))/12)} a month in England, Wales or Northern Ireland, before pension contributions."),
    ("What is the Personal Allowance for 2026/27?", "£12,570, the same as since April 2021. It is frozen until April 2031. It is reduced by £1 for every £2 of income over £100,000."),
    ("What are the Scottish income tax rates for 2026/27?", "19% starter rate from £12,571 to £16,537, 20% basic to £29,526, 21% intermediate to £43,662, 42% higher to £75,000, 45% advanced to £125,140 and 48% top rate above."),
    ("What is the National Insurance rate in 2026/27?", "Employees pay 8% on earnings between £12,570 and £50,270 a year and 2% on earnings above £50,270."),
    ("Does a pension contribution reduce tax?", "Yes. Contributions taken from pay before tax reduce your income tax. Under salary sacrifice they also reduce National Insurance."),
    ("When does the 2026/27 tax year run?", "From 6 April 2026 to 5 April 2027."),
]

page('uk-take-home-pay-calculator', 'UK Take-Home Pay Calculator 2026/27: Salary After Tax and NI | ToolPinch',
     'Work out your 2026/27 UK take-home pay after income tax, National Insurance, pension and student loan. Includes Scottish tax bands and the £100k taper.',
     'UK Take-Home Pay Calculator 2026/27', 'Tax year 6 April 2026 to 5 April 2027',
     'See your salary after income tax, National Insurance, pension and student loan, per month, week or year, for England, Wales, Northern Ireland or Scotland.',
     ['HMRC 2026/27 rates', 'Scottish bands', 'No signup'], calc, body, faqs, script)
