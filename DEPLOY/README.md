Deployment guide — quick steps

This folder contains guidance and sample files to deploy the project.

1) Backend (recommended: Render / Railway / Fly)
   - Connect your GitHub repository and select branch `main` (or the branch you want).
   - Set the root/build to the `BACKEND` folder.
   - Install requirements from `BACKEND/requirements.txt`.
   - Set environment variables in the host dashboard using `BACKEND/.env.example` as reference.
   - Start command (Render / Railway):
       gunicorn app:app --bind 0.0.0.0:$PORT

2) Frontend (recommended: Netlify / Vercel)
   - Create a new site from Git and point to the `FRONTEND` folder.
   - No build command needed if purely static; set publish directory to `FRONTEND`.
   - If the backend is on a different domain, set `API_BASE_URL` in the site settings as an environment variable (Netlify: `window.API_BASE_URL`).

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
