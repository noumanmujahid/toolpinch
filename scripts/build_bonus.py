"""Build /tools/bonus-tax-calculator (US 2026, UK 2026/27, Pakistan TY2027)."""
import json
from tax_common import page, related, BT_JS

F = lambda b: [[t, r / 100] for t, r in b]
US = {'single': (F([[0,10],[12400,12],[50400,22],[105700,24],[201775,32],[256225,35],[640600,37]]), 16100),
      'married': (F([[0,10],[24800,12],[100800,22],[211400,24],[403550,32],[512450,35],[768700,37]]), 32200),
      'hoh': (F([[0,10],[17700,12],[67450,22],[105700,24],[201750,32],[256200,35],[640600,37]]), 24150)}
RUK = [[0, .20], [37700, .40], [125140, .45]]
SCO = [[0, .19], [3967, .20], [16956, .21], [31092, .42], [62430, .45], [125140, .48]]
PK = [[600000, .01], [1200000, .11], [2200000, .20], [3200000, .25], [4100000, .29], [5600000, .32], [7000000, .35]]


def bt(x, b):
    t = 0
    for i, (lo, r) in enumerate(b):
        hi = b[i + 1][0] if i + 1 < len(b) else 1e18
        if x > lo:
            t += (min(x, hi) - lo) * r
    return t


def us(sal, bonus, st='single', state=0.0):
    fed_w = min(bonus, max(0, 1e6 - 0)) * .22 if bonus <= 1e6 else 1e6 * .22 + (bonus - 1e6) * .37
    ss = max(0, min(sal + bonus, 184500) - min(sal, 184500)) * .062
    med = bonus * .0145 + max(0, (sal + bonus) - max(sal, 200000)) * .009
    b, sd = US[st]
    actual = bt(max(0, sal + bonus - sd), b) - bt(max(0, sal - sd), b)
    return fed_w, ss, med, bonus * state / 100, actual


def uk_total(g, sco=False):
    pa = max(0, 12570 - max(0, g - 100000) / 2)
    return bt(max(0, g - pa), SCO if sco else RUK) + max(0, min(g, 50270) - 12570) * .08 + max(0, g - 50270) * .02


m = lambda x: f"${x:,.0f}"
r = us(60000, 5000)
print('US 60k+5k', r, 5000 - sum(r[:4]))
assert round(r[0]) == 1100 and round(r[1]) == 310 and round(r[2], 2) == 72.5
uk = uk_total(45000 + 5000) - uk_total(45000)
print('UK 45k+5k', uk)   # 20% + 8% on 5,000 = 1,400
assert round(uk) == 1400
pk = bt(2400000 + 300000, PK) - bt(2400000, PK)
print('PK 2.4M + 300k', pk)  # 20% band
assert round(pk) == 60000

us_ex = []
for sal, bon, st in [(50000, 2000, 'single'), (60000, 5000, 'single'), (85000, 10000, 'single'), (120000, 15000, 'married'), (200000, 30000, 'single')]:
    f, s, md, _, act = us(sal, bon, st)
    us_ex.append(f'<tr><td>{m(sal)}</td><td>{m(bon)}</td><td class="n">{m(f)}</td><td class="n">{m(s+md)}</td><td class="n"><b>{m(bon-f-s-md)}</b></td><td class="n">{m(act)}</td></tr>')
uk_ex = ''.join(f'<tr><td>£{s:,}</td><td>£{b:,}</td><td class="n">£{uk_total(s+b)-uk_total(s):,.0f}</td><td class="n"><b>£{b-(uk_total(s+b)-uk_total(s)):,.0f}</b></td><td class="n">{100*(uk_total(s+b)-uk_total(s))/b:.0f}%</td></tr>' for s, b in [(30000, 2000), (45000, 5000), (60000, 5000), (95000, 10000), (130000, 10000)])
pk_ex = ''.join(f'<tr><td>Rs {s:,}</td><td>Rs {b:,}</td><td class="n">Rs {bt(s*12+b,PK)-bt(s*12,PK):,.0f}</td><td class="n"><b>Rs {b-(bt(s*12+b,PK)-bt(s*12,PK)):,.0f}</b></td></tr>' for s, b in [(80000, 80000), (150000, 150000), (250000, 250000), (400000, 400000)])

data = json.dumps({'US': US, 'R': RUK, 'S': SCO, 'P': PK})
calc = """<div class="mc-calculator"><h2>Bonus after tax</h2>
<label class="mc-field"><span>Country</span><select id="xC"><option value="us">United States</option><option value="uk">United Kingdom</option><option value="pk">Pakistan</option></select></label>
<label class="mc-field"><span id="xSalL">Annual salary before the bonus</span><input id="xSal" type="number" min="0" step="100" value="60000"></label>
<label class="mc-field"><span>Bonus amount</span><input id="xBon" type="number" min="0" step="100" value="5000"></label>
<label class="mc-field" data-c="us"><span>Filing status</span><select id="xSt"><option value="single">Single</option><option value="married">Married filing jointly</option><option value="hoh">Head of household</option></select></label>
<label class="mc-field" data-c="us"><span>State supplemental withholding (%)</span><input id="xState" type="number" min="0" max="20" step="0.01" value="0"></label>
<label class="mc-field" data-c="uk" hidden><span>Where you live</span><select id="xReg"><option value="ruk">England, Wales or N. Ireland</option><option value="sco">Scotland</option></select></label>
<button class="mc-button" data-action="bonus">Calculate</button>
<div class="mc-result tp-res" id="xResult" aria-live="polite">Enter your salary and bonus.</div></div>"""

script = """<script>(()=>{const D=__D__,$=id=>document.getElementById(id);""" + BT_JS + """
const ukT=(g,s)=>{const pa=Math.max(0,12570-Math.max(0,g-100000)/2);return [BT(Math.max(0,g-pa),s?D.S:D.R),Math.max(0,Math.min(g,50270)-12570)*.08+Math.max(0,g-50270)*.02]};
const cur={us:x=>x.toLocaleString('en-US',{style:'currency',currency:'USD'}),uk:x=>x.toLocaleString('en-GB',{style:'currency',currency:'GBP'}),pk:x=>'Rs '+Math.round(x).toLocaleString('en-PK')};
function vis(){const c=$('xC').value;document.querySelectorAll('[data-c]').forEach(e=>e.hidden=e.dataset.c!==c);$('xSalL').textContent=c==='pk'?'Monthly salary before the bonus':'Annual salary before the bonus'}
function table(f,rows,net,b){let h='<p class="tp-big"><strong>'+f(net)+'</strong> bonus after tax</p><div class="tp-scroll"><table class="tp-table"><tbody><tr><td>Bonus</td><td class="n">'+f(b)+'</td></tr>';
rows.forEach(r=>{h+='<tr><td>'+r[0]+'</td><td class="n">−'+f(r[1])+'</td></tr>'});return h+'<tr class="tot"><td>You receive</td><td class="n">'+f(net)+'</td></tr></tbody></table></div><p class="tp-note">Deductions take '+(b?(100*(b-net)/b).toFixed(1):'0')+'% of the bonus.</p>'}
function run(){const c=$('xC').value,s=Math.max(0,+$('xSal').value||0),b=Math.max(0,+$('xBon').value||0),f=cur[c];let h='';
if(c==='us'){const st=$('xSt').value,fw=Math.min(b,1e6)*.22+Math.max(0,b-1e6)*.37,ss=Math.max(0,Math.min(s+b,184500)-Math.min(s,184500))*.062,md=b*.0145+Math.max(0,(s+b)-Math.max(s,200000))*.009,sw=b*Math.max(0,+$('xState').value||0)/100;
const u=D.US[st],act=BT(Math.max(0,s+b-u[1]),u[0])-BT(Math.max(0,s-u[1]),u[0]);
const rows=[['Federal withholding (22% flat rate)',fw],['Social Security (6.2%)',ss],['Medicare',md]];if(sw)rows.push(['State withholding',sw]);h=table(f,rows,b-fw-ss-md-sw,b);
h+='<p>At tax time, the bonus actually adds about <b>'+f(act)+'</b> to your 2026 federal income tax. '+(act<fw-1?'The 22% withholding is more than that, so expect about '+f(fw-act)+' back as part of your refund.':act>fw+1?'The 22% withholding is less than that, so you may owe about '+f(act-fw)+' more when you file.':'That matches the withholding.')+'</p>'}
else if(c==='uk'){const sc=$('xReg').value==='sco',a=ukT(s,sc),z=ukT(s+b,sc);h=table(f,[['Income tax',z[0]-a[0]],['National Insurance',z[1]-a[1]]],b-(z[0]-a[0])-(z[1]-a[1]),b);
h+='<p class="tp-note">Your payslip in the bonus month may show more tax because PAYE treats that month as unusually high pay; any difference is normally corrected in later months or after the tax year ends.</p>'}
else{const a=s*12,t=BT(a+b,D.P)-BT(a,D.P);h=table(f,[['Income tax (tax year 2027 slabs)',t]],b-t,b);h+='<p class="tp-note">Tax on the bonus is the extra tax on your annual salary plus bonus. Employers usually deduct it in the month the bonus is paid.</p>'}
$('xResult').innerHTML=h}
document.addEventListener('DOMContentLoaded',()=>{$('xC').addEventListener('change',()=>{const c=$('xC').value;$('xSal').value=c==='pk'?150000:c==='uk'?45000:60000;$('xBon').value=c==='pk'?150000:5000;vis();run()});
['xSal','xBon','xSt','xState','xReg'].forEach(id=>$(id).addEventListener('input',run));document.querySelectorAll('[data-action="bonus"]').forEach(x=>x.addEventListener('click',run));vis();run()})})();</script>"""
script = script.replace('__D__', data)

r5 = us(60000, 5000)
body = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>How much tax is taken from a bonus?</h2>
<p class="tp-answer"><strong>United States:</strong> employers usually withhold a flat <strong>22%</strong> federal tax on bonuses (37% on any amount over $1 million), plus 7.65% Social Security and Medicare and any state tax. A $5,000 bonus becomes about <strong>{m(5000-sum(r5[:3]))}</strong> before state tax.<br>
<strong>United Kingdom:</strong> a bonus is taxed as ordinary pay at your marginal rates. A basic-rate taxpayer keeps <strong>72%</strong> (20% tax + 8% National Insurance); a higher-rate taxpayer keeps <strong>58%</strong> (40% + 2%).<br>
<strong>Pakistan:</strong> a bonus is added to your annual salary and taxed at your slab rate, from 0% to 35% under the tax year 2027 slabs.</p>
<p>Bonuses are not taxed more than salary; they only look that way because withholding is applied to the bonus in one go.</p></header>

<section><h2>United States: bonus withholding in 2026</h2>
<p>The IRS treats bonuses as <strong>supplemental wages</strong>. Most employers use the <strong>percentage method</strong>: a flat 22% federal withholding on the bonus, separate from your regular paycheck. Some combine the bonus with your regular pay and withhold as if you earned that much every period (the aggregate method), which can withhold even more.</p>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Salary</th><th>Bonus</th><th class="n">Federal (22%)</th><th class="n">Social Security + Medicare</th><th class="n">Take-home (before state)</th><th class="n">Actual extra federal tax</th></tr></thead><tbody>{''.join(us_ex)}</tbody></table></div>
<p><strong>Withholding is not the final tax.</strong> The last column shows how much the bonus really adds to your 2026 federal income tax at your bracket. If you are in the 10% or 12% bracket, 22% is too much and the difference comes back as a refund; in the 24% bracket and above, you may owe a little more when you file.</p>
<p><strong>State tax:</strong> many states also have a flat supplemental rate, for example California withholds 10.23% on bonuses. Enter your state's rate in the calculator. Nine states have no wage income tax.</p></section>

<section><h2>United Kingdom: bonus tax for 2026/27</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Salary</th><th>Bonus</th><th class="n">Tax + NI on bonus</th><th class="n">You keep</th><th class="n">Rate</th></tr></thead><tbody>{uk_ex}</tbody></table></div>
<p>Bonuses between £100,000 and £125,140 of total income are hit hardest: losing part of the Personal Allowance means an effective 60% tax rate plus 2% NI. Paying part of the bonus into a pension through salary sacrifice avoids tax and National Insurance on that portion and can restore the allowance.</p></section>

<section><h2>Pakistan: bonus tax for tax year 2027</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Monthly salary</th><th>Bonus</th><th class="n">Tax on bonus</th><th class="n">You keep</th></tr></thead><tbody>{pk_ex}</tbody></table></div>
<p>Under section 149 of the Income Tax Ordinance, employers deduct tax on the bonus based on your estimated annual salary including the bonus. A bonus that pushes your annual salary into a higher slab is taxed at the higher rate only on the part that falls into that slab.</p></section>

<section><h2>Ways to keep more of a bonus</h2><ul>
<li><strong>Pension or retirement contributions:</strong> a 401(k) contribution from the bonus (US) or a salary sacrifice into a pension (UK) is taken before income tax.</li>
<li><strong>Timing:</strong> if your income will be lower next year, a bonus paid in January rather than December falls into the lower-income year.</li>
<li><strong>Check withholding:</strong> in the US, if 22% is more than your bracket, you will get it back at tax time; adjust your W-4 if you prefer a smaller refund.</li></ul>
<p>Sources: <a href="https://www.irs.gov/publications/p15" rel="noopener" target="_blank">IRS Publication 15 (supplemental wages)</a>, <a href="https://www.gov.uk/income-tax-rates" rel="noopener" target="_blank">GOV.UK income tax rates</a>, <a href="https://www.fbr.gov.pk/" rel="noopener" target="_blank">FBR</a> and the Finance Act 2026 slabs. Estimates only.</p></section>
{related('bonus-tax-calculator')}"""

faqs = [
    ("Why is my bonus taxed so much?", "In the US, employers usually withhold a flat 22% federal tax plus 7.65% Social Security and Medicare and state tax, so 30% to 40% can be withheld. That is withholding, not your final tax; if your actual bracket is lower, you get the difference back as a refund."),
    ("Are bonuses taxed at a higher rate than salary?", "No. Bonuses are taxed as ordinary income. They can look heavily taxed because withholding is calculated on the bonus alone, or as if you earned that much every pay period."),
    ("What is the federal tax rate on bonuses in 2026?", "22% for supplemental wages up to $1 million in a year and 37% on supplemental wages above $1 million, when the employer uses the percentage method."),
    ("How much of a £5,000 bonus will I keep in the UK?", "About £3,600 as a basic-rate taxpayer (20% tax + 8% NI) and about £2,900 as a higher-rate taxpayer (40% tax + 2% NI), in England, Wales or Northern Ireland."),
    ("How is a bonus taxed in Pakistan?", "It is added to your salary income for the tax year and taxed at your slab rate. Under the tax year 2027 slabs, rates run from 0% to 35%."),
    ("Can I avoid tax on my bonus?", "You cannot avoid it entirely, but contributing part of it to a 401(k) in the US or a pension through salary sacrifice in the UK reduces the tax."),
]

page('bonus-tax-calculator', 'Bonus Tax Calculator 2026: How Much of Your Bonus You Keep (US, UK, Pakistan) | ToolPinch',
     'Calculate your bonus after tax: US 22% supplemental withholding plus FICA, UK income tax and National Insurance, and Pakistan salary slabs, with the real tax you will owe.',
     'Bonus Tax Calculator', 'US 2026 · UK 2026/27 · Pakistan tax year 2027',
     'See how much of your bonus you will actually receive after tax, and whether US withholding is more or less than the tax you really owe.',
     ['US, UK and Pakistan', 'Withholding vs real tax', 'No signup'], calc, body, faqs, script)
