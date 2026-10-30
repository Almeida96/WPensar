# Contributing

Install `requirements.txt`, run migrations on a disposable database, and run `python manage.py test`. Include migrations for model changes and test both the form and database boundaries.

Keep monetary calculations in Decimal. Query-count regressions belong in the purchase-summary tests. Do not commit SQLite databases, production settings or real purchase records.
