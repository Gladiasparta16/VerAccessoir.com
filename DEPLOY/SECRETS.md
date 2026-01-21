Where to store secrets and how to create initial admin/test accounts

Files and locations:
- `BACKEND/.env` (NOT committed) — create this file on your server or set env vars in the hosting dashboard.
- `BACKEND/.env.example` — template included in repo.

Important environment variables:
- `SECRET_KEY` — Flask secret key (generate a secure random string)
- `JWT_SECRET_KEY` — JWT signing key
- `FLASK_DEBUG` — set to `False` in production
- `DATABASE_URL` — e.g. `postgresql://user:pass@host:5432/dbname`
- `SENTRY_DSN` — optional

Variables for creating initial users (optional):
- `INITIAL_ADMIN_EMAIL` — if set, `init_db.py` will create an admin with this email
- `INITIAL_ADMIN_PASSWORD` — password for the above admin (use a strong password)
- `INITIAL_TEST_USER_EMAIL` — (optional) create a test user
- `INITIAL_TEST_USER_PASSWORD` — password for the test user

Notes:
- Never commit `BACKEND/.env` to Git. Use the hosting provider's secret manager.
- After the first run (admin created), rotate passwords and remove `INITIAL_*` vars.
- For QA scripts, set `QA_ADMIN_EMAIL` and `QA_ADMIN_PASSWORD` as needed (only for testing environments).
