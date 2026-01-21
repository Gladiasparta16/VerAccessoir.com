import os
from dotenv import load_dotenv

# Charger .env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


class Config:
    # ⚠️ SECRET_KEY DOIT être en .env en production
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-fallback-key")
    if not SECRET_KEY and os.environ.get("FLASK_ENV") == "production":
        raise ValueError(
            "❌ ERREUR CRITIQUE: SECRET_KEY non défini! Créer fichier .env avec SECRET_KEY=..."
        )

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///database.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_HEADERS = "Content-Type"

    # =================== SÉCURITÉ ===================

    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 heure

    # Session
    SESSION_COOKIE_SECURE = True  # HTTPS only
    SESSION_COOKIE_HTTPONLY = True  # Pas d'accès JavaScript
    SESSION_COOKIE_SAMESITE = "Lax"  # CSRF protection
    PERMANENT_SESSION_LIFETIME = 86400  # 24 heures

    # Upload
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # Max 5MB
    UPLOAD_FOLDER = "uploads"
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}

    # Rate limiting
    RATELIMIT_STORAGE_URL = "memory://"

    # Security headers
    SECURITY_HEADERS = {
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'",
    }
