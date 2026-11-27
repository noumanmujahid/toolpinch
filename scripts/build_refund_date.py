"""Build /tools/tax-refund-schedule-2027 (refund date estimator for 2026 returns filed in 2027).
Run from repo root: PYTHONPATH=scripts python3 scripts/build_refund_date.py
IRS facts used: most refunds issued within 21 days; Where's My Refund ~24 hours after e-file, 4 weeks after a paper return;
by law EITC/ACTC refunds can't be issued before mid-February (IRS 2026 target for early e-filers with direct deposit: March 2);
2026 season opened Jan 26, 2026; 2027 opening not yet announced (estimate: Monday, Jan 25, 2027); deadline Thursday, April 15, 2027;
paper refund checks are being phased out. Paper-return and paper-check timings are labelled as estimates."""
import json
from fed_dates import D, T
from tax_common import page

OPEN = D(2027, 1, 25)       # estimate, update when the IRS announces
EITC = D(2027, 3, 2)        # estimate based on the IRS 2026 target (March 2)
fs = lambda d: f"{d.strftime('%a')}, {d.strftime('%b')} {d.day}"


def est(filed, efile=True, dd=True, eitc=False):
    start = max(filed, OPEN)
    if efile:
        lo, hi = start + T(7), start + T(21)
    else:
        lo, hi = start + T(42), start + T(56)
    if eitc:
        lo, hi = max(lo, EITC), max(hi, EITC + T(0 if efile else 21))
    if not dd:
        lo, hi = lo + T(5), hi + T(10)
    return lo, hi


assert est(D(2027, 2, 1)) == (D(2027, 2, 8), D(2027, 2, 22))
assert est(D(2027, 1, 20))[1] == D(2027, 2, 15)
assert est(D(2027, 2, 1), eitc=True) == (D(2027, 3, 2), D(2027, 3, 2))
chart = ''
d = OPEN
while d <= D(2027, 4, 15):
    a = est(d); b = est(d, eitc=True); c = est(d, efile=False)
    chart += f'<tr><td>{fs(d)}</td><td>{fs(a[0])} – {fs(a[1])}</td><td>{fs(b[1]) if b[1] > a[1] else "Same"}</td><td>{fs(c[0])} – {fs(c[1])}</td></tr>'
    d += T(7)
d = D(2027, 4, 15); a = est(d); c = est(d, efile=False)
chart += f'<tr><td>{fs(d)} (deadline)</td><td>{fs(a[0])} – {fs(a[1])}</td><td>Same</td><td>{fs(c[0])} – {fs(c[1])}</td></tr>'
data = json.dumps({'open': OPEN.isoformat(), 'eitc': EITC.isoformat()})

calc = """<div class="mc-calculator"><h2>When will I get my refund?</h2>
<label class="mc-field"><span>Date you file (or plan to file)</span><input id="rdD" type="date" min="2027-01-01" max="2027-10-15" value="2027-02-01"></label>
<label class="mc-field"><span>How you file</span><select id="rdM"><option value="e">E-file</option><option value="p">Paper return by mail</option></select></label>
<label class="mc-field"><span>How you get your refund</span><select id="rdP"><option value="dd">Direct deposit</option><option value="ck">Paper check</option></select></label>
<label class="mc-field"><span>Claiming the Earned Income Credit or Additional Child Tax Credit?</span><select id="rdE"><option value="0">No</option><option value="1">Yes</option></select></label>
<label class="mc-field tp-wide"><span>IRS opening day (estimate until the IRS announces it)</span><input id="rdO" type="date" value="2027-01-25"></label>
<button class="mc-button" data-action="rd">Estimate</button>
<div class="mc-result tp-res" id="rdR" aria-live="polite">Pick your filing date.</div></div>"""

script = """<script>(()=>{const C=__D__,$=id=>document.getElementById(id);const p=s=>{const[a,b,c]=s.split('-').map(Number);return new Date(a,b-1,c,12)};
const add=(d,n)=>{const x=new Date(d);x.setDate(x.getDate()+n);return x},mx=(a,b)=>a>b?a:b,fm=d=>d.toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric',year:'numeric'});
function run(){const v=$('rdD').value;if(!v)return;const f=p(v),op=p($('rdO').value||C.open),ef=$('rdM').value==='e',dd=$('rdP').value==='dd',ei=$('rdE').value==='1',E=p(C.eitc);
const st=mx(f,op);let lo=ef?add(st,7):add(st,42),hi=ef?add(st,21):add(st,56);if(ei){lo=mx(lo,E);hi=mx(hi,ef?E:add(E,21))}if(!dd){lo=add(lo,5);hi=add(hi,10)}
let t='<p class="tp-big"><strong>'+fm(lo)+(+lo===+hi?'':' – '+fm(hi))+'</strong></p><p>Estimated date your refund '+(dd?'reaches your bank account':'arrives by mail')+'.</p><ul>';
if(f<op)t+='<li>The IRS doesn\\'t process returns before opening day, so the clock starts '+fm(op)+'.</li>';
t+=ef?'<li>Most e-filed refunds are issued within 21 days. Where\\'s My Refund shows your status about 24 hours after the IRS accepts your return.</li>':'<li>Paper returns take much longer: Where\\'s My Refund can\\'t show anything until about 4 weeks after you mail it.</li>';
if(ei)t+='<li>By law the IRS can\\'t send refunds that include the Earned Income Credit or Additional Child Tax Credit before mid-February. In 2026 the IRS expected most of them to arrive by March 2.</li>';
if(!dd)t+='<li>The IRS is phasing out paper refund checks; direct deposit is faster.</li>';
t+='</ul><p class="tp-note">An estimate, not an IRS promise. Errors, identity checks or extra review can add weeks.</p>';$('rdR').innerHTML=t}
document.addEventListener('DOMContentLoaded',()=>{['rdD','rdM','rdP','rdE','rdO'].forEach(i=>$(i).addEventListener('input',run));document.querySelectorAll('[data-action="rd"]').forEach(b=>b.addEventListener('click',run));run()})})();</script>"""
script = script.replace('__D__', data)

body = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>When will I get my tax refund in 2027?</h2>
<p class="tp-answer">If you <strong>e-file and choose direct deposit</strong>, most refunds arrive <strong>within 21 days</strong> of the IRS accepting your return. File on February 1, 2027 and you can expect it by about February 22.
If you claim the <strong>Earned Income Credit or Additional Child Tax Credit</strong>, the IRS can't send your refund before mid-February; in 2026 most of those refunds arrived by March 2.</p>
<p>The IRS hasn't announced the first day of the 2027 filing season yet. It was January 26 in 2026, so this page assumes <strong>Monday, January 25, 2027</strong>; change it in the calculator once the date is official. The filing deadline is <strong>Thursday, April 15, 2027</strong>.</p></header>

<section><h2>2027 tax refund schedule chart</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Return accepted</th><th>E-file + direct deposit</th><th>With EITC or ACTC</th><th>Paper return (estimate)</th></tr></thead><tbody>{chart}</tbody></table></div>
<p class="tp-note">E-file range is 7 to 21 days after acceptance. Paper return range is an estimate of 6 to 8 weeks. Returns filed before opening day are processed from opening day.</p></section>

<section><h2>How to get your refund faster</h2>
<ul><li><strong>E-file</strong> instead of mailing a paper return.</li>
<li><strong>Choose direct deposit.</strong> The IRS is phasing out paper refund checks.</li>
<li><strong>Double-check</strong> your Social Security number, bank routing and account numbers, and income from every W-2 and 1099. Mismatches are the most common reason a refund is held.</li>
<li><strong>Respond quickly</strong> if the IRS asks you to verify your identity.</li></ul>
<p>Track your refund with the IRS <a href="https://www.irs.gov/refunds" rel="noopener" target="_blank">Where's My Refund</a> tool, which updates once a day, usually overnight, and moves through three stages: return received, refund approved and refund sent. To estimate how much you'll get back, use the <a href="/tools/tax-refund-estimator">tax refund estimator</a>.</p>
<p>Sources: <a href="https://www.irs.gov/newsroom/irs-announces-first-day-of-2026-filing-season-online-tools-and-resources-help-with-tax-filing" rel="noopener" target="_blank">IRS 2026 filing season announcement</a>, <a href="https://www.irs.gov/credits-deductions/individuals/earned-income-tax-credit/when-to-expect-your-refund-if-you-claimed-the-earned-income-tax-credit-or-additional-child-tax-credit" rel="noopener" target="_blank">IRS: when to expect an EITC or ACTC refund</a>, <a href="https://www.irs.gov/newsroom/check-the-status-of-a-refund-in-just-a-few-clicks-using-the-wheres-my-refund-tool" rel="noopener" target="_blank">IRS: Where's My Refund</a>.</p></section>
<nav class="mc-related-links" aria-label="Related tools"><h2>Related calculators</h2><a href="/tools/tax-refund-estimator">Tax refund estimator</a><a href="/tools/2027-paycheck-calculator">2027 paycheck change</a><a href="/tools/2027-tax-brackets">2027 tax brackets</a><a href="/tools/quarterly-estimated-tax-calculator">Quarterly estimated tax</a><a href="/tools/us-paycheck-calculator">US paycheck calculator</a></nav>"""

faqs = [("How long does it take to get a tax refund in 2027?", "Most refunds for e-filed returns are issued within 21 days of the IRS accepting the return. Paper returns take much longer, and refunds with the Earned Income Credit or Additional Child Tax Credit can't be sent before mid-February."),
        ("When does the IRS start accepting tax returns in 2027?", "The IRS hasn't announced it yet; it usually opens in late January. The 2026 season opened January 26, 2026."),
        ("When will I get my refund if I claim the child tax credit?", "If you claim the Additional Child Tax Credit (the refundable part) or the Earned Income Credit, the IRS can't issue your refund before mid-February. In 2026 most early e-filers with direct deposit received these refunds by March 2."),
        ("How often does Where's My Refund update?", "Once a day, usually overnight. It shows status about 24 hours after an e-filed return is accepted, or about 4 weeks after a paper return is mailed."),
        ("How long does an amended return refund take?", "Amended returns (Form 1040-X) are processed separately and typically take 8 to 12 weeks, sometimes up to 16 weeks."),
        ("What is the tax filing deadline in 2027?", "Thursday, April 15, 2027, for 2026 federal returns. An extension moves the filing deadline to October 15, 2027, but not the deadline to pay.")]

page('tax-refund-schedule-2027', '2027 Tax Refund Schedule: When Will I Get Mine? | ToolPinch',
     'Estimate when your 2027 tax refund will arrive: e-file vs paper, direct deposit, the EITC and child tax credit hold, plus a weekly refund schedule chart.',
     'When Will I Get My Tax Refund?', '2027 refund schedule',
     'Pick the date you file and see when your refund should arrive, based on IRS processing times.',
     ['IRS timelines', 'EITC/ACTC rules', 'No signup'], calc, body, faqs, script)
