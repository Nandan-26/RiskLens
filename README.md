# RiskLens – Business Verification & Risk Intelligence API (Portfolio Demo)

Flask/MySQL REST backend with business CRUD, validation, filtering, pagination, practice web scraping into a separate `scraped_books` table, and **illustrative** data-completeness scoring. This is not a real business verification, compliance, or credit risk product.

## Windows setup
1. Extract ZIP into a writable folder, e.g. `C:\Users\eswar\Documents\RiskLens` (do not extract under another account's protected user folder).
2. In CMD in the extracted project folder: `py -m venv .venv` then `.venv\Scripts\activate` then `python -m pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and enter your local MySQL password. Never commit `.env`.
4. Run `schema.sql` using MySQL Workbench or `mysql -u root -p < schema.sql` if mysql CLI is on PATH. This creates development and separate test databases.
5. Run `python test_risklens.py` (WARNING: tests delete records in **risklens_test_db** only; use a dedicated disposable test database).
6. Run `python run.py`; check `http://127.0.0.1:5000/api/health`. Import `Postman_Collection.json` into Postman.

## Routes
`GET /api/health`; `POST/GET /api/businesses`; `GET/PUT/DELETE /api/businesses/<id>`; `POST /api/scrape/practice-site`; `GET /api/risk/evaluate/<id>`.

No live credentials are packaged. Automated tests require a running MySQL instance and initialized schema; syntax checks alone do not establish passing integration tests.
## Verification

- Flask health endpoint returned a healthy MySQL connection.
- Automated test suite: 4 tests passed.
- Development and testing use separate MySQL databases.
- The scoring functionality is illustrative only.
