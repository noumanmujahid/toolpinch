"""Build /tools/minimum-wage-2027 for ToolPinch. Run from the repo root."""
import json
import re

template = open('tools/overtime-calculator.html', encoding='utf-8').read()
head_shared = re.search(r'(<link rel="icon".*?crossorigin="anonymous"></script>)', template).group(1)
header = re.search(r'(<a class="mc-skip-link".*?</header>)', template).group(1)
footer = re.search(r'(<footer class="mc-footer">.*?</footer>)', template).group(1)
assert 'G-8WM8MS9X9Y' in head_shared and 'ca-pub-3789885855212646' in head_shared

F = 7.25
# state, now (Nov 2026), Jan 1 2027, note
S = [
    ('Alabama', F, F, 'No state minimum wage; federal $7.25 applies'),
    ('Alaska', 14.00, 14.00, 'Rises to $15.00 on July 1, 2027'),
    ('Arizona', 15.15, 15.65, 'Indexed to inflation'),
    ('Arkansas', 11.00, 11.00, 'Employers with 4+ employees'),
    ('California', 16.90, 17.40, 'Many cities set higher rates'),
    ('Colorado', 15.16, 15.71, 'Denver: $19.84 in 2027'),
    ('Connecticut', 16.94, 17.48, 'Indexed to employment cost index'),
    ('Delaware', 15.00, 15.00, ''),
    ('District of Columbia', 18.40, 18.40, 'Adjusted each July 1'),
    ('Florida', 15.00, 15.00, 'Reached $15 on Sept 30, 2026; next inflation increase Jan 1, 2028'),
    ('Georgia', F, F, 'State rate $5.15; federal $7.25 applies to most jobs'),
    ('Hawaii', 16.00, 16.00, 'Rises to $18.00 on Jan 1, 2028'),
    ('Idaho', F, F, ''),
    ('Illinois', 15.00, 15.00, 'Chicago and Cook County set higher rates'),
    ('Indiana', F, F, ''),
    ('Iowa', F, F, ''),
    ('Kansas', F, F, ''),
    ('Kentucky', F, F, ''),
    ('Louisiana', F, F, 'No state minimum wage; federal $7.25 applies'),
    ('Maine', 15.10, 15.70, 'Portland sets a higher rate'),
    ('Maryland', 15.00, 15.00, 'Montgomery County sets a higher rate'),
    ('Massachusetts', 15.00, 15.00, ''),
    ('Michigan', 13.73, 15.00, 'Final step of the 2025 law'),
    ('Minnesota', 11.41, 11.87, 'Minneapolis and St. Paul set higher rates'),
    ('Mississippi', F, F, 'No state minimum wage; federal $7.25 applies'),
    ('Missouri', 15.00, 15.00, 'Automatic inflation increases repealed in 2025'),
    ('Montana', 10.85, 11.20, '$4.00 for small non-FLSA businesses'),
    ('Nebraska', 15.00, 15.26, 'Fixed 1.75% yearly increase (LB 258)'),
    ('Nevada', 12.00, 12.00, ''),
    ('New Hampshire', F, F, ''),
    ('New Jersey', 15.92, 16.48, '$16.25 for seasonal and small employers'),
    ('New Mexico', 12.00, 12.00, 'Some cities set higher rates'),
    ('New York', 16.00, 16.00, 'NYC, Long Island, Westchester: $17.00; 2027 increase suspended'),
    ('North Carolina', F, F, ''),
    ('North Dakota', F, F, ''),
    ('Ohio', 11.00, 11.40, 'Employers with $420,000+ in gross receipts'),
    ('Oklahoma', F, F, ''),
    ('Oregon', 15.55, 15.55, 'Portland metro $16.80, non-urban $14.55; adjusted each July 1'),
    ('Pennsylvania', F, F, ''),
    ('Rhode Island', 16.00, 17.00, ''),
    ('South Carolina', F, F, 'No state minimum wage; federal $7.25 applies'),
    ('South Dakota', 11.85, 12.30, ''),
    ('Tennessee', F, F, 'No state minimum wage; federal $7.25 applies'),
    ('Texas', F, F, ''),
    ('Utah', F, F, ''),
    ('Vermont', 14.42, 14.91, 'Projected; official rate not yet published'),
    ('Virginia', 12.77, 13.75, 'Rises to $15.00 on Jan 1, 2028'),
    ('Washington', 17.13, 17.73, 'Seattle and other cities set higher rates'),
    ('West Virginia', 8.75, 8.75, 'Employers with 6+ employees at one location'),
    ('Wisconsin', F, F, ''),
    ('Wyoming', F, F, 'State rate $5.15; federal $7.25 applies to most jobs'),
]
assert len(S) == 51
raises = [s for s in S if s[2] > s[1]]
assert len(raises) == 16, [r[0] for r in raises]
at_fed = [s for s in S if s[2] == F]
assert len(at_fed) == 20, len(at_fed)
top = max((s for s in S if s[0] != 'District of Columbia'), key=lambda s: s[2])
assert top[0] == 'Washington'
biggest = max(raises, key=lambda s: s[2] - s[1])
assert biggest[0] == 'Michigan'

m = lambda x: f'${x:,.2f}'
rows = ''.join(
    f'<tr{" class=tp-up" if b > a else ""}><td>{n}</td><td>{m(a)}</td><td><b>{m(b)}</b></td>'
    f'<td>{("+" + m(b - a)) if b > a else "—"}</td><td>{note}</td></tr>' for n, a, b, note in S)
raise_list = ', '.join(r[0] for r in raises)
data = json.dumps([{'s': n, 'a': a, 'b': b, 'n': note} for n, a, b, note in S])

STYLE = """<style>
.tp-big{font-size:1.35rem;margin:0 0 6px}.tp-big strong{font-size:2rem}
.tp-table{width:100%;border-collapse:collapse;font-size:.92rem;margin:10px 0}
.tp-table th,.tp-table td{padding:7px 9px;border-bottom:1px solid rgba(0,0,0,.12);text-align:left;vertical-align:top}
.tp-table th{font-weight:700;position:sticky;top:0;background:#fff}.tp-table td:last-child{font-size:.85rem;color:#4a5568}
.tp-table tr.tp-up td:nth-child(4){color:#1a7f5a;font-weight:600}.tp-scroll{overflow-x:auto}
.tp-answer{font-size:1.1rem;border-left:4px solid #1a7f5a;padding:6px 12px;margin:12px 0}
.tp-note{font-size:.88rem;opacity:.9}.tp-filter{width:100%;max-width:320px;padding:8px 10px;border:1px solid rgba(0,0,0,.2);border-radius:8px;font:inherit;margin:6px 0}
.mc-calculator select,.mc-calculator input{width:100%}.mc-calculator>p{grid-column:1/-1}
</style>"""

opts = ''.join(f'<option value="{i}"{" selected" if n == "California" else ""}>{n}</option>' for i, (n, *_r) in enumerate(S))
calc = f"""<div class="mc-calculator"><h2>Your 2027 minimum wage pay</h2>
<label class="mc-field"><span>State</span><select id="mwState">{opts}</select></label>
<label class="mc-field"><span>Hours per week</span><input id="mwHours" type="number" min="1" max="80" step="0.5" value="40"></label>
<button class="mc-button" data-action="minimum-wage-2027">Calculate</button>
<div class="mc-result" id="mwResult" aria-live="polite">Pick a state to see the 2027 minimum wage.</div></div>"""

script = """<script>(()=>{const D=__D__,$=id=>document.getElementById(id);
const m=x=>x.toLocaleString('en-US',{style:'currency',currency:'USD'});
function run(){const s=D[+$('mwState').value],h=Math.min(80,Math.max(0,+$('mwHours').value||0));
const ot=Math.max(h-40,0),reg=h-ot,wk=s.b*(reg+1.5*ot),wkOld=s.a*(reg+1.5*ot),yr=wk*52,diff=(wk-wkOld)*52;
let r='<p class="tp-big"><strong>'+m(s.b)+'</strong> an hour in '+s.s+' on Jan 1, 2027</p>';
r+='<p>'+h+' hours a week: <b>'+m(wk)+'</b> a week, <b>'+m(yr/12)+'</b> a month, <b>'+m(yr)+'</b> a year before tax'+(ot?' (includes '+ot+' overtime hours at 1.5×)':'')+'.</p>';
r+=s.b>s.a?'<p>That is '+m(s.b-s.a)+' an hour more than now ('+m(s.a)+'), or about <b>'+m(diff)+'</b> more a year.</p>':'<p>No statewide change on January 1, 2027.</p>';
if(s.n)r+='<p class="tp-note">'+s.n+'.</p>';$('mwResult').innerHTML=r}
function filt(){const q=$('mwFilter').value.trim().toLowerCase();document.querySelectorAll('#mwTable tbody tr').forEach(tr=>{tr.style.display=!q||tr.firstChild.textContent.toLowerCase().includes(q)?'':'none'})}
document.addEventListener('DOMContentLoaded',()=>{['mwState','mwHours'].forEach(id=>$(id).addEventListener('input',run));
document.querySelectorAll('[data-action="minimum-wage-2027"]').forEach(b=>b.addEventListener('click',run));$('mwFilter').addEventListener('input',filt);run()})})();</script>""".replace('__D__', data)

body = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>Which states raise the minimum wage in 2027?</h2>
<p class="tp-answer"><strong>16 states</strong> raise their minimum wage on <strong>January 1, 2027</strong>: {raise_list}.
The highest state rate is <strong>Washington at {m(top[2])}</strong> an hour. The biggest jump is <strong>Michigan, up {m(biggest[2] - biggest[1])} to $15.00</strong>.
The federal minimum wage stays at <strong>$7.25</strong>, which is still the rate in 20 states.</p>
<p>Alaska rises to $15.00 on July 1, 2027, and Oregon and Washington, D.C. adjust their rates for inflation every July 1. New York's planned 2027 increase was suspended,
so rates stay at $17.00 in New York City, Long Island and Westchester and $16.00 in the rest of the state.</p></header>

<section><h2>Minimum wage by state, 2026 vs 2027</h2>
<p>Statewide rates for most adult, non-tipped employees. Many cities and counties set higher local rates, and some states have lower rates for small employers, minors or trainees.</p>
<input class="tp-filter" id="mwFilter" type="search" placeholder="Filter states…" aria-label="Filter states">
<div class="tp-scroll"><table class="tp-table" id="mwTable"><thead><tr><th>State</th><th>Now</th><th>Jan 1, 2027</th><th>Change</th><th>Notes</th></tr></thead><tbody>{rows}</tbody></table></div></section>

<section><h2>What a minimum wage job pays in 2027</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Hourly rate</th><th>Weekly (40 h)</th><th>Yearly (2,080 h)</th><th>Where</th></tr></thead><tbody>
<tr><td>$7.25</td><td>$290.00</td><td>$15,080</td><td>Federal minimum; 20 states</td></tr>
<tr><td>$12.30</td><td>$492.00</td><td>$25,584</td><td>South Dakota</td></tr>
<tr><td>$15.00</td><td>$600.00</td><td>$31,200</td><td>Michigan, Florida, Illinois, Missouri and others</td></tr>
<tr><td>$16.48</td><td>$659.20</td><td>$34,278</td><td>New Jersey</td></tr>
<tr><td>$17.40</td><td>$696.00</td><td>$36,192</td><td>California</td></tr>
<tr><td>$17.73</td><td>$709.20</td><td>$36,878</td><td>Washington</td></tr></tbody></table></div>
<p>Pay is before tax. Hours over 40 in a week are usually paid at 1.5 times the regular rate; use the <a href="/tools/overtime-calculator">overtime calculator</a> for a full week.</p></section>

<section><h2>What employers should do before January 1</h2>
<div class="mc-example-grid">
<section><h3>Update pay rates</h3><p>The new rate applies to hours worked from January 1. If your pay period crosses New Year's Day, pay the old rate for December hours and the new rate for January hours.</p></section>
<section><h3>Check tipped and salaried staff</h3><p>Tipped cash wages and the minimum salary for exempt employees are tied to the minimum wage in several states, including California, Colorado, New Jersey and Washington.</p></section>
<section><h3>Replace your posters</h3><p>States that change their rate publish a new minimum wage poster. Display the 2027 version where employees can see it.</p></section></div></section>

<section><h2>Sources and limitations</h2>
<p>Rates come from the <a href="https://www.dol.gov/agencies/whd/minimum-wage/state" rel="noopener" target="_blank">U.S. Department of Labor</a> and announcements from state labor departments and governors' offices, checked in November 2026.
Vermont's 2027 rate is a projection until the state publishes it. This page is general information, not legal advice; check your state labor department for coverage rules, local rates and special rates.</p></section>

<nav class="mc-related-links" aria-label="Related tools"><h2>Related calculators</h2>
<a href="/tools/salary-to-hourly-calculator">Salary to Hourly</a><a href="/tools/overtime-calculator">Overtime Calculator</a>
<a href="/tools/payday-calendar-2027">2027 Payday Calendar</a><a href="/tools/overtime-calculator-california">California Overtime</a>
<a href="/pay-calculators">All pay calculators</a></nav>"""

faqs = [
    ("Which states raise the minimum wage on January 1, 2027?", f"16 states: {raise_list}."),
    ("What is the highest state minimum wage in 2027?", f"Washington, at {m(top[2])} an hour from January 1, 2027. Washington, D.C. is higher at $18.40, and some cities, such as Seattle and Denver, are higher still."),
    ("Is the federal minimum wage going up in 2027?", "No. The federal minimum wage has been $7.25 an hour since July 2009, and no increase has been enacted. It remains the minimum in 20 states."),
    ("What is the California minimum wage in 2027?", "$17.40 an hour for all employers from January 1, 2027, up from $16.90. Many California cities set higher local rates."),
    ("What is the New York minimum wage in 2027?", "It stays at $17.00 an hour in New York City, Long Island and Westchester and $16.00 in the rest of the state. The inflation increase planned for 2027 was suspended."),
    ("What is the Michigan minimum wage in 2027?", "$15.00 an hour from January 1, 2027, up from $13.73. It is the largest increase of any state in 2027."),
    ("How much is $15 an hour a year?", "$31,200 a year before tax at 40 hours a week for 52 weeks, or $600 a week."),
    ("Does the minimum wage go up in Florida in 2027?", "No. Florida reached $15.00 on September 30, 2026. The next increase, based on inflation, takes effect January 1, 2028."),
]

url = 'https://www.toolpinch.com/tools/minimum-wage-2027'
title = 'Minimum Wage by State 2027: All 50 States + Calculator | ToolPinch'
desc = 'Every state minimum wage for 2027 vs 2026. 16 states raise pay on Jan 1, 2027; Washington is highest at $17.73. Free calculator for weekly and yearly pay.'
h1 = 'Minimum Wage by State 2027'
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
        f'<a class="mc-back" href="/pay-calculators">Pay calculators</a><p class="mc-kicker">Updated November 2026</p><h1>{h1}</h1>'
        '<p>The 2027 minimum wage for every state and D.C., what changes on January 1, and what it means for weekly and yearly pay.</p>'
        '<div class="mc-trust"><span>All 50 states + DC</span><span>Official sources</span><span>No signup</span></div></div>'
        f'{calc}</div></section><article class="mc-wrap mc-depth mc-tool-content">{body}'
        '<section class="mc-faq"><h2>Frequently asked questions</h2>' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
        + f'</section></article></main>{footer}<script src="/js/money-clock.js"></script>{script}</body></html>')
open('tools/minimum-wage-2027.html', 'w', encoding='utf-8').write(html)
print('written', len(html), 'raises', len(raises), 'at federal', len(at_fed))
