"""Build /tools/social-security-payment-schedule-2027 for ToolPinch. Run from the repo root."""
import datetime as dt
import json
import re

D, T = dt.date, dt.timedelta
template = open('tools/overtime-calculator.html', encoding='utf-8').read()
head_shared = re.search(r'(<link rel="icon".*?crossorigin="anonymous"></script>)', template).group(1)
header = re.search(r'(<a class="mc-skip-link".*?</header>)', template).group(1)
footer = re.search(r'(<footer class="mc-footer">.*?</footer>)', template).group(1)
assert 'G-8WM8MS9X9Y' in head_shared and 'ca-pub-3789885855212646' in head_shared

# federal holidays as observed (SSA pays the business day before a weekend or holiday)
HOL = {D(2026, 12, 25), D(2027, 1, 1), D(2027, 1, 18), D(2027, 2, 15), D(2027, 5, 31), D(2027, 6, 18), D(2027, 7, 5),
       D(2027, 9, 6), D(2027, 10, 11), D(2027, 11, 11), D(2027, 11, 25), D(2027, 12, 24), D(2027, 12, 31)}


def back(d):
    while d.weekday() >= 5 or d in HOL:
        d -= T(1)
    return d


def nth_wed(y, m, n):
    d = D(y, m, 1)
    d += T((2 - d.weekday()) % 7)
    return back(d + T(7 * (n - 1)))


MONTHS = [(2027, m) for m in range(1, 13)]
rows = []
for y, m in MONTHS:
    rows.append({'m': D(y, m, 1).strftime('%B'), 'ssi': back(D(y, m, 1)), 'third': back(D(y, m, 3)),
                 'w2': nth_wed(y, m, 2), 'w3': nth_wed(y, m, 3), 'w4': nth_wed(y, m, 4)})
jan28_ssi = back(D(2028, 1, 1))
# cross-checks against the published 2027 schedules
assert rows[0]['ssi'] == D(2026, 12, 31) and rows[0]['third'] == D(2026, 12, 31)
assert rows[4]['ssi'] == D(2027, 4, 30) and rows[7]['ssi'] == D(2027, 7, 30)
assert rows[3]['third'] == D(2027, 4, 2) and rows[6]['third'] == D(2027, 7, 2) and rows[9]['third'] == D(2027, 10, 1)
assert [r['w2'].day for r in rows] == [13, 10, 10, 14, 12, 9, 14, 11, 8, 13, 10, 8]
assert [r['w4'].day for r in rows] == [27, 24, 24, 28, 26, 23, 28, 25, 22, 27, 24, 22]
assert jan28_ssi == D(2027, 12, 30)

f = lambda d: f"{d.strftime('%a')}, {d.strftime('%b')} {d.day}" + (f", {d.year}" if d.year != 2027 else '')
table = ''.join(f"<tr><td>{r['m']}</td><td>{f(r['ssi'])}</td><td>{f(r['third'])}</td><td>{f(r['w2'])}</td><td>{f(r['w3'])}</td><td>{f(r['w4'])}</td></tr>" for r in rows)
data = json.dumps({'months': [r['m'] for r in rows], 'g': {k: [r[k].isoformat() for r in rows] for k in ('ssi', 'third', 'w2', 'w3', 'w4')}, 'jan28': jan28_ssi.isoformat()})

STYLE = """<style>
.tp-big{font-size:1.35rem;margin:0 0 6px}.tp-big strong{font-size:2rem}
.tp-table{width:100%;border-collapse:collapse;font-size:.9rem;margin:10px 0}
.tp-table th,.tp-table td{padding:7px 8px;border-bottom:1px solid rgba(0,0,0,.12);text-align:left;vertical-align:top;white-space:nowrap}
.tp-table th{font-weight:700;white-space:normal}.tp-scroll{overflow-x:auto}
.tp-answer{font-size:1.08rem;border-left:4px solid #1a7f5a;padding:6px 12px;margin:12px 0}
.tp-note{font-size:.88rem;opacity:.9}.tp-list{list-style:none;padding:0;margin:8px 0;columns:2;column-gap:18px}.tp-list li{padding:2px 0}
.tp-actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.tp-btn{border:1px solid rgba(0,0,0,.2);background:#fff;border-radius:8px;padding:8px 12px;font:inherit;font-size:.9rem;cursor:pointer;color:#16325c}
.tp-btn:hover{background:#eef3fb}.mc-calculator select,.mc-calculator input{width:100%}.mc-calculator>p,.tp-actions{grid-column:1/-1}
@media(max-width:520px){.tp-list{columns:1}}
@media print{.mc-header,.mc-footer,.mc-skip-link,.mc-trust,.tp-actions,.mc-related-links,.mc-faq,.mc-calculator{display:none!important}.mc-tool-hero{background:#fff!important;color:#000!important}}
</style>"""

calc = """<div class="mc-calculator"><h2>Your 2027 payments</h2>
<label class="mc-field"><span>How you are paid</span><select id="ssGroup">
<option value="w2">Social Security, birthday 1st to 10th (2nd Wednesday)</option>
<option value="w3" selected>Social Security, birthday 11th to 20th (3rd Wednesday)</option>
<option value="w4">Social Security, birthday 21st to 31st (4th Wednesday)</option>
<option value="third">Benefits started before May 1997, or SSI plus Social Security (3rd)</option>
<option value="ssi">SSI only (1st)</option></select></label>
<label class="mc-field"><span>Current monthly benefit before the raise ($)</span><input id="ssAmt" type="number" min="0" step="1" value="2095"></label>
<button class="mc-button" data-action="ss-2027">Show my dates</button>
<div class="mc-result" id="ssResult" aria-live="polite">Pick how you are paid to see your 2027 dates.</div>
<div class="tp-actions"><button type="button" class="tp-btn" id="ssIcs">Add my 2027 dates to calendar (.ics)</button><button type="button" class="tp-btn" id="ssPrint">Print</button></div></div>"""

script = """<script>(()=>{const S=__S__,$=id=>document.getElementById(id);
const p=s=>{const[y,m,d]=s.split('-').map(Number);return new Date(y,m-1,d,12)};
const fmt=s=>p(s).toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric'})+(s.startsWith('2027')?'':', '+s.slice(0,4));
const money=x=>x.toLocaleString('en-US',{style:'currency',currency:'USD'});
function dates(){const g=$('ssGroup').value;let d=S.g[g].slice();if(g==='ssi')d.push(S.jan28);return d}
function run(){const g=$('ssGroup').value,a=Math.max(0,+$('ssAmt').value||0),d=dates();
const nb=Math.floor(a*1.036*10)/10,inc=nb-a;
let h='<p class="tp-big"><strong>'+money(nb)+'</strong> a month in 2027</p><p>Up '+money(inc)+' a month ('+money(inc*12)+' a year) with the 3.6% cost-of-living increase, before any Medicare premium change.</p>';
h+='<ul class="tp-list">'+d.map((x,i)=>'<li>'+(g==='ssi'&&i===12?'Jan 2028':S.months[i].slice(0,3))+': <b>'+fmt(x)+'</b></li>').join('')+'</ul>';
if(g==='ssi'||g==='third')h+='<p class="tp-note">Dates move to the business day before when the usual date is a weekend or federal holiday'+(g==='ssi'?', so there are two SSI payments in April, July and December and none in January, May and August.':'.')+'</p>';
$('ssResult').innerHTML=h}
function ics(){const st=new Date().toISOString().replace(/[-:]/g,'').replace(/\\.\\d+/,''),L=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//ToolPinch//Social Security 2027//EN','CALSCALE:GREGORIAN','METHOD:PUBLISH'];
const nx=s=>{const d=p(s);d.setDate(d.getDate()+1);return d.getFullYear()+String(d.getMonth()+1).padStart(2,'0')+String(d.getDate()).padStart(2,'0')};
dates().forEach((x,i)=>L.push('BEGIN:VEVENT','UID:ss-'+$('ssGroup').value+'-'+x+'@toolpinch.com','DTSTAMP:'+st,'DTSTART;VALUE=DATE:'+x.replace(/-/g,''),'DTEND;VALUE=DATE:'+nx(x),'SUMMARY:'+($('ssGroup').value==='ssi'?'SSI payment':'Social Security payment'),'DESCRIPTION:Expected deposit date. Schedule from toolpinch.com/tools/social-security-payment-schedule-2027','TRANSP:TRANSPARENT','END:VEVENT'));
L.push('END:VCALENDAR');const u=URL.createObjectURL(new Blob([L.join('\\r\\n')+'\\r\\n'],{type:'text/calendar'}));const a=document.createElement('a');a.href=u;a.download='social-security-2027.ics';document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1000)}
document.addEventListener('DOMContentLoaded',()=>{['ssGroup','ssAmt'].forEach(id=>$(id).addEventListener('input',run));document.querySelectorAll('[data-action="ss-2027"]').forEach(b=>b.addEventListener('click',run));
$('ssIcs').addEventListener('click',ics);$('ssPrint').addEventListener('click',()=>window.print());run()})})();</script>""".replace('__S__', data)

body = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>When will I get my Social Security payment in 2027?</h2>
<p class="tp-answer">Most people are paid on a <strong>Wednesday</strong> set by their birthday: the <strong>2nd Wednesday</strong> if born on the 1st to 10th, the <strong>3rd Wednesday</strong> for the 11th to 20th, and the <strong>4th Wednesday</strong> for the 21st to 31st.
SSI is paid on the <strong>1st</strong>, and people who started benefits before May 1997 or who get both SSI and Social Security are paid on the <strong>3rd</strong>.
Payments rise <strong>3.6%</strong> in 2027.</p>
<p>The January 2027 SSI payment arrives early on <strong>Thursday, December 31, 2026</strong>, because New Year's Day is a holiday. SSI recipients get two payments in April, July and December 2027 and none in January, May and August.</p></header>

<section><h2>2027 Social Security payment schedule</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Month</th><th>SSI</th><th>Paid on the 3rd</th><th>Born 1st–10th</th><th>Born 11th–20th</th><th>Born 21st–31st</th></tr></thead><tbody>{table}</tbody></table></div>
<p>The SSI payment for January 2028 is paid on <strong>{f(jan28_ssi)}, 2027</strong>, because January 1, 2028 is a Saturday and Friday, December 31 is the observed holiday.
If a payment has not arrived, Social Security asks you to allow three more mail days before contacting them.</p></section>

<section><h2>The 2027 cost-of-living increase</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Average monthly benefit</th><th>Before</th><th>After 3.6% COLA</th></tr></thead><tbody>
<tr><td>All retired workers</td><td>$2,095</td><td><b>$2,170</b></td></tr>
<tr><td>Aged couple, both receiving benefits</td><td>$3,238</td><td><b>$3,355</b></td></tr>
<tr><td>Aged widow(er) alone</td><td>$1,936</td><td><b>$2,005</b></td></tr>
<tr><td>All disabled workers</td><td>$1,642</td><td><b>$1,701</b></td></tr></tbody></table></div>
<p>The increase applies to Social Security benefits paid from January 2027 and to SSI from the payment on December 31, 2026. Your Medicare Part B premium, if deducted, can change your net deposit.</p></section>

<section><h2>Other 2027 Social Security numbers</h2>
<div class="tp-scroll"><table class="tp-table"><tbody>
<tr><td>Maximum SSI payment</td><td>$1,029 a month (individual), $1,544 (couple)</td></tr>
<tr><td>Maximum benefit at full retirement age</td><td>$4,188 a month</td></tr>
<tr><td>Earnings limit before full retirement age</td><td>$25,560 a year ($1 withheld for every $2 above)</td></tr>
<tr><td>Earnings limit in the year you reach full retirement age</td><td>$67,920 a year ($1 withheld for every $3 above)</td></tr>
<tr><td>Maximum earnings taxed for Social Security</td><td>$192,300</td></tr>
<tr><td>Earnings for one credit</td><td>$1,970</td></tr>
<tr><td>Substantial gainful activity (disability)</td><td>$1,770 a month ($2,950 if blind)</td></tr></tbody></table></div></section>

<section><h2>Sources and limitations</h2>
<p>Figures from the <a href="https://www.ssa.gov/cola/factsheets/2027.html" rel="noopener" target="_blank">Social Security 2027 COLA fact sheet</a> and the
<a href="https://www.ssa.gov/pubs/EN-05-10031-2027.pdf" rel="noopener" target="_blank">2027 schedule of payments</a>. Weekend and holiday dates follow Social Security's rule of paying on the business day before.
The calculator estimates your new benefit by applying 3.6% and rounding down to the dime, as Social Security does; your official notice is the final amount.</p></section>

<nav class="mc-related-links" aria-label="Related tools"><h2>Related calculators</h2>
<a href="/tools/payday-calendar-2027">2027 Payday Calendar</a><a href="/tools/federal-pay-periods-2027">2027 Federal Pay Periods</a>
<a href="/tools/minimum-wage-2027">Minimum Wage by State 2027</a><a href="/pay-calculators">All pay calculators</a></nav>"""

faqs = [
    ("When is Social Security paid in 2027?",
     "On the 2nd Wednesday of the month if your birthday is the 1st to 10th, the 3rd Wednesday for the 11th to 20th, and the 4th Wednesday for the 21st to 31st. SSI is paid on the 1st, and some people are paid on the 3rd."),
    ("How much is the 2027 Social Security increase?",
     "3.6%. The average retirement benefit rises from about $2,095 to $2,170 a month, according to Social Security."),
    ("When does the 2027 COLA start?",
     "With the SSI payment on December 31, 2026 and with Social Security payments in January 2027."),
    ("Why is my January 2027 SSI payment on December 31?",
     "January 1, 2027 is New Year's Day, a federal holiday, so the payment is made on the business day before, Thursday, December 31, 2026."),
    ("Which months have two SSI payments in 2027?",
     "April (April 1 and April 30), July (July 1 and July 30) and December (December 1 and December 30). There is no SSI payment in January, May or August 2027 because those payments arrive early."),
    ("What is the maximum SSI payment in 2027?",
     "$1,029 a month for an individual and $1,544 for a couple, before any state supplement."),
    ("What is the 2027 earnings limit for Social Security?",
     "$25,560 a year if you are under full retirement age, and $67,920 in the year you reach full retirement age. There is no limit after you reach full retirement age."),
]

url = 'https://www.toolpinch.com/tools/social-security-payment-schedule-2027'
title = 'Social Security Payment Schedule 2027 + 3.6% COLA Calculator | ToolPinch'
desc = 'Every 2027 Social Security and SSI payment date by birthday, the 3.6% COLA and your new benefit. Includes double SSI months and a calendar download.'
h1 = 'Social Security Payment Schedule 2027'
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
        '<p>See every 2027 Social Security and SSI payment date for your birthday, your new benefit after the 3.6% raise, and add the dates to your calendar.</p>'
        '<div class="mc-trust"><span>Official SSA figures</span><span>No signup</span><span>Calendar export</span></div></div>'
        f'{calc}</div></section><article class="mc-wrap mc-depth mc-tool-content">{body}'
        '<section class="mc-faq"><h2>Frequently asked questions</h2>' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
        + f'</section></article></main>{footer}<script src="/js/money-clock.js"></script>{script}</body></html>')
open('tools/social-security-payment-schedule-2027.html', 'w', encoding='utf-8').write(html)
print('written', len(html))
for r in rows:
    print(r['m'][:3], r['ssi'], r['third'], r['w2'], r['w3'], r['w4'])
