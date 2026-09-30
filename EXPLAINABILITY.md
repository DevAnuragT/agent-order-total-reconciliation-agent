# Decision and Reasoning

An order reconciles when line extensions and the declared discount and tax produce the stated total exactly. The implementation returns structured findings so a reviewer can see how each result was derived.

# Inputs and Data Sources

The caller supplies a currency code, unique line identifiers, unit prices and quantities in minor units, discount, tax, and total in the same currency. The only data source is the caller-provided payload plus the checked-in rules and code; no network or private-file access is used.

# Known Limitations and Constraints

This is arithmetic validation only. It does not determine tax law, refund eligibility, payment settlement, or whether a price is commercially correct. The result is a bounded pre-review aid and must not be presented as professional certification or an official HiDevs result.
