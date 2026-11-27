"""Build /tools/2027-paycheck-calculator ("How will my paycheck change in 2027?").
Run from repo root: PYTHONPATH=scripts python3 scripts/build_paycheck2027.py
Sources: IRS Rev. Proc. 2026-35 (2027 brackets, standard deduction) and Rev. Proc. 2025-32 (2026); SSA 2027 fact sheet
(wage base $184,500 -> $192,300, 6.2% + 1.45%); IRS Notice 2026-66 (401(k) limit $24,500 -> $25,500).
Federal income tax is computed on annual taxable wages (salary - pre-tax deductions - standard deduction), which is how the
IRS percentage method works for a W-4 with no adjustments. Additional Medicare 0.9% is withheld on wages over $200,000."""
import json
from tax_common import page, related, BT_JS

F = lambda b: [[t, r / 100] for t, r in b]
Y = {2027: {'single': (F([[0,10],[12800,12],[52025,22],[109125,24],[208325,32],[264550,35],[661375,37]]), 16600),
            'married': (F([[0,10],[25600,12],[104050,22],[218250,24],[416650,32],[529100,35],[793650,37]]), 33200),
            'hoh': (F([[0,10],[18250,12],[69650,22],[109100,24],[208300,32],[264550,35],[661350,37]]), 24925)},
     2026: {'single': (F([[0,10],[12400,12],[50400,22],[105700,24],[201775,32],[256225,35],[640600,37]]), 16100),
            'married': (F([[0,10],[24800,12],[100800,22],[211400,24],[403550,32],[512450,35],[768700,37]]), 32200),
            'hoh': (F([[0,10],[17700,12],[67450,22],[105700,24],[201750,32],[256200,35],[640600,37]]), 24150)}}
WB = {2026: 184500, 2027: 192300}
K401 = {2026: 24500, 2027: 25500}


def bt(x, b):
    t = 0
    for i, (lo, r) in enumerate(b):
        hi = b[i + 1][0] if i + 1 < len(b) else 1e18
        if x > lo:
            t += (min(x, hi) - lo) * r
    return t


def year(sal, st, yr, k_pct=0.0, other_pre=0.0):
    k = min(sal * k_pct / 100, K401[yr])
    b, sd = Y[yr][st]
    fit = bt(max(0, sal - k - other_pre - sd), b)
    ss = 0.062 * min(sal - other_pre, WB[yr])
    med = 0.0145 * (sal - other_pre) + 0.009 * max(0, sal - other_pre - 200000)
    net = sal - k - other_pre - fit - ss - med
    return dict(k=k, fit=fit, ss=ss, med=med, net=net)


# Hand checks. Single $75,000, no 401(k):
# 2026 taxable 58,900: 1,240 + 0.12*38,000 = 5,800 (to 50,400) + 0.22*8,500 = 1,870 -> 7,670
# 2027 taxable 58,400: 1,280 + 0.12*39,225 = 4,707 + 0.22*6,375 = 1,402.50 -> 7,389.50 ; FICA identical
a, b = year(75000, 'single', 2026), year(75000, 'single', 2027)
assert round(a['fit'], 2) == 7670.00 and round(b['fit'], 2) == 7389.50 and a['ss'] == b['ss']
# $250,000: SS rises by 6.2% x (192,300 - 184,500) = 483.60
assert round(year(250000, 'single', 2027)['ss'] - year(250000, 'single', 2026)['ss'], 2) == 483.60
m = lambda x: f"${x:,.0f}"
m2 = lambda x: ('+' if x >= 0 else '−') + f"${abs(x):,.2f}"
EX = [(40000, 'single'), (60000, 'single'), (75000, 'single'), (100000, 'single'), (150000, 'single'), (200000, 'single'), (250000, 'single'),
      (100000, 'married'), (150000, 'married'), (60000, 'hoh')]
NAMES = {'single': 'Single', 'married': 'Married filing jointly', 'hoh': 'Head of household'}
ex_html = ''
for sal, st in EX:
    a, b = year(sal, st, 2026), year(sal, st, 2027)
    d = b['net'] - a['net']
    ex_html += f'<tr><td>{m(sal)}</td><td>{NAMES[st]}</td><td class="n">{m(a["fit"])}</td><td class="n">{m(b["fit"])}</td><td class="n">{m2(d)}</td><td class="n"><b>{m2(d / 26)}</b></td></tr>'
    print(sal, st, round(d, 2), round(d / 26, 2))
data = json.dumps({'Y': {str(k): v for k, v in Y.items()}, 'WB': WB, 'K': K401})

calc = """<div class="mc-calculator"><h2>2026 vs 2027 paycheck</h2>
<label class="mc-field"><span>2026 annual salary ($)</span><input id="cS" type="number" min="0" step="500" value="75000"></label>
<label class="mc-field"><span>Raise for 2027 (%)</span><input id="cR" type="number" min="0" max="50" step="0.1" value="0"></label>
<label class="mc-field"><span>Filing status (W-4)</span><select id="cF"><option value="single">Single</option><option value="married">Married filing jointly</option><option value="hoh">Head of household</option></select></label>
<label class="mc-field"><span>Pay frequency</span><select id="cP"><option value="52">Weekly</option><option value="26" selected>Every 2 weeks</option><option value="24">Twice a month</option><option value="12">Monthly</option></select></label>
<label class="mc-field"><span>401(k) contribution (% of pay)</span><input id="cK" type="number" min="0" max="100" step="0.5" value="0"></label>
<label class="mc-field"><span>Other pre-tax deductions per year (health, HSA) ($)</span><input id="cO" type="number" min="0" step="100" value="0"></label>
<button class="mc-button" data-action="pc">Compare</button>
<div class="mc-result tp-res" id="cRes" aria-live="polite">Enter your salary.</div></div>"""

script = """<script>(()=>{const D=__D__,$=id=>document.getElementById(id),v=id=>Math.max(0,+$(id).value||0);""" + BT_JS + """
const f=x=>x.toLocaleString('en-US',{style:'currency',currency:'USD'}),sg=x=>(x>=0?'+':'−')+f(Math.abs(x));
function yr(s,st,y,kp,o){const k=Math.min(s*kp/100,D.K[y]),b=D.Y[y][st],fit=BT(Math.max(0,s-k-o-b[1]),b[0]),w=s-o,ss=.062*Math.min(w,D.WB[y]),med=.0145*w+.009*Math.max(0,w-200000);return{k,fit,ss,med,net:s-k-o-fit-ss-med}}
function run(){const s=v('cS'),r=v('cR'),st=$('cF').value,n=+$('cP').value,kp=Math.min(100,v('cK')),o=v('cO'),s2=s*(1+r/100);
const a=yr(s,st,'2026',kp,o),b=yr(s2,st,'2027',kp,o),d=(b.net-a.net)/n,c=x=>'<td class="n">'+f(x/n)+'</td>';
let t='<p class="tp-big"><strong>'+sg(d)+'</strong> per paycheck in 2027</p><div class="tp-scroll"><table class="tp-table"><thead><tr><th>Per paycheck</th><th class="n">2026</th><th class="n">2027</th></tr></thead><tbody>'+
'<tr><td>Gross pay</td>'+c(s)+c(s2)+'</tr>'+(kp?'<tr><td>401(k)</td>'+c(-a.k)+c(-b.k)+'</tr>':'')+(o?'<tr><td>Other pre-tax deductions</td>'+c(-o)+c(-o)+'</tr>':'')+
'<tr><td>Federal income tax</td>'+c(-a.fit)+c(-b.fit)+'</tr><tr><td>Social Security (6.2%)</td>'+c(-a.ss)+c(-b.ss)+'</tr><tr><td>Medicare</td>'+c(-a.med)+c(-b.med)+'</tr>'+
'<tr class="tot"><td>Take-home pay</td>'+c(a.net)+c(b.net)+'</tr></tbody></table></div>';
const why=[],sv=a.fit-yr(s,st,'2027',kp,o).fit;if(sv>0.005)why.push('wider 2027 tax brackets and a higher standard deduction lower federal income tax by '+f(sv/n)+' a paycheck at the same salary');
if(Math.min(s2-o,D.WB['2027'])>Math.min(s-o,D.WB['2026'])&&s-o>D.WB['2026'])why.push('the Social Security wage base rises from $184,500 to $192,300, so Social Security tax runs '+f((b.ss-a.ss)/n)+' a paycheck higher');
if(kp&&b.k>a.k&&a.k>=D.K['2026'])why.push('the 401(k) limit rises to $25,500, so you can put in '+f((b.k-a.k)/n)+' more a paycheck');
if(r)why.push('a '+r+'% raise adds '+f((s2-s)/n)+' gross a paycheck');
t+=(why.length?'<p>Why: '+why.join('; ')+'.</p>':'')+'<p class="tp-note">Federal taxes only; state tax, health premiums and other benefits can also change in January. Assumes a 2020-or-later W-4 with no extra withholding.</p>';
$('cRes').innerHTML=t}
document.addEventListener('DOMContentLoaded',()=>{['cS','cR','cF','cP','cK','cO'].forEach(i=>$(i).addEventListener('input',run));document.querySelectorAll('[data-action="pc"]').forEach(b=>b.addEventListener('click',run));run()})})();</script>"""
script = script.replace('__D__', data)

a75, b75 = year(75000, 'single', 2026), year(75000, 'single', 2027)
body = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>Will my paycheck go up in 2027?</h2>
<p class="tp-answer">For most people, <strong>yes, slightly</strong>, even without a raise. The 2027 tax brackets are about 3% wider and the standard deduction rises to $16,600 for single filers ($33,200 married), so less federal income tax is withheld.
At a $75,000 salary, single, federal income tax falls from {m(a75['fit'])} to {m(b75['fit'])} a year: about <strong>{m2((b75['net'] - a75['net']) / 26)} every two weeks</strong>.</p>
<p>High earners see a partial offset: the Social Security wage base rises from $184,500 to <strong>$192,300</strong>, so anyone earning above $184,500 pays up to $483.60 more Social Security tax in 2027, usually noticed late in the year.</p></header>

<section><h2>What changes on January 1, 2027</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Item</th><th class="n">2026</th><th class="n">2027</th></tr></thead><tbody>
<tr><td>Standard deduction, single</td><td class="n">$16,100</td><td class="n">$16,600</td></tr>
<tr><td>Standard deduction, married filing jointly</td><td class="n">$32,200</td><td class="n">$33,200</td></tr>
<tr><td>Standard deduction, head of household</td><td class="n">$24,150</td><td class="n">$24,925</td></tr>
<tr><td>12% bracket starts (single)</td><td class="n">$12,400</td><td class="n">$12,800</td></tr>
<tr><td>22% bracket starts (single)</td><td class="n">$50,400</td><td class="n">$52,025</td></tr>
<tr><td>24% bracket starts (single)</td><td class="n">$105,700</td><td class="n">$109,125</td></tr>
<tr><td>Social Security wage base</td><td class="n">$184,500</td><td class="n">$192,300</td></tr>
<tr><td>Social Security and Medicare tax rates</td><td class="n">6.2% + 1.45%</td><td class="n">6.2% + 1.45% (unchanged)</td></tr>
<tr><td>401(k), 403(b), TSP limit</td><td class="n">$24,500</td><td class="n">$25,500</td></tr>
<tr><td>401(k) catch-up, age 50+</td><td class="n">$8,000</td><td class="n">$8,500</td></tr>
<tr><td>IRA limit</td><td class="n">$7,500</td><td class="n">$7,500</td></tr></tbody></table></div>
<p>Full brackets for every filing status are on the <a href="/tools/2027-tax-brackets">2027 tax brackets</a> page.</p></section>

<section><h2>2027 paycheck change by salary (no raise)</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Salary</th><th>Filing status</th><th class="n">2026 federal income tax</th><th class="n">2027 federal income tax</th><th class="n">Change in take-home, year</th><th class="n">Per biweekly paycheck</th></tr></thead><tbody>{ex_html}</tbody></table></div>
<p class="tp-note">Same salary both years, no pre-tax deductions, standard W-4. Includes federal income tax, Social Security and Medicare. Between $184,500 and about $214,000 (single), the higher Social Security wage base can outweigh the income tax savings, which is why take-home at $200,000 dips slightly.</p></section>

<section><h2>Other things that can change your first 2027 paycheck</h2>
<ul><li><strong>Health insurance premiums</strong> often rise in January after open enrollment, which can cancel out the tax savings.</li>
<li><strong>State income tax</strong> brackets and rates change in many states; see the <a href="/tools/us-paycheck-calculator">US paycheck calculator</a> for your state.</li>
<li><strong>Your 401(k) election</strong> may reset or auto-increase. If you want to max out at $25,500, divide by your number of paychecks.</li>
<li><strong>Federal employees:</strong> the 2027 GS raise is proposed at 0%; see the <a href="/tools/gs-pay-scale-2027">GS pay scale 2027</a>. Social Security recipients get a 3.6% COLA.</li>
<li><strong>A new W-4</strong> is only needed if your situation changed. Your existing W-4 automatically uses the 2027 tables.</li></ul>
<p>Sources: <a href="https://www.irs.gov/pub/irs-drop/rp-25-32.pdf" rel="noopener" target="_blank">Rev. Proc. 2025-32</a> (2026), IRS Rev. Proc. 2026-35 (2027), <a href="https://www.ssa.gov/cola/factsheets/2027.html" rel="noopener" target="_blank">SSA 2027 fact sheet</a>, <a href="https://www.irs.gov/node/167581" rel="noopener" target="_blank">IRS 2027 retirement plan limits</a>.</p></section>
{related('2027-paycheck-calculator', [('/tools/gs-pay-scale-2027', 'GS pay scale 2027')])}"""

faqs = [("Will my paycheck be bigger in 2027?", f"For most salaried workers with the same pay, slightly, because the 2027 brackets and standard deduction are higher. At $75,000 single, take-home rises about {m(b75['net'] - a75['net'])} a year."),
        ("What is the 2027 standard deduction?", "$16,600 for single filers and married filing separately, $33,200 for married filing jointly, and $24,925 for head of household."),
        ("What is the Social Security wage base for 2027?", "$192,300, up from $184,500 in 2026. Wages above that are not subject to the 6.2% Social Security tax; Medicare tax has no limit."),
        ("What is the 401(k) limit for 2027?", "$25,500, up from $24,500. Workers 50 and older can add $8,500 (total $34,000), and those aged 60 to 63 can add $11,750 instead."),
        ("Do I need a new W-4 for 2027?", "No, unless your situation changed. Employers apply the new 2027 withholding tables to your existing W-4 automatically."),
        ("Why is my January paycheck smaller?", "Usually because health insurance premiums or other benefit costs went up, a 401(k) contribution increased, or your state changed its withholding. Federal income tax withholding goes down slightly for most people in 2027.")]

page('2027-paycheck-calculator', 'How Will My Paycheck Change in 2027? Calculator | ToolPinch',
     'Compare your 2026 and 2027 paychecks: new tax brackets, higher standard deduction, the $192,300 Social Security wage base and the $25,500 401(k) limit.',
     'How Will My Paycheck Change in 2027?', 'New tax tables start Jan 1, 2027',
     'See your take-home pay per paycheck in 2026 and 2027 side by side, and exactly why it changes.',
     ['IRS and SSA 2027 figures', 'Per-paycheck comparison', 'No signup'], calc, body, faqs, script)
