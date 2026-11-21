"""Build /tools/quarterly-estimated-tax-calculator (US federal, tax year 2026).
Run from repo root: PYTHONPATH=scripts python3 scripts/build_estimated.py
Sources: Rev. Proc. 2025-32 (2026 brackets, standard deduction, QBI thresholds), SSA 2026 wage base $184,500,
IRS Form 1040-ES and Publication 505 (safe harbor, due dates), Schedule SE (92.35%, 15.3%)."""
import json
import math
from tax_common import page, related, BT_JS

F = lambda b: [[t, r / 100] for t, r in b]
Y26 = {'single': (F([[0,10],[12400,12],[50400,22],[105700,24],[201775,32],[256225,35],[640600,37]]), 16100),
       'married': (F([[0,10],[24800,12],[100800,22],[211400,24],[403550,32],[512450,35],[768700,37]]), 32200),
       'hoh': (F([[0,10],[17700,12],[67450,22],[105700,24],[201750,32],[256200,35],[640600,37]]), 24150)}
K = {'wb': 184500, 'qbi_t': {'single': 201750, 'hoh': 201750, 'married': 403500}, 'qbi_r': {'single': 75000, 'hoh': 75000, 'married': 150000},
     'am': {'single': 200000, 'hoh': 200000, 'married': 250000}, 'ctc': 2200}


def bt(x, b):
    t = 0
    for i, (lo, r) in enumerate(b):
        hi = b[i + 1][0] if i + 1 < len(b) else 1e18
        if x > lo:
            t += (min(x, hi) - lo) * r
    return t


def est(st, profit, wages=0, other=0, withheld=0, paid=0, kids=0, prior=None, high_prior=False):
    j = st == 'married'
    nese = max(0, profit) * 0.9235
    ss_room = max(0, K['wb'] - wages)
    se_ss = 0.124 * min(nese, ss_room)
    se_med = 0.029 * nese
    se = se_ss + se_med if nese >= 400 else 0
    addl = 0.009 * max(0, nese - max(0, K['am'][st] - wages)) if nese >= 400 else 0
    half = se / 2
    agi = wages + profit + other - half
    b, sd = Y26[st]
    ti0 = max(0, agi - sd)
    qbi_base = max(0, profit - half)
    qbi = min(0.2 * qbi_base, 0.2 * ti0)
    over = ti0 - K['qbi_t'][st]
    if over > 0:
        qbi *= max(0, 1 - over / K['qbi_r'][st])
    ti = max(0, ti0 - qbi)
    inc = bt(ti, b)
    ctc = max(0, kids * K['ctc'] - 50 * math.ceil(max(0, agi - (400000 if j else 200000)) / 1000))
    inc_after = max(0, inc - ctc)
    total = inc_after + se + addl
    owed = total - withheld
    req90 = 0.9 * total
    req = min(req90, prior * (1.1 if high_prior else 1.0)) if prior is not None else req90
    left = max(0, req - withheld - paid)
    return dict(nese=nese, se=se, addl=addl, half=half, agi=agi, qbi=qbi, ti=ti, inc=inc, ctc=ctc, total=total,
                owed=owed, req=req, left=left, still=max(0, total - withheld - paid))


# Hand check: single, $60,000 profit. NESE 55,410; SE tax 0.153*55,410 = 8,477.73; half 4,238.865.
# AGI 55,761.135; before QBI 39,661.135; QBI = min(0.2*55,761.135, 0.2*39,661.135) = 7,932.227; taxable 31,728.908
# tax 1,240 + 0.12*19,328.908 = 3,559.469; total 12,037.20
r = est('single', 60000)
assert abs(r['se'] - 8477.73) < 0.01 and abs(r['total'] - 12037.20) < 0.01, r
# Married, $150,000 profit + $50,000 wages: SS room 134,500 > NESE 138,525? no: SS on 134,500
r = est('married', 150000, wages=50000)
assert abs(r['se'] - (0.124 * 134500 + 0.029 * 138525)) < 0.01, r
# Safe harbor: prior-year tax 8,000 caps the requirement below 90% of 12,037
r = est('single', 60000, prior=8000)
assert abs(r['req'] - 8000) < 0.01
# Under $400 of net SE earnings: no SE tax
assert est('single', 400)['se'] == 0
m = lambda x: f"${x:,.0f}"
EX = [('Single freelancer', 'single', 40000, 0), ('Single freelancer', 'single', 60000, 0), ('Single freelancer', 'single', 100000, 0),
      ('Single, $50k job + $20k side gig', 'single', 20000, 50000), ('Married, one self-employed spouse', 'married', 90000, 0),
      ('Married, $80k job + $40k side business', 'married', 40000, 80000)]
ex_html = ''
for lab, st, p, w in EX:
    r = est(st, p, wages=w)
    # withholding on the job is assumed to cover the wage tax: show the extra tax caused by self-employment income
    base = est(st, 0, wages=w)['total'] if w else 0
    extra = r['total'] - base
    ex_html += f'<tr><td>{lab}</td><td class="n">{m(p)}</td><td class="n">{m(r["se"])}</td><td class="n">{m(extra)}</td><td class="n"><b>{m(extra/4)}</b></td></tr>'
    print(lab, p, w, round(r['se']), round(extra), round(extra / 4))
data = json.dumps({'Y': Y26, 'K': K})

calc = """<div class="mc-calculator"><h2>Your 2026 estimated tax</h2>
<label class="mc-field"><span>Filing status</span><select id="eSt"><option value="single">Single</option><option value="married">Married filing jointly</option><option value="hoh">Head of household</option></select></label>
<label class="mc-field"><span>Self-employment profit for 2026 ($)</span><input id="eP" type="number" min="0" step="100" value="60000"></label>
<label class="mc-field"><span>W-2 wages for 2026 ($)</span><input id="eW" type="number" min="0" step="100" value="0"></label>
<label class="mc-field"><span>Federal tax withheld from wages ($)</span><input id="eH" type="number" min="0" step="10" value="0"></label>
<label class="mc-field"><span>Other taxable income ($)</span><input id="eO" type="number" min="0" step="100" value="0"></label>
<label class="mc-field"><span>Estimated payments already made for 2026 ($)</span><input id="eA" type="number" min="0" step="10" value="0"></label>
<label class="mc-field"><span>Children under 17</span><input id="eK" type="number" min="0" max="12" step="1" value="0"></label>
<label class="mc-field"><span>Total tax on your 2025 return (optional, Form 1040 line 24, $)</span><input id="eY" type="number" min="0" step="10" placeholder="Leave blank if unknown"></label>
<label class="mc-field"><span>2025 adjusted gross income over $150,000?</span><select id="eHi"><option value="0">No</option><option value="1">Yes ($75,000 if married filing separately)</option></select></label>
<button class="mc-button" data-action="est">Calculate</button>
<div class="mc-result tp-res" id="eR" aria-live="polite">Enter your income.</div></div>"""

script = """<script>(()=>{const D=__D__,$=id=>document.getElementById(id),v=id=>Math.max(0,+$(id).value||0);""" + BT_JS + """
const f=x=>x.toLocaleString('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0});
function run(){const st=$('eSt').value,j=st==='married',p=v('eP'),w=v('eW'),wh=v('eH'),o=v('eO'),paid=v('eA'),k=Math.round(v('eK')),K=D.K;
const prRaw=$('eY').value.trim(),prior=prRaw===''?null:Math.max(0,+prRaw||0),hi=$('eHi').value==='1';
const nese=p*.9235,room=Math.max(0,K.wb-w),se=nese>=400?.124*Math.min(nese,room)+.029*nese:0,addl=nese>=400?.009*Math.max(0,nese-Math.max(0,K.am[st]-w)):0,half=se/2;
const agi=w+p+o-half,y=D.Y[st],ti0=Math.max(0,agi-y[1]);let qbi=Math.min(.2*Math.max(0,p-half),.2*ti0);const over=ti0-K.qbi_t[st];if(over>0)qbi*=Math.max(0,1-over/K.qbi_r[st]);
const ti=Math.max(0,ti0-qbi),inc=BT(ti,y[0]),ctc=Math.max(0,k*K.ctc-50*Math.ceil(Math.max(0,agi-(j?400000:200000))/1000)),incA=Math.max(0,inc-ctc),tot=incA+se+addl;
const req90=.9*tot,req=prior===null?req90:Math.min(req90,prior*(hi?1.1:1)),left=Math.max(0,req-wh-paid),still=Math.max(0,tot-wh-paid);
let t='<p class="tp-big"><strong>'+f(left)+'</strong> to pay by January 15, 2027</p>';
t+='<div class="tp-scroll"><table class="tp-table"><tbody><tr><td>Self-employment tax (Social Security and Medicare)</td><td class="n">'+f(se)+'</td></tr>'+(addl?'<tr><td>Additional Medicare tax (0.9%)</td><td class="n">'+f(addl)+'</td></tr>':'')+
'<tr><td>Federal income tax'+(ctc?' after child tax credit':'')+'</td><td class="n">'+f(incA)+'</td></tr><tr class="tot"><td>Total 2026 federal tax</td><td class="n">'+f(tot)+'</td></tr>'+
(wh?'<tr><td>Withheld from wages</td><td class="n">−'+f(wh)+'</td></tr>':'')+(paid?'<tr><td>Estimated payments already made</td><td class="n">−'+f(paid)+'</td></tr>':'')+
'<tr><td>Still owed for 2026 if nothing else is paid</td><td class="n">'+f(still)+'</td></tr></tbody></table></div>';
t+='<p>To avoid an underpayment penalty you need to have paid <b>'+f(req)+'</b> in total ('+(prior!==null&&req<req90?(hi?'110':'100')+'% of your 2025 tax, the safe harbor':'90% of your 2026 tax')+'). '+(left>0?'That leaves '+f(left)+' for the January 15 payment.':'Your withholding and payments already cover it.')+'</p>';
if(left>0&&paid===0)t+='<p>If you made no estimated payments earlier in 2026, paying in January stops the penalty growing but a small charge may still apply for the April, June and September installments.</p>';if(tot-wh<1000)t+='<p>You expect to owe less than $1,000 after withholding, so no estimated tax penalty applies.</p>';
t+='<p class="tp-note">Deductions used: standard deduction '+f(y[1])+', half of self-employment tax '+f(half)+', qualified business income deduction '+f(qbi)+'. Taxable income '+f(ti)+'. Starting 2027 fresh with similar income? That is about <b>'+f(Math.max(0,tot-wh)/4)+'</b> a quarter.</p>';
$('eR').innerHTML=t}
document.addEventListener('DOMContentLoaded',()=>{['eSt','eP','eW','eH','eO','eA','eK','eY','eHi'].forEach(i=>$(i).addEventListener('input',run));document.querySelectorAll('[data-action="est"]').forEach(b=>b.addEventListener('click',run));run()})})();</script>"""
script = script.replace('__D__', data)

DUE = [('1st payment', 'Jan 1 to Mar 31, 2026', 'April 15, 2026'), ('2nd payment', 'Apr 1 to May 31, 2026', 'June 15, 2026'),
       ('3rd payment', 'Jun 1 to Aug 31, 2026', 'September 15, 2026'), ('4th payment', 'Sep 1 to Dec 31, 2026', '<b>January 15, 2027</b>')]
due_html = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in DUE)

body = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>How much estimated tax should you pay?</h2>
<p class="tp-answer">If you are self-employed or have income with no tax withheld, the IRS expects you to pay tax during the year in four installments. The last 2026 payment is due <strong>January 15, 2027</strong>.
To avoid a penalty, pay at least <strong>90% of your 2026 tax</strong> or <strong>100% of your 2025 tax</strong> (110% if your 2025 adjusted gross income was over $150,000), whichever is smaller.</p>
<p>A single freelancer with $60,000 of profit and no other income owes about <strong>$12,037</strong> in 2026 federal tax: $8,478 of self-employment tax and $3,559 of income tax. That is roughly <strong>$3,009 a quarter</strong>.</p></header>

<section><h2>2026 estimated tax due dates</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Payment</th><th>Income earned</th><th>Due date</th></tr></thead><tbody>{due_html}</tbody></table></div>
<p>You can skip the January 15 payment if you file your 2026 return and pay the full balance by <strong>February 1, 2027</strong> (January 31 falls on a Sunday). Farmers and fishermen who file and pay by March 1 don't need to make estimated payments.</p></section>

<section><h2>Estimated tax examples for 2026</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Situation</th><th class="n">Self-employment profit</th><th class="n">Self-employment tax</th><th class="n">Extra federal tax</th><th class="n">Per quarter</th></tr></thead><tbody>{ex_html}</tbody></table></div>
<p class="tp-note">Extra federal tax is the tax caused by the self-employment income, assuming withholding from any job already covers the tax on wages. Standard deduction and the qualified business income deduction are included; state tax is not.</p></section>

<section><h2>How the calculation works</h2>
<ul><li><strong>Self-employment tax:</strong> 15.3% of 92.35% of your profit: 12.4% for Social Security on earnings up to the 2026 wage base of $184,500 (reduced by any W-2 wages), plus 2.9% for Medicare with no cap. No self-employment tax is due if net earnings are under $400.</li>
<li><strong>Additional Medicare tax:</strong> 0.9% on wages and self-employment earnings above $200,000 ($250,000 married filing jointly).</li>
<li><strong>Income tax:</strong> half of your self-employment tax is deducted from income, then the 2026 standard deduction ($16,100 single, $32,200 married, $24,150 head of household) and the 20% qualified business income deduction. The rest is taxed at the 2026 rates of 10% to 37%.</li>
<li><strong>Qualified business income deduction:</strong> 20% of business profit (after half of self-employment tax), limited to 20% of taxable income. Above $201,750 of taxable income ($403,500 married) the calculator phases it out over the next $75,000 ($150,000), which is how it works for service businesses and businesses with no employees or property.</li></ul></section>

<section><h2>How to pay estimated tax</h2>
<p>The quickest options are <a href="https://www.irs.gov/payments/direct-pay" rel="noopener" target="_blank">IRS Direct Pay</a> from a bank account, your <a href="https://www.irs.gov/payments/your-online-account" rel="noopener" target="_blank">IRS online account</a>, or EFTPS. Choose "estimated tax" and tax year 2026 for the January 15 payment. You can also mail a Form 1040-ES voucher with a check.
If you have a job as well, you can instead raise your withholding with a new <a href="https://www.irs.gov/forms-pubs/about-form-w-4" rel="noopener" target="_blank">Form W-4</a>; withholding counts as if it were paid evenly through the year.</p>
<p>Most states with an income tax also expect quarterly payments on similar dates. Check your state revenue department.</p>
<p>Sources: <a href="https://www.irs.gov/forms-pubs/about-form-1040-es" rel="noopener" target="_blank">IRS Form 1040-ES</a>, <a href="https://www.irs.gov/publications/p505" rel="noopener" target="_blank">IRS Publication 505</a>, <a href="https://www.irs.gov/pub/irs-drop/rp-25-32.pdf" rel="noopener" target="_blank">Rev. Proc. 2025-32</a> and the <a href="https://www.ssa.gov/oact/cola/cbb.html" rel="noopener" target="_blank">Social Security wage base</a>.</p></section>
{related('quarterly-estimated-tax-calculator')}"""

faqs = [("When is the next estimated tax payment due?", "The fourth 2026 payment is due January 15, 2027. Payments for 2027 income start April 15, 2027."),
        ("Who has to pay quarterly estimated taxes?", "Anyone who expects to owe at least $1,000 in federal tax for the year after withholding and credits, typically freelancers, contractors, gig workers, landlords and people with large investment income."),
        ("How do I avoid the underpayment penalty?", "Pay, through withholding and estimated payments, at least 90% of this year's tax or 100% of last year's tax (110% if last year's adjusted gross income was over $150,000, or $75,000 married filing separately), whichever is less. You also owe no penalty if your balance due after withholding is under $1,000."),
        ("How much should I set aside for taxes as a freelancer?", "For federal tax, many freelancers with $40,000 to $100,000 of profit end up owing roughly 18% to 23% of profit, because self-employment tax adds about 14% on top of income tax. Use the calculator for your own numbers, and add your state tax."),
        ("Can I pay all my estimated tax in January?", "You can, but the IRS can still charge a penalty for the earlier quarters you underpaid, because each installment is due on its own date. Raising W-2 withholding late in the year is different: withholding is treated as paid evenly through the year."),
        ("Does the calculator include state tax?", "No. It estimates federal income tax and self-employment tax only.")]

page('quarterly-estimated-tax-calculator', 'Quarterly Estimated Tax Calculator 2026 | ToolPinch',
     'Work out your quarterly estimated tax for 2026, including self-employment tax and the safe harbor that avoids penalties. Next payment due January 15, 2027.',
     'Quarterly Estimated Tax Calculator', 'Next payment due: Jan 15, 2027',
     'Estimate your 2026 federal income tax and self-employment tax, see what you still owe, and the amount that keeps you clear of the underpayment penalty.',
     ['Self-employment tax included', 'Safe harbor check', 'No signup'], calc, body, faqs, script)
