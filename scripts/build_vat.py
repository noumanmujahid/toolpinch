"""Build /tools/vat-calculator. Run from repo root with PYTHONPATH=scripts."""
import json
from tax_common import page, related

# country, tax name, standard rate, reduced rates, note
V = [
 ("Afghanistan","Business receipts tax",10,[2],""),("Albania","VAT",20,[6],""),("Algeria","VAT",19,[9],""),
 ("Andorra","IGI",4.5,[9.5,2.5,1],"9.5% is an increased rate"),("Angola","VAT",14,[7,5],""),
 ("Antigua and Barbuda","ABST",17,[],""),("Argentina","IVA",21,[27,10.5],"27% applies to some utilities for businesses"),
 ("Armenia","VAT",20,[],""),("Australia","GST",10,[],"Basic food, health and education are GST-free"),
 ("Austria","VAT",20,[13,10,4.9],"4.9% on staple foods from 1 July 2026"),("Azerbaijan","VAT",18,[],""),
 ("Bahamas","VAT",10,[],""),("Bahrain","VAT",10,[],""),("Bangladesh","VAT",15,[10,7.5,5],""),
 ("Barbados","VAT",17.5,[22,10],"22% on some telecoms"),("Belarus","VAT",20,[10],""),("Belgium","VAT",21,[12,6],""),
 ("Belize","GST",12.5,[],""),("Benin","VAT",18,[],""),("Bhutan","GST",5,[],""),("Bolivia","IVA",13,[],""),
 ("Bosnia and Herzegovina","VAT",17,[],""),("Botswana","VAT",14,[],""),
 ("Brazil","ICMS / IPI / PIS-COFINS",17,[],"Rates vary by state and product; the 2027 to 2033 reform replaces them with CBS and IBS"),
 ("Bulgaria","VAT",20,[9],""),("Burkina Faso","VAT",18,[],""),("Burundi","VAT",18,[10],""),("Cambodia","VAT",10,[],""),
 ("Cameroon","VAT",19.25,[],"17.5% VAT plus 10% municipal surcharge"),("Cape Verde","VAT",15,[],""),
 ("Canada – Alberta","GST",5,[],"Federal GST only"),("Canada – British Columbia","GST + PST",12,[5],"5% GST plus 7% PST"),
 ("Canada – Manitoba","GST + RST",12,[5],"5% GST plus 7% RST"),("Canada – New Brunswick","HST",15,[],""),
 ("Canada – Newfoundland and Labrador","HST",15,[],""),("Canada – Northwest Territories","GST",5,[],""),
 ("Canada – Nova Scotia","HST",14,[],"Cut from 15% on 1 April 2025"),("Canada – Nunavut","GST",5,[],""),
 ("Canada – Ontario","HST",13,[],""),("Canada – Prince Edward Island","HST",15,[],""),
 ("Canada – Quebec","GST + QST",14.975,[5],"5% GST plus 9.975% QST"),("Canada – Saskatchewan","GST + PST",11,[5],"5% GST plus 6% PST"),
 ("Canada – Yukon","GST",5,[],""),("Central African Republic","VAT",19,[5],""),("Chad","VAT",18,[9],""),
 ("Chile","IVA",19,[],""),("China","VAT",13,[9,6,3],""),("Colombia","IVA",19,[5],""),("Congo (Brazzaville)","VAT",18,[5],""),
 ("Congo (DR)","VAT",16,[8],""),("Cook Islands","VAT",15,[],""),("Costa Rica","IVA",13,[4,2,1],""),
 ("Côte d'Ivoire","VAT",18,[9],""),("Croatia","PDV",25,[13,5],""),("Cyprus","VAT",19,[9,5,3],""),
 ("Czech Republic","DPH",21,[12],""),("Denmark","Moms",25,[],""),("Djibouti","VAT",10,[],""),("Dominica","VAT",15,[10],""),
 ("Dominican Republic","ITBIS",18,[16],""),("Ecuador","IVA",15,[8,5],""),("Egypt","VAT",14,[5],""),
 ("El Salvador","IVA",13,[],""),("Equatorial Guinea","VAT",15,[6],""),("Estonia","Käibemaks",24,[13,9],"24% since 1 July 2025"),
 ("Eswatini","VAT",15,[],""),("Ethiopia","VAT",15,[],""),("Fiji","VAT",12.5,[],"Cut from 15% in August 2025"),
 ("Finland","ALV",25.5,[13.5,10],""),("France","TVA",20,[10,5.5,2.1],""),("Gabon","VAT",18,[10],""),
 ("Gambia","VAT",15,[],""),("Georgia","VAT",18,[],""),("Germany","USt",19,[7],""),
 ("Ghana","VAT",12.5,[3],"Levies (NHIL, GETFund) are charged on top"),("Greece","ΦΠΑ",24,[13,6],"Lower rates on some islands"),
 ("Grenada","VAT",15,[],""),("Guatemala","IVA",12,[],""),("Guinea","VAT",18,[],""),("Guinea-Bissau","VAT",19,[10],""),
 ("Guyana","VAT",14,[],""),("Haiti","TCA",10,[],""),("Honduras","ISV",15,[18],"18% on alcohol, tobacco and some services"),
 ("Hong Kong","None",0,[],"No VAT or sales tax"),("Hungary","ÁFA",27,[18,5],""),("Iceland","VSK",24,[11],""),
 ("India","GST",18,[40,5,3],"Since 22 September 2025: 5% and 18% main slabs, 40% on luxury and sin goods, 3% on gold"),
 ("Indonesia","PPN",12,[],"Effective 11% on most goods; full 12% on luxury goods"),("Iran","VAT",10,[],""),
 ("Ireland","VAT",23,[13.5,9,4.8],""),("Israel","Ma'am",18,[],""),("Italy","IVA",22,[10,5,4],""),
 ("Jamaica","GCT",15,[],""),("Japan","Consumption tax",10,[8],"8% on food and newspapers"),("Jersey","GST",5,[],""),
 ("Jordan","Sales tax",16,[8,4],""),("Kazakhstan","VAT",16,[],"Raised from 12% in 2026"),("Kenya","VAT",16,[8],""),
 ("Kosovo","VAT",18,[8],""),("Kuwait","None",0,[],"No VAT"),("Kyrgyzstan","VAT",12,[],""),("Laos","VAT",10,[],""),
 ("Latvia","PVN",21,[12,5],""),("Lebanon","VAT",11,[],""),("Lesotho","VAT",15,[],""),("Liechtenstein","MWST",8.1,[3.8,2.6],""),
 ("Lithuania","PVM",21,[12,5],""),("Luxembourg","TVA",17,[14,8,3],""),("Madagascar","VAT",20,[],""),("Malawi","VAT",16.5,[],""),
 ("Malaysia","Sales and service tax",10,[8,6,5],"Sales tax 10% or 5%; service tax 8% (6% on some services)"),
 ("Maldives","GST",8,[17],"17% on tourism goods and services"),("Mali","VAT",18,[5],""),("Malta","VAT",18,[12,7,5],""),
 ("Mauritania","VAT",16,[],""),("Mauritius","VAT",15,[],""),("Mexico","IVA",16,[8],"8% in northern and southern border regions"),
 ("Moldova","VAT",20,[12,8],""),("Monaco","TVA",20,[10,5.5,2.1],""),("Mongolia","VAT",10,[],""),("Montenegro","PDV",21,[15,7],""),
 ("Morocco","TVA",20,[10],""),("Mozambique","VAT",16,[],""),("Namibia","VAT",15,[],""),("Nepal","VAT",13,[],""),
 ("Netherlands","BTW",21,[9],""),("New Zealand","GST",15,[],""),("Nicaragua","IVA",15,[],""),("Niger","VAT",19,[10],""),
 ("Nigeria","VAT",7.5,[],""),("North Macedonia","VAT",18,[10,5],""),("Norway","MVA",25,[15,12],""),("Oman","VAT",5,[],""),
 ("Pakistan","Sales tax",18,[],"Provinces charge their own sales tax on services (13% to 16%)"),("Panama","ITBMS",7,[15,10],""),
 ("Papua New Guinea","GST",10,[],""),("Paraguay","IVA",10,[5],""),("Peru","IGV",18,[10.5],"18% includes the 2% municipal tax"),
 ("Philippines","VAT",12,[],""),("Poland","VAT",23,[8,5],""),("Portugal","IVA",23,[13,6],"Lower rates in Madeira and the Azores"),
 ("Puerto Rico","IVU",11.5,[4],"Sales and use tax"),("Qatar","None",0,[],"No VAT"),("Romania","TVA",21,[11],"21% since 1 August 2025"),
 ("Russia","VAT",22,[10],"Raised from 20% on 1 January 2026"),("Rwanda","VAT",18,[],""),("Saint Kitts and Nevis","VAT",17,[10],""),
 ("Saint Lucia","VAT",12.5,[10],""),("Saint Vincent and the Grenadines","VAT",16,[11],""),("Samoa","VAGST",15,[],""),
 ("Saudi Arabia","VAT",15,[],""),("Senegal","VAT",18,[10],""),("Serbia","PDV",20,[10],""),("Seychelles","VAT",15,[],""),
 ("Sierra Leone","GST",15,[],""),("Singapore","GST",9,[],""),("Slovakia","DPH",23,[19,5],"23% since 1 January 2025"),
 ("Slovenia","DDV",22,[9.5,5],""),("South Africa","VAT",15,[],""),("South Korea","VAT",10,[],""),("Spain","IVA",21,[10,4],""),
 ("Sri Lanka","VAT",18,[],""),("Sudan","VAT",17,[],""),("Sweden","Moms",25,[12,6],"Food at 6% from 1 April 2026"),
 ("Switzerland","MWST",8.1,[3.8,2.6],"3.8% for accommodation"),("Taiwan","Business tax",5,[],""),("Tajikistan","VAT",14,[],""),
 ("Tanzania","VAT",18,[],""),("Thailand","VAT",7,[],""),("Togo","VAT",18,[10],""),("Tonga","CT",15,[],""),
 ("Trinidad and Tobago","VAT",12.5,[],""),("Tunisia","TVA",19,[13,7],""),("Türkiye","KDV",20,[10,1],""),
 ("Turkmenistan","VAT",15,[],""),("Uganda","VAT",18,[],""),("Ukraine","PDV",20,[14,7],""),
 ("United Arab Emirates","VAT",5,[],""),("United Kingdom","VAT",20,[5],"0% on most food, books and children's clothes"),
 ("United States","Sales tax (no VAT)",0,[],"No national VAT. States charge sales tax of 0% to 7.25%, and local taxes can add more"),
 ("Uruguay","IVA",22,[10],""),("Uzbekistan","VAT",12,[],""),("Vanuatu","VAT",15,[],""),("Venezuela","IVA",16,[8],""),
 ("Vietnam","VAT",10,[8,5],"Most 10% goods taxed at 8% until 31 December 2026"),("Yemen","GST",5,[],""),
 ("Zambia","VAT",16,[],""),("Zimbabwe","VAT",15.5,[],""),
]
V.sort(key=lambda v: v[0].replace('Côte', 'Cote').replace('Türkiye','Turkiye').lower())
names = [v[0] for v in V]
assert len(names) == len(set(names)), 'duplicate'
EU = {"Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
      "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia",
      "Slovenia", "Spain", "Sweden"}
assert EU <= set(names) and len(EU) == 27
fr = lambda r: (f"{r:g}%")
real = [v for v in V if v[2] > 0]
top = max(real, key=lambda v: v[2]); low = min(real, key=lambda v: v[2])
nc = len([v for v in V if not v[0].startswith('Canada')]) + 1
print('countries', nc, len(V), 'top', top[0], top[2], 'low', low[0], low[2])

opts = ''.join(f'<option value="{i}"{" selected" if v[0]=="United Kingdom" else ""}>{v[0]} ({fr(v[2])})</option>' for i, v in enumerate(V))
rows = ''.join(f'<tr><td>{v[0]}{" <small>(EU)</small>" if v[0] in EU else ""}</td><td>{v[1]}</td><td class="n"><b>{fr(v[2])}</b></td><td>{", ".join(fr(r) for r in v[3]) or "—"}</td><td class="tp-note">{v[4]}</td></tr>' for v in V)
data = json.dumps([[v[0], v[1], v[2], v[3], v[4]] for v in V], ensure_ascii=False)

calc = f"""<div class="mc-calculator"><h2>VAT calculator</h2>
<label class="mc-field"><span>Country</span><select id="vCountry">{opts}<option value="custom">Custom rate…</option></select></label>
<label class="mc-field"><span>Rate (%)</span><select id="vRate"></select></label>
<label class="mc-field" id="vCustomWrap" hidden><span>Custom rate (%)</span><input id="vCustom" type="number" min="0" step="0.01" value="20"></label>
<label class="mc-field"><span>Amount</span><input id="vAmt" type="number" min="0" step="0.01" value="100"></label>
<div class="mc-field tp-wide"><span>The amount is</span><div class="tp-seg"><label><input type="radio" name="vMode" value="add" checked> before VAT (add VAT)</label><label><input type="radio" name="vMode" value="remove"> including VAT (remove VAT)</label></div></div>
<button class="mc-button" data-action="vat">Calculate</button>
<div class="mc-result tp-res" id="vResult" aria-live="polite">Enter an amount to see the VAT.</div></div>"""

script = """<script>(()=>{const V=__V__,$=id=>document.getElementById(id);
const f=x=>x.toLocaleString(undefined,{minimumFractionDigits:2,maximumFractionDigits:2});
function rates(){const c=$('vCountry').value,s=$('vRate');$('vCustomWrap').hidden=c!=='custom';s.parentElement.hidden=c==='custom';if(c==='custom')return;
const v=V[+c];s.innerHTML='<option value="'+v[2]+'">Standard '+v[2]+'%</option>'+v[3].map(r=>'<option value="'+r+'">'+(r>v[2]?'Higher ':'Reduced ')+r+'%</option>').join('')}
function run(){const c=$('vCountry').value,r=c==='custom'?Math.max(0,+$('vCustom').value||0):+$('vRate').value,a=Math.max(0,+$('vAmt').value||0),add=document.querySelector('input[name=vMode]:checked').value==='add';
const net=add?a:a/(1+r/100),vat=net*r/100,gross=net+vat,v=c==='custom'?null:V[+c];
let h='<p class="tp-big"><strong>'+f(vat)+'</strong> '+(v?v[1]:'VAT')+' at '+r+'%</p><div class="tp-scroll"><table class="tp-table"><tbody>'+
'<tr><td>Net amount (before tax)</td><td class="n">'+f(net)+'</td></tr><tr><td>'+(v?v[1]:'VAT')+' ('+r+'%)</td><td class="n">'+f(vat)+'</td></tr>'+
'<tr class="tot"><td>Gross amount (including tax)</td><td class="n">'+f(gross)+'</td></tr></tbody></table></div>';
h+='<p class="tp-note">'+(add?'Formula: VAT = net × '+r+' ÷ 100.':'Formula: VAT = gross × '+r+' ÷ '+(100+r)+'.')+(v&&v[4]?' '+v[4]+'.':'')+'</p>';
if(v&&v[2]===0)h='<p>'+v[0]+' has no VAT. '+v[4]+'.</p>';$('vResult').innerHTML=h}
function filt(){const q=$('vFilter').value.trim().toLowerCase();document.querySelectorAll('#vTable tbody tr').forEach(tr=>{tr.hidden=q&&!tr.textContent.toLowerCase().includes(q)})}
document.addEventListener('DOMContentLoaded',()=>{rates();$('vCountry').addEventListener('change',()=>{rates();run()});['vRate','vCustom','vAmt'].forEach(id=>$(id).addEventListener('input',run));
document.querySelectorAll('input[name=vMode]').forEach(e=>e.addEventListener('change',run));document.querySelectorAll('[data-action="vat"]').forEach(b=>b.addEventListener('click',run));
$('vFilter').addEventListener('input',filt);run()})})();</script>""".replace('__V__', data)

body = f"""
<header><p class="mc-kicker mc-dark">The short answer</p><h2>How do you calculate VAT?</h2>
<p class="tp-answer">To <strong>add VAT</strong>, multiply the net price by the rate: at 20%, £100 × 0.20 = <strong>£20 VAT</strong>, so the total is £120.
To <strong>remove VAT</strong> from a price that already includes it, divide by 1 plus the rate: £120 ÷ 1.20 = <strong>£100</strong>, so the VAT was £20.
Taking 20% off £120 gives the wrong answer (£96), because VAT is charged on the net price, not the gross.</p></header>

<section><h2>How VAT and GST work around the world</h2>
<p>About 175 countries charge a value-added tax. It is called VAT in Europe and most of Africa, GST (goods and services tax) in Australia, Canada, India, New Zealand, Singapore and Malaysia, IVA in Spanish- and Portuguese-speaking countries, and consumption tax in Japan.
Businesses charge it on each sale and reclaim the tax they paid on their own purchases, so the final consumer bears the full tax.</p>
<ul><li><strong>Standard rate</strong>: applies to most goods and services. It ranges from {fr(low[2])} in {low[0]} to {fr(top[2])} in {top[0]}.</li>
<li><strong>Reduced rates</strong>: lower rates for essentials such as food, medicine, books, public transport or hotels. Many countries have one or two.</li>
<li><strong>Zero rate and exemptions</strong>: zero-rated items (exports, often basic food) carry 0% VAT but the seller can still reclaim input tax. Exempt items (usually finance, insurance, health and education) carry no VAT and the seller cannot reclaim it.</li>
<li><strong>No VAT</strong>: the United States has no national VAT and uses state sales taxes instead; Hong Kong, Kuwait and Qatar have no VAT.</li></ul>
<p><strong>European Union:</strong> all 27 member states must charge a standard rate of at least 15%. Hungary is highest at 27%, followed by Croatia, Denmark and Sweden at 25% and Finland at 25.5%; Luxembourg is lowest at 17%.
<strong>Gulf states:</strong> the UAE and Oman charge 5%, Bahrain 10% and Saudi Arabia 15%.
<strong>Canada</strong> combines a 5% federal GST with provincial tax, so the rate depends on the province; each one is listed separately below.</p></section>

<section><h2>VAT and GST rates by country (2026)</h2>
<p>Standard and reduced rates for {nc} countries, with each Canadian province listed separately. Type to filter.</p>
<input class="tp-filter" id="vFilter" type="search" placeholder="Filter by country or tax name" aria-label="Filter countries">
<div class="tp-scroll"><table class="tp-table" id="vTable"><thead><tr><th>Country</th><th>Tax</th><th class="n">Standard</th><th>Other rates</th><th>Notes</th></tr></thead><tbody>{rows}</tbody></table></div></section>

<section><h2>Worked examples</h2><div class="mc-example-grid">
<div><h3>Add 20% UK VAT to £250</h3><p>£250 × 0.20 = £50 VAT. Total £300.</p></div>
<div><h3>Remove 19% German VAT from €119</h3><p>€119 ÷ 1.19 = €100 net. VAT €19.</p></div>
<div><h3>Add 18% Indian GST to ₹10,000</h3><p>₹10,000 × 0.18 = ₹1,800 GST (₹900 CGST + ₹900 SGST within one state). Total ₹11,800.</p></div>
<div><h3>Remove 5% UAE VAT from AED 525</h3><p>AED 525 ÷ 1.05 = AED 500 net. VAT AED 25.</p></div></div></section>

<section><h2>Sources and limitations</h2>
<p>Rates were checked in November 2026 against national tax authority publications and the
<a href="https://taxation-customs.ec.europa.eu/taxation/vat_en" rel="noopener" target="_blank">European Commission VAT rates database</a>,
<a href="https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses/charge-collect-which-rate.html" rel="noopener" target="_blank">CRA GST/HST rates</a> and
<a href="https://www.gst.gov.in/" rel="noopener" target="_blank">India's GST portal</a>.
Which rate applies to a specific product depends on local rules, and rates change, sometimes with little notice. Check with the tax authority or an adviser before invoicing.</p></section>
{related('vat-calculator', [('/tools/discount-calculator', 'Discount calculator'), ('/tools/percentage-calculator', 'Percentage calculator')])}"""

faqs = [
    ("How do I add VAT to a price?", "Multiply the net price by 1 plus the VAT rate. For 20% VAT, £100 × 1.20 = £120, of which £20 is VAT."),
    ("How do I remove VAT from a price?", "Divide the gross price by 1 plus the VAT rate. For 20% VAT, £120 ÷ 1.20 = £100 net, so the VAT is £20. Do not subtract 20% of the gross price."),
    ("Which country has the highest VAT rate?", f"{top[0]}, at {fr(top[2])}. In the EU, Croatia, Denmark and Sweden charge 25% and Finland 25.5%."),
    ("Which countries have no VAT?", "The United States has no national VAT and uses state sales taxes instead. Hong Kong, Kuwait and Qatar also have no VAT."),
    ("What is the difference between VAT and GST?", "They are the same kind of tax: a tax on consumption collected at each stage of the supply chain, with businesses reclaiming the tax on their purchases. GST is the name used in Australia, Canada, India, New Zealand, Singapore and some other countries."),
    ("What are India's GST rates in 2026?", "Since 22 September 2025, most goods and services are taxed at 5% or 18%. A 40% rate applies to luxury and sin goods, and gold is taxed at 3%. The 12% and 28% slabs were removed."),
    ("What is the VAT rate in the UAE and Saudi Arabia?", "The UAE charges 5% VAT. Saudi Arabia charges 15%."),
    ("What is the minimum VAT rate in the EU?", "EU law requires a standard rate of at least 15%. Member states can apply up to two reduced rates of at least 5% to listed goods and services, and some keep lower legacy rates."),
]

page('vat-calculator', 'VAT Calculator: Add or Remove VAT, Rates for Every Country (2026) | ToolPinch',
     f'Add or remove VAT or GST for {nc} countries. Standard and reduced 2026 rates for the UK, EU, India, UAE, Canada, Australia and more, with the formulas.',
     'VAT Calculator for Every Country', 'Updated November 2026',
     'Add VAT to a net price or remove it from a gross price, using the standard or reduced rate for any country.',
     [f'{nc} countries', 'Reduced rates included', 'No signup'], calc, body, faqs, script)
