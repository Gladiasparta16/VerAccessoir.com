Deployment guide — quick steps

This folder contains guidance and sample files to deploy the project.

1) Backend (deploy anywhere supporting Python/WSGI)
   - Connect your Git repository and select the branch to deploy.
   - Set the root/build to the `BACKEND` folder and install requirements from `BACKEND/requirements.txt`.
   - Set environment variables on your host using `BACKEND/.env.example` as a reference.
   - Start command for a WSGI server (example):
       gunicorn app:app --bind 0.0.0.0:$PORT

2) Frontend (static hosting or serve from backend)
   - The `FRONTEND` folder is static HTML/CSS/JS; you can host it on any static hosting or serve it with the backend.
   - No build command needed if purely static; ensure the publish directory is `FRONTEND`.
   - If the backend is on a different domain, configure `API_BASE_URL` appropriately in the hosting environment or via a small config file.

3) Env vars (minimum)
   - SECRET_KEY
   - JWT_SECRET_KEY
   - FLASK_DEBUG=False
   - DATABASE_URL

4) Security checklist
   - Ensure `FLASK_DEBUG` is false in production.
   - Restrict CORS to your frontend origin (modify `CORS(app)` configuration if needed).
   - Use HTTPS for frontend and backend.
   - Do not commit `.env` to the repo.

5) Post-deploy test
   - Visit frontend URL and try adding a product to the cart — badge should update.
   - Check `/api/health` on backend URL.

6) Creating initial admin (recommended secure flow)
   - Preferred: use `BACKEND/create_admin.py` after the app and DB are deployed.
     - On the server, run:
       ```bash
       python BACKEND/create_admin.py
       ```
       The script will prompt for email and password (or read `INITIAL_ADMIN_EMAIL` and `INITIAL_ADMIN_PASSWORD` env vars).
   - Alternative: set `INITIAL_ADMIN_EMAIL` and `INITIAL_ADMIN_PASSWORD` in your env and run `python BACKEND/init_db.py` once. Then remove those env vars immediately.

7) Mail & password reset
   - Configure SMTP env vars (see DEPLOY/ENV_VARS.md) so the `/api/auth/forgot` endpoint sends real emails.
   - If SMTP is not configured, the forgot/reset flow will still work in DEBUG mode and return a token for testing.

