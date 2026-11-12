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
| build_shopping.py | Black Friday deal, unit price, BNPL and price drop calculators |

`tax_common.py` holds the shared page template, styles and calculator helpers.
`expand_content.py` / `apply_expand.py` and `expand_dt.py` / `apply_dt.py` hold extra content added to math and date-time tools (the apply scripts skip pages that already have it).

When a tax rate changes, edit the numbers in the matching script and run it again, rather than editing the HTML by hand; otherwise the next rebuild will overwrite the hand edit.
