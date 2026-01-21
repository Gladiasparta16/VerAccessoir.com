Environment variables required for production

- SECRET_KEY: Flask secret key (use a secure random string)
- JWT_SECRET_KEY: Secret used to sign JWT tokens (secure random)
- FLASK_DEBUG: set to `False` in production
- DATABASE_URL: DB connection string (e.g. Postgres)
- SENTRY_DSN: optional, for error monitoring

Notes:
- Store secrets in the hosting provider's secret manager (Render / Netlify / Vercel env settings).
- Never commit `.env` with real secrets.
