"""Build /tools/us-paycheck-calculator (2026 federal, FICA, 50 states + DC)."""
import json
from tax_common import page, related, BT_JS, RENDER_JS, PERIOD_SELECT

# code: name, single(brackets, std, exemption, credit), married(brackets, std, exemption, credit); None = no wage income tax
F = lambda b: [[t, r / 100] for t, r in b]
S = {
 'AL': ('Alabama', (F([[0,2],[500,4],[3000,5]]),3000,1500,0), (F([[0,2],[1000,4],[6000,5]]),8500,3000,0)),
 'AK': ('Alaska', None, None),
 'AZ': ('Arizona', (F([[0,2.5]]),8350,0,0), (F([[0,2.5]]),16700,0,0)),
 'AR': ('Arkansas', (F([[0,2],[4600,3.9]]),2470,0,29), (F([[0,2],[4600,3.9]]),4940,0,58)),
 'CA': ('California', (F([[0,1],[11079,2],[26264,4],[41452,6],[57542,8],[72724,9.3],[371479,10.3],[445771,11.3],[742953,12.3],[1000000,13.3]]),5540,0,153),
        (F([[0,1],[22158,2],[52528,4],[82904,6],[115084,8],[145448,9.3],[742958,10.3],[891542,11.3],[1000000,12.3],[1485906,13.3]]),11080,0,306)),
 'CO': ('Colorado', (F([[0,4.4]]),16100,0,0), (F([[0,4.4]]),32200,0,0)),
 'CT': ('Connecticut', (F([[0,2],[10000,4.5],[50000,5.5],[100000,6],[200000,6.5],[250000,6.9],[500000,6.99]]),0,15000,0),
        (F([[0,2],[20000,4.5],[100000,5.5],[200000,6],[400000,6.5],[500000,6.9],[1000000,6.99]]),0,24000,0)),
 'DE': ('Delaware', (F([[2000,2.2],[5000,3.9],[10000,4.8],[20000,5.2],[25000,5.55],[60000,6.6]]),3250,0,110),
        (F([[2000,2.2],[5000,3.9],[10000,4.8],[20000,5.2],[25000,5.55],[60000,6.6]]),6500,0,220)),
 'DC': ('District of Columbia', (F([[0,4],[10000,6],[40000,6.5],[60000,8.5],[250000,9.25],[500000,9.75],[1000000,10.75]]),16100,0,0),
        (F([[0,4],[10000,6],[40000,6.5],[60000,8.5],[250000,9.25],[500000,9.75],[1000000,10.75]]),32200,0,0)),
 'FL': ('Florida', None, None),
 'GA': ('Georgia', (F([[0,5.19]]),12000,0,0), (F([[0,5.19]]),24000,0,0)),
 'HI': ('Hawaii', (F([[0,1.4],[9600,3.2],[14400,5.5],[19200,6.4],[24000,6.8],[36000,7.2],[48000,7.6],[125000,7.9],[175000,8.25],[225000,9],[275000,10],[325000,11]]),4400,1144,0),
        (F([[0,1.4],[19200,3.2],[28800,5.5],[38400,6.4],[48000,6.8],[72000,7.2],[96000,7.6],[250000,7.9],[350000,8.25],[450000,9],[550000,10],[650000,11]]),8800,2288,0)),
 'ID': ('Idaho', (F([[4811,5.3]]),16100,0,0), (F([[9622,5.3]]),32200,0,0)),
 'IL': ('Illinois', (F([[0,4.95]]),0,2925,0), (F([[0,4.95]]),0,5850,0)),
 'IN': ('Indiana', (F([[0,2.95]]),0,1000,0), (F([[0,2.95]]),0,2000,0)),
 'IA': ('Iowa', (F([[0,3.8]]),16100,0,40), (F([[0,3.8]]),32200,0,80)),
 'KS': ('Kansas', (F([[0,5.2],[23000,5.58]]),3605,9160,0), (F([[0,5.2],[46000,5.58]]),8240,18320,0)),
 'KY': ('Kentucky', (F([[0,3.5]]),3360,0,0), (F([[0,3.5]]),3360,0,0)),
 'LA': ('Louisiana', (F([[0,3]]),12875,0,0), (F([[0,3]]),25750,0,0)),
 'ME': ('Maine', (F([[0,5.8],[27399,6.75],[64849,7.15]]),8350,5300,0), (F([[0,5.8],[54849,6.75],[129749,7.15]]),16700,10600,0)),
 'MD': ('Maryland', (F([[0,2],[1000,3],[2000,4],[3000,4.75],[100000,5],[125000,5.25],[150000,5.5],[250000,5.75],[500000,6.25],[1000000,6.5]]),3350,3200,0),
        (F([[0,2],[1000,3],[2000,4],[3000,4.75],[150000,5],[175000,5.25],[225000,5.5],[300000,5.75],[600000,6.25],[1200000,6.5]]),6700,6400,0)),
 'MA': ('Massachusetts', (F([[0,5],[1083150,9]]),0,4400,0), (F([[0,5],[1083150,9]]),0,8800,0)),
 'MI': ('Michigan', (F([[0,4.25]]),0,5900,0), (F([[0,4.25]]),0,11800,0)),
 'MN': ('Minnesota', (F([[0,5.35],[33310,6.8],[109430,7.85],[203150,9.85]]),15300,0,0), (F([[0,5.35],[48700,6.8],[193480,7.85],[337930,9.85]]),30600,0,0)),
 'MS': ('Mississippi', (F([[10000,4]]),2300,6000,0), (F([[10000,4]]),4600,12000,0)),
 'MO': ('Missouri', (F([[1348,2],[2696,2.5],[4044,3],[5392,3.5],[6740,4],[8088,4.5],[9436,4.7]]),16100,0,0),
        (F([[1348,2],[2696,2.5],[4044,3],[5392,3.5],[6740,4],[8088,4.5],[9436,4.7]]),32200,0,0)),
 'MT': ('Montana', (F([[0,4.7],[47500,5.65]]),16100,0,0), (F([[0,4.7],[95000,5.65]]),32200,0,0)),
 'NE': ('Nebraska', (F([[0,2.46],[4130,3.51],[24760,4.55]]),8850,0,176), (F([[0,2.46],[8250,3.51],[49530,4.55]]),17700,0,352)),
 'NV': ('Nevada', None, None), 'NH': ('New Hampshire', None, None),
 'NJ': ('New Jersey', (F([[0,1.4],[20000,1.75],[35000,3.5],[40000,5.53],[75000,6.37],[500000,8.97],[1000000,10.75]]),0,1000,0),
        (F([[0,1.4],[20000,1.75],[50000,2.45],[70000,3.5],[80000,5.53],[150000,6.37],[500000,8.97],[1000000,10.75]]),0,2000,0)),
 'NM': ('New Mexico', (F([[0,1.5],[5500,3.2],[16500,4.3],[33500,4.7],[66500,4.9],[210000,5.9]]),16100,0,0),
        (F([[0,1.5],[8000,3.2],[25000,4.3],[50000,4.7],[100000,4.9],[315000,5.9]]),32200,0,0)),
 'NY': ('New York', (F([[0,3.9],[8500,4.4],[11700,5.15],[13900,5.4],[80650,5.9],[215400,6.85],[1077550,9.65],[5000000,10.3],[25000000,10.9]]),8000,0,0),
        (F([[0,3.9],[17150,4.4],[23600,5.15],[27900,5.4],[161550,5.9],[323200,6.85],[2155350,9.65],[5000000,10.3],[25000000,10.9]]),16050,0,0)),
 'NC': ('North Carolina', (F([[0,3.99]]),12750,0,0), (F([[0,3.99]]),25500,0,0)),
 'ND': ('North Dakota', (F([[48475,1.95],[244825,2.5]]),16100,0,0), (F([[80975,1.95],[298075,2.5]]),32200,0,0)),
 'OH': ('Ohio', (F([[26050,2.75]]),0,2400,0), (F([[26050,2.75]]),0,4800,0)),
 'OK': ('Oklahoma', (F([[3750,2.5],[4900,3.5],[7200,4.5]]),6350,1000,0), (F([[7500,2.5],[9800,3.5],[14400,4.5]]),12700,2000,0)),
 'OR': ('Oregon', (F([[0,4.75],[4550,6.75],[11400,8.75],[125000,9.9]]),2910,0,256), (F([[0,4.75],[9100,6.75],[22800,8.75],[250000,9.9]]),5820,0,512)),
 'PA': ('Pennsylvania', (F([[0,3.07]]),0,0,0), (F([[0,3.07]]),0,0,0)),
 'RI': ('Rhode Island', (F([[0,3.75],[82050,4.75],[186450,5.99]]),11200,5250,0), (F([[0,3.75],[82050,4.75],[186450,5.99]]),22400,10500,0)),
 'SC': ('South Carolina', (F([[3640,3],[18230,6]]),8350,0,0), (F([[3640,3],[18230,6]]),16700,0,0)),
 'SD': ('South Dakota', None, None), 'TN': ('Tennessee', None, None), 'TX': ('Texas', None, None),
 'UT': ('Utah', (F([[0,4.5]]),0,0,966), (F([[0,4.5]]),0,0,1932)),
 'VT': ('Vermont', (F([[0,3.35],[49400,6.6],[119700,7.6],[249700,8.75]]),7650,5300,0), (F([[0,3.35],[82500,6.6],[199450,7.6],[304000,8.75]]),15300,10600,0)),
 'VA': ('Virginia', (F([[0,2],[3000,3],[5000,5],[17000,5.75]]),8750,930,0), (F([[0,2],[3000,3],[5000,5],[17000,5.75]]),17500,1860,0)),
 'WA': ('Washington', None, None),
 'WV': ('West Virginia', (F([[0,2.22],[10000,2.96],[25000,3.33],[40000,4.44],[60000,4.82]]),0,2000,0), (F([[0,2.22],[10000,2.96],[25000,3.33],[40000,4.44],[60000,4.82]]),0,4000,0)),
 'WI': ('Wisconsin', (F([[0,3.5],[15110,4.4],[51950,5.3],[332720,7.65]]),13960,700,0), (F([[0,3.5],[20150,4.4],[69260,5.3],[443630,7.65]]),25840,1400,0)),
 'WY': ('Wyoming', None, None),
}
assert len(S) == 51
FED = {'single': (F([[0,10],[12400,12],[50400,22],[105700,24],[201775,32],[256225,35],[640600,37]]),16100,200000),
       'married': (F([[0,10],[24800,12],[100800,22],[211400,24],[403550,32],[512450,35],[768700,37]]),32200,250000),
       'hoh': (F([[0,10],[17700,12],[67450,22],[105700,24],[201750,32],[256200,35],[640600,37]]),24150,200000)}
SS_BASE = 184500
NOTE = {'IN': 'Indiana counties add a local income tax of about 0.5% to 3%, not included.',
        'MD': 'Maryland counties add a local income tax of 2.25% to 3.3%, not included.',
        'NY': 'New York City residents also pay city income tax of 3.078% to 3.876%, not included.',
        'PA': 'Most Pennsylvania municipalities add a local earned income tax (Philadelphia 3.74%), not included. Pennsylvania does not let 401(k) contributions reduce state taxable wages.',
        'OH': 'Many Ohio cities charge a municipal income tax of 1% to 2.5%, not included.',
        'MI': 'Detroit and some other Michigan cities add a city income tax, not included.',
        'KY': 'Kentucky cities and counties charge occupational license taxes, not included.',
        'CA': 'California also deducts State Disability Insurance (SDI) from wages, not included.',
        'WA': 'Washington has no wage income tax. Its 7% to 9% tax applies only to large capital gains. WA Cares and paid leave premiums are not included.',
        'TX': 'Texas has no state income tax.', 'FL': 'Florida has no state income tax.', 'NV': 'Nevada has no state income tax.',
        'NH': 'New Hampshire has no tax on wages; its tax on interest and dividends ended in 2025.', 'SD': 'South Dakota has no state income tax.',
        'TN': 'Tennessee has no state income tax.', 'WY': 'Wyoming has no state income tax.', 'AK': 'Alaska has no state income tax.',
        'NJ': 'New Jersey also deducts small state disability and family leave contributions, not included.'}

order = sorted(S, key=lambda k: S[k][0])
opts = ''.join(f'<option value="{k}"{" selected" if k=="CA" else ""}>{S[k][0]}</option>' for k in order)
data = json.dumps({'S': S, 'F': FED, 'N': NOTE, 'B': SS_BASE})


def stax(code, taxable_gross, status):
    s = S[code][1 if status != 'married' else 2]
    if s is None:
        return 0
    b, std, ex, cr = s
    ti = max(0, taxable_gross - std - ex)
    t = 0
    for i, (lo, r) in enumerate(b):
        hi = b[i + 1][0] if i + 1 < len(b) else 1e18
        if ti > lo:
            t += (min(ti, hi) - lo) * r
    return max(0, t - cr)


def btax(x, b):
    t = 0
    for i, (lo, r) in enumerate(b):
        hi = b[i + 1][0] if i + 1 < len(b) else 1e18
        if x > lo:
            t += (min(x, hi) - lo) * r
    return t


def calc_py(gross, status, code, k401=0, health=0):
    b, std, addl = FED[status]
    fed = btax(max(0, gross - k401 - health - std), b)
    fw = gross - health
    ss = min(fw, SS_BASE) * 0.062
    med = fw * 0.0145 + max(0, fw - addl) * 0.009
    st = stax(code, gross - k401 - health, status)
    return round(fed, 2), round(ss, 2), round(med, 2), round(st, 2)


# hand-checked examples
fed, ss, med, st = calc_py(75000, 'single', 'TX')
assert fed == 1240 + 0.12 * (50400 - 12400) + 0.22 * (58900 - 50400), fed   # 1240+4560+1870 = 7670
assert ss == 4650 and med == 1087.5 and st == 0
fed, ss, med, st = calc_py(75000, 'single', 'CA')
print('CA 75k single', fed, ss, med, st)
ex_rows = []
for g, s_, c in [(50000, 'single', 'TX'), (75000, 'single', 'CA'), (100000, 'single', 'NY'), (150000, 'married', 'IL'), (60000, 'single', 'FL'), (90000, 'hoh', 'NC')]:
    fed, ss, med, st = calc_py(g, s_, c)
    net = g - fed - ss - med - st
    ex_rows.append((g, {'single': 'Single', 'married': 'Married filing jointly', 'hoh': 'Head of household'}[s_], S[c][0], fed, ss + med, st, net))
    print(g, s_, c, fed, ss + med, st, round(net, 2))
m = lambda x: f"${x:,.0f}"
ex_html = ''.join(f'<tr><td>{m(g)}</td><td>{s_}</td><td>{c}</td><td class="n">{m(f_)}</td><td class="n">{m(fi)}</td><td class="n">{m(st)}</td><td class="n"><b>{m(n)}</b><br><small>{m(n/12)}/mo</small></td></tr>' for g, s_, c, f_, fi, st, n in ex_rows)

state_rows = []
for k in order:
    s = S[k][1]
    if s is None:
        state_rows.append(f'<tr><td>{S[k][0]}</td><td>None</td><td class="n">0%</td></tr>')
    else:
        rs = [r for _, r in s[0]]
        kind = 'Flat' if len(rs) == 1 else f'{len(rs)} brackets'
        rng = f'{rs[0]*100:g}%' if len(rs) == 1 else f'{rs[0]*100:g}% – {rs[-1]*100:g}%'
        state_rows.append(f'<tr><td>{S[k][0]}</td><td>{kind}</td><td class="n">{rng}</td></tr>')
state_html = ''.join(state_rows)
NFLAT = sum(1 for k in S if S[k][1] and len(S[k][1][0]) == 1)
NNONE = sum(1 for k in S if S[k][1] is None)
print('flat', NFLAT, 'none', NNONE)

calc = f"""<div class="mc-calculator"><h2>Your 2026 take-home pay</h2>
<label class="mc-field"><span>Annual salary before tax ($)</span><input id="uGross" type="number" min="0" step="100" value="75000"></label>
<label class="mc-field"><span>State</span><select id="uState">{opts}</select></label>
<label class="mc-field"><span>Filing status</span><select id="uStatus"><option value="single">Single</option><option value="married">Married filing jointly</option><option value="hoh">Head of household</option></select></label>
<label class="mc-field"><span>401(k) / 403(b) contribution (% of pay)</span><input id="u401" type="number" min="0" max="100" step="0.5" value="0"></label>
<label class="mc-field"><span>Pre-tax health premiums ($ per year)</span><input id="uHealth" type="number" min="0" step="10" value="0"></label>
{PERIOD_SELECT}
<button class="mc-button" data-action="us-pay">Calculate</button>
<div class="mc-result tp-res" id="uResult" aria-live="polite">Enter your salary to see your take-home pay.</div></div>"""

script = """<script>(()=>{const D=__D__,$=id=>document.getElementById(id);""" + BT_JS + RENDER_JS + """
const fmt=x=>x.toLocaleString('en-US',{style:'currency',currency:'USD'});
function run(){const g=Math.max(0,+$('uGross').value||0),st=$('uStatus').value,code=$('uState').value,k=Math.min(g,g*Math.max(0,+$('u401').value||0)/100),hl=Math.min(g-k,Math.max(0,+$('uHealth').value||0));
const f=D.F[st],fed=BT(Math.max(0,g-k-hl-f[1]),f[0]),fw=g-hl,ss=Math.min(fw,D.B)*0.062,med=fw*0.0145+Math.max(0,fw-f[2])*0.009;
const s=D.S[code][st==='married'?2:1];let sTax=0;if(s){sTax=Math.max(0,BT(Math.max(0,g-k-hl-s[1]-s[2]),s[0])-s[3])}
const name=D.S[code][0],rows=[['Federal income tax',fed,1],['Social Security (6.2%)',ss,0],['Medicare (1.45%'+(fw>f[2]?' + 0.9%':'')+')',med,0],[name+' income tax',sTax,1]];
if(k>0)rows.push(['401(k) contribution',k,0]);if(hl>0)rows.push(['Health premiums',hl,0]);
const net=g-rows.reduce((a,r)=>a+r[1],0);renderRes($('uResult'),g,rows,net,fmt,$('per').value);
const n=D.N[code];if(n)$('uResult').insertAdjacentHTML('beforeend','<p class="tp-note">'+n+'</p>');
if(st==='hoh'&&s)$('uResult').insertAdjacentHTML('beforeend','<p class="tp-note">State tax for head of household uses the single-filer brackets.</p>')}
document.addEventListener('DOMContentLoaded',()=>{['uGross','uState','uStatus','u401','uHealth','per'].forEach(id=>$(id).addEventListener('input',run));
document.querySelectorAll('[data-action="us-pay"]').forEach(b=>b.addEventListener('click',run));run()})})();</script>""".replace('__D__', data)

fb = lambda st: ''.join(f'<tr><td class="n">{r*100:g}%</td><td>{m(lo)} – {m(FED[st][0][i+1][0])}</td></tr>' if i + 1 < len(FED[st][0]) else f'<tr><td class="n">{r*100:g}%</td><td>Over {m(lo)}</td></tr>' for i, (lo, r) in enumerate(FED[st][0]))
script = script.replace('__D__', data)
body = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>How much is taken out of a US paycheck in 2026?</h2>
<p class="tp-answer">Four main deductions come out of most paychecks: <strong>federal income tax</strong> (10% to 37% on income above the $16,100 standard deduction for a single filer),
<strong>Social Security</strong> (6.2% up to $184,500 of wages), <strong>Medicare</strong> (1.45%, plus 0.9% above $200,000) and <strong>state income tax</strong> (0% in nine states, up to 13.3% in California).
A single filer earning $75,000 in Texas takes home about <strong>{m(75000 - sum(calc_py(75000,'single','TX')))}</strong> a year.</p></header>

<section><h2>Take-home pay examples for 2026</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Salary</th><th>Status</th><th>State</th><th class="n">Federal tax</th><th class="n">FICA</th><th class="n">State tax</th><th class="n">Take-home</th></tr></thead><tbody>{ex_html}</tbody></table></div>
<p class="tp-note">No 401(k) or pre-tax benefits, no credits. Local income taxes not included.</p></section>

<section><h2>2026 federal income tax brackets</h2>
<p>Brackets apply to taxable income: salary minus pre-tax contributions minus the standard deduction ($16,100 single, $32,200 married filing jointly, $24,150 head of household).
Each rate applies only to the income inside its band.</p>
<div class="mc-example-grid"><div><h3>Single</h3><table class="tp-table"><tbody>{fb('single')}</tbody></table></div>
<div><h3>Married filing jointly</h3><table class="tp-table"><tbody>{fb('married')}</tbody></table></div>
<div><h3>Head of household</h3><table class="tp-table"><tbody>{fb('hoh')}</tbody></table></div></div></section>

<section><h2>FICA: Social Security and Medicare</h2>
<p>Employees pay <strong>6.2%</strong> Social Security tax on wages up to the 2026 wage base of <strong>$184,500</strong> (a maximum of $11,439) and <strong>1.45%</strong> Medicare tax on all wages.
An extra <strong>0.9%</strong> Additional Medicare Tax applies to wages above $200,000 (single or head of household) or $250,000 (married filing jointly). Your employer pays a matching 6.2% and 1.45%.
401(k) contributions do not reduce FICA wages; health premiums paid through a cafeteria (Section 125) plan do.</p></section>

<section><h2>State income tax rates for 2026</h2>
<p>Nine states have no tax on wages: Alaska, Florida, Nevada, New Hampshire, South Dakota, Tennessee, Texas, Washington and Wyoming. {NFLAT} states use a single flat rate.
The calculator applies each state's 2026 brackets, standard deduction, personal exemption and credits for single and married filers.</p>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>State</th><th>Structure</th><th class="n">Rates (single)</th></tr></thead><tbody>{state_html}</tbody></table></div></section>

<section><h2>How the calculator works</h2>
<ol><li>Federal taxable income = salary − 401(k) − pre-tax health premiums − standard deduction. The 2026 brackets for your filing status are applied.</li>
<li>Social Security = 6.2% of wages after health premiums, capped at $184,500. Medicare = 1.45% plus 0.9% over the threshold.</li>
<li>State taxable income = salary − 401(k) − health premiums − the state's standard deduction and personal exemption, then the state's brackets, minus any personal credit.</li></ol>
<p><strong>Not included:</strong> tax credits (child tax credit, earned income credit), itemized deductions, the 2025 law's deductions for tips, overtime and seniors, phase-outs of state deductions at higher incomes, local and city income taxes, and state disability or paid leave contributions.
Your actual paycheck withholding depends on your W-4 and can differ from the tax you owe for the year.</p></section>

<section><h2>Sources</h2>
<p>Federal brackets and standard deductions: <a href="https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026-including-amendments-from-the-one-big-beautiful-bill" rel="noopener" target="_blank">IRS 2026 inflation adjustments</a> (Rev. Proc. 2025-32).
Social Security wage base: <a href="https://www.ssa.gov/oact/cola/cbb.html" rel="noopener" target="_blank">Social Security Administration</a>.
State rates: <a href="https://taxfoundation.org/data/all/state/state-income-tax-rates-2026/" rel="noopener" target="_blank">Tax Foundation, State Individual Income Tax Rates and Brackets, 2026</a>, as of January 1, 2026.</p></section>
{related('us-paycheck-calculator', [('/tools/salary-to-hourly-calculator', 'Salary to hourly'), ('/tools/overtime-calculator', 'Overtime calculator'), ('/tools/payday-calendar-2027', '2027 payday calendar')])}"""

tx = 75000 - sum(calc_py(75000, 'single', 'TX'))
faqs = [
    ("How much tax is taken out of a $75,000 salary?", f"For a single filer in a state with no income tax, about {m(75000-tx)} a year: {m(calc_py(75000,'single','TX')[0])} federal income tax and {m(sum(calc_py(75000,'single','TX')[1:3]))} Social Security and Medicare. Take-home pay is about {m(tx)} a year, or {m(tx/12)} a month. State income tax adds more in most states."),
    ("What are the 2026 federal tax brackets?", "For single filers: 10% up to $12,400 of taxable income, 12% to $50,400, 22% to $105,700, 24% to $201,775, 32% to $256,225, 35% to $640,600 and 37% above. Married couples filing jointly have brackets twice as wide up to the 35% band."),
    ("What is the 2026 standard deduction?", "$16,100 for single filers, $32,200 for married couples filing jointly and $24,150 for heads of household."),
    ("What is the Social Security wage base for 2026?", "$184,500. Wages above that are not subject to the 6.2% Social Security tax, though Medicare tax still applies."),
    ("Which states have no income tax?", "Alaska, Florida, Nevada, New Hampshire, South Dakota, Tennessee, Texas, Washington and Wyoming do not tax wages."),
    ("Which state has the highest income tax?", "California, with a top rate of 13.3% on income above $1 million (12.3% plus a 1% mental health surcharge). Hawaii, New York, New Jersey and Washington DC also have top rates above 10%."),
    ("Does a 401(k) reduce my taxes?", "Traditional 401(k) contributions reduce federal and most state taxable income, so you pay less income tax now. They do not reduce Social Security or Medicare tax."),
    ("Why is my paycheck different from this estimate?", "Withholding depends on your W-4, pay frequency and benefits, and the calculator does not include tax credits, local taxes or state disability insurance. The estimate shows the tax for a full year at a steady salary."),
]

page('us-paycheck-calculator', 'US Paycheck Calculator 2026: Take-Home Pay After Tax, All 50 States | ToolPinch',
     '2026 take-home pay after federal tax, Social Security, Medicare and state income tax for all 50 states and DC. Single, married and head of household.',
     'US Paycheck Calculator 2026', 'Updated for 2026 tax year',
     'See your take-home pay after federal income tax, Social Security, Medicare and state income tax for any state, per paycheck or per year.',
     ['2026 IRS brackets', 'All 50 states + DC', 'No signup'], calc, body, faqs, script)
