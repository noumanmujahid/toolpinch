"""Build /tools/2027-401k-ira-hsa-limits. Run from repo root: PYTHONPATH=scripts python3 scripts/build_limits2027.py
Sources: IRS IR-2026-136 / Notice 2026-66 (Nov 12, 2026) for 401(k), IRA, SIMPLE, Roth and Saver's credit figures;
Rev. Proc. 2026-24 (May 29, 2026) for HSA/HDHP; HSA age-55 catch-up $1,000 is statutory (IRC 223(b)(3)).
2026 ages 60-63 catch-up ($11,250) and 2026 Roth catch-up wage threshold ($150,000) from the IRS 2026 release."""
import json
from tax_common import page, related

L = {'k': 25500, 'cu50': 8500, 'cu6063': 11750, 'ira': 7500, 'iracu': 1100, 'simple': 17500, 'simplecu': 4000, 'simple6063': 5250,
     'hsa_self': 4500, 'hsa_fam': 9000, 'hsacu': 1000}
m = lambda x: f"${x:,}"


def kmax(age):
    return L['k'] + (L['cu6063'] if 60 <= age <= 63 else L['cu50'] if age >= 50 else 0)


assert kmax(45) == 25500 and kmax(55) == 34000 and kmax(61) == 37250 and kmax(64) == 34000
per = [(52, 'weekly'), (26, 'biweekly'), (24, 'semimonthly'), (12, 'monthly')]
max_rows = ''.join(f'<tr><td>{lab}</td>' + ''.join(f'<td class="n">${kmax(a) / n:,.2f}</td>' for n, _ in per) + '</tr>'
                   for lab, a in [('Under 50', 40), ('Age 50 to 59 or 64+', 55), ('Age 60 to 63', 61)])
data = json.dumps(L)

calc = """<div class="mc-calculator"><h2>Max out in 2027</h2>
<label class="mc-field"><span>Your age at the end of 2027</span><input id="lA" type="number" min="16" max="100" step="1" value="40"></label>
<label class="mc-field"><span>2027 salary ($)</span><input id="lS" type="number" min="0" step="500" value="90000"></label>
<label class="mc-field"><span>Pay frequency</span><select id="lP"><option value="52">Weekly</option><option value="26" selected>Every 2 weeks</option><option value="24">Twice a month</option><option value="12">Monthly</option></select></label>
<label class="mc-field"><span>Workplace plan</span><select id="lT"><option value="k">401(k), 403(b), 457 or TSP</option><option value="s">SIMPLE IRA</option></select></label>
<label class="mc-field"><span>Employer match (% of pay matched)</span><input id="lM" type="number" min="0" max="100" step="0.5" value="4"></label>
<label class="mc-field"><span>HSA coverage</span><select id="lH"><option value="0">No HSA</option><option value="self">Self-only HDHP</option><option value="fam">Family HDHP</option></select></label>
<button class="mc-button" data-action="lim">Calculate</button>
<div class="mc-result tp-res" id="lR" aria-live="polite">Enter your age and salary.</div></div>"""

script = """<script>(()=>{const L=__D__,$=id=>document.getElementById(id),v=id=>Math.max(0,+$(id).value||0),f=x=>x.toLocaleString('en-US',{style:'currency',currency:'USD'}),f0=x=>x.toLocaleString('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0});
function run(){const a=v('lA'),s=v('lS'),n=+$('lP').value,t=$('lT').value,mt=v('lM'),h=$('lH').value;
const cu=t==='k'?(a>=60&&a<=63?L.cu6063:a>=50?L.cu50:0):(a>=60&&a<=63?L.simple6063:a>=50?L.simplecu:0),base=t==='k'?L.k:L.simple,mx=base+cu;
const cap=Math.min(mx,s),pct=s?100*cap/s:0,match=s*mt/100,ira=L.ira+(a>=50?L.iracu:0),hsa=h==='0'?0:(h==='self'?L.hsa_self:L.hsa_fam)+(a>=55?L.hsacu:0);
let r='<p class="tp-big"><strong>'+f(cap/n)+'</strong> per paycheck to max your '+(t==='k'?'401(k)':'SIMPLE IRA')+'</p><div class="tp-scroll"><table class="tp-table"><tbody>'+
'<tr><td>2027 limit'+(cu?' including '+f0(cu)+' catch-up':'')+'</td><td class="n">'+f0(mx)+'</td></tr><tr><td>Percent of salary to elect</td><td class="n">'+pct.toFixed(1)+'%</td></tr>'+
(mt?'<tr><td>Employer match (doesn\\'t count toward your limit)</td><td class="n">'+f0(match)+'</td></tr>':'')+
'<tr><td>IRA limit'+(a>=50?' with $1,100 catch-up':'')+' ('+f(ira/12)+' a month)</td><td class="n">'+f0(ira)+'</td></tr>'+(hsa?'<tr><td>HSA limit ('+f(hsa/n)+' per paycheck)</td><td class="n">'+f0(hsa)+'</td></tr>':'')+
'<tr class="tot"><td>Total you can save with tax benefits</td><td class="n">'+f0(cap+ira+hsa)+'</td></tr></tbody></table></div>';
if(s<mx)r+='<p>Your salary is below the limit, so the most you can defer is 100% of pay.</p>';
if(a>=60&&a<=63)r+='<p>Ages 60 to 63 get the larger "super catch-up" of '+f0(cu)+'.</p>';
if(mt&&pct<mt)r+='<p>Contributing at least '+mt+'% of pay gets your full match.</p>';
if(cu)r+='<p class="tp-note">If your 2026 Social Security wages were over the IRS threshold ($150,000 for 2026), catch-up contributions must go in as Roth (after tax).</p>';r+='<p class="tp-note">Your plan may also have its own limits.</p>';$('lR').innerHTML=r}
document.addEventListener('DOMContentLoaded',()=>{['lA','lS','lP','lT','lM','lH'].forEach(i=>$(i).addEventListener('input',run));document.querySelectorAll('[data-action="lim"]').forEach(b=>b.addEventListener('click',run));run()})})();</script>"""
script = script.replace('__D__', data)

body = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>2027 contribution limits at a glance</h2>
<p class="tp-answer">In 2027 you can put up to <strong>$25,500</strong> into a 401(k), 403(b), 457 or the Thrift Savings Plan, up from $24,500. Workers 50 and older can add <strong>$8,500</strong> (total $34,000), and those aged <strong>60 to 63 can add $11,750</strong> (total $37,250).
The IRA limit stays at <strong>$7,500</strong> ($8,600 at 50+). HSA limits rise to <strong>$4,500</strong> for self-only coverage and <strong>$9,000</strong> for family coverage.</p>
<p>To max out a 401(k) in 2027 you need to contribute <strong>$980.77 every two weeks</strong> (26 paychecks) or $2,125 a month.</p></header>

<section><h2>2027 vs 2026 limits</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Account</th><th class="n">2026</th><th class="n">2027</th></tr></thead><tbody>
<tr><td>401(k), 403(b), 457, TSP: employee deferral</td><td class="n">$24,500</td><td class="n">$25,500</td></tr>
<tr><td>Catch-up, age 50+</td><td class="n">$8,000</td><td class="n">$8,500</td></tr>
<tr><td>Catch-up, ages 60 to 63</td><td class="n">$11,250</td><td class="n">$11,750</td></tr>
<tr><td>IRA (traditional and Roth combined)</td><td class="n">$7,500</td><td class="n">$7,500</td></tr>
<tr><td>IRA catch-up, age 50+</td><td class="n">$1,100</td><td class="n">$1,100</td></tr>
<tr><td>SIMPLE IRA deferral</td><td class="n">$17,000</td><td class="n">$17,500</td></tr>
<tr><td>SIMPLE catch-up, age 50+ / ages 60 to 63</td><td class="n">$4,000 / $5,250</td><td class="n">$4,000 / $5,250</td></tr>
<tr><td>HSA, self-only</td><td class="n">$4,400</td><td class="n">$4,500</td></tr>
<tr><td>HSA, family</td><td class="n">$8,750</td><td class="n">$9,000</td></tr>
<tr><td>HSA catch-up, age 55+</td><td class="n">$1,000</td><td class="n">$1,000</td></tr></tbody></table></div></section>

<section><h2>How much per paycheck to max your 401(k) in 2027</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Age</th>{''.join(f'<th class="n">{lab.capitalize()}</th>' for _, lab in per)}</tr></thead><tbody>{max_rows}</tbody></table></div></section>

<section><h2>Roth IRA and IRA deduction income limits for 2027</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Rule</th><th class="n">Single / head of household</th><th class="n">Married filing jointly</th></tr></thead><tbody>
<tr><td>Roth IRA contribution phase-out</td><td class="n">$158,000 – $173,000</td><td class="n">$250,000 – $260,000</td></tr>
<tr><td>Traditional IRA deduction phase-out, covered by a workplace plan</td><td class="n">$83,000 – $93,000</td><td class="n">$133,000 – $153,000</td></tr>
<tr><td>Traditional IRA deduction phase-out, spouse covered (you aren't)</td><td class="n">–</td><td class="n">$250,000 – $260,000</td></tr>
<tr><td>Saver's Credit income limit</td><td class="n">$41,500 / $62,250</td><td class="n">$83,000</td></tr></tbody></table></div>
<p>To use an HSA in 2027 your health plan must have a deductible of at least $1,750 (self-only) or $3,500 (family), with out-of-pocket costs capped at $8,700 or $17,400.</p></section>

<section><h2>Good to know</h2>
<ul><li><strong>Employer matches don't count</strong> toward your $25,500 employee limit.</li>
<li><strong>Roth catch-up rule:</strong> if your prior-year Social Security wages from the employer were above the IRS threshold ($150,000 for 2026), catch-up contributions must be Roth.</li>
<li><strong>Raising your contribution</strong> lowers your taxable pay. See how it affects take-home pay with the <a href="/tools/2027-paycheck-calculator">2027 paycheck calculator</a>.</li>
<li><strong>Deadlines:</strong> 401(k) deferrals must come out of 2027 paychecks; IRA and HSA contributions for 2027 can be made until the April 2028 tax deadline.</li></ul>
<p>Sources: <a href="https://www.irs.gov/node/167581" rel="noopener" target="_blank">IRS IR-2026-136, 2027 retirement plan limits</a>, <a href="https://www.irs.gov/pub/irs-drop/rp-26-24.pdf" rel="noopener" target="_blank">Rev. Proc. 2026-24 (HSA)</a>.</p></section>
{related('2027-401k-ira-hsa-limits', [('/tools/gs-pay-scale-2027', 'GS pay scale 2027')])}"""

faqs = [("What is the 401(k) limit for 2027?", "$25,500 for employee deferrals, up from $24,500 in 2026. It applies to 401(k), 403(b), most 457 plans and the federal Thrift Savings Plan."),
        ("What is the 401(k) catch-up limit for 2027?", "$8,500 for ages 50 and older, for a total of $34,000. Workers aged 60 to 63 can contribute $11,750 instead, for a total of $37,250."),
        ("What is the IRA limit for 2027?", "$7,500, the same as 2026, plus a $1,100 catch-up at age 50 and older ($8,600 total)."),
        ("What are the 2027 HSA limits?", "$4,500 for self-only coverage and $9,000 for family coverage, plus $1,000 if you are 55 or older."),
        ("How much should I contribute per paycheck to max my 401(k) in 2027?", "$980.77 per biweekly paycheck, $1,062.50 twice a month, $2,125 monthly or $490.38 weekly if you are under 50."),
        ("What is the Roth IRA income limit for 2027?", "Contributions phase out between $158,000 and $173,000 of modified AGI for single filers and between $250,000 and $260,000 for married couples filing jointly.")]

page('2027-401k-ira-hsa-limits', '2027 401(k), IRA and HSA Limits + Calculator | ToolPinch',
     '2027 contribution limits: 401(k) $25,500, catch-up $8,500 or $11,750 at 60-63, IRA $7,500, HSA $4,500/$9,000. See how much per paycheck to max out.',
     '2027 401(k), IRA and HSA Limits', 'IRS figures released Nov 12, 2026',
     'The new 2027 contribution limits and exactly how much to set aside each paycheck to max out.',
     ['Official IRS figures', 'Per-paycheck amounts', 'No signup'], calc, body, faqs, script)
