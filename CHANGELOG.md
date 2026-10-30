# Changelog

## 2026-10-30

- Upgrade the supported runtime to Django 5.2 LTS.
- Return form errors for duplicate or missing product names.
- Store prices as decimals and enforce positive quantities and nonnegative prices.
- Require login for product, purchase and summary pages.
- Replace per-product queries with one product query and one purchase query.
- Load secrets and host settings from the environment; remove IDE state from tracking.
- Add migrations, tests, CI and setup documentation.
