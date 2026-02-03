Environment variables required for production

- SECRET_KEY: Flask secret key (use a secure random string)
- JWT_SECRET_KEY: Secret used to sign JWT tokens (secure random)
- FLASK_DEBUG: set to `False` in production
- DATABASE_URL: DB connection string (e.g. Postgres)
- SENTRY_DSN: optional, for error monitoring

Mail settings (for password reset emails):
- MAIL_SERVER: e.g. smtp.sendgrid.net or smtp.gmail.com
- MAIL_PORT: 587
- MAIL_USERNAME: SMTP username
- MAIL_PASSWORD: SMTP password
- MAIL_USE_TLS: True/False
- MAIL_DEFAULT_SENDER: optional from address

Password reset token expiration:
- PASSWORD_RESET_TOKEN_EXP: seconds (default 3600)

Frontend origin (optional):
- FRONTEND_ORIGIN: full URL of frontend (used to build reset links)

Notes:
- Store secrets in your host's secret manager or a secure vault; do not commit `.env` with real secrets.
- Ensure FLASK_DEBUG is disabled in production and use HTTPS for both frontend and backend.
