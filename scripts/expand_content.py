# Rich content for 15 ToolPinch calculators. Each entry: (short answer, body sections HTML, [(q, a), ...])
C = {}

C['percentage-calculator'] = (
"""To find <strong>X% of Y</strong>, multiply Y by X and divide by 100: 20% of 150 = 150 × 20 ÷ 100 = <strong>30</strong>.
To find <strong>what percent X is of Y</strong>, divide X by Y and multiply by 100: 45 of 60 = 45 ÷ 60 × 100 = <strong>75%</strong>.
For <strong>percentage change</strong>, divide the difference by the starting value: 80 to 100 is (100 − 80) ÷ 80 × 100 = <strong>+25%</strong>.""",
"""<section><h2>The three percentage questions</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Question</th><th>Formula</th><th>Example</th></tr></thead><tbody>
<tr><td>What is X% of Y?</td><td>Y × X ÷ 100</td><td>15% of 240 = 36</td></tr>
<tr><td>X is what % of Y?</td><td>X ÷ Y × 100</td><td>18 of 72 = 25%</td></tr>
<tr><td>% change from X to Y</td><td>(Y − X) ÷ X × 100</td><td>50 to 65 = +30%</td></tr>
<tr><td>Original before a % increase</td><td>New ÷ (1 + % ÷ 100)</td><td>120 after +20% → 100</td></tr></tbody></table></div></section>
<section><h2>Worked examples</h2><div class="mc-example-grid">
<div><h3>A pay rise</h3><p>Your hourly rate goes from $18.00 to $19.80. The change is 1.80 ÷ 18.00 × 100 = <b>10%</b>.</p></div>
<div><h3>Test score</h3><p>You scored 42 out of 48. 42 ÷ 48 × 100 = <b>87.5%</b>.</p></div>
<div><h3>Price drop</h3><p>A $250 phone falls to $200. (200 − 250) ÷ 250 × 100 = <b>−20%</b>.</p></div>
<div><h3>Reverse a markup</h3><p>A price of $138 includes a 15% markup. 138 ÷ 1.15 = <b>$120</b> before the markup.</p></div></div></section>
<section><h2>Common mistakes</h2><ul>
<li><strong>Up and down are not symmetric.</strong> A 20% fall followed by a 20% rise does not return to the start: 100 → 80 → 96. Going from 100 to 80 is −20%, but going from 80 back to 100 is +25%.</li>
<li><strong>Percent versus percentage points.</strong> An interest rate rising from 4% to 5% is up 1 percentage point, but 25% in relative terms.</li>
<li><strong>Dividing by the wrong base.</strong> Percentage change always divides by the starting value, not the new one.</li>
<li><strong>Adding percentages of different totals.</strong> 10% of one group and 10% of another is not 20% of the combined group unless the groups are the same size.</li></ul></section>
<section><h2>Mental-math shortcuts</h2><p>10% is the number divided by 10; 5% is half of that; 1% is the number divided by 100. 25% is a quarter, 50% a half, 75% three quarters. So 15% of $60 is $6 + $3 = $9, and 35% of 80 is 8 + 8 + 8 + 4 = 28. X% of Y is also the same as Y% of X: 8% of 50 is the same as 50% of 8, which is 4.</p></section>""",
[("How do I calculate a percentage of a number?", "Multiply the number by the percentage and divide by 100. For example, 20% of 150 is 150 × 20 ÷ 100 = 30."),
 ("How do I work out what percent one number is of another?", "Divide the part by the whole and multiply by 100. 45 out of 60 is 45 ÷ 60 × 100 = 75%."),
 ("How do I calculate percentage increase or decrease?", "Subtract the old value from the new value, divide by the old value and multiply by 100. A positive result is an increase and a negative result is a decrease."),
 ("How do I find the original number before a percentage was added?", "Divide by 1 plus the percentage as a decimal. If $138 includes a 15% markup, the original was 138 ÷ 1.15 = $120."),
 ("What is the difference between percent and percentage points?", "Percentage points measure the simple difference between two percentages (4% to 5% is 1 point). Percent change measures the relative change (4% to 5% is a 25% increase)."),
 ("Why doesn't a 50% loss and a 50% gain cancel out?", "Because each percentage is taken from a different base. 100 falls 50% to 50, and a 50% gain on 50 only brings it back to 75.")])

C['discount-calculator'] = (
"""Multiply the price by the discount and divide by 100 to get the saving, then subtract it: 25% off $80 saves 80 × 25 ÷ 100 = <strong>$20</strong>, so you pay <strong>$60</strong>.
A faster route is to multiply by what you keep: 25% off means you pay 75%, and $80 × 0.75 = $60.""",
"""<section><h2>Worked examples</h2><div class="mc-example-grid">
<div><h3>Simple sale</h3><p>$120 jacket at 30% off: saving $36, price <b>$84</b>.</p></div>
<div><h3>Stacked discounts</h3><p>20% off, then an extra 10% at the till on $100: $100 → $80 → <b>$72</b>. That is 28% off in total, not 30%.</p></div>
<div><h3>Discount, then sales tax</h3><p>$60 after discount plus 8% tax: 60 × 1.08 = <b>$64.80</b>. Tax is normally charged on the discounted price.</p></div>
<div><h3>Find the original price</h3><p>Paid $45 after 25% off: 45 ÷ 0.75 = <b>$60</b> original price.</p></div></div></section>
<section><h2>What percentage off was it?</h2><p>If you know the old and new prices, the discount percentage is (old − new) ÷ old × 100. A price cut from $120 to $90 is 30 ÷ 120 × 100 = <strong>25% off</strong>.</p>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Deal</th><th>Effective discount</th></tr></thead><tbody>
<tr><td>Buy one, get one free</td><td>50% off each item</td></tr><tr><td>Buy one, get one half price</td><td>25% off each item</td></tr>
<tr><td>3 for the price of 2</td><td>33.3% off each item</td></tr><tr><td>20% off, then 20% off again</td><td>36% off</td></tr>
<tr><td>Spend $100, get $20 off</td><td>20% off at exactly $100, less above it</td></tr></tbody></table></div></section>
<section><h2>Common mistakes</h2><ul>
<li><strong>Adding stacked discounts.</strong> 20% plus 10% is 28% off, because the second discount applies to the already reduced price.</li>
<li><strong>Removing a discount by adding the percentage back.</strong> $60 plus 25% is $75, not the $80 original. Divide by 0.75 instead.</li>
<li><strong>Ignoring shipping and tax.</strong> Compare the final amount you pay, not just the headline percentage.</li></ul></section>""",
[("How do I calculate a discount?", "Multiply the original price by the discount percentage and divide by 100 to get the saving, then subtract it from the price. 25% off $80 is $20 off, so you pay $60."),
 ("How do I calculate two discounts on top of each other?", "Apply them one after the other. 20% off then 10% off leaves 0.8 × 0.9 = 72% of the price, which is 28% off in total."),
 ("How do I find the original price from a sale price?", "Divide the sale price by 1 minus the discount as a decimal. A $45 price after 25% off was 45 ÷ 0.75 = $60."),
 ("How do I work out the percentage off?", "Subtract the sale price from the original, divide by the original and multiply by 100. $120 down to $90 is 25% off."),
 ("Is sales tax charged before or after a discount?", "Usually after: tax is charged on the price you actually pay. Manufacturer coupons can be treated differently in some US states."),
 ("Is buy one get one half price the same as 50% off?", "No. You pay 1.5 prices for 2 items, which is 25% off each item.")])

C['roi-calculator'] = (
"""ROI = net gain ÷ total cost × 100. If you invest <strong>$1,000</strong>, pay <strong>$50</strong> in costs and end with <strong>$1,250</strong>, the net gain is $200 and ROI is 200 ÷ 1,050 × 100 = <strong>19.05%</strong>.
The investment multiple is final value ÷ total cost: 1,250 ÷ 1,050 = 1.19×.""",
"""<section><h2>Worked examples</h2><div class="mc-example-grid">
<div><h3>Shares</h3><p>Bought for $2,000, sold for $2,600, $20 in fees. Net gain $580. ROI = 580 ÷ 2,020 = <b>28.7%</b>.</p></div>
<div><h3>A loss</h3><p>Invested $2,000, now worth $1,700. Net loss $300. ROI = <b>−15%</b>.</p></div>
<div><h3>Marketing campaign</h3><p>Spent $500 on ads that produced $1,500 of gross profit. Net gain $1,000. ROI = <b>200%</b>. Use profit, not revenue.</p></div>
<div><h3>Equipment</h3><p>A $3,000 machine saves $1,200 a year. After 3 years: (3,600 − 3,000) ÷ 3,000 = <b>20%</b>. Payback takes 2.5 years.</p></div></div></section>
<section><h2>Annualized ROI: comparing different time periods</h2><p>Plain ROI ignores time. A 50% return over 3 years is not the same as 50% in one year. To compare, convert to an annual rate:
<strong>annualized ROI = (1 + ROI)<sup>1 ÷ years</sup> − 1</strong>. For 50% over 3 years: 1.5<sup>1/3</sup> − 1 = <strong>14.5% a year</strong>.</p>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Total ROI</th><th class="n">Over 2 years</th><th class="n">Over 5 years</th><th class="n">Over 10 years</th></tr></thead><tbody>
<tr><td>25%</td><td class="n">11.8% / yr</td><td class="n">4.6% / yr</td><td class="n">2.3% / yr</td></tr>
<tr><td>50%</td><td class="n">22.5% / yr</td><td class="n">8.4% / yr</td><td class="n">4.1% / yr</td></tr>
<tr><td>100%</td><td class="n">41.4% / yr</td><td class="n">14.9% / yr</td><td class="n">7.2% / yr</td></tr></tbody></table></div></section>
<section><h2>What ROI leaves out</h2><ul><li><strong>Time</strong>: use the annualized figure to compare investments held for different periods.</li>
<li><strong>Risk</strong>: two investments with the same ROI can carry very different chances of loss.</li>
<li><strong>Cash flows along the way</strong>: dividends, rent or extra contributions need to be included in the gain or cost. For many irregular cash flows, IRR is the better measure.</li>
<li><strong>Inflation and tax</strong>: a 5% return with 3% inflation is about a 2% real return, before any tax on the gain.</li></ul></section>""",
[("How do I calculate ROI?", "Subtract the total cost from the final value to get the net gain, divide by the total cost and multiply by 100. $1,250 back on $1,050 of total cost is a 19.05% ROI."),
 ("What is a good ROI?", "It depends on the risk and time involved. Broad stock market indexes have historically returned roughly 7% to 10% a year before inflation over long periods, so many people use that as a benchmark for risky investments."),
 ("How do I calculate annualized ROI?", "Use (1 + ROI) raised to the power of 1 ÷ years, minus 1. A 50% total return over 3 years is about 14.5% a year."),
 ("Should ROI use revenue or profit?", "Profit. For marketing or business projects, use the gross profit the spending produced, not total sales, or the ROI will be overstated."),
 ("Can ROI be negative?", "Yes. If the final value is less than the total cost, the net gain is negative and so is the ROI."),
 ("What is the difference between ROI and the investment multiple?", "ROI is the gain as a percentage of cost. The multiple is final value ÷ cost. A 1.5× multiple equals a 50% ROI.")])

C['loan-amortization-calculator'] = (
"""A fixed-rate loan payment is <strong>P × r × (1 + r)<sup>n</sup> ÷ ((1 + r)<sup>n</sup> − 1)</strong>, where P is the amount borrowed, r is the interest rate per payment and n is the number of payments.
A <strong>$20,000</strong> loan at <strong>7%</strong> over <strong>5 years</strong> costs <strong>$396.02 a month</strong> and $3,761.44 in total interest.""",
"""<section><h2>Example payments</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Loan</th><th class="n">Monthly payment</th><th class="n">Total interest</th></tr></thead><tbody>
<tr><td>$20,000 car loan, 7%, 5 years</td><td class="n">$396.02</td><td class="n">$3,761.44</td></tr>
<tr><td>$300,000 mortgage, 6.5%, 30 years</td><td class="n">$1,896.20</td><td class="n">$382,633.47</td></tr>
<tr><td>$300,000 mortgage, 6.5%, 15 years</td><td class="n">$2,613.32</td><td class="n">$170,397.98</td></tr>
<tr><td>$250,000 mortgage, 6%, 30 years</td><td class="n">$1,498.88</td><td class="n">$289,595.47</td></tr></tbody></table></div>
<p>The 15-year mortgage costs $717 a month more than the 30-year one but saves over $212,000 in interest.</p></section>
<section><h2>How amortization works</h2><p>Each payment first covers the interest due on the current balance; the rest reduces the balance. Early payments are mostly interest. On the $300,000 mortgage at 6.5%, the first month's interest is 300,000 × 0.065 ÷ 12 = <strong>$1,625</strong>, so only <strong>$271.20</strong> of the $1,896.20 payment reduces the balance.
As the balance falls, the interest share shrinks and the principal share grows, which is why the schedule pays the loan down slowly at first and faster near the end.</p></section>
<section><h2>Ways to pay less interest</h2><ul>
<li><strong>Shorter term</strong>: higher payments, much less total interest.</li>
<li><strong>Extra principal payments</strong>: every extra amount reduces the balance that interest is charged on. Check that your lender has no prepayment penalty.</li>
<li><strong>Biweekly payments</strong>: paying half the monthly amount every two weeks makes 26 half-payments, or 13 full payments a year, which shortens a 30-year mortgage by several years.</li>
<li><strong>Lower rate</strong>: on a $300,000, 30-year loan, each 1 percentage point of rate changes the payment by roughly $200 a month.</li></ul></section>
<section><h2>What the calculator does not include</h2><p>The payment covers principal and interest only. Mortgage payments often also include property tax, homeowners insurance and mortgage insurance held in escrow. Fees, variable rates and interest-only periods are not modelled.</p></section>""",
[("How is a loan payment calculated?", "With the amortization formula P × r × (1 + r)^n ÷ ((1 + r)^n − 1), where P is the loan amount, r the rate per period (annual rate ÷ payments per year) and n the number of payments."),
 ("What is the monthly payment on a $300,000 mortgage at 6.5%?", "$1,896.20 a month over 30 years, or $2,613.32 over 15 years, for principal and interest only."),
 ("Why is most of my early payment interest?", "Interest is charged on the outstanding balance, which is highest at the start. As you pay the balance down, less of each payment goes to interest."),
 ("Do biweekly payments save money?", "Yes, if the lender applies them as they arrive. 26 half-payments a year equal 13 monthly payments, so you pay down principal faster and pay less interest."),
 ("What is an amortization schedule?", "A table showing every payment over the life of the loan, split into interest and principal, with the remaining balance after each payment."),
 ("Does this include taxes and insurance?", "No. It shows principal and interest only. Add escrow items such as property tax and insurance separately.")])

C['tip-split-calculator'] = (
"""Multiply the bill by the tip percentage, add it to the bill, then divide by the number of people.
An <strong>$84</strong> bill with an <strong>18%</strong> tip is 84 × 0.18 = $15.12 tip, $99.12 in total, or <strong>$24.78 each</strong> for four people.""",
"""<section><h2>Quick tip table</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Bill</th><th class="n">15%</th><th class="n">18%</th><th class="n">20%</th><th class="n">25%</th></tr></thead><tbody>
<tr><td>$25</td><td class="n">$3.75</td><td class="n">$4.50</td><td class="n">$5.00</td><td class="n">$6.25</td></tr>
<tr><td>$50</td><td class="n">$7.50</td><td class="n">$9.00</td><td class="n">$10.00</td><td class="n">$12.50</td></tr>
<tr><td>$75</td><td class="n">$11.25</td><td class="n">$13.50</td><td class="n">$15.00</td><td class="n">$18.75</td></tr>
<tr><td>$100</td><td class="n">$15.00</td><td class="n">$18.00</td><td class="n">$20.00</td><td class="n">$25.00</td></tr>
<tr><td>$150</td><td class="n">$22.50</td><td class="n">$27.00</td><td class="n">$30.00</td><td class="n">$37.50</td></tr></tbody></table></div>
<p>Shortcut for 20%: move the decimal point one place left and double it. $64 → $6.40 → <strong>$12.80</strong>.</p></section>
<section><h2>Worked examples</h2><div class="mc-example-grid">
<div><h3>Dinner for six</h3><p>$231 bill, 20% tip: $46.20 tip, $277.20 total, <b>$46.20 each</b>.</p></div>
<div><h3>Tip on the pre-tax amount</h3><p>$90 food + $7.20 tax. 18% of $90 = $16.20, total $113.40.</p></div>
<div><h3>Uneven split</h3><p>One person ordered $40 of a $100 bill. With 20% tip they pay 40 × 1.2 = <b>$48</b>; the rest share $72.</p></div></div></section>
<section><h2>Tipping customs differ by country</h2><p>In the United States, 15% to 20% is usual for table service, and many people tip 20% or more. In Canada 15% to 20% is also common. In the UK and much of Europe a 10% to 12.5% service charge is often already added to the bill, so check before tipping again.
In Japan and South Korea tipping is not expected. In Australia and New Zealand, tipping is optional and usually reserved for good service.</p></section>""",
[("How do I calculate a tip?", "Multiply the bill by the tip percentage as a decimal. An 18% tip on $84 is 84 × 0.18 = $15.12."),
 ("How do I split a bill with tip?", "Add the tip to the bill and divide the total by the number of people. $99.12 shared by four is $24.78 each."),
 ("Should I tip on the total before or after tax?", "Etiquette guides usually suggest tipping on the pre-tax amount, though many people tip on the total for simplicity. The difference is small."),
 ("How much should I tip at a restaurant in the US?", "15% to 20% of the pre-tax bill is standard for table service, with 20% or more common for good service."),
 ("What is a quick way to work out a 15% tip?", "Take 10% (move the decimal one place left) and add half of it. For $60: $6 + $3 = $9."),
 ("What if one person ordered much more?", "Work out each person's share of the food, then add the same tip percentage to each share instead of splitting equally.")])

C['accounting-equation-calculator'] = (
"""The accounting equation is <strong>Assets = Liabilities + Equity</strong>. Rearranged, <strong>Equity = Assets − Liabilities</strong> and <strong>Liabilities = Assets − Equity</strong>.
A business with $50,000 of assets and $20,000 of liabilities has <strong>$30,000 of equity</strong>.""",
"""<section><h2>What each part means</h2><ul>
<li><strong>Assets</strong>: what the business owns or controls: cash, money owed by customers (receivables), inventory, equipment, property.</li>
<li><strong>Liabilities</strong>: what it owes to others: loans, supplier bills (payables), wages owed, taxes due.</li>
<li><strong>Equity</strong>: the owners' claim on what is left: money the owners put in plus profits kept in the business, minus losses and withdrawals.</li></ul></section>
<section><h2>How transactions keep it balanced</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Transaction</th><th>Assets</th><th>Liabilities</th><th>Equity</th></tr></thead><tbody>
<tr><td>Owner invests $5,000 cash</td><td>+5,000 cash</td><td></td><td>+5,000</td></tr>
<tr><td>Borrow $10,000 from a bank</td><td>+10,000 cash</td><td>+10,000 loan</td><td></td></tr>
<tr><td>Buy $3,000 of stock on credit</td><td>+3,000 inventory</td><td>+3,000 payable</td><td></td></tr>
<tr><td>Pay the supplier $3,000</td><td>−3,000 cash</td><td>−3,000 payable</td><td></td></tr>
<tr><td>Earn $2,000 revenue in cash</td><td>+2,000 cash</td><td></td><td>+2,000 (profit)</td></tr>
<tr><td>Pay $800 rent</td><td>−800 cash</td><td></td><td>−800 (expense)</td></tr></tbody></table></div>
<p>After these six transactions: assets $16,200 = liabilities $10,000 + equity $6,200. Every transaction changes at least two items so that both sides stay equal; this is the basis of double-entry bookkeeping.</p></section>
<section><h2>The expanded equation</h2><p>Because profit increases equity, the equation is often written as <strong>Assets = Liabilities + Owner's capital + Revenue − Expenses − Drawings</strong>. This shows how day-to-day income and spending flow into the balance sheet.</p>
<p><strong>Negative equity</strong> means liabilities are larger than assets: the business owes more than it owns. It is a warning sign for lenders, though new businesses with start-up losses can show it for a while.</p></section>""",
[("What is the accounting equation?", "Assets = Liabilities + Equity. Everything a business owns is financed either by borrowing (liabilities) or by its owners (equity)."),
 ("How do I calculate equity?", "Subtract total liabilities from total assets. $50,000 of assets minus $20,000 of liabilities is $30,000 of equity."),
 ("Why must the accounting equation always balance?", "Because every transaction is recorded in at least two places in double-entry bookkeeping. If one side changes, another item changes by the same amount."),
 ("What is the expanded accounting equation?", "Assets = Liabilities + Owner's capital + Revenue − Expenses − Drawings. It splits equity into the parts that change it."),
 ("What does negative equity mean?", "Liabilities exceed assets, so the business owes more than it owns. Equity is negative when accumulated losses and withdrawals are larger than the owners' investment."),
 ("Is the accounting equation the same as a balance sheet?", "The balance sheet is the accounting equation in detail: it lists assets on one side and liabilities and equity on the other at a point in time.")])

C['gpa-calculator'] = (
"""Multiply each course's grade points by its credits, add the results and divide by the total credits.
An A (4.0) in a 3-credit course, a B (3.0) in a 4-credit course, an A− (3.7) in 3 credits and a C (2.0) in 2 credits give 39.1 quality points ÷ 12 credits = <strong>3.26 GPA</strong>.""",
"""<section><h2>4.0 grade point scale</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Letter</th><th class="n">Points</th><th>Typical %</th><th>Letter</th><th class="n">Points</th><th>Typical %</th></tr></thead><tbody>
<tr><td>A / A+</td><td class="n">4.0</td><td>93–100</td><td>C+</td><td class="n">2.3</td><td>77–79</td></tr>
<tr><td>A−</td><td class="n">3.7</td><td>90–92</td><td>C</td><td class="n">2.0</td><td>73–76</td></tr>
<tr><td>B+</td><td class="n">3.3</td><td>87–89</td><td>C−</td><td class="n">1.7</td><td>70–72</td></tr>
<tr><td>B</td><td class="n">3.0</td><td>83–86</td><td>D+ / D</td><td class="n">1.3 / 1.0</td><td>65–69</td></tr>
<tr><td>B−</td><td class="n">2.7</td><td>80–82</td><td>F</td><td class="n">0.0</td><td>Below 65</td></tr></tbody></table></div>
<p class="tp-note">Scales vary between schools; some count A+ as 4.3, and percentage cut-offs differ. Use your school's own scale where it is published.</p></section>
<section><h2>Worked example</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Course</th><th>Grade</th><th class="n">Points</th><th class="n">Credits</th><th class="n">Quality points</th></tr></thead><tbody>
<tr><td>Biology</td><td>A</td><td class="n">4.0</td><td class="n">3</td><td class="n">12.0</td></tr><tr><td>Calculus</td><td>B</td><td class="n">3.0</td><td class="n">4</td><td class="n">12.0</td></tr>
<tr><td>History</td><td>A−</td><td class="n">3.7</td><td class="n">3</td><td class="n">11.1</td></tr><tr><td>Art</td><td>C</td><td class="n">2.0</td><td class="n">2</td><td class="n">4.0</td></tr>
<tr><td colspan="3"><b>Total</b></td><td class="n"><b>12</b></td><td class="n"><b>39.1</b></td></tr></tbody></table></div>
<p>GPA = 39.1 ÷ 12 = <strong>3.26</strong>. Notice that the B in the 4-credit course pulls the average down more than it would in a 2-credit course.</p></section>
<section><h2>Cumulative GPA and raising your GPA</h2><p>To combine terms, add all quality points and divide by all credits. With a 3.20 GPA over 60 credits (192 quality points) and this term's 39.1 over 12 credits, the new cumulative GPA is (192 + 39.1) ÷ 72 = <strong>3.21</strong>.
The more credits you have completed, the more slowly your cumulative GPA moves, so improvements show fastest early on and in high-credit courses.</p>
<p><strong>Weighted versus unweighted:</strong> many US high schools add 0.5 or 1.0 point for honors, AP or IB classes (so an A can count as 5.0). Colleges often recalculate on an unweighted 4.0 scale.</p></section>""",
[("How is GPA calculated?", "Multiply each course's grade points by its credit hours to get quality points, add them up and divide by total credit hours."),
 ("What is a 3.5 GPA as a letter grade?", "Roughly between a B+ (3.3) and an A− (3.7) average on a 4.0 scale."),
 ("How do I calculate cumulative GPA?", "Add the quality points from all terms and divide by all credits attempted. Do not simply average the term GPAs unless every term had the same number of credits."),
 ("What is the difference between weighted and unweighted GPA?", "Unweighted GPA uses the 0–4.0 scale for every class. Weighted GPA adds extra points for harder classes such as honors, AP or IB, so it can exceed 4.0."),
 ("Do pass/fail courses count toward GPA?", "Usually not. Pass/fail credits count toward graduation but carry no grade points at most schools; check your school's policy."),
 ("How can I raise my GPA quickly?", "Focus on high-credit courses, since they carry the most weight, and on retaking failed courses if your school replaces the old grade.")])

C['final-grade-calculator'] = (
"""Required final score = (target grade − current grade × (1 − final weight)) ÷ final weight.
With <strong>82%</strong> going into a final worth <strong>30%</strong>, you need (85 − 82 × 0.70) ÷ 0.30 = <strong>92%</strong> on the final to finish with an 85%.""",
"""<section><h2>What you need on the final</h2><p>For a student with 82% going into a final worth 30% of the course grade:</p>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Target course grade</th><th class="n">Score needed on final</th></tr></thead><tbody>
<tr><td>90% (A−)</td><td class="n">108.7% (not possible)</td></tr><tr><td>85%</td><td class="n">92.0%</td></tr>
<tr><td>80% (B−)</td><td class="n">75.3%</td></tr><tr><td>70% (C−)</td><td class="n">42.0%</td></tr><tr><td>60% (D−)</td><td class="n">8.7%</td></tr></tbody></table></div>
<p>A result above 100% means the target cannot be reached on the final alone; a result below 0% means you have already secured it.</p></section>
<section><h2>Worked examples</h2><div class="mc-example-grid">
<div><h3>Heavy final</h3><p>Current 75%, final worth 40%, target 80%: (80 − 75 × 0.6) ÷ 0.4 = <b>87.5%</b>.</p></div>
<div><h3>Light final</h3><p>Current 91%, final worth 15%, target 90%: (90 − 91 × 0.85) ÷ 0.15 = <b>84.3%</b>.</p></div>
<div><h3>Points-based course</h3><p>If grades are in points, use your percentage so far: 412 of 480 points = 85.8%, then apply the formula.</p></div></div></section>
<section><h2>Things to check first</h2><ul>
<li><strong>Is your current grade already weighted?</strong> Learning platforms usually show a weighted current grade; use that number.</li>
<li><strong>Exam floors and drop rules.</strong> Some courses require a minimum score on the final to pass, or drop your lowest quiz, which changes the maths.</li>
<li><strong>Letter-grade cut-offs.</strong> Check your syllabus: an 89.5% is rounded to an A− in some courses and not in others.</li></ul></section>""",
[("How do I calculate what I need on my final exam?", "Subtract your current grade times the share of the course already completed from your target grade, then divide by the final's weight. With 82% now, a 30% final and an 85% target: (85 − 82 × 0.7) ÷ 0.3 = 92%."),
 ("What if the calculator says I need more than 100%?", "Your target is out of reach through the final alone, unless extra credit is available. Try a lower target to see what you can still achieve."),
 ("How much will the final exam change my grade?", "Each point on the final moves your course grade by the final's weight. On a 30% final, scoring 10 points higher raises your course grade by 3 points."),
 ("What if my class uses points instead of percentages?", "Convert to a percentage first by dividing the points earned by the points possible so far, and use the final's share of total points as its weight."),
 ("Can I fail a class by failing the final?", "Yes, if the final carries enough weight or the course requires a minimum exam score. Use the calculator with a 60% or 70% target to see the score you need to pass."),
 ("Is my current grade the same as my grade so far?", "Use the weighted grade for the work completed. If your platform shows a grade that already treats missing work as zero, it will understate your standing.")])

C['grade-calculator'] = (
"""Multiply each score by its weight, add the results and divide by the total weight you entered.
Homework 92% (weight 20), quizzes 78% (weight 30) and a midterm 85% (weight 25) give (18.4 + 23.4 + 21.25) ÷ 75 × 100 = <strong>84.1%</strong> so far.""",
"""<section><h2>Worked example</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Category</th><th class="n">Score</th><th class="n">Weight</th><th class="n">Score × weight</th></tr></thead><tbody>
<tr><td>Homework</td><td class="n">92%</td><td class="n">20%</td><td class="n">18.40</td></tr><tr><td>Quizzes</td><td class="n">78%</td><td class="n">30%</td><td class="n">23.40</td></tr>
<tr><td>Midterm</td><td class="n">85%</td><td class="n">25%</td><td class="n">21.25</td></tr><tr><td><b>Total</b></td><td></td><td class="n"><b>75%</b></td><td class="n"><b>63.05</b></td></tr></tbody></table></div>
<p>63.05 ÷ 75 = <strong>84.1%</strong>. The remaining 25% (perhaps a final exam) has not been graded yet; dividing by the weight completed gives your standing on the work done so far.</p></section>
<section><h2>Common US letter grade scale</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Letter</th><th>Percentage</th></tr></thead><tbody>
<tr><td>A</td><td>90–100%</td></tr><tr><td>B</td><td>80–89%</td></tr><tr><td>C</td><td>70–79%</td></tr><tr><td>D</td><td>60–69%</td></tr><tr><td>F</td><td>Below 60%</td></tr></tbody></table></div>
<p class="tp-note">Many schools add plus and minus grades and some use stricter cut-offs (for example 93% for an A). Your syllabus is the authority.</p></section>
<section><h2>Weighted versus unweighted averages</h2><p>A simple average treats every score equally: (92 + 78 + 85) ÷ 3 = 85%. The weighted average is 84.1% because the quiz score, the lowest, carries the most weight.
When categories have different weights, always use the weighted method. If your course grades by total points instead of weights, divide the points earned by the points possible.</p></section>""",
[("How do I calculate a weighted grade?", "Multiply each score by its weight, add the products and divide by the sum of the weights. Scores of 92, 78 and 85 with weights 20, 30 and 25 give 84.1%."),
 ("What if my weights don't add up to 100%?", "That is normal partway through a course. Dividing by the weight completed so far gives your current standing on the work graded."),
 ("What is the difference between weighted and points-based grading?", "Weighted grading assigns each category a fixed share of the grade. Points-based grading adds all points earned and divides by all points possible, so larger assignments count more automatically."),
 ("What percentage is a B?", "On the common US scale, 80% to 89%. Schools that use plus and minus grades often set B− at 80–82, B at 83–86 and B+ at 87–89."),
 ("How do I calculate my grade if a category is empty?", "Leave it out and divide by the weights of the categories that have scores. Including it as zero would understate your grade."),
 ("How do I find what I need on the final exam?", "Use the final grade calculator, which works backwards from your current weighted grade and the final's weight.")])

C['average-calculator'] = (
"""The average (arithmetic mean) is the sum of the values divided by how many there are.
For 4, 8, 15, 16, 23 and 42 the sum is 108, and 108 ÷ 6 = <strong>18</strong>.""",
"""<section><h2>Worked examples</h2><div class="mc-example-grid">
<div><h3>Weekly hours</h3><p>Worked 38, 42, 40, 36 and 44 hours: 200 ÷ 5 = <b>40 hours</b> a week on average.</p></div>
<div><h3>Test scores</h3><p>Scores of 72, 85, 90 and 81: 328 ÷ 4 = <b>82</b>.</p></div>
<div><h3>Monthly spending</h3><p>$1,240 + $1,180 + $1,420 = $3,840 over 3 months, an average of <b>$1,280</b>.</p></div></div></section>
<section><h2>When the plain average misleads</h2><ul>
<li><strong>Outliers.</strong> Salaries of $40k, $45k, $50k, $55k and $300k average $98k, but four of the five people earn far less. The median ($50k) describes the typical value better.</li>
<li><strong>Averaging averages.</strong> A class of 20 averaging 70% and a class of 30 averaging 80% have a combined average of (20 × 70 + 30 × 80) ÷ 50 = <strong>76%</strong>, not 75%. Weight each average by its group size.</li>
<li><strong>Rates and speeds.</strong> Driving 60 km at 30 km/h and 60 km back at 60 km/h averages 40 km/h, not 45, because you spend longer at the slower speed. Divide total distance by total time.</li>
<li><strong>Percentage returns.</strong> +50% one year and −50% the next averages 0% arithmetically, but $100 becomes $75. Use the geometric mean for growth rates.</li></ul></section>
<section><h2>Mean, median and mode</h2><p>The <strong>mean</strong> is the average above. The <strong>median</strong> is the middle value when sorted. The <strong>mode</strong> is the value that appears most often. For symmetric data the three are close; for skewed data such as incomes or house prices the median is usually the better summary.
The mean, median and mode calculator gives all three plus the range.</p></section>""",
[("How do I calculate an average?", "Add all the values and divide by how many values there are. The average of 4, 8, 15, 16, 23 and 42 is 108 ÷ 6 = 18."),
 ("What is the difference between average and median?", "The average (mean) uses every value's size; the median is the middle value. A few very large or small values pull the mean but barely move the median."),
 ("How do I calculate a weighted average?", "Multiply each value by its weight, add the results and divide by the sum of the weights."),
 ("Can I average percentages?", "Only if they are based on groups of the same size. Otherwise weight each percentage by its group size, or go back to the underlying totals."),
 ("How do I calculate average speed?", "Divide total distance by total time. Averaging the speeds of each leg gives the wrong answer when the legs take different amounts of time."),
 ("Does the average calculator handle negative numbers and decimals?", "Yes. Paste numbers separated by commas, spaces or new lines, including decimals and negatives.")])

C['fraction-calculator'] = (
"""To <strong>add or subtract</strong> fractions, rewrite them over a common denominator: 1/2 + 1/3 = 3/6 + 2/6 = <strong>5/6</strong>.
To <strong>multiply</strong>, multiply tops and bottoms: 2/3 × 9/10 = 18/30 = <strong>3/5</strong>. To <strong>divide</strong>, multiply by the flipped second fraction: 3/4 ÷ 1/8 = 3/4 × 8/1 = <strong>6</strong>.""",
"""<section><h2>Worked examples</h2><div class="mc-example-grid">
<div><h3>Subtract</h3><p>3/4 − 1/6. Common denominator 12: 9/12 − 2/12 = <b>7/12</b>.</p></div>
<div><h3>Mixed numbers</h3><p>2 1/2 + 1 3/4 = 5/2 + 7/4 = 10/4 + 7/4 = 17/4 = <b>4 1/4</b>.</p></div>
<div><h3>Recipe scaling</h3><p>A recipe needs 2/3 cup of milk; make 1 1/2 batches: 2/3 × 3/2 = <b>1 cup</b>.</p></div>
<div><h3>Simplify</h3><p>24/36: the greatest common factor is 12, so 24/36 = <b>2/3</b>.</p></div></div></section>
<section><h2>Fraction to decimal and percent</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Fraction</th><th class="n">Decimal</th><th class="n">Percent</th><th>Fraction</th><th class="n">Decimal</th><th class="n">Percent</th></tr></thead><tbody>
<tr><td>1/2</td><td class="n">0.5</td><td class="n">50%</td><td>1/8</td><td class="n">0.125</td><td class="n">12.5%</td></tr>
<tr><td>1/3</td><td class="n">0.333…</td><td class="n">33.3%</td><td>3/8</td><td class="n">0.375</td><td class="n">37.5%</td></tr>
<tr><td>2/3</td><td class="n">0.667…</td><td class="n">66.7%</td><td>5/8</td><td class="n">0.625</td><td class="n">62.5%</td></tr>
<tr><td>1/4</td><td class="n">0.25</td><td class="n">25%</td><td>1/5</td><td class="n">0.2</td><td class="n">20%</td></tr>
<tr><td>3/4</td><td class="n">0.75</td><td class="n">75%</td><td>1/10</td><td class="n">0.1</td><td class="n">10%</td></tr></tbody></table></div></section>
<section><h2>Common mistakes</h2><ul>
<li><strong>Adding denominators.</strong> 1/2 + 1/3 is not 2/5. The denominators must match before you add numerators.</li>
<li><strong>Forgetting to flip when dividing.</strong> Dividing by 1/8 is the same as multiplying by 8.</li>
<li><strong>Mixed numbers in multiplication.</strong> Convert 2 1/2 to 5/2 first; multiplying the whole parts and fraction parts separately gives the wrong answer.</li></ul></section>""",
[("How do I add fractions with different denominators?", "Find a common denominator (the least common multiple of the denominators), convert each fraction, then add the numerators. 1/2 + 1/3 = 3/6 + 2/6 = 5/6."),
 ("How do I divide fractions?", "Multiply the first fraction by the reciprocal of the second. 3/4 ÷ 1/8 = 3/4 × 8 = 6."),
 ("How do I simplify a fraction?", "Divide the numerator and denominator by their greatest common factor. 24/36 ÷ 12/12 = 2/3."),
 ("How do I convert a mixed number to an improper fraction?", "Multiply the whole number by the denominator and add the numerator. 2 1/2 = (2 × 2 + 1)/2 = 5/2."),
 ("How do I turn a fraction into a decimal?", "Divide the numerator by the denominator. 3/8 = 3 ÷ 8 = 0.375."),
 ("Why can't the denominator be zero?", "Division by zero is undefined, so a fraction with a zero denominator has no value.")])

C['ratio-calculator'] = (
"""To complete a proportion A : B = C : ?, cross-multiply: ? = B × C ÷ A. For 3 : 5 = 12 : ?, the answer is 5 × 12 ÷ 3 = <strong>20</strong>.
To simplify a ratio, divide both sides by their greatest common factor: 18 : 24 ÷ 6 = <strong>3 : 4</strong>.""",
"""<section><h2>Worked examples</h2><div class="mc-example-grid">
<div><h3>Recipe</h3><p>2 cups of flour make 12 cookies. For 30 cookies: 2 × 30 ÷ 12 = <b>5 cups</b>.</p></div>
<div><h3>Screen size</h3><p>A 16 : 9 image 1,920 pixels wide is 1,920 × 9 ÷ 16 = <b>1,080 pixels</b> tall.</p></div>
<div><h3>Share money</h3><p>Split $1,000 in the ratio 2 : 3. Total parts 5, one part $200: <b>$400 and $600</b>.</p></div>
<div><h3>Map scale</h3><p>At 1 : 50,000, 4 cm on the map is 200,000 cm = <b>2 km</b>.</p></div></div></section>
<section><h2>Ratios, fractions and percentages</h2><p>A ratio of 2 : 3 compares two parts. As fractions of the whole, the parts are 2/5 and 3/5, or 40% and 60%. To turn a part-to-part ratio into a share of the total, add the parts and divide each by the sum.</p>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Ratio</th><th>Shares of total</th><th>Common use</th></tr></thead><tbody>
<tr><td>1 : 1</td><td>50% / 50%</td><td>Equal split</td></tr><tr><td>16 : 9</td><td>64% / 36%</td><td>Widescreen video</td></tr>
<tr><td>4 : 3</td><td>57% / 43%</td><td>Older screens, photos</td></tr><tr><td>3 : 2</td><td>60% / 40%</td><td>35 mm photos</td></tr>
<tr><td>1 : 3</td><td>25% / 75%</td><td>Mixing concentrate and water</td></tr></tbody></table></div></section>
<section><h2>Common mistakes</h2><ul>
<li><strong>Keep the order.</strong> 3 : 5 is not the same as 5 : 3; keep the same quantity first on both sides of a proportion.</li>
<li><strong>Use the same units.</strong> Convert 30 minutes : 2 hours to 30 : 120 = 1 : 4 before simplifying.</li>
<li><strong>Not every relationship is proportional.</strong> Doubling a recipe's baking time or a fixed fee does not scale with the ratio.</li></ul></section>""",
[("How do I solve a ratio or proportion?", "Cross-multiply. For A : B = C : D, A × D = B × C, so the missing value is D = B × C ÷ A."),
 ("How do I simplify a ratio?", "Divide each number by their greatest common factor. 18 : 24 has a GCF of 6, so it simplifies to 3 : 4."),
 ("How do I split an amount in a ratio?", "Add the parts, divide the amount by that total to get one part, then multiply. $1,000 in a 2 : 3 ratio is $400 and $600."),
 ("How do I convert a ratio to a percentage?", "Divide each part by the sum of the parts and multiply by 100. 2 : 3 is 40% and 60%."),
 ("What is the ratio of 1920 by 1080?", "16 : 9. Both numbers divide by 120."),
 ("Can ratios have decimals?", "Yes. You can multiply both sides by the same number to clear decimals: 1.5 : 2 is the same as 3 : 4.")])

C['scientific-calculator'] = (
"""Type an expression and the calculator works it out using the standard order of operations: brackets first, then powers and roots, then multiplication and division, then addition and subtraction.
So <strong>2 + 3 × 4 = 14</strong>, while <strong>(2 + 3) × 4 = 20</strong>.""",
"""<section><h2>What you can type</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Operation</th><th>Type</th><th>Example</th><th class="n">Result</th></tr></thead><tbody>
<tr><td>Add, subtract, multiply, divide</td><td>+ − * /</td><td>18 / 4 + 2</td><td class="n">6.5</td></tr>
<tr><td>Powers</td><td>^</td><td>2^10</td><td class="n">1024</td></tr>
<tr><td>Square root</td><td>sqrt( )</td><td>sqrt(144)</td><td class="n">12</td></tr>
<tr><td>Other roots</td><td>^(1/n)</td><td>27^(1/3)</td><td class="n">3</td></tr>
<tr><td>Pi</td><td>pi or π</td><td>pi * 5^2</td><td class="n">78.54</td></tr>
<tr><td>Sine, cosine, tangent</td><td>sin( ) cos( ) tan( )</td><td>sin(pi/6)</td><td class="n">0.5</td></tr></tbody></table></div>
<p><strong>Angles are in radians.</strong> To use degrees, multiply by pi/180: sin(30 × pi/180) = 0.5. One full turn is 2π radians = 360°.</p></section>
<section><h2>Worked examples</h2><div class="mc-example-grid">
<div><h3>Area of a circle</h3><p>Radius 7 cm: pi * 7^2 = <b>153.94 cm²</b>.</p></div>
<div><h3>Compound growth</h3><p>$1,000 at 5% for 10 years: 1000 * 1.05^10 = <b>$1,628.89</b>.</p></div>
<div><h3>Pythagoras</h3><p>Sides 6 and 8: sqrt(6^2 + 8^2) = <b>10</b>.</p></div>
<div><h3>Height of a ramp</h3><p>4 m long at 10°: 4 * sin(10 * pi/180) = <b>0.69 m</b>.</p></div></div></section>
<section><h2>Order-of-operations traps</h2><ul>
<li><strong>Division and multiplication go left to right.</strong> 8 / 2 * 4 = 16, not 1. Add brackets if you mean 8 / (2 × 4).</li>
<li><strong>Negative numbers and powers.</strong> Always put a negative base in brackets: (−3)^2 = 9. Without brackets the expression is ambiguous and may be rejected.</li>
<li><strong>Fractions in exponents.</strong> 8^1/3 is read as (8^1) / 3. Write 8^(1/3) for the cube root.</li>
<li><strong>Rounding.</strong> Results are shown to a sensible number of decimal places; very large or tiny numbers may appear in scientific notation.</li></ul></section>""",
[("Does the scientific calculator use degrees or radians?", "Radians. To work in degrees, multiply the angle by pi/180, for example sin(30 * pi/180) = 0.5."),
 ("How do I type a square root or cube root?", "Use sqrt(x) for a square root and x^(1/3) for a cube root. Any nth root is x^(1/n)."),
 ("What order does the calculator use?", "Brackets, then powers and roots, then multiplication and division from left to right, then addition and subtraction from left to right."),
 ("Why does 8 / 2 * 4 equal 16?", "Multiplication and division have equal priority and are worked left to right: 8 / 2 = 4, then 4 × 4 = 16."),
 ("How do I use pi?", "Type pi or tap the π key. pi * 5^2 gives the area of a circle with radius 5."),
 ("Is my calculation sent anywhere?", "No. Expressions are evaluated in your browser.")])

C['standard-deviation-calculator'] = (
"""Standard deviation measures how far values typically sit from the mean. Find the mean, square each value's distance from it, average those squares and take the square root.
For 2, 4, 4, 4, 5, 5, 7, 9 the mean is 5 and the <strong>population standard deviation is 2</strong>; the <strong>sample standard deviation is 2.14</strong>.""",
"""<section><h2>Step by step</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th class="n">Value</th><th class="n">Minus mean (5)</th><th class="n">Squared</th></tr></thead><tbody>
<tr><td class="n">2</td><td class="n">−3</td><td class="n">9</td></tr><tr><td class="n">4</td><td class="n">−1</td><td class="n">1</td></tr><tr><td class="n">4</td><td class="n">−1</td><td class="n">1</td></tr><tr><td class="n">4</td><td class="n">−1</td><td class="n">1</td></tr>
<tr><td class="n">5</td><td class="n">0</td><td class="n">0</td></tr><tr><td class="n">5</td><td class="n">0</td><td class="n">0</td></tr><tr><td class="n">7</td><td class="n">2</td><td class="n">4</td></tr><tr><td class="n">9</td><td class="n">4</td><td class="n">16</td></tr>
<tr><td colspan="2"><b>Sum of squares</b></td><td class="n"><b>32</b></td></tr></tbody></table></div>
<p>Population variance = 32 ÷ 8 = 4, so σ = √4 = <strong>2</strong>. Sample variance = 32 ÷ 7 = 4.571, so s = √4.571 = <strong>2.14</strong>.</p></section>
<section><h2>Population or sample?</h2><p>Use the <strong>population</strong> formula (divide by n) when your data includes every member of the group you care about, such as the scores of everyone in one class.
Use the <strong>sample</strong> formula (divide by n − 1) when your data is a sample used to estimate a larger group, such as 50 customers surveyed out of thousands. Dividing by n − 1 (Bessel's correction) corrects the tendency of a sample to understate the spread.</p></section>
<section><h2>Reading the result</h2><p>For roughly bell-shaped data, about <strong>68%</strong> of values fall within 1 standard deviation of the mean, <strong>95%</strong> within 2 and <strong>99.7%</strong> within 3. If exam scores average 70 with a standard deviation of 8, about two-thirds of students scored between 62 and 78.</p>
<p>A small standard deviation means values cluster tightly around the mean; a large one means they are spread out. Because it is in the same units as the data, it is easier to interpret than the variance. To compare spread between datasets with different means, use the coefficient of variation (standard deviation ÷ mean).</p></section>""",
[("How do I calculate standard deviation?", "Find the mean, subtract it from each value, square the results, add them up, divide by n (population) or n − 1 (sample), and take the square root."),
 ("What is the difference between population and sample standard deviation?", "Population standard deviation divides by the number of values n and is used when you have every value. Sample standard deviation divides by n − 1 and is used to estimate the spread of a larger group from a sample."),
 ("What does a standard deviation of 0 mean?", "Every value is identical, so there is no spread around the mean."),
 ("What is the 68-95-99.7 rule?", "For normally distributed data, about 68% of values lie within one standard deviation of the mean, 95% within two and 99.7% within three."),
 ("What is variance?", "Variance is the average squared distance from the mean, and standard deviation is its square root. Standard deviation is easier to read because it uses the same units as the data."),
 ("Which one does Excel use?", "STDEV.S (or STDEV) gives the sample standard deviation; STDEV.P gives the population standard deviation.")])

C['mean-median-mode-calculator'] = (
"""<strong>Mean</strong> = sum ÷ count. <strong>Median</strong> = the middle value when sorted (the average of the two middle values if the count is even). <strong>Mode</strong> = the most frequent value. <strong>Range</strong> = largest − smallest.
For 2, 4, 4, 4, 5, 5, 7, 9: mean <strong>5</strong>, median <strong>4.5</strong>, mode <strong>4</strong>, range <strong>7</strong>.""",
"""<section><h2>Worked example with an odd count</h2><p>House prices (in $1,000s): 210, 245, 260, 275, 940.</p><ul>
<li>Mean = 1,930 ÷ 5 = <strong>386</strong></li><li>Median = the third value = <strong>260</strong></li><li>Mode = none (every value appears once)</li><li>Range = 940 − 210 = <strong>730</strong></li></ul>
<p>One expensive house lifts the mean far above what most of the homes cost. This is why house prices and incomes are usually reported as medians.</p></section>
<section><h2>Which measure should you use?</h2>
<div class="tp-scroll"><table class="tp-table"><thead><tr><th>Measure</th><th>Best for</th><th>Weakness</th></tr></thead><tbody>
<tr><td>Mean</td><td>Symmetric data without extreme values; totals and budgets</td><td>Pulled by outliers</td></tr>
<tr><td>Median</td><td>Skewed data such as incomes, prices, waiting times</td><td>Ignores how far the extremes are</td></tr>
<tr><td>Mode</td><td>Categories and the most common choice (shoe size, survey answer)</td><td>There may be none, or several</td></tr>
<tr><td>Range</td><td>A quick sense of spread</td><td>Depends only on the two extreme values</td></tr></tbody></table></div></section>
<section><h2>Finding the median step by step</h2><ol><li>Sort the values from smallest to largest.</li><li>If the count is odd, the median is the middle value: position (n + 1) ÷ 2.</li>
<li>If the count is even, average the two middle values: for 3, 7, 8, 12 the median is (7 + 8) ÷ 2 = 7.5.</li></ol>
<p>A dataset can have more than one mode (bimodal or multimodal) or no mode at all when every value appears the same number of times. For a fuller picture of spread, add the standard deviation.</p></section>""",
[("How do I find the mean, median and mode?", "Mean: add all values and divide by the count. Median: sort the values and take the middle one (or the average of the two middle ones). Mode: the value that appears most often."),
 ("What is the median of an even set of numbers?", "The average of the two middle values after sorting. For 3, 7, 8 and 12 the median is 7.5."),
 ("Can there be more than one mode?", "Yes. If two or more values tie for most frequent, the data is bimodal or multimodal. If every value appears equally often, there is no mode."),
 ("When is the median better than the mean?", "When the data is skewed or has outliers, such as incomes or house prices. The median shows the typical value without being pulled by a few extreme numbers."),
 ("How do I calculate the range?", "Subtract the smallest value from the largest. For 2 to 9 the range is 7."),
 ("What is the difference between mean and average?", "In everyday use they mean the same thing: the arithmetic mean. Median and mode are other kinds of average.")])
