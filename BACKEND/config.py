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

    # Normalize SQLite path to an absolute path inside BACKEND to avoid issues when
    # the process is started from a different working directory (prevents using
    # different empty DB files and causing intermittent auth failures).
    _db_url = os.environ.get("DATABASE_URL", "sqlite:///database.db")
    if _db_url.startswith("sqlite:///"):
        _db_path = _db_url.replace("sqlite:///", "")
        # If the user gave a relative path, prefer the file under BACKEND/instance
        # if it exists (this is where init_db writes the DB during setup).
        if not os.path.isabs(_db_path):
            backend_dir = os.path.dirname(__file__)
            candidate = os.path.join(backend_dir, _db_path)
            instance_candidate = os.path.join(backend_dir, "instance", os.path.basename(_db_path))
            if os.path.exists(instance_candidate):
                _db_path = instance_candidate
            else:
                _db_path = candidate
        _db_url = f"sqlite:///{os.path.abspath(_db_path)}"
    SQLALCHEMY_DATABASE_URI = _db_url

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_HEADERS = "Content-Type"

    # =================== SÉCURITÉ ===================

    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 heure

    # DEBUG mode (useful for local override)
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() in ("1", "true", "yes")

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

    # Security headers (can be overridden via environment in .env)
    # connect-src includes https: to allow frontends hosted on HTTPS-only platforms
    SECURITY_HEADERS = {
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' https:",
    }
