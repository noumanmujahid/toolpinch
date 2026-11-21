"""Nov 2026: remove off-topic SEO, novelty and thin math pages and every link to them. Run from repo root."""
import os, re, glob
REMOVE = """search-social-preview seo-page-audit structured-data-builder domain-verification-helper sitemap-indexing-checker robots-txt-tester
readability-checker keyword-suggestion-tool slug-generator meta-description-generator seo-title-generator serp-preview-tool keyword-research-tool
meta-description-length-checker horoscope-calculator age-on-planets planet-time-calculator life-in-weeks dice-roller random-number-generator
prime-factor-calculator probability-calculator exponent-root-calculator circle-calculator slope-calculator distance-midpoint-calculator
area-perimeter-calculator right-triangle-calculator volume-calculator quadratic-calculator rounding-calculator lcm-gcf-calculator
hex-binary-calculator roof-area-calculator arithmetic-sequence-calculator""".split()
paths = ['/tools/' + s for s in REMOVE] + ['/seo-tools']
for s in REMOVE:
    if os.path.exists(f'tools/{s}.html'): os.remove(f'tools/{s}.html')
for f in ['seo-tools.html', 'js/seo-suite.js', 'functions/api/seo-fetch.js', 'functions/api/dns-txt.js']:
    if os.path.exists(f): os.remove(f)
alt = '|'.join(re.escape(p) for p in sorted(paths, key=len, reverse=True))
href = rf'href="(?:https://www\.toolpinch\.com)?(?:{alt})(?:\.html)?(?:[#?][^"]*)?"'
changed = 0
for f in glob.glob('*.html') + glob.glob('tools/*.html') + glob.glob('embed/*.html'):
    h = o = open(f, encoding='utf-8').read()
    h = re.sub(r'<section class="mc-category-band tool-category" id="seo-tools">.*?</section>', '', h, flags=re.S)
    h = re.sub(r'<a class="mc-card"[^>]*' + href + r'[^>]*>.*?</a>', '', h, flags=re.S)       # tool cards
    h = re.sub(r'<a [^>]*' + href + r'[^>]*>.*?</a>', '', h, flags=re.S)                       # nav, footer and related links
    if h != o:
        open(f, 'w', encoding='utf-8').write(h); changed += 1
sm = open('sitemap.xml').read()
sm2 = re.sub(r'\s*<url>\s*<loc>https://www\.toolpinch\.com(?:' + alt + r')</loc>.*?</url>', '', sm, flags=re.S)
open('sitemap.xml', 'w').write(sm2)
red = [l for l in open('_redirects').read().splitlines() if not re.search(r'\s(?:' + alt + r')\s', ' ' + l + ' ')]
open('_redirects', 'w').write('\n'.join(red) + '\n')
print('removed', len(REMOVE), 'pages; edited', changed, 'files; sitemap urls', sm2.count('<loc>'))
