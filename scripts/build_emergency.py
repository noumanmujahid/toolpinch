"""Build /tools/emergency-supply-calculator for ToolPinch. Run from the repo root."""
import json
import re

template = open('tools/overtime-calculator.html', encoding='utf-8').read()
head_shared = re.search(r'(<link rel="icon".*?crossorigin="anonymous"></script>)', template).group(1)
header = re.search(r'(<a class="mc-skip-link".*?</header>)', template).group(1)
footer = re.search(r'(<footer class="mc-footer">.*?</footer>)', template).group(1)
assert 'G-8WM8MS9X9Y' in head_shared and 'ca-pub-3789885855212646' in head_shared

# German BBK 10-day list, per person (kg)
BBK = [('Cereals, bread, potatoes, pasta, rice', 3.5), ('Vegetables and pulses (canned or jarred)', 4.0),
       ('Fruit and nuts', 2.5), ('Milk and milk products (UHT milk, hard cheese)', 2.6),
       ('Fish, meat, eggs or egg powder', 1.5), ('Fats and oils', 0.357)]

STYLE = """<style>
.tp-big{font-size:1.35rem;margin:0 0 6px}.tp-big strong{font-size:2rem}
.tp-table{width:100%;border-collapse:collapse;font-size:.93rem;margin:10px 0}
.tp-table th,.tp-table td{padding:7px 9px;border-bottom:1px solid rgba(0,0,0,.12);text-align:left;vertical-align:top}
.tp-table th{font-weight:700}.tp-scroll{overflow-x:auto}
.mc-result .tp-table th,.mc-result .tp-table td{border-bottom-color:rgba(255,255,255,.15)}
.tp-answer{font-size:1.08rem;border-left:4px solid #1a7f5a;padding:6px 12px;margin:12px 0}
.tp-note{font-size:.88rem;opacity:.9}.tp-check{list-style:none;padding:0;margin:6px 0;columns:2;column-gap:20px}
.tp-check li{break-inside:avoid;padding:3px 0}.tp-check li:before{content:"\\2610  "}
.tp-actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.tp-btn{border:1px solid rgba(0,0,0,.2);background:#fff;border-radius:8px;padding:8px 12px;font:inherit;font-size:.9rem;cursor:pointer;color:#16325c}
.tp-btn:hover{background:#eef3fb}
.mc-calculator select,.mc-calculator input{width:100%}.mc-calculator>p,.tp-actions{grid-column:1/-1}
@media(max-width:600px){.tp-check{columns:1}}
@media print{.mc-header,.mc-footer,.mc-skip-link,.mc-trust,.tp-actions,.mc-related-links,.mc-faq,.mc-calculator label,.mc-calculator .mc-button,.mc-tool-content>*:not(#esPrint){display:none!important}.mc-tool-hero,.mc-result{background:#fff!important;color:#000!important}.tp-check li:before{content:"\\2610  "}}
</style>"""

calc = """<div class="mc-calculator"><h2>Your household supply</h2>
<label class="mc-field"><span>Adults and teens</span><input id="esAdults" type="number" min="0" max="20" value="2"></label>
<label class="mc-field"><span>Children (under 12)</span><input id="esKids" type="number" min="0" max="20" value="0"></label>
<label class="mc-field"><span>Number of days</span><select id="esDays"><option value="3">3 days (72 hours: EU, UK, France, Canada)</option><option value="7">7 days (Sweden, Norway)</option><option value="10" selected>10 days (Germany)</option><option value="14">14 days (US "2 weeks ready")</option></select></label>
<label class="mc-field"><span>Water guideline</span><select id="esWater"><option value="3.785" selected>1 gallon (3.8 L) per person per day: US Ready.gov, includes basic hygiene</option><option value="2">2 litres per person per day: Germany, drinking and cooking only</option></select></label>
<label class="mc-field"><span>Pets</span><input id="esPets" type="number" min="0" max="20" value="0"></label>
<label class="mc-field"><span>Units</span><select id="esUnits"><option value="us">Gallons and pounds</option><option value="metric">Litres and kilograms</option></select></label>
<button class="mc-button" data-action="emergency-supply">Calculate my supply</button>
<div class="mc-result" id="esResult" aria-live="polite">Enter your household to see how much to store.</div>
<div class="tp-actions"><button type="button" class="tp-btn" id="esPrintBtn">Print my checklist</button></div></div>"""

script = """<script>(()=>{const F=__F__,$=id=>document.getElementById(id);
const n=(id,max)=>Math.min(max,Math.max(0,Math.floor(+$(id).value||0)));
const fmt=(x,d=1)=>x.toLocaleString('en-US',{maximumFractionDigits:d});
function run(){const a=n('esAdults',20),k=n('esKids',20),p=n('esPets',20),days=+$('esDays').value,wl=+$('esWater').value,us=$('esUnits').value==='us';
const people=a+k;if(!people){$('esResult').innerHTML='Add at least one person.';return}
const L=people*wl*days,gal=L/3.785,kcal=(a*2200+k*1600)*days,eq=(a+k*0.75)*days/10;
const water=us?'<strong>'+fmt(Math.ceil(gal*10)/10)+' gallons</strong> ('+fmt(Math.ceil(L))+' litres)':'<strong>'+fmt(Math.ceil(L))+' litres</strong> ('+fmt(Math.ceil(gal*10)/10)+' gallons)';
let h='<p class="tp-big">'+water+' of water</p><p>For '+people+' '+(people>1?'people':'person')+' for '+days+' days at '+(wl>3?'1 gallon':'2 litres')+' per person per day.'+(us?' That is about '+Math.ceil(gal)+' one-gallon jugs or '+Math.ceil(L/1.5)+' 1.5-litre bottles.':' That is about '+Math.ceil(L/1.5)+' 1.5-litre bottles.')+'</p>';
h+='<p>Food: about <strong>'+fmt(kcal,0)+' calories</strong> in total ('+fmt(Math.round(kcal/days),0)+' a day). Example amounts based on the German government list:</p>';
h+='<div class="tp-scroll"><table class="tp-table"><tbody>'+F.map(f=>{const kg=f[1]*eq;return '<tr><td>'+f[0]+'</td><td><b>'+(us?fmt(kg*2.2046)+' lb':fmt(kg)+' kg')+'</b></td></tr>'}).join('')+'</tbody></table></div>';
if(p)h+='<p class="tp-note">Plus food, water and medicine for '+p+' pet'+(p>1?'s':'')+' for '+days+' days: use your pet\\'s normal daily amounts.</p>';
h+='<p class="tp-note">Children are counted at 1,600 calories and three quarters of the adult food amounts. Store foods your household already eats and that keep without a fridge.</p>';
$('esResult').innerHTML=h;
$('esPrint').innerHTML='<h2>My '+days+'-day emergency supply checklist</h2><p>'+people+' people'+(p?', '+p+' pets':'')+'. Water: '+(us?fmt(Math.ceil(gal*10)/10)+' gallons':fmt(Math.ceil(L))+' litres')+'. Food: about '+fmt(kcal,0)+' calories.</p><ul class="tp-check">'+
F.map(f=>'<li>'+f[0]+': '+(us?fmt(f[1]*eq*2.2046)+' lb':fmt(f[1]*eq)+' kg')+'</li>').join('')+
['Prescription medicines for '+days+' days','First aid kit','Flashlight and spare batteries','Battery or hand-crank radio','Phone power bank, charged','Some cash in small notes','Copies of ID and important documents','Manual can opener','Toilet paper, soap, hygiene items','Garbage bags for sanitation','Baby or pet supplies if needed'].map(x=>'<li>'+x+'</li>').join('')+'</ul>'}
document.addEventListener('DOMContentLoaded',()=>{['esAdults','esKids','esDays','esWater','esPets','esUnits'].forEach(id=>$(id).addEventListener('input',run));
document.querySelectorAll('[data-action="emergency-supply"]').forEach(b=>b.addEventListener('click',run));$('esPrintBtn').addEventListener('click',()=>{run();window.print()});run()})})();</script>""".replace('__F__', json.dumps(BBK))

bbk_rows = ''.join(f'<tr><td>{name}</td><td>{kg:g} kg ({kg * 2.2046:.1f} lb)</td></tr>' for name, kg in BBK)

body = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>How much food and water should you store for an emergency?</h2>
<p class="tp-answer">Plan on <strong>1 gallon (about 3.8 litres) of water per person per day</strong> (US Ready.gov) and about <strong>2,200 calories of food per adult per day</strong> (German government guidance).
For a family of four, 10 days means about <strong>40 gallons (150 litres) of water</strong> and 88,000 calories of food that keeps without a fridge.</p>
<p>Most governments ask for at least <strong>72 hours</strong> of supplies. Sweden and Norway suggest one week, and Germany up to 10 days. Use the calculator above for your exact household.</p></header>

<section><h2>Why are 33 countries telling people to stock up?</h2>
<p>In late October 2026, a map of at least 33 countries that advise households to keep emergency supplies spread widely online. The advice itself is not new and is not a warning about a specific event.
Governments update it as they plan for power cuts, extreme weather, cyberattacks and supply disruptions. The EU's Preparedness Union Strategy, adopted in March 2025, asks every household to be able to manage on its own for at least 72 hours.</p>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Country or region</th><th>Recommended supply</th></tr></thead><tbody>
<tr><td>European Union (Preparedness Union Strategy)</td><td>At least 72 hours</td></tr>
<tr><td>United Kingdom, France, Netherlands, Canada, Mexico, Japan</td><td>72 hours (3 days)</td></tr>
<tr><td>Sweden, Norway</td><td>About one week</td></tr>
<tr><td>Germany</td><td>Up to 10 days</td></tr>
<tr><td>United States (Ready.gov)</td><td>Several days; many US states recommend being "2 weeks ready"</td></tr>
</tbody></table></div>
<p class="tp-note">Summarised from Newsweek's October 2026 map and national guidance. Check your own government's emergency website for local advice.</p></section>

<section><h2>Germany's 10-day food list (per person)</h2>
<p>The German Federal Office of Civil Protection publishes this example for one adult for 10 days, about 2,200 calories a day, plus 20 litres of drinks:</p>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Food group</th><th>Amount for 10 days</th></tr></thead><tbody>{bbk_rows}</tbody></table></div>
<p>It is an example, not a rule. Swap in foods your household already eats, and rotate them so nothing expires.</p></section>

<section><h2>Tips that make a supply actually useful</h2>
<div class="mc-example-grid">
<section><h3>Build it slowly</h3><p>Buy one or two extra items with each weekly shop instead of everything at once. It costs less and avoids empty shelves for others.</p></section>
<section><h3>Rotate what you store</h3><p>Use the oldest items in normal cooking and replace them. Store-bought bottled water keeps until its best-before date; replace tap water you bottle yourself about every 6 months.</p></section>
<section><h3>Plan for no power</h3><p>Choose food that needs little or no cooking, keep a manual can opener, and have light, a radio and a charged power bank ready.</p></section></div></section>

<section id="esPrint" class="tp-printable"></section>

<section><h2>Sources and limitations</h2>
<p>Water guidance from <a href="https://www.ready.gov/water" rel="noopener" target="_blank">Ready.gov (FEMA)</a>. Food amounts from the German Federal Office of Civil Protection and Disaster Assistance's
<a href="https://www.ernaehrungsvorsorge.de/fileadmin/SITE_MASTER/content/Dokumente/ratgeber-englisch-disasters-alarm-3.pdf" rel="noopener" target="_blank">emergency supply guide</a>.
Country recommendations from <a href="https://www.newsweek.com/map-shows-countries-urging-residents-to-stockpile-food-12629524" rel="noopener" target="_blank">Newsweek</a> and national guidance.
People who are pregnant, nursing, ill, very active or in hot climates may need more water. This is general information, not medical advice.</p></section>

<nav class="mc-related-links" aria-label="Related tools"><h2>Related calculators</h2>
<a href="/tools/date-difference-calculator">Days Between Dates</a><a href="/tools/countdown-timer">Countdown Timer</a>
<a href="/tools/percentage-calculator">Percentage Calculator</a><a href="/date-time-tools">All date and time tools</a></nav>"""

faqs = [
    ("How much water do I need for an emergency?",
     "Ready.gov recommends at least 1 gallon (about 3.8 litres) per person per day, for drinking and basic hygiene. Germany's guidance is 2 litres per person per day for drinking and cooking. For 2 people for 10 days that is 20 gallons at the US rate."),
    ("How many days of food and water should I store?",
     "At least 72 hours is the minimum in the EU, UK, France, Canada and Japan. Sweden and Norway suggest about a week, Germany up to 10 days, and many US states recommend being ready for 2 weeks."),
    ("Why are 33 countries telling people to stockpile food?",
     "Governments are updating routine preparedness advice for power cuts, extreme weather, cyberattacks and supply disruptions. A map of at least 33 countries giving this advice went viral in October 2026. The advice is not tied to a specific announced emergency."),
    ("How much food does one person need for 10 days?",
     "About 22,000 calories, or 2,200 a day. Germany's example list for one adult is 3.5 kg of grains, bread, pasta or rice, 4 kg of vegetables and pulses, 2.5 kg of fruit and nuts, 2.6 kg of milk products, 1.5 kg of fish, meat or eggs and about 0.36 kg of fats and oils."),
    ("What should be in a basic emergency kit?",
     "Water, food that keeps without a fridge, prescription medicines, a first aid kit, a flashlight, a battery or hand-crank radio, spare batteries, a charged power bank, some cash, copies of important documents, a manual can opener and hygiene items."),
    ("How long does stored water last?",
     "Commercially bottled water keeps until its best-before date if unopened and stored somewhere cool and dark. Ready.gov suggests replacing water you store yourself about every six months."),
    ("Do I need to buy everything at once?",
     "No. Adding a few long-lasting items to each normal shop builds a supply within a few weeks, costs less and avoids panic buying."),
]

url = 'https://www.toolpinch.com/tools/emergency-supply-calculator'
title = 'Emergency Supply Calculator: Food & Water for 3, 7 or 10 Days | ToolPinch'
desc = 'How much water and food to store for your household for 3, 7, 10 or 14 days, using US Ready.gov and German government guidance. Free printable checklist.'
h1 = 'Emergency Food and Water Calculator'
app = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": h1, "description": desc, "url": url,
       "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any modern web browser", "isAccessibleForFree": True,
       "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "author": {"@type": "Organization", "name": "ToolPinch", "url": "https://www.toolpinch.com"}}
faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "ToolPinch", "item": "https://www.toolpinch.com/"},
    {"@type": "ListItem", "position": 2, "name": "Date and time tools", "item": "https://www.toolpinch.com/date-time-tools"},
    {"@type": "ListItem", "position": 3, "name": h1, "item": url}]}
html = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">'
        f'<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}">'
        f'<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:site_name" content="ToolPinch">'
        f'<meta property="og:url" content="{url}"><meta property="og:image" content="https://www.toolpinch.com/assets/icon-512.png?v=31">'
        f'{head_shared}<meta name="twitter:card" content="summary_large_image">'
        + ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (app, faq, crumbs))
        + f'{STYLE}</head><body>{header}<main id="main-content" class="mc-main"><section class="mc-tool-hero"><div class="mc-wrap mc-tool-grid"><div>'
        f'<a class="mc-back" href="/date-time-tools">Date and time tools</a><p class="mc-kicker">Updated November 2026</p><h1>{h1}</h1>'
        '<p>Work out how much water and food your household needs for 3, 7, 10 or 14 days, based on official US and German guidance, and print a checklist.</p>'
        '<div class="mc-trust"><span>Official guidance</span><span>No signup</span><span>Printable checklist</span></div></div>'
        f'{calc}</div></section><article class="mc-wrap mc-depth mc-tool-content">{body}'
        '<section class="mc-faq"><h2>Frequently asked questions</h2>' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
        + f'</section></article></main>{footer}<script src="/js/money-clock.js"></script>{script}</body></html>')
open('tools/emergency-supply-calculator.html', 'w', encoding='utf-8').write(html)
print('written', len(html))
