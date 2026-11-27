"""Build /tools/gs-pay-scale-2027. Run from repo root: PYTHONPATH=scripts python3 scripts/build_gs2027.py
Data: OPM Salary Table 2026-GS (1% increase, effective first pay period on or after Jan 1, 2026) and the 58 OPM 2026
locality tables (locality percentages held at 2025 levels, EO 14368). Locality rate = round(base x (1 + pct)), capped at
$197,200 (EX-IV); verified to match all 8,700 published 2026 locality figures on Nov 27, 2026.
2027 status as of Nov 27, 2026: President's alternative pay plan (Aug 2026) proposes 0% across the board and 0% locality,
3.8% for law enforcement via special rates; Congress may override in appropriations (funding expires Dec 11, 2026)."""
import json
from tax_common import page

BASE = [[22584,23341,24092,24840,25589,26028,26771,27519,27550,28248],[25393,25997,26839,27550,27858,28677,29496,30315,31134,31953],
        [27708,28632,29556,30480,31404,32328,33252,34176,35100,36024],[31103,32140,33177,34214,35251,36288,37325,38362,39399,40436],
        [34799,35959,37119,38279,39439,40599,41759,42919,44079,45239],[38791,40084,41377,42670,43963,45256,46549,47842,49135,50428],
        [43106,44543,45980,47417,48854,50291,51728,53165,54602,56039],[47738,49329,50920,52511,54102,55693,57284,58875,60466,62057],
        [52727,54485,56243,58001,59759,61517,63275,65033,66791,68549],[58064,59999,61934,63869,65804,67739,69674,71609,73544,75479],
        [63795,65922,68049,70176,72303,74430,76557,78684,80811,82938],[76463,79012,81561,84110,86659,89208,91757,94306,96855,99404],
        [90925,93956,96987,100018,103049,106080,109111,112142,115173,118204],[107446,111028,114610,118192,121774,125356,128938,132520,136102,139684],
        [126384,130597,134810,139023,143236,147449,151662,155875,160088,164301]]
CAP = 197200
LOC = {"AL":["Albany-Schenectady, NY-MA",20.77],"AQ":["Albuquerque-Santa Fe-Las Vegas, NM",18.33],"ATL":["Atlanta--Athens-Clarke County--Sandy Springs, GA-AL",23.79],
"AU":["Austin-Round Rock-Georgetown, TX",20.35],"BH":["Birmingham-Hoover-Talladega, AL",18.24],"BOS":["Boston-Worcester-Providence, MA-RI-NH-CT-ME-VT",32.58],
"BU":["Buffalo-Cheektowaga-Olean, NY",22.41],"BN":["Burlington-South Burlington-Barre, VT",19.45],"CT":["Charlotte-Concord, NC-SC",19.67],
"CHI":["Chicago-Naperville, IL-IN-WI",30.86],"CIN":["Cincinnati-Wilmington-Maysville, OH-KY-IN",21.93],"CLE":["Cleveland-Akron-Canton, OH-PA",22.23],
"CS":["Colorado Springs, CO",20.15],"COL":["Columbus-Marion-Zanesville, OH",22.15],"CC":["Corpus Christi-Kingsville-Alice, TX",17.63],
"DFW":["Dallas-Fort Worth, TX-OK",27.26],"DV":["Davenport-Moline, IA-IL",18.93],"DAY":["Dayton-Springfield-Kettering, OH",21.42],
"DEN":["Denver-Aurora, CO",30.52],"DM":["Des Moines-Ames-West Des Moines, IA",18.01],"DET":["Detroit-Warren-Ann Arbor, MI",29.12],
"FN":["Fresno-Madera-Hanford, CA",17.65],"HB":["Harrisburg-Lebanon, PA",19.43],"HAR":["Hartford-East Hartford, CT-MA",32.08],
"HOU":["Houston-The Woodlands, TX",35.0],"HNT":["Huntsville-Decatur, AL-TN",21.91],"IND":["Indianapolis-Carmel-Muncie, IN",18.15],
"KC":["Kansas City-Overland Park-Kansas City, MO-KS",18.97],"LR":["Laredo, TX",21.59],"LV":["Las Vegas-Henderson, NV-AZ",19.57],
"LA":["Los Angeles-Long Beach, CA",36.47],"MFL":["Miami-Port St. Lucie-Fort Lauderdale, FL",24.67],"MIL":["Milwaukee-Racine-Waukesha, WI",22.42],
"MSP":["Minneapolis-St. Paul, MN-WI",27.62],"NY":["New York-Newark, NY-NJ-CT-PA",37.95],"OM":["Omaha-Council Bluffs-Fremont, NE-IA",18.23],
"PB":["Palm Bay-Melbourne-Titusville, FL",17.93],"PHL":["Philadelphia-Reading-Camden, PA-NJ-DE-MD",28.99],"PX":["Phoenix-Mesa, AZ",22.45],
"PIT":["Pittsburgh-New Castle-Weirton, PA-OH-WV",21.03],"POR":["Portland-Vancouver-Salem, OR-WA",26.13],"RA":["Raleigh-Durham-Cary, NC",22.24],
"RN":["Reno-Fernley, NV",17.52],"RCH":["Richmond, VA",22.28],"RT":["Rochester-Batavia-Seneca Falls, NY",17.88],"SAC":["Sacramento-Roseville, CA-NV",29.76],
"SO":["San Antonio-New Braunfels-Pearsall, TX",18.78],"SD":["San Diego-Chula Vista-Carlsbad, CA",33.72],"SF":["San Jose-San Francisco-Oakland, CA",46.34],
"SEA":["Seattle-Tacoma, WA",31.57],"SN":["Spokane-Spokane Valley-Coeur d'Alene, WA-ID",17.67],"SL":["St. Louis-St. Charles-Farmington, MO-IL",20.03],
"TU":["Tucson-Nogales, AZ",19.28],"VB":["Virginia Beach-Norfolk, VA-NC",18.8],"DCB":["Washington-Baltimore-Arlington, DC-MD-VA-WV-PA",33.94],
"AK":["State of Alaska",32.36],"HI":["State of Hawaii",22.21],"RUS":["Rest of U.S.",17.06]}
assert len(LOC) == 58

rate = lambda g, s, c: min(CAP, int(BASE[g - 1][s - 1] * (1 + LOC[c][1] / 100) + 0.5))  # same rounding as JS Math.round
# spot checks against published OPM 2026 tables
assert rate(1, 1, 'DCB') == 30249 and rate(15, 1, 'DCB') == 169279 and rate(15, 6, 'DCB') == 197200 and rate(5, 1, 'DCB') == 46610
m = lambda x: f"${x:,}"

order = ['DCB', 'RUS'] + sorted([c for c in LOC if c not in ('DCB', 'RUS', 'AK', 'HI')], key=lambda c: LOC[c][0]) + ['AK', 'HI']
opts = ''.join(f'<option value="{c}"{" selected" if c == "DCB" else ""}>{LOC[c][0]} ({LOC[c][1]:.2f}%)</option>' for c in order)
base_rows = ''.join(f'<tr><td>GS-{g}</td>' + ''.join(f'<td class="n">{v:,}</td>' for v in BASE[g - 1]) + '</tr>' for g in range(1, 16))
dc_rows = ''.join(f'<tr><td>GS-{g}</td>' + ''.join(f'<td class="n">{rate(g, s, "DCB"):,}</td>' for s in range(1, 11)) + '</tr>' for g in range(1, 16))
loc_rows = ''.join(f'<tr><td>{LOC[c][0]}</td><td class="n">{LOC[c][1]:.2f}%</td><td class="n">{m(rate(7, 1, c))}</td><td class="n">{m(rate(12, 1, c))}</td><td class="n">{m(rate(13, 1, c))}</td></tr>'
                   for c in sorted(LOC, key=lambda c: -LOC[c][1]))
data = json.dumps({'B': BASE, 'L': {c: v[1] for c, v in LOC.items()}, 'cap': CAP})

calc = f"""<div class="mc-calculator"><h2>Your GS salary for 2027</h2>
<label class="mc-field"><span>Grade</span><select id="gG">{''.join(f'<option value="{g}"{" selected" if g == 12 else ""}>GS-{g}</option>' for g in range(1, 16))}</select></label>
<label class="mc-field"><span>Step</span><select id="gS">{''.join(f'<option value="{s}">Step {s}</option>' for s in range(1, 11))}</select></label>
<label class="mc-field tp-wide"><span>Locality pay area</span><select id="gL">{opts}</select></label>
<label class="mc-field"><span>2027 raise scenario</span><select id="gR"><option value="0" selected>0% freeze (President's plan)</option><option value="3.8">3.8% (unions' request)</option><option value="4.1">4.1% (FAIR Act)</option><option value="c">Custom</option></select></label>
<label class="mc-field"><span>Custom raise (%)</span><input id="gC" type="number" min="0" max="10" step="0.1" value="2"></label>
<button class="mc-button" data-action="gs">Calculate</button>
<div class="mc-result tp-res" id="gRes" aria-live="polite">Choose a grade, step and location.</div></div>"""

script = """<script>(()=>{const D=__D__,$=id=>document.getElementById(id),f=x=>x.toLocaleString('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}),f2=x=>x.toLocaleString('en-US',{style:'currency',currency:'USD'});
function run(){const g=+$('gG').value,s=+$('gS').value,c=$('gL').value,rv=$('gR').value,r=rv==='c'?Math.max(0,+$('gC').value||0):+rv;
const b=D.B[g-1][s-1],p=D.L[c],y26=Math.min(D.cap,Math.round(b*(1+p/100))),cap27=Math.round(D.cap*(1+r/100)),y27=Math.min(cap27,Math.round(y26*(1+r/100)));
const hr=y27/2087,bw=hr*80;
let t='<p class="tp-big"><strong>'+f(y27)+'</strong> a year in 2027</p><div class="tp-scroll"><table class="tp-table"><tbody>'+
'<tr><td>2026 salary (GS-'+g+' step '+s+', locality '+p.toFixed(2)+'%)</td><td class="n">'+f(y26)+'</td></tr><tr><td>2026 base pay before locality</td><td class="n">'+f(b)+'</td></tr>'+
'<tr><td>2027 raise ('+r+'%)</td><td class="n">+'+f(y27-y26)+'</td></tr><tr class="tot"><td>2027 annual salary</td><td class="n">'+f(y27)+'</td></tr>'+
'<tr><td>Biweekly gross pay (80 hours)</td><td class="n">'+f2(bw)+'</td></tr><tr><td>Hourly rate (2,087 hours a year)</td><td class="n">'+f2(hr)+'</td></tr></tbody></table></div>';
if(y26>=D.cap)t+='<p>This salary is held at the $197,200 cap on GS pay (Executive Schedule level IV).</p>';
t+='<p class="tp-note">'+(r===0?'Under a freeze, 2027 GS tables stay at 2026 rates.':'Raise scenarios are applied to the total salary; Congress could split a raise differently between base and locality pay, so treat this as an estimate.')+' Gross pay before taxes, retirement and insurance.</p>';
$('gRes').innerHTML=t}
document.addEventListener('DOMContentLoaded',()=>{['gG','gS','gL','gR','gC'].forEach(i=>$(i).addEventListener('input',run));document.querySelectorAll('[data-action="gs"]').forEach(b=>b.addEventListener('click',run));run()})})();</script>"""
script = script.replace('__D__', data)

steps = ''.join(f'<th class="n">Step {s}</th>' for s in range(1, 11))
body = f"""
<header><p class="mc-kicker mc-dark">Where the 2027 raise stands</p><h2>Will federal employees get a raise in 2027?</h2>
<p class="tp-answer">As of November 27, 2026, the 2027 GS raise is <strong>proposed at 0%</strong>. In late August 2026 the President sent Congress an alternative pay plan with no across-the-board increase and no locality increase for 2027, and a <strong>3.8% raise for federal law enforcement</strong> through special pay rates.
Congress can still change this in a funding bill. Current funding runs out on <strong>December 11, 2026</strong>.</p>
<p>If the freeze holds, the 2027 GS pay scale will be the same as 2026. A GS-12 step 1 in the Washington, DC area would stay at <strong>{m(rate(12, 1, 'DCB'))}</strong>, and a GS-9 step 1 in the Rest of U.S. area at <strong>{m(rate(9, 1, 'RUS'))}</strong>.</p></header>

<section><h2>2027 federal pay raise timeline</h2>
<ul><li><strong>Late August 2026:</strong> the President's alternative pay plan sets the 2027 adjustment at 0% for most civilian employees, with 3.8% for law enforcement.</li>
<li><strong>November 2026:</strong> 40 federal unions asked appropriators for at least 3.8%. The FAIR Act would give an average 4.1% (3.1% base plus 1% locality). Neither the House nor the Senate spending bill included a general raise as of late November.</li>
<li><strong>December 11, 2026:</strong> current government funding expires. A raise could be added to the next spending bill.</li>
<li><strong>Mid to late December 2026:</strong> the President's executive order sets the final 2027 pay tables, and OPM publishes them.</li>
<li><strong>January 10, 2027:</strong> new rates take effect for most employees, at the start of the first pay period of 2027 (paid by NFC on February 1). A raise passed later can be made retroactive.</li></ul></section>

<section><h2>2026 GS base pay table (2027 under a freeze)</h2>
<p>Base pay before locality, effective January 11, 2026, including the 1% raise for 2026. Your actual salary adds your locality payment.</p>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Grade</th>{steps}</tr></thead><tbody>{base_rows}</tbody></table></div></section>

<section><h2>Washington, DC area GS pay table (locality 33.94%)</h2>
<p>The Washington-Baltimore-Arlington area has the largest number of federal employees. Rates above $197,200 are capped.</p>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Grade</th>{steps}</tr></thead><tbody>{dc_rows}</tbody></table></div></section>

<section><h2>Locality pay by area</h2>
<p>All 58 locality pay areas with their 2026 locality percentage (unchanged from 2025) and sample step 1 salaries. Under the proposed freeze these stay the same in 2027.</p>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Locality pay area</th><th class="n">Locality</th><th class="n">GS-7 step 1</th><th class="n">GS-12 step 1</th><th class="n">GS-13 step 1</th></tr></thead><tbody>{loc_rows}</tbody></table></div></section>

<section><h2>How GS pay works</h2>
<ul><li><strong>Grade and step:</strong> your grade (GS-1 to GS-15) sets the pay range; steps 1 to 10 are within-grade increases. Steps 2 to 4 come after 52 weeks each, steps 5 to 7 after 104 weeks, and steps 8 to 10 after 156 weeks, with acceptable performance.</li>
<li><strong>Locality pay:</strong> a percentage added to base pay for your duty station, from 17.06% (Rest of U.S.) to 46.34% (San Jose-San Francisco-Oakland).</li>
<li><strong>Pay cap:</strong> GS pay including locality can't exceed Executive Schedule level IV, $197,200 in 2026.</li>
<li><strong>Hourly and biweekly pay:</strong> divide the annual salary by 2,087 hours for the hourly rate; biweekly pay is 80 hours at that rate.</li></ul>
<p>Sources: <a href="https://www.opm.gov/policy-data-oversight/pay-leave/salaries-wages/salary-tables/26Tables/html/GS.aspx" rel="noopener" target="_blank">OPM Salary Table 2026-GS</a> and 2026 locality tables, <a href="https://www.govinfo.gov/content/pkg/FR-2026-02-03/html/2026-02189.htm" rel="noopener" target="_blank">OPM notice on January 2026 pay adjustments</a>, <a href="https://www.govexec.com/pay-benefits/2026/08/trump-formally-proposes-pay-freeze-most-federal-workers-38-increase-law-enforcement/415707/" rel="noopener" target="_blank">Government Executive on the 2027 pay plan</a> and <a href="https://www.fedsmith.com/2026/11/23/december-funding-bill-2027-pay-freeze/" rel="noopener" target="_blank">FedSmith on the December funding bill</a>.</p></section>
<nav class="mc-related-links" aria-label="Related tools"><h2>Related calculators</h2><a href="/tools/2027-paycheck-calculator">2027 paycheck change</a><a href="/tools/what-pay-period-is-it">What pay period is it?</a><a href="/tools/federal-holidays-2027">Federal holidays 2027</a><a href="/tools/military-pay-dates-2027">Military pay dates 2027</a><a href="/tools/federal-pay-periods-2027">NFC pay period calendar 2027</a><a href="/tools/us-paycheck-calculator">US paycheck calculator</a><a href="/tools/2027-tax-brackets">2027 tax brackets</a><a href="/tools/salary-to-hourly-calculator">Salary to hourly</a></nav>"""

faqs = [("Is there a federal pay raise in 2027?", "Not under the current plan. The President's alternative pay plan sets the 2027 raise at 0% for most GS employees, with 3.8% for law enforcement. Congress could add a raise in a spending bill before the final pay tables are set in December 2026."),
        ("What is the GS pay scale for 2027?", "If the proposed freeze takes effect, the 2027 GS pay scale is the same as 2026: GS-1 step 1 base pay of $22,584 up to GS-15 step 10 base pay of $164,301, plus locality pay of 17.06% to 46.34%, capped at $197,200."),
        ("When will the 2027 GS pay tables be released?", "Usually in late December, after the President signs the pay executive order. New rates take effect January 10, 2027, the first pay period of the year."),
        ("How much is a GS-12 step 1 in 2026?", f"$76,463 base pay. With locality pay it is {m(rate(12, 1, 'RUS'))} in the Rest of U.S. area and {m(rate(12, 1, 'DCB'))} in the Washington, DC area."),
        ("Do law enforcement officers get a raise in 2027?", "Yes, under the President's plan federal law enforcement personnel receive a 3.8% basic pay increase in 2027 through special pay rates."),
        ("How do I calculate my hourly GS pay?", "Divide your annual salary, including locality pay, by 2,087 hours. Biweekly gross pay is that hourly rate times 80.")]

page('gs-pay-scale-2027', 'GS Pay Scale 2027: Pay Tables and Raise Status | ToolPinch',
     '2027 GS pay scale with the latest federal pay raise status (0% proposed), 2026 GS base and locality tables for all 58 areas, and a salary calculator.',
     'GS Pay Scale 2027', 'Updated Nov 27, 2026',
     "Find your 2027 federal salary by grade, step and locality, and see where the 2027 pay raise stands.",
     ['All 58 locality areas', 'Official OPM rates', 'No signup'], calc, body, faqs, script)
