Title: fix(frontend,backend): fix client storage, API fallback, migrations, E2E tests

Summary:
- Centralized and hardened localStorage usage (added `js/utils/storage.js`).
- Fixed cart badge and cart helpers to handle missing `window.storage` and fallback to localStorage.
- Added API fallback (`http://127.0.0.1:5000/api`) in `js/api/client.js` to avoid 404/HTML responses when front is served by a static dev server.
- Made product loader (`products.js`) use `APIClient.getProducts()` with safe fallbacks.
- Added `tools/run_migrations.py` to apply small SQLite migrations (adds `featured` column if missing).
- Improved QA script `tools/qa_test.py` to wait for server readiness and provide clearer errors.
- Added/ran Playwright E2E scripts and fixed frontend issues uncovered by tests.

Checklist:
- [x] linter & formatting run (ruff, prettier where applicable)
- [x] QA script passes locally
- [x] E2E smoke tests run locally
- [x] DB migration helper in `tools/run_migrations.py`
- [x] Branch pushed: `fix/all-errors-e2e`

How to test locally:
1. Activate venv: `.venv\Scripts\Activate.ps1`
2. Install deps: `pip install -r BACKEND/requirements.txt`
3. (Optional) Install Playwright: `pip install playwright` then `playwright install chromium`
4. Start server: `.venv\Scripts\python.exe BACKEND/app.py`
5. If needed, initialize DB: `.venv\Scripts\python.exe BACKEND/init_db.py`
6. Run migrations: `.venv\Scripts\python.exe tools/run_migrations.py`
7. Run QA: `.venv\Scripts\python.exe tools/qa_test.py`
8. Run E2E (optional): `.venv\Scripts\python.exe BACKEND/tools/e2e_shop_cart_test.py`

Notes:
- I could not create the GitHub PR automatically (no `gh` CLI or token), but the branch is pushed. Use the link provided by Git to open the PR, or I can create the PR if you provide a token/allow me.
