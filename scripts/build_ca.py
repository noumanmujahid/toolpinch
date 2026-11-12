"""Build /tools/canada-take-home-pay-calculator (2026)."""
import json
from tax_common import page, related, BT_JS, RENDER_JS, PERIOD_SELECT

F = lambda b: [[t, r / 100] for t, r in b]
FED = F([[0, 14], [58523, 20.5], [117045, 26], [181440, 29], [258482, 33]])
# code: name, brackets, basic personal amount, credit rate
P = {
 'AB': ('Alberta', F([[0,8],[61200,10],[154259,12],[185111,13],[246813,14],[370220,15]]), 22769, .08),
 'BC': ('British Columbia', F([[0,5.6],[50363,7.7],[100728,10.5],[115648,12.29],[140430,14.7],[190405,16.8],[265545,20.5]]), 13216, .056),
 'MB': ('Manitoba', F([[0,10.8],[47564,12.75],[101200,17.4]]), 15780, .108),
 'NB': ('New Brunswick', F([[0,9.4],[52333,14],[104666,16],[193861,19.5]]), 13664, .094),
 'NL': ('Newfoundland and Labrador', F([[0,8.7],[44678,14.5],[89354,15.8],[159528,17.8],[223340,19.8],[285319,20.8],[570638,21.3],[1141275,21.8]]), 11188, .087),
 'NS': ('Nova Scotia', F([[0,8.79],[30995,14.95],[61991,16.67],[97417,17.5],[157124,21]]), 11932, .0879),
 'NT': ('Northwest Territories', F([[0,5.9],[53003,8.6],[106009,12.2],[172346,14.05]]), 18198, .059),
 'NU': ('Nunavut', F([[0,4],[55801,7],[111602,9],[181439,11.5]]), 19659, .04),
 'ON': ('Ontario', F([[0,5.05],[53891,9.15],[107785,11.16],[150000,12.16],[220000,13.16]]), 12989, .0505),
 'PE': ('Prince Edward Island', F([[0,9.5],[33928,13.47],[65820,16.6],[106890,17.62],[142520,19],[200000,20]]), 15000, .095),
 'QC': ('Quebec', F([[0,14],[54345,19],[108680,24],[132245,25.75]]), 18952, .14),
 'SK': ('Saskatchewan', F([[0,10.5],[54532,12.5],[155805,14.5]]), 20381, .105),
 'YT': ('Yukon', F([[0,6.4],[58523,9],[117045,10.9],[181440,12.8],[500000,15]]), 16452, .064),
}
YMPE, YAMPE, EXEMPT = 74600, 85000, 3500
CEA = 1501


def bt(x, b):
    t = 0
    for i, (lo, r) in enumerate(b):
        hi = b[i + 1][0] if i + 1 < len(b) else 1e18
        if x > lo:
            t += (min(x, hi) - lo) * r
    return t


def ohp(ti):  # Ontario Health Premium
    if ti <= 20000: return 0
    if ti <= 36000: return min(300, .06 * (ti - 20000))
    if ti <= 48000: return min(450, 300 + .06 * (ti - 36000))
    if ti <= 72000: return min(600, 450 + .25 * (ti - 48000))
    if ti <= 200000: return min(750, 600 + .25 * (ti - 72000))
    return min(900, 750 + .25 * (ti - 200000))


def calc_py(g, prov, rrsp=0):
    qc = prov == 'QC'
    rate, base_r = (.063, .053) if qc else (.0595, .0495)
    pens_e = max(0, min(g, YMPE) - EXEMPT)
    cpp1 = pens_e * rate
    cpp_base = pens_e * base_r
    cpp_enh = cpp1 - cpp_base
    cpp2 = max(0, min(g, YAMPE) - YMPE) * .04
    ei = min(g, 68900) * (.013 if qc else .0163)
    qpip = min(g, 103000) * .0043 if qc else 0
    ti = max(0, g - rrsp - cpp_enh - cpp2)
    bpa = 16452 - 1623 * min(1, max(0, (ti - 181440) / (258482 - 181440)))
    fcred = .14 * (bpa + cpp_base + ei + qpip + min(CEA, g))
    fed = max(0, bt(ti, FED) - fcred)
    if qc:
        fed *= (1 - .165)
    name, pb, pbpa, pr = P[prov]
    pcred = pr * pbpa if qc else pr * (pbpa + cpp_base + ei + (min(CEA, g) if prov == 'YT' else 0))
    pt = max(0, bt(ti, pb) - pcred)
    extra = 0
    if prov == 'ON':
        extra = .20 * max(0, pt - 5818) + .36 * max(0, pt - 7446) + ohp(ti)
    return dict(fed=round(fed, 2), prov=round(pt + extra, 2), cpp=round(cpp1 + cpp2, 2), ei=round(ei + qpip, 2))


r = calc_py(60000, 'ON')
print('ON 60k', r, 60000 - sum(r.values()))
# CPP check: (60000-3500)*.0595 = 3361.75; EI 60000*.0163 = 978
assert r['cpp'] == 3361.75 and r['ei'] == 978.0
assert calc_py(100000, 'AB')['cpp'] == 4230.45 + 416
m = lambda x: f"${x:,.0f}"
ex = [(g, p, calc_py(g, p)) for g, p in [(50000, 'ON'), (75000, 'ON'), (100000, 'ON'), (75000, 'BC'), (75000, 'AB'), (75000, 'QC'), (75000, 'MB'), (75000, 'NS')]]
for g, p, r in ex:
    print(g, p, r, round(g - sum(r.values())))
ex_html = ''.join(f'<tr><td>{m(g)}</td><td>{P[p][0]}</td><td class="n">{m(r["fed"])}</td><td class="n">{m(r["prov"])}</td><td class="n">{m(r["cpp"]+r["ei"])}</td><td class="n"><b>{m(g-sum(r.values()))}</b><br><small>{m((g-sum(r.values()))/12)}/mo</small></td></tr>' for g, p, r in ex)
order = sorted(P, key=lambda k: P[k][0])
opts = ''.join(f'<option value="{k}"{" selected" if k=="ON" else ""}>{P[k][0]}</option>' for k in order)
prov_rows = ''.join(f'<tr><td>{P[k][0]}</td><td class="n">{P[k][1][0][1]*100:g}%</td><td class="n">{P[k][1][-1][1]*100:g}% over {m(P[k][1][-1][0])}</td><td class="n">{m(P[k][2])}</td></tr>' for k in order)
data = json.dumps({'F': FED, 'P': P})

calc = f"""<div class="mc-calculator"><h2>Your 2026 take-home pay</h2>
<label class="mc-field"><span>Annual salary before tax ($)</span><input id="cGross" type="number" min="0" step="100" value="75000"></label>
<label class="mc-field"><span>Province or territory</span><select id="cProv">{opts}</select></label>
<label class="mc-field"><span>RRSP contribution ($ per year)</span><input id="cRrsp" type="number" min="0" step="100" value="0"></label>
{PERIOD_SELECT}
<button class="mc-button" data-action="ca-pay">Calculate</button>
<div class="mc-result tp-res" id="cResult" aria-live="polite">Enter your salary to see your take-home pay.</div></div>"""

script = """<script>(()=>{const D=__D__,$=id=>document.getElementById(id);""" + BT_JS + RENDER_JS + """
const fmt=x=>x.toLocaleString('en-CA',{style:'currency',currency:'CAD'});
function ohp(t){if(t<=20000)return 0;if(t<=36000)return Math.min(300,.06*(t-20000));if(t<=48000)return Math.min(450,300+.06*(t-36000));if(t<=72000)return Math.min(600,450+.25*(t-48000));if(t<=200000)return Math.min(750,600+.25*(t-72000));return Math.min(900,750+.25*(t-200000))}
function run(){const g=Math.max(0,+$('cGross').value||0),pv=$('cProv').value,qc=pv==='QC',rr=Math.min(g,Math.max(0,+$('cRrsp').value||0));
const rate=qc?.063:.0595,br=qc?.053:.0495,pe=Math.max(0,Math.min(g,74600)-3500),c1=pe*rate,cb=pe*br,c2=Math.max(0,Math.min(g,85000)-74600)*.04;
const ei=Math.min(g,68900)*(qc?.013:.0163),qp=qc?Math.min(g,103000)*.0043:0,ti=Math.max(0,g-rr-(c1-cb)-c2);
const bpa=16452-1623*Math.min(1,Math.max(0,(ti-181440)/(258482-181440)));let fed=Math.max(0,BT(ti,D.F)-.14*(bpa+cb+ei+qp+Math.min(1501,g)));if(qc)fed*=.835;
const p=D.P[pv],pc=qc?p[3]*p[2]:p[3]*(p[2]+cb+ei+(pv==='YT'?Math.min(1501,g):0));let pt=Math.max(0,BT(ti,p[1])-pc);
let extra='';if(pv==='ON'){const s=.2*Math.max(0,pt-5818)+.36*Math.max(0,pt-7446),h=ohp(ti);pt+=s+h;extra=' Includes Ontario surtax '+fmt(s)+' and Ontario Health Premium '+fmt(h)+'.'}
const rows=[['Federal tax'+(qc?' (after 16.5% Quebec abatement)':''),fed,1],[p[0]+' tax',pt,1],[qc?'QPP':'CPP',c1+c2,0],[qc?'EI + QPIP':'EI',ei+qp,0]];if(rr>0)rows.push(['RRSP',rr,0]);
const net=g-rows.reduce((a,r)=>a+r[1],0);renderRes($('cResult'),g,rows,net,fmt,$('per').value);
$('cResult').insertAdjacentHTML('beforeend','<p class="tp-note">Taxable income '+fmt(ti)+'.'+extra+'</p>')}
document.addEventListener('DOMContentLoaded',()=>{['cGross','cProv','cRrsp','per'].forEach(id=>$(id).addEventListener('input',run));
document.querySelectorAll('[data-action="ca-pay"]').forEach(b=>b.addEventListener('click',run));run()})})();</script>""".replace('__D__', data)

on75 = calc_py(75000, 'ON'); n75 = 75000 - sum(on75.values())
script = script.replace('__D__', data)
body = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>How much tax do you pay in Canada in 2026?</h2>
<p class="tp-answer">Canadians pay <strong>federal tax</strong> (14% to 33%), <strong>provincial or territorial tax</strong> (4% to 25.75%), <strong>CPP</strong> (5.95% of earnings between $3,500 and $74,600, plus 4% up to $85,000) and <strong>EI</strong> (1.63% up to $68,900).
On a $75,000 salary in Ontario you take home about <strong>{m(n75)}</strong> a year, or {m(n75/12)} a month.</p>
<p>2026 is the first full year at the new 14% lowest federal rate, cut from 15% on July 1, 2025.</p></header>

<section><h2>Take-home pay examples for 2026</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Salary</th><th>Province</th><th class="n">Federal tax</th><th class="n">Provincial tax</th><th class="n">CPP/QPP + EI</th><th class="n">Take-home</th></tr></thead><tbody>{ex_html}</tbody></table></div>
<p class="tp-note">Basic personal amounts, CPP/EI and Canada employment credits only. No RRSP.</p></section>

<section><h2>2026 federal tax brackets</h2>
<table class="tp-table"><tbody><tr><td class="n">14%</td><td>Up to $58,523</td></tr><tr><td class="n">20.5%</td><td>$58,523 – $117,045</td></tr><tr><td class="n">26%</td><td>$117,045 – $181,440</td></tr>
<tr><td class="n">29%</td><td>$181,440 – $258,482</td></tr><tr><td class="n">33%</td><td>Over $258,482</td></tr></tbody></table>
<p>The federal basic personal amount is <strong>$16,452</strong>, reduced gradually to $14,829 for taxable income between $181,440 and $258,482. Non-refundable credits are worth 14% of the amount.</p></section>

<section><h2>Provincial and territorial tax for 2026</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Province / territory</th><th class="n">Lowest rate</th><th class="n">Top rate</th><th class="n">Basic personal amount</th></tr></thead><tbody>{prov_rows}</tbody></table></div>
<p><strong>Ontario</strong> also charges a surtax of 20% of provincial tax above $5,818 and a further 36% above $7,446, plus the Ontario Health Premium of up to $900.
<strong>Quebec</strong> residents file a separate provincial return, pay QPP (6.3%) instead of CPP, a lower EI rate (1.30%) plus QPIP (0.43%), and get a 16.5% reduction of federal tax (the Quebec abatement).</p></section>

<section><h2>CPP and EI in 2026</h2>
<div class="tp-scroll"><table class="tp-table"><tbody>
<tr><td>CPP (first tier)</td><td>5.95% of earnings from $3,500 to $74,600</td><td class="n">Max $4,230.45</td></tr>
<tr><td>CPP2 (second tier)</td><td>4% of earnings from $74,600 to $85,000</td><td class="n">Max $416</td></tr>
<tr><td>QPP (Quebec)</td><td>6.3% of earnings from $3,500 to $74,600, plus QPP2 4%</td><td class="n">Max $4,479.30 + $416</td></tr>
<tr><td>EI</td><td>1.63% of earnings up to $68,900 (1.30% in Quebec)</td><td class="n">Max $1,123.07</td></tr>
<tr><td>QPIP (Quebec)</td><td>0.43% of earnings</td><td class="n"></td></tr></tbody></table></div></section>

<section><h2>How the calculator works</h2>
<p>Taxable income is salary minus RRSP contributions and the deductible enhanced part of CPP/QPP (the 1% first additional contribution and all of CPP2).
Federal and provincial tax are applied to taxable income, then reduced by non-refundable credits for the basic personal amount, base CPP, EI and (federally) the $1,501 Canada employment amount.
Not included: other credits and deductions (spousal, dependants, tuition, medical, union dues), the Quebec deduction for workers, low-income tax reductions in some provinces, and benefits such as the GST/HST credit or Canada Child Benefit.</p>
<p>Sources: <a href="https://www.canada.ca/en/revenue-agency/services/tax/individuals/tax-rates-brackets/current-year.html" rel="noopener" target="_blank">CRA tax rates and income brackets 2026</a>,
<a href="https://www.taxtips.ca/nrcredits/tax-credits-2026.htm" rel="noopener" target="_blank">TaxTips.ca 2026 personal tax credits</a>,
<a href="https://www.taxtips.ca/cpp-qpp-and-ei/cpp-qpp-contribution-rates.htm" rel="noopener" target="_blank">CPP and QPP 2026 contribution rates</a> and
<a href="https://www.revenuquebec.ca/en/" rel="noopener" target="_blank">Revenu Québec</a>.</p></section>
{related('canada-take-home-pay-calculator', [('/tools/salary-to-hourly-calculator', 'Salary to hourly'), ('/tools/pay-period-converter', 'Pay period converter')])}"""

on50 = calc_py(50000, 'ON'); on100 = calc_py(100000, 'ON')
faqs = [
    ("How much is $75,000 after tax in Ontario?", f"About {m(n75)} a year or {m(n75/12)} a month in 2026, after {m(on75['fed'])} federal tax, {m(on75['prov'])} Ontario tax and health premium, and {m(on75['cpp']+on75['ei'])} CPP and EI."),
    ("How much is $50,000 after tax in Ontario?", f"About {m(50000-sum(on50.values()))} a year or {m((50000-sum(on50.values()))/12)} a month."),
    ("How much is $100,000 after tax in Ontario?", f"About {m(100000-sum(on100.values()))} a year or {m((100000-sum(on100.values()))/12)} a month."),
    ("What are the 2026 federal tax brackets in Canada?", "14% up to $58,523, 20.5% to $117,045, 26% to $181,440, 29% to $258,482 and 33% above."),
    ("What is the basic personal amount for 2026?", "$16,452 federally for most people, reducing to $14,829 at higher incomes. Each province has its own amount, from $11,188 in Newfoundland and Labrador to $22,769 in Alberta."),
    ("What are the CPP and EI rates for 2026?", "CPP is 5.95% of earnings between $3,500 and $74,600 (maximum $4,230.45), plus CPP2 at 4% up to $85,000 (maximum $416). EI is 1.63% of earnings up to $68,900 (maximum $1,123.07)."),
    ("Which province has the lowest income tax?", "For most incomes, Alberta, Nunavut and the Northwest Territories have the lowest combined tax, while Quebec and the Atlantic provinces are generally highest."),
    ("Does an RRSP contribution reduce my tax?", "Yes. RRSP contributions are deducted from taxable income, so they save tax at your marginal rate. They do not reduce CPP or EI."),
]

page('canada-take-home-pay-calculator', 'Canada Take-Home Pay Calculator 2026: Salary After Tax by Province | ToolPinch',
     'Calculate 2026 take-home pay in every Canadian province and territory after federal tax, provincial tax, CPP and EI, with the new 14% federal rate.',
     'Canada Take-Home Pay Calculator 2026', 'Updated for 2026 tax year',
     'See your salary after federal and provincial income tax, CPP or QPP, and EI, for every province and territory.',
     ['CRA 2026 brackets', 'All 13 provinces and territories', 'No signup'], calc, body, faqs, script)
