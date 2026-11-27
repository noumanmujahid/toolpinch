"""Build /tools/federal-holidays-2027 and /tools/military-pay-dates-2027.
Run from repo root: PYTHONPATH=scripts python3 scripts/build_holidays_military_2027.py
Rules: 5 U.S.C. 6103 and OPM (Saturday holidays observed Friday, Sunday holidays Monday); Federal Reserve K.8 (banks open the
Friday before a Saturday holiday, closed Monday after a Sunday holiday); DFAS (active duty paid 1st and 15th, prior business day
if weekend/holiday; retired pay due the 1st, last business day of prior month if weekend/holiday; annuitants first business day)."""
import json
from fed_dates import holidays, HOL, D, T
from tax_common import page

f = lambda d: f"{d.strftime('%A')}, {d.strftime('%B')} {d.day}, {d.year}"
fs = lambda d: f"{d.strftime('%a')}, {d.strftime('%b')} {d.day}"
ACTUAL = {"New Year's Day": (1, 1), 'Juneteenth': (6, 19), 'Independence Day': (7, 4), 'Veterans Day': (11, 11), 'Christmas Day': (12, 25)}

# ---------------- Federal holidays 2027 ----------------
H27 = sorted(holidays(2027).items())
assert len(H27) == 12  # includes New Year's Day 2028 observed Dec 31, 2027
rows, fed_notes = '', []
for d, n in H27:
    base = n.replace(' (observed)', '')
    act = ACTUAL.get(base)
    yr = 2028 if '(observed)' in n else 2027
    actual = D(yr, *act) if act else d
    obs = '' if actual == d else f'Falls on {actual.strftime("%A")}, {actual.strftime("%b")} {actual.day}{", 2028" if yr == 2028 else ""}'
    bank = 'Closed'
    if actual.weekday() == 5:
        bank = 'Open (Saturday holiday)'
    rows += f'<tr><td>{n.replace(" (observed)", " 2028 (observed)") if yr == 2028 else n}</td><td>{fs(d)}</td><td>{obs}</td><td>{bank}</td></tr>'
assert HOL[D(2027, 6, 18)] == 'Juneteenth' and HOL[D(2027, 7, 5)] == 'Independence Day' and HOL[D(2027, 12, 24)] == 'Christmas Day'
lw = []
for d, n in H27:
    if d.weekday() in (0, 4):
        a, b = (d - T(3), d) if d.weekday() == 0 else (d, d + T(2))
        lw.append(f'<li><strong>{n.replace(" (observed)", "")}:</strong> {fs(a)} to {fs(b)}{", 2028" if b.year == 2028 else ""}</li>')
ics_h = json.dumps([[d.isoformat(), n] for d, n in H27])

hcalc = """<div class="mc-calculator"><h2>Next federal holiday</h2>
<div class="mc-result tp-res" id="hN" aria-live="polite"></div>
<div class="tp-actions"><button type="button" class="tp-btn" id="hIcs">Add 2027 federal holidays to my calendar (.ics)</button></div></div>"""
hscript = """<script>(()=>{const H=__H__,$=id=>document.getElementById(id);const p=s=>{const[a,b,c]=s.split('-').map(Number);return new Date(a,b-1,c,12)};
const fm=s=>p(s).toLocaleDateString('en-US',{weekday:'long',month:'long',day:'numeric',year:'numeric'});
document.addEventListener('DOMContentLoaded',()=>{const t=new Date(),ti=t.getFullYear()+'-'+String(t.getMonth()+1).padStart(2,'0')+'-'+String(t.getDate()).padStart(2,'0');
const up=H.filter(h=>h[0]>=ti);const nx=up[0]||H[0];const dd=Math.round((p(nx[0])-p(ti))/864e5);
$('hN').innerHTML='<p class="tp-big"><strong>'+nx[1].replace(' (observed)','')+'</strong></p><p>'+fm(nx[0])+(dd>0?' &middot; in '+dd+' days':dd===0?' &middot; today':'')+'</p><p class="tp-note">'+(ti<H[0][0]?'The first federal holiday of 2027.':'Of the 2027 federal holidays, '+up.length+' remain.')+'</p>';
$('hIcs').addEventListener('click',()=>{const st=new Date().toISOString().replace(/[-:]/g,'').replace(/\\.\\d+/,'');const L=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//ToolPinch//Federal Holidays 2027//EN','CALSCALE:GREGORIAN'];
H.forEach((h,i)=>{const d=p(h[0]);d.setDate(d.getDate()+1);const e=d.getFullYear()+String(d.getMonth()+1).padStart(2,'0')+String(d.getDate()).padStart(2,'0');L.push('BEGIN:VEVENT','UID:fedhol'+i+'-2027@toolpinch.com','DTSTAMP:'+st,'DTSTART;VALUE=DATE:'+h[0].replace(/-/g,''),'DTEND;VALUE=DATE:'+e,'SUMMARY:'+h[1]+' (federal holiday)','TRANSP:TRANSPARENT','END:VEVENT')});L.push('END:VCALENDAR');
const u=URL.createObjectURL(new Blob([L.join('\\r\\n')+'\\r\\n'],{type:'text/calendar'}));const a=document.createElement('a');a.href=u;a.download='federal-holidays-2027.ics';document.body.appendChild(a);a.click();a.remove()})})})();</script>""".replace('__H__', ics_h)

hbody = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>How many federal holidays are in 2027?</h2>
<p class="tp-answer">There are <strong>11 federal holidays</strong> in 2027, and federal employees get an extra day off on <strong>Friday, December 31, 2027</strong>, when New Year's Day 2028 (a Saturday) is observed. Three 2027 holidays move because they fall on a weekend: Juneteenth is observed Friday, June 18; Independence Day Monday, July 5; and Christmas Day Friday, December 24.</p></header>

<section><h2>2027 federal holiday calendar</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Holiday</th><th>Day off for federal employees</th><th>Note</th><th>Banks (Federal Reserve)</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="tp-note">When a holiday falls on a Saturday, federal employees get the Friday before off, but Federal Reserve Banks stay open that Friday, so most banks are open on June 18, December 24 and December 31, 2027. When a holiday falls on a Sunday, everyone observes the Monday after.</p></section>

<section><h2>Three-day weekends in 2027</h2>
<ul>{''.join(lw)}</ul>
<p>See <a href="/tools/long-weekends-2027">long weekends 2027</a> for ways to turn these into longer breaks with a day or two of leave.</p></section>

<section><h2>What's closed on federal holidays</h2>
<ul><li><strong>Federal offices and the Postal Service</strong> are closed and there is no regular mail delivery on all 11 holidays.</li>
<li><strong>Banks</strong> generally follow the Federal Reserve schedule above.</li>
<li><strong>Stock markets</strong> follow their own calendar: the NYSE and Nasdaq stay open on Columbus Day and Veterans Day, and close on Good Friday (March 26, 2027), which is not a federal holiday.</li>
<li><strong>Private employers</strong> choose which holidays they observe. Federal law doesn't require private employers to give holidays off or pay a premium; see the <a href="/tools/holiday-pay-calculator">holiday pay calculator</a>.</li></ul>
<p>Sources: <a href="https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/" rel="noopener" target="_blank">OPM federal holidays</a>, <a href="https://www.federalreserve.gov/aboutthefed/k8.htm" rel="noopener" target="_blank">Federal Reserve holidays observed</a>, 5 U.S.C. 6103.</p></section>
<nav class="mc-related-links" aria-label="Related tools"><h2>Related calculators</h2><a href="/tools/long-weekends-2027">Long weekends 2027</a><a href="/tools/federal-pay-periods-2027">NFC pay period calendar 2027</a><a href="/tools/what-pay-period-is-it">What pay period is it?</a><a href="/tools/military-pay-dates-2027">Military pay dates 2027</a><a href="/tools/working-days-2027">Working days in 2027</a></nav>"""

hfaqs = [("What are the federal holidays in 2027?", "New Year's Day (Jan 1), Martin Luther King Jr. Day (Jan 18), Washington's Birthday (Feb 15), Memorial Day (May 31), Juneteenth (observed Fri, Jun 18), Independence Day (observed Mon, Jul 5), Labor Day (Sep 6), Columbus Day (Oct 11), Veterans Day (Thu, Nov 11), Thanksgiving (Nov 25) and Christmas Day (observed Fri, Dec 24). New Year's Day 2028 is observed Fri, Dec 31, 2027."),
         ("Is Christmas Eve 2027 a federal holiday?", "Friday, December 24, 2027 is the observed Christmas Day holiday for federal employees, because December 25 falls on a Saturday."),
         ("Are banks open on December 24, 2027?", "Generally yes. Federal Reserve Banks are open on the Friday before a holiday that falls on a Saturday, so most banks are open on December 24 and December 31, 2027, even though federal offices are closed."),
         ("When is the July 4th holiday in 2027?", "Independence Day falls on Sunday, July 4, 2027, so the federal holiday is Monday, July 5."),
         ("How many paid holidays do federal employees get in 2027?", "Eleven federal holidays fall in calendar 2027, plus Friday, December 31, 2027 for New Year's Day 2028, so federal employees have 12 holiday days off during calendar year 2027."),
         ("Is Good Friday a federal holiday?", "No. Good Friday (March 26, 2027) is not a federal holiday, though the stock markets close.")]

page('federal-holidays-2027', 'Federal Holidays 2027: List and Observed Dates | ToolPinch',
     'All 11 federal holidays in 2027 with observed dates, which days banks are open, three-day weekends, and a free calendar download.',
     'Federal Holidays 2027', '11 holidays + Dec 31 observed',
     'Every 2027 federal holiday with the day federal offices close, bank openings and three-day weekends.',
     ['OPM rules', 'Bank schedule', 'Calendar export'], hcalc, hbody, hfaqs, hscript, crumb=('Work time tools', '/work-time-tools'), back='Work time tools')

# ---------------- Military pay dates 2027 ----------------
bd = lambda d: d.weekday() < 5 and d not in HOL
def prev_bd(d):
    while not bd(d): d -= T(1)
    return d
def next_bd(d):
    while not bd(d): d += T(1)
    return d

active = []
for y, mth in [(2027, m) for m in range(1, 13)] + [(2028, 1)]:
    for day in (1, 15):
        due = D(y, mth, day)
        pay = due if bd(due) else prev_bd(due - T(1))
        if pay.year == 2027 or (pay.year == 2026 and due == D(2027, 1, 1)):
            active.append((due, pay))
assert active[0] == (D(2027, 1, 1), D(2026, 12, 31))
retire = []
for mth in range(1, 13):
    due = D(2027, mth, 1)
    retire.append((due, due if bd(due) else prev_bd(due - T(1)), next_bd(due)))
due28 = D(2028, 1, 1)
retire.append((due28, prev_bd(due28 - T(1)), next_bd(due28)))
assert prev_bd(D(2027, 12, 31)) == D(2027, 12, 30)  # Dec 31, 2027 is a federal holiday

arows = ''.join(f'<tr><td>{fs(due)}{", " + str(due.year) if due.year != 2027 else ""}</td><td><b>{fs(pay)}{", " + str(pay.year) if pay.year != 2027 else ""}</b></td><td>{"" if pay == due else ("Holiday" if due in HOL else "Weekend") + " – paid early"}</td></tr>' for due, pay in active)
rrows = ''.join(f'<tr><td>{due.strftime("%B %Y")}</td><td>{fs(r)}{", " + str(r.year) if r.year != 2027 else ""}</td><td>{fs(a)}{", " + str(a.year) if a.year != 2027 else ""}</td></tr>' for due, r, a in retire)
early = [(d, p) for d, p in active if d != p]
dec26 = [d if bd(d) else prev_bd(d - T(1)) for d in (D(2026, 12, 1), D(2026, 12, 15))]
mdata = json.dumps([x.isoformat() for x in dec26] + [p.isoformat() for d, p in active])  # widget also covers the rest of 2026

mcalc = """<div class="mc-calculator"><h2>Next military payday</h2>
<div class="mc-result tp-res" id="mN" aria-live="polite"></div>
<div class="tp-actions"><button type="button" class="tp-btn" id="mIcs">Add 2027 active duty paydays to my calendar (.ics)</button></div></div>"""
mscript = """<script>(()=>{const P=__P__,$=id=>document.getElementById(id);const p=s=>{const[a,b,c]=s.split('-').map(Number);return new Date(a,b-1,c,12)};
const fm=s=>p(s).toLocaleDateString('en-US',{weekday:'long',month:'long',day:'numeric',year:'numeric'});
document.addEventListener('DOMContentLoaded',()=>{const t=new Date(),ti=t.getFullYear()+'-'+String(t.getMonth()+1).padStart(2,'0')+'-'+String(t.getDate()).padStart(2,'0');
const up=P.filter(x=>x>=ti);let h;if(!up.length){h='<p>All 2027 paydays have passed.</p>'}else{const dd=Math.round((p(up[0])-p(ti))/864e5);
h='<p class="tp-big"><strong>'+fm(up[0])+'</strong></p><p>'+(dd===0?'Today':'In '+dd+' days')+(up[0]==='2026-12-31'?'. This is the January 1, 2027 payday, paid early.':'')+'</p><p class="tp-note">Following paydays: '+up.slice(1,4).map(x=>p(x).toLocaleDateString('en-US',{month:'short',day:'numeric'})).join(', ')+'.</p>'}
$('mN').innerHTML=h;
$('mIcs').addEventListener('click',()=>{const st=new Date().toISOString().replace(/[-:]/g,'').replace(/\\.\\d+/,'');const L=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//ToolPinch//Military Paydays 2027//EN','CALSCALE:GREGORIAN'];
P.filter(x=>x>='2026-12-31').forEach((x,i)=>{const d=p(x);d.setDate(d.getDate()+1);const e=d.getFullYear()+String(d.getMonth()+1).padStart(2,'0')+String(d.getDate()).padStart(2,'0');L.push('BEGIN:VEVENT','UID:milpay'+i+'-2027@toolpinch.com','DTSTAMP:'+st,'DTSTART;VALUE=DATE:'+x.replace(/-/g,''),'DTEND;VALUE=DATE:'+e,'SUMMARY:Military payday','TRANSP:TRANSPARENT','END:VEVENT')});L.push('END:VCALENDAR');
const u=URL.createObjectURL(new Blob([L.join('\\r\\n')+'\\r\\n'],{type:'text/calendar'}));const a=document.createElement('a');a.href=u;a.download='military-paydays-2027.ics';document.body.appendChild(a);a.click();a.remove()})})})();</script>""".replace('__P__', mdata)

mbody = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>When do military members get paid in 2027?</h2>
<p class="tp-answer">Active duty service members are paid on the <strong>1st and 15th</strong> of each month. When either date falls on a weekend or federal holiday, pay arrives the <strong>business day before</strong>. In 2027 that happens {len(early)} times, starting with the January 1 payday, which is paid on <strong>Thursday, December 31, 2026</strong>.</p></header>

<section><h2>2027 active duty pay dates</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Scheduled payday</th><th>Actual pay date</th><th>Why it moves</th></tr></thead><tbody>{arows}</tbody></table></div>
<p class="tp-note">The January 1, 2028 payday moves to Thursday, December 30, 2027, because January 1 is a Saturday and Friday, December 31 is the observed New Year's Day holiday. Many banks and credit unions release military direct deposits a day or two early.</p></section>

<section><h2>2027 military retiree and annuitant pay dates</h2>
<p>DFAS pays retired pay and Survivor Benefit Plan annuities monthly for the previous month. Pay is due on the 1st. If the 1st is a weekend or holiday, <strong>retirees</strong> are paid the last business day of the month before and <strong>annuitants</strong> the first business day after.</p>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Payment due</th><th>Retired pay</th><th>Annuitant pay</th></tr></thead><tbody>{rrows}</tbody></table></div></section>

<section><h2>Good to know</h2>
<ul><li><strong>Reserve and Guard drill pay</strong> is paid after drills are processed, not on a fixed 1st/15th schedule; check your Leave and Earnings Statement in myPay.</li>
<li><strong>2027 military pay raise:</strong> the military raise is set separately from civilian pay in the National Defense Authorization Act and takes effect January 1, 2027. Civilian GS pay is covered on the <a href="/tools/gs-pay-scale-2027">GS pay scale 2027</a> page.</li>
<li><strong>Government shutdowns</strong> can delay military pay unless Congress provides funding; current federal funding runs through December 11, 2026.</li></ul>
<p>Sources: <a href="https://www.dfas.mil/RetiredMilitary/manage/payschedule" rel="noopener" target="_blank">DFAS retired and annuitant pay schedule</a>, <a href="https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/" rel="noopener" target="_blank">OPM federal holidays</a>.</p></section>
<nav class="mc-related-links" aria-label="Related tools"><h2>Related calculators</h2><a href="/tools/federal-holidays-2027">Federal holidays 2027</a><a href="/tools/federal-pay-periods-2027">NFC pay period calendar 2027</a><a href="/tools/gs-pay-scale-2027">GS pay scale 2027</a><a href="/tools/payday-calendar-2027">2027 payday calendar</a><a href="/tools/us-paycheck-calculator">US paycheck calculator</a></nav>"""

mfaqs = [("When is military payday in January 2027?", "The January 1 payday is paid on Thursday, December 31, 2026 because New Year's Day is a holiday. The mid-month payday is Friday, January 15, 2027."),
         ("What happens if the 1st or 15th is on a weekend?", "Active duty pay is deposited on the last business day before the weekend or holiday."),
         ("When do military retirees get paid in 2027?", "On the 1st of each month for the previous month, or the last business day before if the 1st is a weekend or holiday. Annuitants are paid the first business day after."),
         ("Is the January 1, 2028 military payday early?", "Yes. It is paid on Thursday, December 30, 2027, because January 1, 2028 is a Saturday and Friday, December 31, 2027 is a federal holiday."),
         ("Do banks pay military members early?", "Many banks and credit unions release military direct deposits one or two business days early, but the official pay date is the one listed here.")]

page('military-pay-dates-2027', 'Military Pay Dates 2027: Active Duty and Retiree | ToolPinch',
     'All 2027 military pay dates: active duty paydays on the 1st and 15th with early-pay dates, plus retiree and annuitant pay dates and a calendar download.',
     'Military Pay Dates 2027', 'Paid the 1st and 15th',
     'Every 2027 active duty payday, when weekends and holidays move it earlier, and the retiree and annuitant schedule.',
     ['DFAS rules', 'Holiday adjusted', 'Calendar export'], mcalc, mbody, mfaqs, mscript)
for d, p in early:
    print('early', d, '->', p)
