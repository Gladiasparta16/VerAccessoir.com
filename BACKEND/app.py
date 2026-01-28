from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from csrf_protection import init_csrf
import os
from datetime import timedelta
from time import time

# =================== INITIALISATION ===================
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "..", "FRONTEND"),
    static_url_path="",
)
CORS(app)

# Configuration
app.config.from_object(Config)

# Initialiser la base de données
db.init_app(app)

# JWT
jwt = JWTManager(app)

# CSRF Protection
init_csrf(app)

# =================== CONFIGURATION SESSION ===================
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)
app.config["SESSION_COOKIE_SECURE"] = not app.debug  # True en production
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


# =================== SÉCURITÉ HEADERS ===================
@app.after_request
def set_security_headers(response):
    """Ajouter les headers de sécurité à chaque réponse"""
    # Apply headers defined in configuration so they can be changed from .env
    sec = app.config.get("SECURITY_HEADERS", {})
    for k, v in sec.items():
        try:
            response.headers[k] = v
        except Exception:
            pass

    # Default security headers (only set if not provided by config)
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-XSS-Protection", "1; mode=block")

    # Content Security Policy: if not already set via config, set a sensible default.
    if "Content-Security-Policy" not in response.headers:
        default_src = "'self'"
        connect_src = "'self'"
        if app.debug:
            dev_hosts = (
                "http://127.0.0.1:5500 http://localhost:5500 "
                "ws://127.0.0.1:5500 ws://localhost:5500 http://127.0.0.1:9222"
            )
            # Allow dev hosts in both default-src and connect-src to reduce CSP noise during development
            default_src = f"'self' {dev_hosts}"
            connect_src = f"'self' {dev_hosts}"

        response.headers["Content-Security-Policy"] = (
            f"default-src {default_src}; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            f"connect-src {connect_src}"
        )

    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers["Permissions-Policy"] = (
        "geolocation=(), microphone=(), camera=(), payment=()"
    )

    if not app.debug:
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )

    return response


# =================== RATE LIMITING ===================
request_history = {}
failed_logins = {}  # Track failed login attempts
MAX_REQUESTS_PER_MINUTE = 100
MAX_FAILED_LOGINS = 5
LOCKOUT_TIME = 900  # 15 minutes


@app.before_request
def check_rate_limit():
    """Vérifier le rate limiting par IP"""
    ip = request.remote_addr
    current_time = time()

    if ip not in request_history:
        request_history[ip] = []

    # Nettoyer les anciennes requêtes (> 1 minute)
    request_history[ip] = [t for t in request_history[ip] if current_time - t < 60]

    # Si trop de requêtes, bloquer (100 par minute)
    if len(request_history[ip]) > MAX_REQUESTS_PER_MINUTE:
        return jsonify({"error": "Rate limit exceeded. Try again later."}), 429

    # Enregistrer la requête
    request_history[ip].append(current_time)

    # ⚠️ Rate limiting sur tentatives de connexion échouées
    if request.path == "/api/auth/login" and request.method == "POST":
        if ip not in failed_logins:
            failed_logins[ip] = {"count": 0, "lockout_until": 0}

        # Vérifier si l'IP est bloquée
        if current_time < failed_logins[ip]["lockout_until"]:
            return (
                jsonify(
                    {
                        "error": f'Trop de tentatives échouées. Réessayez dans {int(failed_logins[ip]["lockout_until"] - current_time)} secondes.'
                    }
                ),
                429,
            )


# =================== PROTECTION DIRECTORY TRAVERSAL ===================
@app.before_request
def prevent_directory_traversal():
    """Prévenir les attaques directory traversal"""
    # Bloquer .. dans l'URL
    if ".." in request.path:
        return jsonify({"error": "Invalid path"}), 400


# =================== REGISTRER LES BLUEPRINTS ===================
from routes.products import products_bp
from routes.auth import auth_bp
from routes.orders import orders_bp
from routes.admin import admin_bp

app.register_blueprint(products_bp, url_prefix="/api/products")
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(orders_bp, url_prefix="/api/orders")
app.register_blueprint(admin_bp, url_prefix="/api/admin")


# =================== ROUTES API ===================
@app.route("/api/health", methods=["GET"])
def health():
    return {"status": "OK", "message": "API is running"}, 200


# Backwards-compatible health endpoint for auth prefix
@app.route("/api/auth/health", methods=["GET"])
def auth_health():
    return {"status": "OK", "message": "Auth API is running"}, 200


# =================== SERVIR LE FRONTEND ===================
@app.route("/")
@app.route("/index.html")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")


# Routes explicites pour pages situées dans FRONTEND/pages
@app.route("/shop.html")
def serve_shop():
    return send_from_directory(os.path.join(app.static_folder, "pages"), "shop.html")


@app.route("/cart.html")
def serve_cart():
    return send_from_directory(os.path.join(app.static_folder, "pages"), "cart.html")


@app.route("/login.html")
def serve_login():
    return send_from_directory(os.path.join(app.static_folder, "pages"), "login.html")


@app.route("/admin-login.html")
def serve_admin_login():
    return send_from_directory(
        os.path.join(app.static_folder, "pages"), "admin-login.html"
    )


@app.route("/admin.html")
@app.route("/admin")
def serve_admin():
    return send_from_directory(os.path.join(app.static_folder, "pages"), "admin.html")


# Supporter les requêtes qui utilisent le préfixe /pages/ (ex: /pages/cart.html)
@app.route('/pages/<path:filename>')
def serve_pages(filename):
    return send_from_directory(os.path.join(app.static_folder, 'pages'), filename)


@app.route("/forgot-password.html")
def serve_forgot_password():
    return send_from_directory(
        os.path.join(app.static_folder, "pages"), "forgot-password.html"
    )


@app.route("/<path:filename>")
def serve_static(filename):
    """Servir les fichiers statiques avec support de casse insensible"""
    filepath = os.path.join(app.static_folder, filename)

    # Vérifier le chemin exact d'abord
    if os.path.isfile(filepath):
        return send_from_directory(app.static_folder, filename)

    # Si pas trouvé, chercher avec des variantes de casse (CSS vs css, JS vs js)
    parts = filename.split("/")
    for i, part in enumerate(parts):
        for item in os.listdir(os.path.join(app.static_folder, *parts[:i])):
            if item.lower() == part.lower():
                parts[i] = item
                break

    corrected_path = "/".join(parts)
    filepath_corrected = os.path.join(app.static_folder, corrected_path)

    if os.path.isfile(filepath_corrected):
        return send_from_directory(app.static_folder, corrected_path)

    # Si le fichier existe dans le dossier 'pages', servir depuis là (ex: /shop.html -> /pages/shop.html)
    pages_path = os.path.join(app.static_folder, "pages", filename)
    if os.path.isfile(pages_path):
        return send_from_directory(os.path.join(app.static_folder, "pages"), filename)

    # Fallback: servir index.html pour le routing frontend
    return send_from_directory(app.static_folder, "index.html")


@app.route("/about.html")
def serve_about():
    return send_from_directory(os.path.join(app.static_folder, "pages"), "about.html")


@app.route("/contact.html")
def serve_contact():
    return send_from_directory(os.path.join(app.static_folder, "pages"), "contact.html")


@app.route("/register.html")
def serve_register():
    return send_from_directory(
        os.path.join(app.static_folder, "pages"), "register.html"
    )


# =================== INITIALISATION DATABASE ===================
with app.app_context():
    db.create_all()

# =================== DÉMARRAGE ===================
if __name__ == "__main__":
    # Respect the DEBUG flag from configuration (set FLASK_DEBUG in .env for local overrides)
    app.run(debug=app.config.get("DEBUG", False), host="0.0.0.0", port=5000)
