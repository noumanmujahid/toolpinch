# ToolPinch build scripts

These Python scripts generate some of the calculator pages in `tools/`. They are not published to the website (`build.sh` excludes this folder).

Run any of them from the repository root, for example:

    PYTHONPATH=scripts python3 scripts/build_us.py

| Script | Page it writes |
|---|---|
| build_vat.py | tools/vat-calculator.html |
| build_us.py | tools/us-paycheck-calculator.html |
| build_uk.py | tools/uk-take-home-pay-calculator.html |
| build_ca.py | tools/canada-take-home-pay-calculator.html |
| build_au.py | tools/australia-take-home-pay-calculator.html |
| build_in.py | tools/india-income-tax-calculator.html |
| build_pk.py | tools/pakistan-salary-tax-calculator.html |
| build_2027brackets.py | tools/2027-tax-brackets.html |
| build_bonus.py | tools/bonus-tax-calculator.html |
| build_federal.py | tools/federal-pay-periods-2027.html |
| build_minwage.py | tools/minimum-wage-2027.html |
| build_emergency.py | tools/emergency-supply-calculator.html |
| build_ss.py | tools/social-security-payment-schedule-2027.html |
| build_holiday.py | tools/holiday-pay-calculator.html |
| build_refund.py | tools/tax-refund-estimator.html |
| build_shopping.py | Black Friday deal, unit price, BNPL and price drop calculators |

`tax_common.py` holds the shared page template, styles and calculator helpers.
`expand_content.py` / `apply_expand.py` and `expand_dt.py` / `apply_dt.py` hold extra content added to math and date-time tools (the apply scripts skip pages that already have it).

When a tax rate changes, edit the numbers in the matching script and run it again, rather than editing the HTML by hand; otherwise the next rebuild will overwrite the hand edit.
| cleanup_offtopic.py | Nov 21 2026: removed 35 off-topic SEO, novelty and thin math pages and all links to them (already run; kept for the record) |
| make_embeds.py | Builds /embed widgets for the US paycheck, tax refund and holiday pay calculators from the generated tool pages |
| build_estimated.py | /tools/quarterly-estimated-tax-calculator: 2026 federal estimated tax, SE tax, QBI, safe harbor |
| fed_dates.py | Shared federal holiday rules, leave years and NFC pay date logic (self-checked against the 2027 NFC schedule) |
| build_payperiod_now.py | /tools/what-pay-period-is-it: federal pay period for any date, leave years 2026-2028 |
| build_gs2027.py | /tools/gs-pay-scale-2027: 2026 GS base + 58 locality areas (verified vs OPM), 2027 raise status. UPDATE when the December 2026 pay executive order and OPM 2027 tables are published |
| build_holidays_military_2027.py | /tools/federal-holidays-2027 and /tools/military-pay-dates-2027 (OPM, Federal Reserve K.8 and DFAS rules) |
| build_paycheck2027.py | /tools/2027-paycheck-calculator: 2026 vs 2027 paycheck (IRS brackets, SSA wage base $192,300, 401(k) $25,500) |
| build_refund_date.py | /tools/tax-refund-schedule-2027: refund date estimator. UPDATE OPEN date when the IRS announces the 2027 filing season start (January) and the EITC/ACTC date |
