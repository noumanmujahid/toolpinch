"""Build /tools/tax-refund-estimator (US federal, tax year 2026, returns filed in 2027).
Run from repo root: PYTHONPATH=scripts python3 scripts/build_refund.py"""
import json
from tax_common import page, related, BT_JS

F = lambda b: [[t, r / 100] for t, r in b]
Y26 = {'single': (F([[0,10],[12400,12],[50400,22],[105700,24],[201775,32],[256225,35],[640600,37]]), 16100),
       'married': (F([[0,10],[24800,12],[100800,22],[211400,24],[403550,32],[512450,35],[768700,37]]), 32200),
       'hoh': (F([[0,10],[17700,12],[67450,22],[105700,24],[201750,32],[256200,35],[640600,37]]), 24150)}
C = {'ctc': 2200, 'actc': 1700, 'odc': 500, 'addl_m': 1650, 'addl_u': 2050}


def bt(x, b):
    t = 0
    for i, (lo, r) in enumerate(b):
        hi = b[i + 1][0] if i + 1 < len(b) else 1e18
        if x > lo:
            t += (min(x, hi) - lo) * r
    return t


def est(st, wages, other, withheld, kids=0, deps=0, itemized=0, tips=0, ot=0, seniors=0):
    joint = st == 'married'
    agi = wages + other
    b, sd = Y26[st]
    sd += seniors * (C['addl_m'] if joint else C['addl_u'])
    ded = max(sd, itemized)
    ph = max(0, agi - (300000 if joint else 150000)) / 1000 * 100
    tipd = max(0, min(tips, 25000) - ph)
    otd = max(0, min(ot, 25000 if joint else 12500) - ph)
    sen = max(0, seniors * 6000 - .06 * max(0, agi - (150000 if joint else 75000)))
    ti = max(0, agi - ded - tipd - otd - sen)
    tax = bt(ti, b)
    cred = kids * C['ctc'] + deps * C['odc']
    import math
    cred = max(0, cred - 50 * math.ceil(max(0, agi - (400000 if joint else 200000)) / 1000))
    nonref = min(tax, cred)
    child_left = max(0, min(cred, kids * C['ctc']) - nonref)
    actc = min(child_left, kids * C['actc'], .15 * max(0, wages - 2500))
    owed = tax - nonref
    return dict(agi=agi, ded=ded, tipd=tipd, otd=otd, sen=sen, ti=ti, tax=tax, nonref=nonref, actc=actc, owed=owed, refund=withheld + actc - owed)


# hand check: single, $55,000 wages, $5,500 withheld. taxable 38,900: 1,240 + 0.12*26,500 = 4,420. refund 1,080
r = est('single', 55000, 0, 5500)
assert round(r['tax']) == 4420 and round(r['refund']) == 1080, r
# married, 2 kids, $90,000 wages, $6,000 withheld: taxable 57,800: 2,480 + 0.12*33,000 = 6,440; CTC 4,400 -> owed 2,040; refund 3,960
r = est('married', 90000, 0, 6000, kids=2)
assert round(r['owed']) == 2040 and round(r['refund']) == 3960, r
# low income HoH with 2 kids: wages 30,000, withheld 900: taxable 5,850 -> 585 tax; CTC covers it; ACTC min(4400-585, 3400, 0.15*27500=4125)=3400 -> refund 4,300
r = est('hoh', 30000, 0, 900, kids=2)
assert round(r['actc']) == 3400 and round(r['refund']) == 4300, r
m = lambda x: f"${x:,.0f}"
EX = [('Single, no children', 'single', 55000, 5500, 0), ('Single, no children', 'single', 80000, 10000, 0), ('Married, 2 children', 'married', 90000, 6000, 2),
      ('Married, 1 child', 'married', 140000, 15000, 1), ('Head of household, 2 children', 'hoh', 30000, 900, 2), ('Head of household, 1 child', 'hoh', 55000, 3500, 1)]
ex_html = ''
for lab, st, w, wh, k in EX:
    r = est(st, w, 0, wh, kids=k)
    ex_html += f'<tr><td>{lab}</td><td class="n">{m(w)}</td><td class="n">{m(wh)}</td><td class="n">{m(r["owed"]-r["actc"])}</td><td class="n"><b>{("" if r["refund"]>=0 else "−")+m(abs(r["refund"]))}</b></td></tr>'
    print(lab, w, wh, round(r['refund']))
data = json.dumps({'Y': Y26, 'C': C})

calc = """<div class="mc-calculator"><h2>Your 2026 federal refund</h2>
<label class="mc-field"><span>Filing status</span><select id="rSt"><option value="single">Single</option><option value="married">Married filing jointly</option><option value="hoh">Head of household</option></select></label>
<label class="mc-field"><span>Wages for 2026 (W-2 box 1, $)</span><input id="rW" type="number" min="0" step="100" value="55000"></label>
<label class="mc-field"><span>Federal tax withheld (W-2 box 2, $)</span><input id="rH" type="number" min="0" step="10" value="5500"></label>
<label class="mc-field"><span>Other taxable income ($)</span><input id="rO" type="number" min="0" step="100" value="0"></label>
<label class="mc-field"><span>Children under 17</span><input id="rK" type="number" min="0" max="12" step="1" value="0"></label>
<label class="mc-field"><span>Other dependents</span><input id="rD" type="number" min="0" max="12" step="1" value="0"></label>
<label class="mc-field"><span>People on the return aged 65+</span><input id="rS" type="number" min="0" max="2" step="1" value="0"></label>
<label class="mc-field"><span>Qualified tips ($)</span><input id="rT" type="number" min="0" step="100" value="0"></label>
<label class="mc-field"><span>Overtime premium pay (the "half" in time-and-a-half, $)</span><input id="rOT" type="number" min="0" step="100" value="0"></label>
<label class="mc-field"><span>Itemized deductions, if more than standard ($)</span><input id="rI" type="number" min="0" step="100" value="0"></label>
<button class="mc-button" data-action="refund">Estimate refund</button>
<div class="mc-result tp-res" id="rR" aria-live="polite">Enter your W-2 details.</div></div>"""

script = """<script>(()=>{const D=__D__,$=id=>document.getElementById(id),v=id=>Math.max(0,+$(id).value||0);""" + BT_JS + """
const f=x=>x.toLocaleString('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0});
function run(){const st=$('rSt').value,j=st==='married',w=v('rW'),wh=v('rH'),o=v('rO'),k=Math.round(v('rK')),dp=Math.round(v('rD')),s=Math.min(j?2:1,Math.round(v('rS')));
const agi=w+o,y=D.Y[st],sd=y[1]+s*(j?D.C.addl_m:D.C.addl_u),ded=Math.max(sd,v('rI')),ph=Math.max(0,agi-(j?300000:150000))/1000*100;
const tipd=Math.max(0,Math.min(v('rT'),25000)-ph),otd=Math.max(0,Math.min(v('rOT'),j?25000:12500)-ph),sen=Math.max(0,s*6000-.06*Math.max(0,agi-(j?150000:75000)));
const ti=Math.max(0,agi-ded-tipd-otd-sen),tax=BT(ti,y[0]);let cr=k*D.C.ctc+dp*D.C.odc;cr=Math.max(0,cr-50*Math.ceil(Math.max(0,agi-(j?400000:200000))/1000));
const nr=Math.min(tax,cr),left=Math.max(0,Math.min(cr,k*D.C.ctc)-nr),actc=Math.min(left,k*D.C.actc,.15*Math.max(0,w-2500)),owed=tax-nr,ref=wh+actc-owed;
let h='<p class="tp-big">'+(ref>=0?'Estimated refund <strong>'+f(ref)+'</strong>':'Estimated amount owed <strong>'+f(-ref)+'</strong>')+'</p><div class="tp-scroll"><table class="tp-table"><tbody>'+
'<tr><td>Adjusted gross income</td><td class="n">'+f(agi)+'</td></tr><tr><td>'+(ded>sd?'Itemized':'Standard')+' deduction</td><td class="n">−'+f(ded)+'</td></tr>'+
(tipd?'<tr><td>No tax on tips deduction</td><td class="n">−'+f(tipd)+'</td></tr>':'')+(otd?'<tr><td>No tax on overtime deduction</td><td class="n">−'+f(otd)+'</td></tr>':'')+(sen?'<tr><td>Senior deduction</td><td class="n">−'+f(sen)+'</td></tr>':'')+
'<tr><td>Taxable income</td><td class="n">'+f(ti)+'</td></tr><tr><td>Income tax</td><td class="n">'+f(tax)+'</td></tr>'+(nr?'<tr><td>Child and dependent credits</td><td class="n">−'+f(nr)+'</td></tr>':'')+
'<tr><td>Tax after credits</td><td class="n">'+f(owed)+'</td></tr><tr><td>Federal tax withheld</td><td class="n">'+f(wh)+'</td></tr>'+(actc?'<tr><td>Refundable child tax credit</td><td class="n">+'+f(actc)+'</td></tr>':'')+
'<tr class="tot"><td>'+(ref>=0?'Refund':'Amount owed')+'</td><td class="n">'+f(Math.abs(ref))+'</td></tr></tbody></table></div>';
h+='<p class="tp-note">Estimate for the federal return only. Not included: the earned income tax credit, education and other credits, self-employment tax and state tax.</p>';$('rR').innerHTML=h}
document.addEventListener('DOMContentLoaded',()=>{['rSt','rW','rH','rO','rK','rD','rS','rT','rOT','rI'].forEach(i=>$(i).addEventListener('input',run));document.querySelectorAll('[data-action="refund"]').forEach(b=>b.addEventListener('click',run));run()})})();</script>"""
script = script.replace('__D__', data)

body = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>How is a tax refund calculated?</h2>
<p class="tp-answer">Your refund is the federal tax your employer <strong>withheld</strong> during 2026, plus any <strong>refundable credits</strong>, minus the <strong>tax you actually owe</strong> for the year.
A single filer with $55,000 of wages owes $4,420 in 2026 federal income tax after the $16,100 standard deduction. If $5,500 was withheld, the refund is about <strong>$1,080</strong>.</p>
<p>2026 returns are filed in early 2027. The IRS says most refunds for electronically filed returns with direct deposit arrive within 21 days.</p></header>

<section><h2>Example refunds for tax year 2026</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Household</th><th class="n">Wages</th><th class="n">Withheld</th><th class="n">Tax after credits</th><th class="n">Refund</th></tr></thead><tbody>{ex_html}</tbody></table></div>
<p class="tp-note">Standard deduction; child tax credit included; earned income tax credit not included (it would add to the refunds of the lower-income households).</p></section>

<section><h2>What changed for 2026 returns</h2><ul>
<li><strong>Standard deduction:</strong> $16,100 single, $32,200 married filing jointly, $24,150 head of household. People 65 or older add $2,050 (single) or $1,650 each (married).</li>
<li><strong>Child tax credit:</strong> up to $2,200 per child under 17, of which up to $1,700 is refundable for families with earned income above $2,500. It phases out above $200,000 of income ($400,000 joint).</li>
<li><strong>No tax on tips:</strong> up to $25,000 of qualified tips can be deducted, reduced above $150,000 of income ($300,000 joint).</li>
<li><strong>No tax on overtime:</strong> the premium part of overtime pay (the extra half in time-and-a-half) can be deducted, up to $12,500 ($25,000 joint), with the same phase-out.</li>
<li><strong>Senior deduction:</strong> an extra $6,000 per person aged 65 or older, reduced by 6% of income above $75,000 ($150,000 joint).</li></ul>
<p>The tips, overtime and senior deductions apply for 2025 through 2028 and can be claimed whether or not you itemize.</p></section>

<section><h2>Why refunds are bigger or smaller than expected</h2><ul>
<li><strong>Withholding changes:</strong> a new W-4, a second job or a raise changes how much was taken from each paycheck.</li>
<li><strong>Bonuses:</strong> bonuses are usually withheld at a flat 22%. If your bracket is lower, that extra comes back as refund.</li>
<li><strong>Credits:</strong> a child turning 17 during the year loses eligibility for the child tax credit.</li>
<li><strong>Side income:</strong> freelance or gig income has no withholding, so tax on it reduces your refund or creates a balance due.</li></ul>
<p>A big refund means you overpaid during the year. If you would rather have the money in each paycheck, adjust your W-4 with your employer.</p></section>

<section><h2>Sources</h2><p><a href="https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026-including-amendments-from-the-one-big-beautiful-bill" rel="noopener" target="_blank">IRS: tax year 2026 inflation adjustments</a> (Rev. Proc. 2025-32),
<a href="https://www.irs.gov/newsroom/one-big-beautiful-bill-provisions" rel="noopener" target="_blank">IRS: One, Big, Beautiful Bill provisions</a> and
<a href="https://www.irs.gov/refunds" rel="noopener" target="_blank">IRS: refunds</a>. This is an estimate, not tax advice; use IRS Free File or a tax professional to prepare your return.</p></section>
{related('tax-refund-estimator')}"""

faqs = [("How do I estimate my tax refund?", "Work out your tax for the year (income minus deductions, taxed at the 2026 brackets, minus credits), then subtract it from the federal tax withheld shown in box 2 of your W-2. A positive result is a refund."),
        ("When will I get my 2026 tax refund?", "The IRS says most refunds for e-filed returns with direct deposit are issued within 21 days. Refunds that include the earned income tax credit or additional child tax credit cannot be issued before mid-February by law."),
        ("How much is the child tax credit for 2026?", "Up to $2,200 per child under 17. Up to $1,700 per child is refundable, so it can increase your refund even if you owe no tax."),
        ("Is overtime tax-free in 2026?", "Not entirely. You can deduct the premium part of overtime pay (the extra half in time-and-a-half), up to $12,500 or $25,000 for joint filers. Social Security and Medicare tax still apply."),
        ("Are tips tax-free in 2026?", "Up to $25,000 of qualified tips can be deducted from federal income tax for 2025 through 2028, with a phase-out above $150,000 of income ($300,000 joint)."),
        ("Why is my refund smaller this year?", "Common reasons are less withholding after a W-4 change, higher income, a child aging out of the child tax credit, or untaxed side income.")]

page('tax-refund-estimator', 'Tax Refund Estimator 2026: How Much Will I Get Back in 2027? | ToolPinch',
     'Estimate your 2026 federal tax refund from your W-2: 2026 brackets, child tax credit, and the new no-tax-on-tips, overtime and senior deductions.',
     'Tax Refund Estimator 2026', 'Tax year 2026 · Returns filed in 2027',
     'Estimate your federal refund or balance due from your W-2 wages and withholding, including the child tax credit and the new tips, overtime and senior deductions.',
     ['2026 IRS figures', 'Tips and overtime deductions', 'No signup'], calc, body, faqs, script)
