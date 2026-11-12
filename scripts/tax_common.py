"""Shared page builder for ToolPinch tax pages. Run builders from the repo root."""
import json
import re

template = open('tools/overtime-calculator.html', encoding='utf-8').read()
head_shared = re.search(r'(<link rel="icon".*?crossorigin="anonymous"></script>)', template).group(1)
header = re.search(r'(<a class="mc-skip-link".*?</header>)', template).group(1)
footer = re.search(r'(<footer class="mc-footer">.*?</footer>)', template).group(1)
assert 'G-8WM8MS9X9Y' in head_shared and 'ca-pub-3789885855212646' in head_shared

STYLE = """<style>
.tp-big{font-size:1.2rem;margin:0 0 6px}.tp-big strong{font-size:2rem}
.tp-table{width:100%;border-collapse:collapse;font-size:.9rem;margin:10px 0}
.tp-table th,.tp-table td{padding:7px 8px;border-bottom:1px solid rgba(0,0,0,.12);text-align:left;vertical-align:top}
.tp-table th{font-weight:700}.tp-table td.n,.tp-table th.n{text-align:right;white-space:nowrap}.tp-scroll{overflow-x:auto}
.tp-answer{font-size:1.05rem;border-left:4px solid #1a7f5a;padding:6px 12px;margin:12px 0}
.tp-note{font-size:.86rem;opacity:.9}
.tp-actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.tp-btn{border:1px solid rgba(0,0,0,.2);background:#fff;border-radius:8px;padding:8px 12px;font:inherit;font-size:.9rem;cursor:pointer;color:#16325c}
.tp-btn:hover{background:#eef3fb}.mc-calculator select,.mc-calculator input{width:100%}
.mc-calculator>p,.tp-actions,.tp-wide{grid-column:1/-1}
.tp-res .tp-table{font-size:.88rem;margin:6px 0}.tp-res .tp-table td{padding:5px 6px}
.tp-res tr.tot td{font-weight:700;border-top:2px solid rgba(0,0,0,.25)}
.tp-bar{display:flex;height:12px;border-radius:6px;overflow:hidden;margin:8px 0 4px;background:#e6e9ef}
.tp-bar i{display:block;height:100%}.tp-key{display:flex;flex-wrap:wrap;gap:4px 12px;font-size:.8rem}.tp-key span:before{content:"";display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:4px;background:var(--c)}
.tp-filter{width:100%;max-width:360px;padding:8px 10px;border:1px solid rgba(0,0,0,.25);border-radius:8px;font:inherit;margin:6px 0}
.tp-seg{display:flex;gap:6px;flex-wrap:wrap}.tp-seg label{display:flex;align-items:center;gap:5px;font-size:.92rem}
.tp-seg input{width:auto!important}
</style>"""

PERIOD_JS = """const PER={year:1,month:12,biweek:26,week:52};"""


def page(slug, title, desc, h1, kicker, intro, trust, calc, body, faqs, script, crumb=('Pay calculators', '/pay-calculators'), back='Pay calculators'):
    url = f'https://www.toolpinch.com/tools/{slug}'
    app = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": h1, "description": desc, "url": url,
           "applicationCategory": "FinanceApplication", "operatingSystem": "Any modern web browser", "isAccessibleForFree": True,
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
           "author": {"@type": "Organization", "name": "ToolPinch", "url": "https://www.toolpinch.com"}}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', a)}} for q, a in faqs]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "ToolPinch", "item": "https://www.toolpinch.com/"},
        {"@type": "ListItem", "position": 2, "name": crumb[0], "item": "https://www.toolpinch.com" + crumb[1]},
        {"@type": "ListItem", "position": 3, "name": h1, "item": url}]}
    html = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">'
            f'<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}">'
            f'<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:site_name" content="ToolPinch">'
            f'<meta property="og:url" content="{url}"><meta property="og:image" content="https://www.toolpinch.com/assets/icon-512.png?v=31">'
            f'{head_shared}<meta name="twitter:card" content="summary_large_image">'
            + ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (app, faq, crumbs))
            + f'{STYLE}</head><body>{header}<main id="main-content" class="mc-main"><section class="mc-tool-hero"><div class="mc-wrap mc-tool-grid"><div>'
            f'<a class="mc-back" href="{crumb[1]}">{back}</a><p class="mc-kicker">{kicker}</p><h1>{h1}</h1><p>{intro}</p>'
            '<div class="mc-trust">' + ''.join(f'<span>{t}</span>' for t in trust) + '</div></div>'
            f'{calc}</div></section><article class="mc-wrap mc-depth mc-tool-content">{body}'
            '<section class="mc-faq"><h2>Frequently asked questions</h2>' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
            + f'</section></article></main>{footer}<script src="/js/money-clock.js"></script>{script}</body></html>')
    open(f'tools/{slug}.html', 'w', encoding='utf-8').write(html)
    print('written', slug, len(html))


# shared JS: progressive bracket tax. brackets = [[lowerThreshold, rate], ...] ascending; below first threshold is 0%.
BT_JS = """const BT=(x,b)=>{let t=0;for(let i=0;i<b.length;i++){const lo=b[i][0],hi=i+1<b.length?b[i+1][0]:Infinity;if(x>lo)t+=(Math.min(x,hi)-lo)*b[i][1]}return t};"""

# shared JS: result renderer. rows = [[label, annual, colour|null]], gross, net, cur formatter
RENDER_JS = """const COL=['#1a7f5a','#c0392b','#e67e22','#2c6fbb','#8e44ad','#16a085','#7f8c8d','#d35400'];
function renderRes(el,gross,rows,net,fmt,per){const P={year:['Year',1],month:['Month',12],biweek:['2 weeks',26],week:['Week',52]};const d=P[per]||P.year;
const ded=rows.filter(r=>r[1]>0.004);let bar='',key='';const tot=Math.max(gross,1);
bar+='<i style="width:'+(Math.max(net,0)/tot*100).toFixed(2)+'%;background:'+COL[0]+'"></i>';key+='<span style="--c:'+COL[0]+'">Take-home</span>';
ded.forEach((r,i)=>{const c=COL[(i+1)%COL.length];bar+='<i style="width:'+(r[1]/tot*100).toFixed(2)+'%;background:'+c+'"></i>';key+='<span style="--c:'+c+'">'+r[0]+'</span>'});
let h='<p class="tp-big"><strong>'+fmt(net/d[1])+'</strong> take-home per '+d[0].toLowerCase()+'</p>';
h+='<div class="tp-bar">'+bar+'</div><div class="tp-key">'+key+'</div>';
const one=d[1]===1,cell=(x,neg)=>(one?'':'<td class="n">'+(neg?'−':'')+fmt(x/d[1])+'</td>')+'<td class="n">'+(neg?'−':'')+fmt(x)+'</td>';
h+='<div class="tp-scroll"><table class="tp-table"><thead><tr><th></th>'+(one?'':'<th class="n">Per '+d[0].toLowerCase()+'</th>')+'<th class="n">Year</th></tr></thead><tbody>';
h+='<tr><td>Gross pay</td>'+cell(gross,false)+'</tr>';
rows.forEach(r=>{h+='<tr><td>'+r[0]+'</td>'+cell(Math.abs(r[1]),r[1]>0)+'</tr>'});
h+='<tr class="tot"><td>Take-home pay</td>'+cell(net,false)+'</tr></tbody></table></div>';
const taxes=rows.reduce((s,r)=>s+(r[2]?r[1]:0),0);
h+='<p class="tp-note">Tax and deductions take <b>'+(gross>0?(100*(gross-net)/gross).toFixed(1):'0.0')+'%</b> of gross pay.'+(gross>0?' Average income tax rate '+(100*taxes/gross).toFixed(1)+'%.':'')+'</p>';
el.innerHTML=h}"""

PERIOD_SELECT = """<label class="mc-field"><span>Show results per</span><select id="per"><option value="year">Year</option><option value="month" selected>Month</option><option value="biweek">2 weeks</option><option value="week">Week</option></select></label>"""

TAX_LINKS = [('/tools/vat-calculator', 'VAT calculator (all countries)'), ('/tools/us-paycheck-calculator', 'US paycheck calculator'),
             ('/tools/uk-take-home-pay-calculator', 'UK take-home pay'), ('/tools/canada-take-home-pay-calculator', 'Canada take-home pay'),
             ('/tools/australia-take-home-pay-calculator', 'Australia take-home pay'), ('/tools/india-income-tax-calculator', 'India income tax'),
             ('/tools/pakistan-salary-tax-calculator', 'Pakistan salary tax'), ('/tools/2027-tax-brackets', '2027 US tax brackets'), ('/tools/bonus-tax-calculator', 'Bonus tax calculator')]


def related(slug, extra=()):
    links = [l for l in TAX_LINKS if not l[0].endswith(slug)] + list(extra)
    return ('<nav class="mc-related-links" aria-label="Related tools"><h2>Related calculators</h2>'
            + ''.join(f'<a href="{h}">{t}</a>' for h, t in links) + '</nav>')
