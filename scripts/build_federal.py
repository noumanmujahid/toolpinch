"""Build /tools/federal-pay-periods-2027 for ToolPinch. Run from the repo root."""
import datetime as dt
import json
import re

D, T = dt.date, dt.timedelta
template = open('tools/overtime-calculator.html', encoding='utf-8').read()
head_shared = re.search(r'(<link rel="icon".*?crossorigin="anonymous"></script>)', template).group(1)
header = re.search(r'(<a class="mc-skip-link".*?</header>)', template).group(1)
footer = re.search(r'(<footer class="mc-footer">.*?</footer>)', template).group(1)
assert 'G-8WM8MS9X9Y' in head_shared and 'ca-pub-3789885855212646' in head_shared

HOL = {
    D(2026, 12, 25): 'Christmas Day', D(2027, 1, 1): "New Year's Day", D(2027, 1, 18): 'Martin Luther King Jr. Day',
    D(2027, 2, 15): "Washington's Birthday", D(2027, 5, 31): 'Memorial Day', D(2027, 6, 18): 'Juneteenth (observed)',
    D(2027, 7, 5): 'Independence Day (observed)', D(2027, 9, 6): 'Labor Day', D(2027, 10, 11): 'Columbus Day',
    D(2027, 11, 11): 'Veterans Day', D(2027, 11, 25): 'Thanksgiving Day', D(2027, 12, 24): 'Christmas Day (observed)',
    D(2027, 12, 31): "New Year's Day 2028 (observed)", D(2028, 1, 17): 'Martin Luther King Jr. Day',
}


def nfc(end):
    """NFC: deposit settles the second Monday after the period ends (Tuesday if that Monday is a holiday);
    the official pay date is the Thursday of that week."""
    mon = end + T(9)
    dep = mon + T(1) if mon in HOL else mon
    return dep, end + T(12)


# leave year 2027: first full pay period starting in calendar 2027 (OPM)
START = D(2027, 1, 10)
assert START.weekday() == 6
periods = []
for i in range(26):
    s = START + T(14 * i)
    e = s + T(13)
    dep, off = nfc(e)
    periods.append((i + 1, s, e, dep, off))
assert periods[-1][2] == D(2028, 1, 8)
# spot checks against the published NFC 2027 schedule
assert periods[0][3:] == (D(2027, 2, 1), D(2027, 2, 4))
assert periods[1][3] == D(2027, 2, 16) and periods[11][3] == D(2027, 7, 6) and periods[18][3] == D(2027, 10, 12)
assert periods[25][3] == D(2028, 1, 18)

# paydays landing in calendar 2027 also include PP 25 and 26 of leave year 2026
prev = [(25, D(2026, 12, 13), D(2026, 12, 26)), (26, D(2026, 12, 27), D(2027, 1, 9))]
cal = [(f'2026 PP {n}', *nfc(e)) for n, s, e in prev] + [(f'2027 PP {n}', dep, off) for n, s, e, dep, off in periods]
cal2027 = [c for c in cal if c[1].year == 2027]
assert len(cal2027) == 26, len(cal2027)
assert cal2027[0][1] == D(2027, 1, 4) and cal2027[1][1] == D(2027, 1, 19)

f = lambda d: f"{d.strftime('%a')}, {d.strftime('%b')} {d.day}" + (f', {d.year}' if d.year != 2027 else '')
s_ = lambda d: f"{d.strftime('%b')} {d.day}" + (f', {d.year}' if d.year != 2027 else '')


def note(n, s, e, dep, off):
    out = []
    if dep.weekday() == 1:
        out.append(f'{HOL[dep - T(1)]} moves the deposit to Tuesday')
    if off in HOL:
        out.append(f'Official pay date is {HOL[off]}')
    if n == 1:
        out.append('A January 2027 pay adjustment, if any, starts here')
    if n == 23:
        out.append('Use-or-lose scheduling deadline: Nov 27')
    return '; '.join(out)


rows = ''.join(f'<tr><td>{n}</td><td>{s_(s)} – {s_(e)}</td><td>{f(dep)}</td><td>{f(off)}</td><td>{note(n, s, e, dep, off)}</td></tr>'
               for n, s, e, dep, off in periods)
months = {}
for lab, dep, off in cal2027:
    months.setdefault(dep.month, []).append(dep)
three = [m for m, v in months.items() if len(v) >= 3]
two_pay_months = ', '.join(D(2027, m, 1).strftime('%B') for m, v in months.items() if len(v) == 3)
print('3-deposit months', three)

data = json.dumps([{'n': n, 's': s.isoformat(), 'e': e.isoformat(), 'd': dep.isoformat(), 'o': off.isoformat()} for n, s, e, dep, off in periods])

STYLE = """<style>
.tp-big{font-size:1.35rem;margin:0 0 6px}.tp-big strong{font-size:2rem}
.tp-table{width:100%;border-collapse:collapse;font-size:.92rem;margin:10px 0}
.tp-table th,.tp-table td{padding:7px 9px;border-bottom:1px solid rgba(0,0,0,.12);text-align:left;vertical-align:top}
.tp-table th{font-weight:700}.tp-table td:last-child{font-size:.85rem;color:#4a5568}.tp-scroll{overflow-x:auto}
.tp-answer{font-size:1.1rem;border-left:4px solid #1a7f5a;padding:6px 12px;margin:12px 0}
.tp-actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.tp-btn{border:1px solid rgba(0,0,0,.2);background:#fff;border-radius:8px;padding:8px 12px;font:inherit;font-size:.9rem;cursor:pointer;color:#16325c}
.tp-btn:hover{background:#eef3fb}.tp-note{font-size:.88rem;opacity:.9}
.mc-calculator select,.mc-calculator input{width:100%}
.mc-calculator>p,.tp-actions,.tp-sub{grid-column:1/-1}.tp-sub{margin:14px 0 0;font-size:1.05rem}
@media print{.mc-header,.mc-footer,.mc-skip-link,.mc-trust,.tp-actions,.mc-related-links,.mc-faq,.mc-calculator{display:none!important}.mc-tool-hero{background:#fff!important;color:#000!important}}
</style>"""

calc = """<div class="mc-calculator"><h2>Look up a date</h2>
<label class="mc-field"><span>Any date in 2027</span><input id="fpDate" type="date" min="2027-01-10" max="2028-01-08" value="2027-01-10"></label>
<div class="mc-result" id="fpResult" aria-live="polite">Pick a date to see its pay period and NFC pay date.</div>
<h3 class="tp-sub">Annual leave: will you lose any?</h3>
<label class="mc-field"><span>Years of federal service</span><select id="fpCat"><option value="4">Less than 3 years (4 h per pay period)</option><option value="6" selected>3 to 15 years (6 h per pay period)</option><option value="8">15 years or more (8 h per pay period)</option></select></label>
<label class="mc-field"><span>Annual leave balance on Jan 10, 2027 (hours)</span><input id="fpBal" type="number" min="0" step="1" value="200"></label>
<label class="mc-field"><span>Annual leave you plan to use in 2027 (hours)</span><input id="fpUse" type="number" min="0" step="1" value="80"></label>
<label class="mc-field"><span>Carryover limit (hours)</span><select id="fpCap"><option value="240" selected>240 (most employees)</option><option value="360">360 (overseas)</option><option value="720">720 (SES)</option></select></label>
<div class="mc-result" id="fpLeave" aria-live="polite"></div>
<div class="tp-actions"><button type="button" class="tp-btn" id="fpIcs">Add NFC pay dates to my calendar (.ics)</button><button type="button" class="tp-btn" id="fpCsv">Download CSV</button><button type="button" class="tp-btn" id="fpPrint">Print</button></div></div>"""

script = """<script>(()=>{const P=__P__,$=id=>document.getElementById(id);
const p=s=>{const[y,m,d]=s.split('-').map(Number);return new Date(y,m-1,d,12)};
const fmt=s=>p(s).toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric',year:'numeric'});
function look(){const v=$('fpDate').value;if(!v)return;const x=P.find(q=>v>=q.s&&v<=q.e);
if(!x){$('fpResult').innerHTML='That date is outside leave year 2027 (Jan 10, 2027 to Jan 8, 2028).';return}
const day=Math.round((p(v)-p(x.s))/864e5)+1;
$('fpResult').innerHTML='<p class="tp-big"><strong>Pay period '+x.n+'</strong> of 26</p><p>Day '+day+' of 14 ('+(day<=7?'week 1':'week 2')+'). Period runs '+fmt(x.s)+' to '+fmt(x.e)+'.</p><p>NFC deposit: <b>'+fmt(x.d)+'</b><br>NFC official pay date: '+fmt(x.o)+'</p>'}
function leave(){const r=+$('fpCat').value,bal=Math.max(0,+$('fpBal').value||0),use=Math.max(0,+$('fpUse').value||0),cap=+$('fpCap').value;
const earn=r===6?25*6+10:26*r,end=bal+earn-use,lose=Math.max(0,end-cap);
let h='<p>You earn <b>'+earn+' hours</b> of annual leave in 2027 ('+(r===6?'6 h a pay period, 10 h in the last one':r+' h a pay period')+'), plus 104 hours of sick leave.</p><p>Projected balance on Jan 8, 2028: <b>'+end+' hours</b>.</p>';
h+=lose>0?'<p class="tp-big"><strong>'+lose+' h</strong> use-or-lose</p><p>Schedule it in writing by <b>Saturday, Nov 27, 2027</b> and use it by Jan 8, 2028, or it is forfeited.</p>':'<p class="tp-big"><strong>0 h</strong> at risk</p><p>You stay '+(cap-end)+' hours under the '+cap+'-hour carryover limit.</p>';
$('fpLeave').innerHTML=h}
function dl(name,type,body){const u=URL.createObjectURL(new Blob([body],{type}));const a=document.createElement('a');a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1000)}
function ics(){const st=new Date().toISOString().replace(/[-:]/g,'').replace(/\\.\\d+/,'');const L=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//ToolPinch//Federal Pay Periods 2027//EN','CALSCALE:GREGORIAN','METHOD:PUBLISH'];
const nx=s=>{const d=p(s);d.setDate(d.getDate()+1);return d.getFullYear()+String(d.getMonth()+1).padStart(2,'0')+String(d.getDate()).padStart(2,'0')};
P.forEach(x=>L.push('BEGIN:VEVENT','UID:fed-pp'+x.n+'-2027@toolpinch.com','DTSTAMP:'+st,'DTSTART;VALUE=DATE:'+x.d.replace(/-/g,''),'DTEND;VALUE=DATE:'+nx(x.d),'SUMMARY:Payday (PP '+x.n+')','DESCRIPTION:NFC deposit for pay period '+x.n+' ('+x.s+' to '+x.e+'). Official pay date '+x.o+'. toolpinch.com/tools/federal-pay-periods-2027','TRANSP:TRANSPARENT','END:VEVENT'));
L.push('END:VCALENDAR');dl('federal-paydays-2027.ics','text/calendar',L.join('\\r\\n')+'\\r\\n')}
function csv(){dl('federal-pay-periods-2027.csv','text/csv','pay_period,start,end,nfc_deposit,nfc_official_pay_date\\r\\n'+P.map(x=>[x.n,x.s,x.e,x.d,x.o].join(',')).join('\\r\\n')+'\\r\\n')}
document.addEventListener('DOMContentLoaded',()=>{const t=new Date(),ti=t.getFullYear()+'-'+String(t.getMonth()+1).padStart(2,'0')+'-'+String(t.getDate()).padStart(2,'0');if(ti>='2027-01-10'&&ti<='2028-01-08')$('fpDate').value=ti;
$('fpDate').addEventListener('input',look);['fpCat','fpBal','fpUse','fpCap'].forEach(id=>$(id).addEventListener('input',leave));
$('fpIcs').addEventListener('click',ics);$('fpCsv').addEventListener('click',csv);$('fpPrint').addEventListener('click',()=>window.print());look();leave()})})();</script>""".replace('__P__', data)

first = cal2027[0]
body = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>How many federal pay periods are in 2027?</h2>
<p class="tp-answer"><strong>26 pay periods.</strong> Leave year 2027 starts on <strong>Sunday, January 10, 2027</strong> (pay period 1) and ends on
<strong>Saturday, January 8, 2028</strong> (pay period 26). The deadline to schedule use-or-lose annual leave is <strong>Saturday, November 27, 2027</strong>.</p>
<p>Federal employees paid by the USDA National Finance Center (NFC) get <strong>26 paydays in calendar 2027</strong>. The first deposit is
Monday, January 4 (pay period 25 of 2026) and the last is Monday, December 20 (pay period 24 of 2027).
{('Months with three deposits: ' + two_pay_months + '.') if two_pay_months else 'No month has three NFC deposits in 2027.'}</p></header>

<section><h2>2027 federal pay period calendar</h2>
<p>Every pay period is 14 days, from Sunday to the Saturday two weeks later. Pay dates are for agencies paid by NFC; other payroll providers are listed below.</p>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>PP</th><th>Pay period</th><th>NFC deposit</th><th>Official pay date</th><th>Notes</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="tp-note">Deposits are usually available on the deposit date; the official pay date is the Thursday that week. Some banks post funds a day or two earlier.</p></section>

<section><h2>How federal pay dates work</h2>
<div class="mc-example-grid">
<section><h3>NFC (USDA and many agencies)</h3><p>Pay settles on the second Monday after the pay period ends. If that Monday is a federal holiday, it moves to Tuesday. In 2027 that happens four times: after Washington's Birthday, Independence Day, Columbus Day and, for pay period 26, MLK Day 2028.</p></section>
<section><h3>DFAS, IBC and GSA</h3><p>Defense (DFAS), Interior Business Center (IBC) and GSA payroll use the same 26 pay periods but pay on a different day of the following week. Your pay period numbers and leave dates are the same; check your earnings statement for your exact pay day.</p></section>
<section><h3>Pay raises and step increases</h3><p>Annual pay adjustments take effect on the first day of the first pay period starting on or after January 1, which in 2027 is January 10. The first paycheck that reflects them is pay period 1, deposited around February 1 for NFC.</p></section></div></section>

<section><h2>Annual and sick leave in 2027</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Years of service</th><th>Annual leave per pay period</th><th>Annual leave in 2027</th></tr></thead><tbody>
<tr><td>Less than 3 years</td><td>4 hours</td><td>104 hours (13 days)</td></tr>
<tr><td>3 to 15 years</td><td>6 hours (10 in the last full pay period)</td><td>160 hours (20 days)</td></tr>
<tr><td>15 years or more</td><td>8 hours</td><td>208 hours (26 days)</td></tr></tbody></table></div>
<p>Full-time employees also earn 4 hours of sick leave per pay period, 104 hours in 2027. Most employees can carry up to 240 hours of annual leave
into the next leave year. Anything above that is forfeited unless it was scheduled in writing before November 27, 2027 and then cancelled for an
approved reason, such as an exigency of the public business. Use the calculator above to check how much you need to use.</p></section>

<section><h2>Sources and limitations</h2>
<p>Pay period and leave year dates follow the OPM rule that a leave year begins with the first full biweekly pay period of the calendar year
(<a href="https://www.opm.gov/policy-data-oversight/pay-leave/leave-administration/fact-sheets/leave-year-beginning-and-ending-dates" rel="noopener" target="_blank">OPM leave year dates</a>).
NFC pay dates follow the NFC pay schedule (<a href="https://www.nfc.usda.gov/Publications/Forms/pay_period_calendar.php" rel="noopener" target="_blank">NFC pay period calendars</a>).
Some agencies and part-time or seasonal schedules differ, so confirm with your payroll office before planning around a specific date.</p></section>

<nav class="mc-related-links" aria-label="Related tools"><h2>Related calculators</h2>
<a href="/tools/payday-calendar-2027">2027 Payday Calendar</a><a href="/tools/long-weekends-2027">Long Weekends 2027</a>
<a href="/tools/working-days-2027">Working Days in 2027</a><a href="/tools/pay-period-converter">Pay Period Converter</a>
<a href="/pay-calculators">All pay calculators</a></nav>"""

faqs = [
    ("How many pay periods are in 2027 for federal employees?",
     "26. Leave year 2027 runs from Sunday, January 10, 2027 to Saturday, January 8, 2028, which is 26 biweekly pay periods."),
    ("When does pay period 1 of 2027 start?",
     "Sunday, January 10, 2027. It ends Saturday, January 23, and NFC pays it on Monday, February 1 (official pay date Thursday, February 4)."),
    ("Is 2027 a 27 pay period year?",
     "No. Leave year 2027 has the normal 26 pay periods. NFC-paid employees also receive 26 deposits during calendar year 2027."),
    ("What is the use-or-lose deadline for 2027?",
     "Saturday, November 27, 2027. Annual leave above your carryover limit (240 hours for most employees) must be scheduled in writing by then to be restored if it is later cancelled for an approved reason."),
    ("When is the first federal payday in 2027?",
     "For NFC-paid employees, Monday, January 4, 2027, which pays pay period 25 of 2026. The next is Tuesday, January 19, moved a day by MLK Day."),
    ("When does the 2027 leave year end?",
     "Saturday, January 8, 2028, the last day of pay period 26. Leave year 2028 starts Sunday, January 9, 2028."),
    ("How much annual leave will I earn in 2027?",
     "104 hours with less than 3 years of service, 160 hours with 3 to 15 years, and 208 hours with 15 years or more, plus 104 hours of sick leave for full-time employees."),
    ("Do holidays change federal pay dates?",
     "For NFC, if the Monday settlement date is a federal holiday the deposit moves to Tuesday. In 2027 that happens on February 16, July 6 and October 12, and on January 18, 2028 for pay period 26."),
]

url = 'https://www.toolpinch.com/tools/federal-pay-periods-2027'
title = '2027 Federal Pay Period Calendar & Paydays (NFC) | ToolPinch'
desc = 'All 26 federal pay periods for 2027 with NFC pay dates, leave year dates, the Nov 27 use-or-lose deadline and a leave calculator. Free .ics and CSV download.'
h1 = '2027 Federal Pay Period Calendar'
app = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": h1, "description": desc, "url": url,
       "applicationCategory": "FinanceApplication", "operatingSystem": "Any modern web browser", "isAccessibleForFree": True,
       "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "author": {"@type": "Organization", "name": "ToolPinch", "url": "https://www.toolpinch.com"}}
faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "ToolPinch", "item": "https://www.toolpinch.com/"},
    {"@type": "ListItem", "position": 2, "name": "Pay calculators", "item": "https://www.toolpinch.com/pay-calculators"},
    {"@type": "ListItem", "position": 3, "name": h1, "item": url}]}
html = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">'
        f'<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}">'
        f'<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:site_name" content="ToolPinch">'
        f'<meta property="og:url" content="{url}"><meta property="og:image" content="https://www.toolpinch.com/assets/icon-512.png?v=31">'
        f'{head_shared}<meta name="twitter:card" content="summary_large_image">'
        + ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (app, faq, crumbs))
        + f'{STYLE}</head><body>{header}<main id="main-content" class="mc-main"><section class="mc-tool-hero"><div class="mc-wrap mc-tool-grid"><div>'
        f'<a class="mc-back" href="/pay-calculators">Pay calculators</a><p class="mc-kicker">Updated for 2027</p><h1>{h1}</h1>'
        '<p>All 26 pay periods for leave year 2027 with NFC pay dates. Look up any date, check your use-or-lose leave, and add every payday to your calendar.</p>'
        '<div class="mc-trust"><span>No signup</span><span>OPM and NFC rules</span><span>Calendar export</span></div></div>'
        f'{calc}</div></section><article class="mc-wrap mc-depth mc-tool-content">{body}'
        '<section class="mc-faq"><h2>Frequently asked questions</h2>' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
        + f'</section></article></main>{footer}<script src="/js/money-clock.js"></script>{script}</body></html>')
open('tools/federal-pay-periods-2027.html', 'w', encoding='utf-8').write(html)
print('written', len(html))
for c in cal2027:
    print(c[0], c[1], c[2])
