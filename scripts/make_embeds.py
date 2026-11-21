"""Build /embed/<slug> widgets from generated tool pages. Run from repo root after the tool builders."""
import re
from tax_common import STYLE
SLUGS = {'us-paycheck-calculator': 'US Paycheck Calculator', 'tax-refund-estimator': 'Tax Refund Estimator',
         'holiday-pay-calculator': 'Holiday Pay Calculator'}
for slug, name in SLUGS.items():
    h = open(f'tools/{slug}.html', encoding='utf-8').read()
    i = h.index('<div class="mc-calculator">'); j = h.index('</div></section><article', i)
    calc = h[i:j]
    k = h.index('<script src="/js/money-clock.js"></script>') + len('<script src="/js/money-clock.js"></script>')
    script = h[k:h.index('</body>')]
    links = re.search(r'<link rel="stylesheet"[^>]*>(?:<link rel="stylesheet"[^>]*>)*', h)
    css = links.group(0) if links else '<link rel="stylesheet" href="/css/style.css"><link rel="stylesheet" href="/css/v2.css"><link rel="stylesheet" href="/css/money-clock.css?v=31">'
    out = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<meta name="robots" content="noindex,follow"><title>{name} widget | ToolPinch</title><link rel="canonical" href="https://www.toolpinch.com/tools/{slug}">'
           f'{css}{STYLE}<style>html,body{{background:transparent;margin:0}}body{{padding:8px}}.mc-calculator{{margin:0;max-width:none;box-shadow:none}}'
           '.tp-embed-foot{font-size:12px;text-align:right;margin:6px 4px 0;opacity:.85}.tp-embed-foot a{color:inherit}</style></head><body>'
           f'{calc}<p class="tp-embed-foot">Free calculator by <a href="https://www.toolpinch.com/tools/{slug}?utm_source=embed&amp;utm_medium=widget" target="_blank" rel="noopener">ToolPinch</a></p>'
           '<script src="/js/money-clock.js"></script>' + script +
           '<script>(()=>{const send=()=>{try{parent.postMessage({toolpinch:"resize",h:document.documentElement.scrollHeight},"*")}catch(e){}};new ResizeObserver(send).observe(document.body);addEventListener("load",send)})();</script></body></html>')
    open(f'embed/{slug}.html', 'w', encoding='utf-8').write(out)
    print('embed', slug, len(out))
