# WPensar purchase tracker

A Django application for registering products and purchases, then comparing total spend and quantity-weighted unit prices. This repository began as a small programming exercise; the current version adds validation, decimal money values, authentication and regression tests.

## Run locally

Requires Python 3.11+.

```sh
python -m venv .venv
# Activate .venv for your shell.
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open [the local admin login](http://127.0.0.1:8000/admin/login/), sign in, then use:

| Path | Purpose |
| --- | --- |
| `/adicionar-produto/` | Register a product |
| `/adicionar-compra/` | Record quantity and unit price |
| `/compras/` | View totals and weighted average prices |

All application pages require an authenticated account. This is a shared purchase register: signed-in users see the same records. It does not implement per-user ownership, payments or stock control.

## Calculation

Two units at 0.10 plus one unit at 0.40 cost 0.60. The weighted average is 0.20 per unit, rather than the unweighted mean of the two purchase prices.

Prices use decimal values with two fractional digits. Quantity must be at least one; price cannot be negative. Product names are trimmed and duplicate names are rejected case-insensitively for SQLite's supported case mappings. The summary uses two queries regardless of the number of products.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `DJANGO_DEBUG` | `true` | Local development mode |
| `DJANGO_SECRET_KEY` | Random per process in debug mode | Set a persistent secret outside Git |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated hostnames |

With debug disabled, a secret is required and cookies require HTTPS. The development server binds to loopback by default. Configure a production server, HTTPS, backups and static-file serving before exposing the app. A random development key invalidates sessions when the server restarts.

SQLite data lives in `db.sqlite3`, which is ignored by Git. Back up an older database before migration. Existing zero/negative quantities, missing prices or duplicate product names must be corrected before the new constraints can be applied; migrations do not delete those records automatically. Float prices from the original schema are converted to two-decimal values.

## Development

```sh
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Tests cover duplicate and missing names, database constraints, authenticated forms, exact monetary totals and query count. See [contributing](CONTRIBUTING.md) and [changes](CHANGELOG.md).

No application-source license has been declared.
