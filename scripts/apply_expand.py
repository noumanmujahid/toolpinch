import json,re,sys
sys.path.insert(0,'scripts')
from expand_content import C
STY='<style>.tp-table{width:100%;border-collapse:collapse;font-size:.92rem;margin:10px 0}.tp-table th,.tp-table td{padding:7px 8px;border-bottom:1px solid rgba(0,0,0,.12);text-align:left;vertical-align:top}.tp-table th{font-weight:700}.tp-table .n{text-align:right;white-space:nowrap}.tp-scroll{overflow-x:auto}.tp-answer{font-size:1.05rem;border-left:4px solid #1a7f5a;padding:6px 12px;margin:12px 0}.tp-note{font-size:.86rem;opacity:.9}</style>'
for slug,(ans,body,faqs) in C.items():
    f=f'tools/{slug}.html'; s=open(f,encoding='utf-8').read()
    a0=s.index('<article class="mc-wrap mc-depth mc-tool-content">')+len('<article class="mc-wrap mc-depth mc-tool-content">')
    a1=s.index('<nav class="mc-related-links"',a0)
    faq_html='<section class="mc-faq"><h2>Frequently asked questions</h2>'+''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)+'</section>'
    new=f'<header><p class="mc-kicker mc-dark">The short answer</p><h2>How it works</h2><p class="tp-answer">{ans}</p></header>{body}{faq_html}'
    s=s[:a0]+new+s[a1:]
    # JSON-LD FAQ
    m=re.search(r'<script type="application/ld\+json">(\{"@context":"https://schema.org","@graph":.*?)</script>',s)
    g=json.loads(m.group(1))
    for node in g['@graph']:
        if node.get('@type')=='FAQPage':
            node['mainEntity']=[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a)}} for q,a in faqs]
    s=s[:m.start(1)]+json.dumps(g,ensure_ascii=False,separators=(',',':'))+s[m.end(1):]
    if 'tp-answer{' not in s: s=s.replace('</head>',STY+'</head>',1)
    open(f,'w',encoding='utf-8').write(s)
    w=len(re.sub(r'<[^>]+>',' ',re.sub(r'<script.*?</script>|<style.*?</style>','',re.search(r'<main.*?</main>',s,re.S).group(0),flags=re.S)).split())
    print(slug,w)
