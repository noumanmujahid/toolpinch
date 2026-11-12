"""Build the shopping / Black Friday calculators. Run from repo root: PYTHONPATH=scripts python3 scripts/build_shopping.py"""
from tax_common import page

SHOP = [('/tools/black-friday-deal-calculator', 'Black Friday deal calculator'), ('/tools/unit-price-calculator', 'Unit price comparison'),
        ('/tools/bnpl-calculator', 'Buy now, pay later cost'), ('/tools/price-adjustment-calculator', 'Price drop refund calculator'),
        ('/tools/discount-calculator', 'Discount calculator'), ('/tools/percentage-calculator', 'Percentage calculator'), ('/tools/vat-calculator', 'VAT / sales tax calculator')]


def rel(slug):
    return ('<nav class="mc-related-links" aria-label="Related tools"><h2>Related calculators</h2>'
            + ''.join(f'<a href="{h}">{t}</a>' for h, t in SHOP if not h.endswith(slug)) + '</nav>')


CR = ('Pay calculators', '/pay-calculators')
FMT = "const f=x=>x.toLocaleString('en-US',{style:'currency',currency:'USD'}),$=id=>document.getElementById(id),v=id=>Math.max(0,+$(id).value||0);"


def wire(ids, action, fn='run'):
    return ("document.addEventListener('DOMContentLoaded',()=>{" + ''.join(f"$('{i}').addEventListener('input',{fn});" for i in ids)
            + f"document.querySelectorAll('[data-action=\"{action}\"]').forEach(b=>b.addEventListener('click',{fn}));{fn}()}})")


# ---------------- 1. Black Friday deal calculator ----------------
calc = """<div class="mc-calculator"><h2>What will you really pay?</h2>
<label class="mc-field"><span>Original price ($)</span><input id="dP" type="number" min="0" step="0.01" value="200"></label>
<label class="mc-field"><span>Sale discount (%)</span><input id="dA" type="number" min="0" max="100" step="0.5" value="30"></label>
<label class="mc-field"><span>Extra % off at checkout</span><input id="dB" type="number" min="0" max="100" step="0.5" value="10"></label>
<label class="mc-field"><span>Coupon ($ off)</span><input id="dC" type="number" min="0" step="0.01" value="0"></label>
<label class="mc-field"><span>Sales tax (%)</span><input id="dT" type="number" min="0" max="20" step="0.01" value="7"></label>
<label class="mc-field"><span>Shipping ($)</span><input id="dS" type="number" min="0" step="0.01" value="0"></label>
<button class="mc-button" data-action="deal">Calculate</button>
<div class="mc-result tp-res" id="dR" aria-live="polite">Enter the deal details.</div></div>"""
script = "<script>(()=>{" + FMT + """
function run(){const p=v('dP'),a=Math.min(100,v('dA')),b=Math.min(100,v('dB')),c=v('dC'),t=v('dT'),s=v('dS');
const s1=p*(1-a/100),s2=s1*(1-b/100),s3=Math.max(0,s2-c),tax=s3*t/100,tot=s3+tax+s,save=p-s3,eff=p?100*save/p:0;
let h='<p class="tp-big"><strong>'+f(tot)+'</strong> total to pay</p><div class="tp-scroll"><table class="tp-table"><tbody>'+
'<tr><td>Original price</td><td class="n">'+f(p)+'</td></tr>'+(a?'<tr><td>After '+a+'% sale</td><td class="n">'+f(s1)+'</td></tr>':'')+(b?'<tr><td>After extra '+b+'% off</td><td class="n">'+f(s2)+'</td></tr>':'')+
(c?'<tr><td>After $'+c+' coupon</td><td class="n">'+f(s3)+'</td></tr>':'')+'<tr><td>Sales tax ('+t+'%)</td><td class="n">'+f(tax)+'</td></tr>'+(s?'<tr><td>Shipping</td><td class="n">'+f(s)+'</td></tr>':'')+
'<tr class="tot"><td>Total</td><td class="n">'+f(tot)+'</td></tr></tbody></table></div>';
h+='<p>You save <b>'+f(save)+'</b>, a real discount of <b>'+eff.toFixed(1)+'%</b>'+(a&&b?' (not '+(a+b)+'%, because the second discount applies to the already reduced price)':'')+'.</p>';$('dR').innerHTML=h}
""" + wire(['dP', 'dA', 'dB', 'dC', 'dT', 'dS'], 'deal') + "})();</script>"
body = """
<header><p class="mc-kicker mc-dark">The short answer</p><h2>How do stacked Black Friday discounts work?</h2>
<p class="tp-answer">Discounts multiply, they do not add. <strong>30% off</strong> plus an <strong>extra 10% off</strong> is 0.70 × 0.90 = 0.63 of the price, a real discount of <strong>37%</strong>, not 40%. On a $200 item you pay $126 before tax.
Sales tax is then charged on the discounted price, so with 7% tax the total is <strong>$134.82</strong>.</p>
<p><strong>Black Friday 2026 is Friday, November 27</strong>, the day after Thanksgiving (November 26). Cyber Monday is November 30.</p></header>
<section><h2>Stacked discount table</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Sale</th><th class="n">+ extra 10%</th><th class="n">+ extra 15%</th><th class="n">+ extra 20%</th></tr></thead><tbody>
<tr><td>20% off</td><td class="n">28% off</td><td class="n">32% off</td><td class="n">36% off</td></tr>
<tr><td>25% off</td><td class="n">32.5% off</td><td class="n">36.25% off</td><td class="n">40% off</td></tr>
<tr><td>30% off</td><td class="n">37% off</td><td class="n">40.5% off</td><td class="n">44% off</td></tr>
<tr><td>40% off</td><td class="n">46% off</td><td class="n">49% off</td><td class="n">52% off</td></tr>
<tr><td>50% off</td><td class="n">55% off</td><td class="n">57.5% off</td><td class="n">60% off</td></tr></tbody></table></div>
<p>Formula: total discount = 1 − (1 − first) × (1 − second). A fixed-dollar coupon is worth more on a cheap item: $20 off a $50 item is 40%, but only 10% on a $200 item.</p></section>
<section><h2>Is it really a deal? A checklist</h2><ul>
<li><strong>Check the "was" price.</strong> Some retailers raise the reference price before a sale. Price-history tools and the store's own price over the past few weeks show whether the discount is real.</li>
<li><strong>Compare the final total, not the percentage.</strong> Shipping, tax and membership requirements can erase a headline saving.</li>
<li><strong>Compare per unit.</strong> Bigger packs and bundles are not always cheaper; use the unit price calculator.</li>
<li><strong>Know the return and price-adjustment rules.</strong> Some stores refund the difference if the price drops again after you buy.</li>
<li><strong>Think about financing.</strong> Splitting a purchase with buy now, pay later is only free if every payment is on time.</li>
<li><strong>Set a budget first.</strong> A 40% discount on something you did not plan to buy is still spending.</li></ul></section>
<section><h2>Worked examples</h2><div class="mc-example-grid">
<div><h3>TV</h3><p>$899 TV, 25% off, $50 coupon, 8% tax: 899 × 0.75 = $674.25, − $50 = $624.25, + tax = <b>$674.19</b>. Real saving 30.6%.</p></div>
<div><h3>Clothing</h3><p>$80 jacket, 40% off, extra 20% at checkout, $6 shipping, no tax: 80 × 0.6 × 0.8 = $38.40 + $6 = <b>$44.40</b>.</p></div>
<div><h3>Small item with a coupon</h3><p>$35 item, $15 off a $35 purchase: you pay $20, a 43% discount; one item at $34.99 would not qualify.</p></div></div></section>
""" + rel('black-friday-deal-calculator')
faqs = [("How do I calculate two discounts together?", "Multiply the remaining shares of the price. 30% off then 10% off leaves 0.7 × 0.9 = 63% of the price, which is 37% off in total."),
        ("Is sales tax charged before or after a discount?", "Usually after: sales tax is charged on the price you actually pay. Manufacturer coupons are treated differently in some US states."),
        ("When is Black Friday 2026?", "Friday, November 27, 2026. Thanksgiving is Thursday, November 26, and Cyber Monday is November 30."),
        ("Is a percentage coupon or a dollar coupon better?", "It depends on the price. A $20 coupon beats 10% off on items under $200; above $200, 10% off saves more."),
        ("How can I tell if a Black Friday deal is real?", "Compare against the price over the previous weeks, not the store's list price, and compare the final total including shipping and tax."),
        ("Does the order of discounts matter?", "For two percentage discounts, no: 30% then 10% gives the same result as 10% then 30%. A dollar coupon applied before a percentage discount saves less than one applied after.")]
page('black-friday-deal-calculator', 'Black Friday Deal Calculator 2026: Stacked Discounts, Coupons and Tax | ToolPinch',
     'Work out the real price of a Black Friday or Cyber Monday deal with stacked discounts, coupons, sales tax and shipping. Black Friday 2026 is November 27.',
     'Black Friday Deal Calculator', 'Black Friday: Nov 27, 2026 · Cyber Monday: Nov 30',
     'Combine a sale discount, an extra percentage off, a coupon, sales tax and shipping to see the real final price and the true discount.',
     ['Stacked discounts', 'Tax and shipping', 'No signup'], calc, body, faqs, script, crumb=CR)

# ---------------- 2. Unit price calculator ----------------
UNITS = {'oz': ('w', 28.349523125), 'lb': ('w', 453.59237), 'g': ('w', 1), 'kg': ('w', 1000),
         'fl oz': ('v', 29.5735295625), 'ml': ('v', 1), 'l': ('v', 1000), 'gal': ('v', 3785.411784), 'count': ('c', 1)}
uopts = ''.join(f'<option value="{u}">{u}</option>' for u in UNITS)
rows = ''
for i, (pr, q, u) in enumerate([(4.99, 12, 'oz'), (8.49, 24, 'oz'), (11.99, 2, 'lb')], 1):
    rows += (f'<div class="tp-wide" style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px"><label class="mc-field"><span>Item {i} price ($)</span><input id="uP{i}" type="number" min="0" step="0.01" value="{pr}"></label>'
             f'<label class="mc-field"><span>Size</span><input id="uQ{i}" type="number" min="0" step="any" value="{q}"></label>'
             f'<label class="mc-field"><span>Unit</span><select id="uU{i}">{uopts.replace(f"value=\"{u}\"", f"value=\"{u}\" selected")}</select></label></div>')
calc = f"""<div class="mc-calculator"><h2>Which is cheaper?</h2>{rows}
<button class="mc-button" data-action="unit">Compare</button>
<div class="mc-result tp-res" id="uR" aria-live="polite">Enter prices and sizes.</div></div>"""
import json
script = "<script>(()=>{const U=" + json.dumps(UNITS) + ";" + FMT + """
const show={w:['oz',28.349523125,'100 g',100],v:['fl oz',29.5735295625,'100 ml',100],c:['item',1,'item',1]};
function run(){const it=[1,2,3].map(i=>({i,p:v('uP'+i),q:v('uQ'+i),u:$('uU'+i).value})).filter(x=>x.p>0&&x.q>0);if(!it.length){$('uR').textContent='Enter prices and sizes.';return}
const k=U[it[0].u][0];if(it.some(x=>U[x.u][0]!==k)){$('uR').innerHTML='<p>Choose units of the same kind (all weight, all volume or all counts) to compare.</p>';return}
it.forEach(x=>{x.base=x.p/(x.q*U[x.u][1])});const best=it.reduce((a,b)=>b.base<a.base?b:a),s=show[k];
let h='<p class="tp-big"><strong>Item '+best.i+'</strong> is the best value</p><div class="tp-scroll"><table class="tp-table"><thead><tr><th>Item</th><th class="n">Per '+s[0]+'</th><th class="n">Per '+s[2]+'</th><th class="n">vs best</th></tr></thead><tbody>';
it.forEach(x=>{h+='<tr'+(x===best?' class="tot"':'')+'><td>Item '+x.i+' ('+f(x.p)+' for '+x.q+' '+x.u+')</td><td class="n">'+f(x.base*s[1])+'</td><td class="n">'+f(x.base*s[3])+'</td><td class="n">'+(x===best?'Best':'+'+(100*(x.base/best.base-1)).toFixed(1)+'%')+'</td></tr>'});
h+='</tbody></table></div>';const worst=it.reduce((a,b)=>b.base>a.base?b:a);if(worst!==best)h+='<p>Buying the same amount as item '+worst.i+' at item '+best.i+'\\'s unit price would save <b>'+f(worst.p-best.base*worst.q*U[worst.u][1])+'</b>.</p>';$('uR').innerHTML=h}
""" + wire([f'{a}{i}' for i in (1, 2, 3) for a in ('uP', 'uQ', 'uU')], 'unit') + "})();</script>"
body = """
<header><p class="mc-kicker mc-dark">The short answer</p><h2>How do you compare unit prices?</h2>
<p class="tp-answer">Divide the price by the quantity. A <strong>$4.99</strong> 12-ounce bag costs 4.99 ÷ 12 = <strong>41.6¢ per ounce</strong>; a <strong>$8.49</strong> 24-ounce bag costs <strong>35.4¢ per ounce</strong>, so the bigger bag is 15% cheaper per ounce.
When sizes use different units, convert first: 1 lb = 16 oz = 453.6 g, 1 kg = 2.2 lb, and 1 US gallon = 128 fl oz = 3.785 litres.</p></header>
<section><h2>Unit conversions</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>From</th><th>Equals</th></tr></thead><tbody>
<tr><td>1 ounce (oz)</td><td>28.35 grams</td></tr><tr><td>1 pound (lb)</td><td>16 oz = 453.6 g</td></tr><tr><td>1 kilogram (kg)</td><td>1,000 g = 2.205 lb</td></tr>
<tr><td>1 US fluid ounce (fl oz)</td><td>29.57 ml</td></tr><tr><td>1 litre (l)</td><td>33.81 fl oz</td></tr><tr><td>1 US gallon (gal)</td><td>128 fl oz = 3.785 l</td></tr></tbody></table></div>
<p class="tp-note">Weight ounces (oz) and fluid ounces (fl oz) measure different things; compare weight with weight and volume with volume.</p></section>
<section><h2>When bigger is not cheaper</h2><ul>
<li><strong>Sales on small sizes.</strong> A discounted small pack can beat the regular price of the family size.</li>
<li><strong>Multi-buy offers.</strong> "2 for $5" on 10-oz cans is 25¢ per ounce; compare it with the large can's unit price rather than assuming the deal wins.</li>
<li><strong>Waste.</strong> The cheapest unit price only saves money if you use it all before it spoils or expires.</li>
<li><strong>Shelf labels.</strong> Shelf tags show unit prices, but stores sometimes use different units for similar products (per ounce versus per count); convert before comparing.</li></ul></section>
<section><h2>Worked examples</h2><div class="mc-example-grid">
<div><h3>Coffee</h3><p>$11.99 for 2 lb (32 oz) is 37.5¢ per ounce, about 6% more than the 24-oz bag at 35.4¢.</p></div>
<div><h3>Laundry detergent</h3><p>$13.97 for 92 fl oz is 15.2¢/fl oz; $19.97 for 150 fl oz is 13.3¢/fl oz. The large bottle saves about 12%.</p></div>
<div><h3>Paper towels</h3><p>Compare per sheet or per square foot, not per roll; "double rolls" vary between brands.</p></div></div></section>
""" + rel('unit-price-calculator')
faqs = [("How do I calculate unit price?", "Divide the price by the quantity in the same unit. $8.49 for 24 oz is 8.49 ÷ 24 = $0.354 per ounce."),
        ("How do I compare prices in ounces and grams?", "Convert to one unit first: 1 ounce = 28.35 grams. The calculator converts automatically."),
        ("Is the bigger size always cheaper?", "No. Sales on smaller sizes and multi-buy offers can make smaller packs cheaper per unit, so compare the unit price each time."),
        ("How many ounces are in a pound?", "16 ounces (weight)."),
        ("Can I compare a weight with a volume?", "Not directly. Ounces of weight and fluid ounces of volume measure different things; compare products sold in the same kind of unit.")]
page('unit-price-calculator', 'Unit Price Calculator: Compare Price per Ounce, Pound, Gram or Litre | ToolPinch',
     'Compare up to three products by price per ounce, pound, gram, kilogram, fluid ounce, litre or item to find the best value. Converts units automatically.',
     'Unit Price Comparison Calculator', 'Smart shopping',
     'Compare package sizes and find which product is really cheaper per ounce, pound, gram, litre or item.',
     ['Up to 3 products', 'Automatic unit conversion', 'No signup'], calc, body, faqs, script, crumb=CR)

# ---------------- 3. Buy now, pay later ----------------
calc = """<div class="mc-calculator"><h2>What does the plan really cost?</h2>
<label class="mc-field"><span>Purchase price ($)</span><input id="bP" type="number" min="0" step="0.01" value="600"></label>
<label class="mc-field"><span>Plan type</span><select id="bT"><option value="p4">Pay in 4 (every 2 weeks)</option><option value="mo">Monthly installments with APR</option></select></label>
<label class="mc-field" data-p="mo"><span>Number of monthly payments</span><input id="bN" type="number" min="1" max="60" step="1" value="12"></label>
<label class="mc-field" data-p="mo"><span>APR (%)</span><input id="bA" type="number" min="0" max="40" step="0.1" value="20"></label>
<label class="mc-field" data-p="mo"><span>Down payment ($)</span><input id="bD" type="number" min="0" step="0.01" value="0"></label>
<label class="mc-field"><span>Late fee per missed payment ($)</span><input id="bL" type="number" min="0" step="0.01" value="7"></label>
<label class="mc-field"><span>Late payments you expect</span><input id="bM" type="number" min="0" max="60" step="1" value="0"></label>
<button class="mc-button" data-action="bnpl">Calculate</button>
<div class="mc-result tp-res" id="bR" aria-live="polite">Enter the plan details.</div></div>"""
script = "<script>(()=>{" + FMT + """
function vis(){const t=$('bT').value;document.querySelectorAll('[data-p]').forEach(e=>e.hidden=e.dataset.p!==t)}
function run(){vis();const p=v('bP'),t=$('bT').value,late=v('bL')*v('bM');let h;
if(t==='p4'){const pay=p/4,tot=p+late;h='<p class="tp-big"><strong>'+f(pay)+'</strong> every two weeks, 4 times</p><div class="tp-scroll"><table class="tp-table"><tbody>'+
'<tr><td>Today</td><td class="n">'+f(pay)+'</td></tr><tr><td>In 2 weeks</td><td class="n">'+f(pay)+'</td></tr><tr><td>In 4 weeks</td><td class="n">'+f(pay)+'</td></tr><tr><td>In 6 weeks</td><td class="n">'+f(pay)+'</td></tr>'+
(late?'<tr><td>Late fees</td><td class="n">'+f(late)+'</td></tr>':'')+'<tr class="tot"><td>Total paid</td><td class="n">'+f(tot)+'</td></tr></tbody></table></div>';
h+=late?'<p>Late fees add <b>'+(100*late/p).toFixed(1)+'%</b> to the price. Over six weeks, that is like paying an annual rate of roughly '+Math.round(100*late/p*52/6)+'%.</p>':'<p>Paid on time, pay-in-4 plans usually cost nothing extra.</p>'}
else{const n=Math.max(1,Math.round(v('bN'))),a=v('bA'),d=Math.min(p,v('bD')),P=p-d,r=a/1200,pay=r?P*r/(1-Math.pow(1+r,-n)):P/n,int=pay*n-P,tot=d+pay*n+late;
h='<p class="tp-big"><strong>'+f(pay)+'</strong> a month for '+n+' months</p><div class="tp-scroll"><table class="tp-table"><tbody>'+(d?'<tr><td>Down payment</td><td class="n">'+f(d)+'</td></tr>':'')+
'<tr><td>Amount financed</td><td class="n">'+f(P)+'</td></tr><tr><td>Interest</td><td class="n">'+f(int)+'</td></tr>'+(late?'<tr><td>Late fees</td><td class="n">'+f(late)+'</td></tr>':'')+
'<tr class="tot"><td>Total paid</td><td class="n">'+f(tot)+'</td></tr></tbody></table></div><p>Financing costs <b>'+f(tot-p)+'</b> ('+(p?(100*(tot-p)/p).toFixed(1):0)+'% of the price) compared with paying up front.</p>'}
$('bR').innerHTML=h}
document.addEventListener('DOMContentLoaded',()=>{['bP','bT','bN','bA','bD','bL','bM'].forEach(i=>$(i).addEventListener('input',run));document.querySelectorAll('[data-action="bnpl"]').forEach(b=>b.addEventListener('click',run));run()})})();</script>"""


def amort(P, apr, n):
    r = apr / 1200
    return P * r / (1 - (1 + r) ** -n) if r else P / n


ex = ''
for P, apr, n in [(600, 0, 6), (600, 15, 12), (600, 30, 12), (1500, 20, 24), (1500, 36, 24)]:
    pay = amort(P, apr, n)
    ex += f'<tr><td>${P:,}</td><td class="n">{apr}%</td><td class="n">{n}</td><td class="n">${pay:,.2f}</td><td class="n">${pay*n-P:,.2f}</td></tr>'
body = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>Is buy now, pay later free?</h2>
<p class="tp-answer"><strong>Pay-in-4 plans</strong> split a purchase into four payments two weeks apart and usually charge no interest if every payment is on time; late fees are the main cost.
<strong>Longer monthly plans</strong> often charge interest: $600 over 12 months at 20% APR costs about <strong>${amort(600,20,12)*12-600:,.2f}</strong> in interest. Use the calculator to see the real total before you check out.</p></header>
<section><h2>Monthly plan costs</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Price</th><th class="n">APR</th><th class="n">Months</th><th class="n">Monthly payment</th><th class="n">Total interest</th></tr></thead><tbody>{ex}</tbody></table></div>
<p class="tp-note">Fixed-rate installments. Providers set APRs from 0% to around 36% depending on the merchant and your credit, and some charge fees instead of interest.</p></section>
<section><h2>Things to check before you split a payment</h2><ul>
<li><strong>Late fees and what happens after a missed payment.</strong> Fees, account suspension and collections policies differ by provider.</li>
<li><strong>Credit reporting.</strong> Some providers report payments to credit bureaus, and longer financing may involve a credit check.</li>
<li><strong>Returns.</strong> If you return the item, keep paying until the refund is processed and the plan is updated, or you can be charged late fees.</li>
<li><strong>Several plans at once.</strong> Four small plans can add up to more than your budget allows; total all upcoming payments.</li>
<li><strong>Debit versus credit card.</strong> Paying installments from a debit card can overdraw your account; a missed payment on a credit card adds that card's interest.</li></ul></section>
{rel('bnpl-calculator')}"""
faqs = [("How does pay in 4 work?", "You pay 25% at checkout and the rest in three equal payments every two weeks, so the purchase is paid off in six weeks. Most pay-in-4 plans charge no interest if you pay on time."),
        ("How much interest do buy now, pay later loans charge?", "Pay-in-4 plans are usually interest-free. Longer monthly plans can charge from 0% to around 36% APR depending on the provider, merchant and your credit."),
        ("What does $600 over 12 months at 20% APR cost?", f"About ${amort(600,20,12):,.2f} a month, or ${amort(600,20,12)*12-600:,.2f} in total interest."),
        ("Does buy now, pay later affect my credit score?", "It can. Some providers report payment history to credit bureaus and some run credit checks for longer plans. Late payments can hurt your score."),
        ("What happens if I return something bought with buy now, pay later?", "The provider adjusts or cancels the plan once the merchant processes the refund. Keep making payments until then to avoid late fees.")]
page('bnpl-calculator', 'Buy Now, Pay Later Calculator: Pay in 4 and Monthly Plan Costs | ToolPinch',
     'See the real cost of buy now, pay later: pay-in-4 schedules, monthly installment interest at any APR, and how late fees add up.',
     'Buy Now, Pay Later Cost Calculator', 'Pay in 4 and monthly plans',
     'Work out your payment schedule, the interest on monthly plans and the cost of late fees before you split a purchase.',
     ['Pay in 4 and APR plans', 'Late fee impact', 'No signup'], calc, body, faqs, script, crumb=CR)

# ---------------- 4. Price adjustment / price drop ----------------
calc = """<div class="mc-calculator"><h2>Are you owed a refund?</h2>
<label class="mc-field"><span>Price you paid ($)</span><input id="aP" type="number" min="0" step="0.01" value="249.99"></label>
<label class="mc-field"><span>New lower price ($)</span><input id="aN" type="number" min="0" step="0.01" value="199.99"></label>
<label class="mc-field"><span>Quantity</span><input id="aQ" type="number" min="1" step="1" value="1"></label>
<label class="mc-field"><span>Purchase date</span><input id="aD" type="date"></label>
<label class="mc-field"><span>Store's price adjustment window (days)</span><input id="aW" type="number" min="0" max="120" step="1" value="14"></label>
<label class="mc-field"><span>Sales tax (%)</span><input id="aT" type="number" min="0" max="20" step="0.01" value="7"></label>
<button class="mc-button" data-action="adj">Check</button>
<div class="mc-result tp-res" id="aR" aria-live="polite">Enter what you paid and the new price.</div></div>"""
script = "<script>(()=>{" + FMT + """
function run(){const p=v('aP'),n=v('aN'),q=Math.max(1,Math.round(v('aQ'))),w=Math.round(v('aW')),t=v('aT'),ds=$('aD').value;
if(!ds){const d=new Date();d.setDate(d.getDate()-5);$('aD').value=d.toISOString().slice(0,10);return run()}
const diff=Math.max(0,p-n)*q,ref=diff*(1+t/100),buy=new Date(ds+'T12:00:00'),end=new Date(buy);end.setDate(end.getDate()+w);
const now=new Date();now.setHours(12,0,0,0);const left=Math.round((end-now)/864e5),fd=d=>d.toLocaleDateString(undefined,{weekday:'short',year:'numeric',month:'short',day:'numeric'});
let h;if(diff<=0)h='<p>The new price is not lower than what you paid, so there is no difference to claim.</p>';
else{h='<p class="tp-big"><strong>'+f(ref)+'</strong> potential refund</p><div class="tp-scroll"><table class="tp-table"><tbody><tr><td>Price difference × '+q+'</td><td class="n">'+f(diff)+'</td></tr><tr><td>Sales tax on the difference</td><td class="n">'+f(ref-diff)+'</td></tr>'+
'<tr><td>Window ends</td><td class="n">'+fd(end)+'</td></tr></tbody></table></div>';
h+=left>=0?'<p><b>'+left+' day'+(left===1?'':'s')+' left</b> to ask. Bring your receipt or order number and proof of the lower price from the same store.</p>':'<p>The window ended '+(-left)+' days ago. If the item is still returnable, returning it and buying again at the lower price may be an option.</p>'}
$('aR').innerHTML=h}
""" + wire(['aP', 'aN', 'aQ', 'aD', 'aW', 'aT'], 'adj') + "})();</script>"
body = """
<header><p class="mc-kicker mc-dark">The short answer</p><h2>Can you get money back if the price drops after you buy?</h2>
<p class="tp-answer">Sometimes. Some retailers offer a <strong>price adjustment</strong>: if their own price drops within a set number of days (often 14 to 30), they refund the difference plus the tax on it. If you paid <strong>$249.99</strong> and the price falls to <strong>$199.99</strong>, the difference is <strong>$50</strong>, or $53.50 with 7% sales tax.
Many stores exclude Black Friday doorbusters, limited-time and clearance prices, so check the policy before you buy.</p></header>
<section><h2>Ways to recover a price drop</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Option</th><th>How it works</th><th>Watch out for</th></tr></thead><tbody>
<tr><td>Price adjustment</td><td>The same store refunds the difference within its window</td><td>Exclusions for doorbusters, flash sales, clearance and marketplace sellers</td></tr>
<tr><td>Price match</td><td>A store matches a competitor's lower price at the time you buy</td><td>Usually only listed competitors, identical model, in-stock items</td></tr>
<tr><td>Return and rebuy</td><td>Return the item within the return window and buy it again at the new price</td><td>Restocking fees, opened-box rules, the new price selling out</td></tr>
<tr><td>Ask customer service</td><td>Some stores offer a credit even without a formal policy</td><td>Discretionary, so be polite and have the order details ready</td></tr></tbody></table></div></section>
<section><h2>Tips for the holiday season</h2><ul>
<li><strong>Extended holiday returns.</strong> Many retailers extend returns for purchases made in November and December into January, which can make return-and-rebuy possible even when the price adjustment window has passed.</li>
<li><strong>Save the evidence.</strong> Take a screenshot showing the lower price, the date and the product page.</li>
<li><strong>Set a reminder.</strong> Note the last day of the window when you buy; the calculator shows the deadline.</li>
<li><strong>Policies change.</strong> Read the store's current price adjustment and return policy rather than relying on last year's rules.</li></ul></section>
""" + rel('price-adjustment-calculator')
faqs = [("What is a price adjustment?", "A refund of the difference when a store lowers its own price on an item you already bought, within a set number of days after purchase."),
        ("Do I get the sales tax back too?", "Usually yes. The refund normally includes the sales tax paid on the price difference."),
        ("Do price adjustments apply to Black Friday prices?", "Often not. Many stores exclude doorbusters, limited-quantity and flash-sale prices from price adjustments. Check the policy."),
        ("What is the difference between price matching and a price adjustment?", "Price matching meets a competitor's lower price when you buy. A price adjustment refunds the difference when the same store lowers its own price after you buy."),
        ("What if the price adjustment window has passed?", "If the item is still within its return period, you can return it and buy it again at the lower price, if the store allows that.")]
page('price-adjustment-calculator', 'Price Drop Refund Calculator: Price Adjustment Deadline and Amount | ToolPinch',
     'Bought something and the price dropped? Calculate the refund you can ask for, including sales tax, and the last day of the store\'s price adjustment window.',
     'Price Drop Refund Calculator', 'Price adjustment and price match',
     'Find out how much you could get back if a price falls after you buy, and how many days are left to ask.',
     ['Refund with tax', 'Deadline countdown', 'No signup'], calc, body, faqs, script, crumb=CR)
