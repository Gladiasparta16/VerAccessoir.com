from app import app

# app est l'instance Flask créée par create_app() dans app.py
# command for production test: gunicorn -w 3 -b 0.0.0.0:5000 wsgi:app
