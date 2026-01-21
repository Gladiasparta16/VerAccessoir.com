from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User
from security_logger import security_logger
from rate_limiter import rate_limit_manager
import re
import os
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import smtplib
from email.message import EmailMessage

auth_bp = Blueprint("auth", __name__)


def _get_serializer():
    secret = os.environ.get('SECRET_KEY') or os.environ.get('JWT_SECRET_KEY') or 'dev-secret'
    return URLSafeTimedSerializer(secret)


def _send_reset_email(to_email, reset_link):
    # If SMTP settings provided, send real email; otherwise log/return
    mail_server = os.environ.get('MAIL_SERVER')
    if mail_server:
        port = int(os.environ.get('MAIL_PORT', 587))
        username = os.environ.get('MAIL_USERNAME')
        password = os.environ.get('MAIL_PASSWORD')
        use_tls = os.environ.get('MAIL_USE_TLS', 'True').lower() in ('1', 'true', 'yes')

        msg = EmailMessage()
        msg['Subject'] = 'Réinitialisation de votre mot de passe'
        msg['From'] = os.environ.get('MAIL_DEFAULT_SENDER', username or 'no-reply@example.com')
        msg['To'] = to_email
        msg.set_content(f"Pour réinitialiser votre mot de passe, cliquez sur ce lien:\n\n{reset_link}\n\nSi vous n'avez pas demandé cela, ignorez ce message.")

        try:
            with smtplib.SMTP(mail_server, port, timeout=10) as s:
                if use_tls:
                    s.starttls()
                if username and password:
                    s.login(username, password)
                s.send_message(msg)
            return True, None
        except Exception as e:
            return False, str(e)
    else:
        # No mail configured; return token for dev/debug use (only safe when debug)
        return False, 'MAIL_NOT_CONFIGURED'



# =================== VALIDATION MOTS DE PASSE ===================
def validate_password(password):
    """Valider la complexité du mot de passe"""
    # Politique raisonnable pour les formulaires publics:
    # - minimum 8 caractères
    # - au moins une lettre
    # - au moins un chiffre
    if not password or len(password) < 8:
        return False, "Minimum 8 caractères"
    if not re.search(r"[A-Za-z]", password):
        return False, "Au moins 1 lettre"
    if not re.search(r"[0-9]", password):
        return False, "Au moins 1 chiffre"
    return True, "OK"


# =================== REGISTER ===================
@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        if not data or not data.get("email") or not data.get("password"):
            return jsonify({"error": "Email et mot de passe requis"}), 400

        # Valider complexité mot de passe
        is_valid, message = validate_password(data["password"])
        if not is_valid:
            return jsonify({"error": f"Mot de passe invalide: {message}"}), 400

        # Valider email format
        if not re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", data["email"]
        ):
            return jsonify({"error": "Email invalide"}), 400

        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email déjà utilisé"}), 400

        # Nom optionnel: extraire la partie avant @ si absent
        name = data.get("name") or (
            data.get("email").split("@")[0] if "@" in data.get("email") else ""
        )

        user = User(
            email=data["email"],
            name=name,
            password=generate_password_hash(data["password"], method="pbkdf2:sha256"),
        )

        db.session.add(user)
        db.session.commit()

        # 📝 Logging
        security_logger.log_auth_attempt(email=data["email"], success=True)

        access_token = create_access_token(identity=user.id)

        return (
            jsonify(
                {
                    "message": "Utilisateur créé",
                    "access_token": access_token,
                    "user": {"id": user.id, "email": user.email, "name": user.name},
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        # ⚠️ Ne PAS exposer le vrai erreur
        return jsonify({"error": "Erreur lors de l'inscription"}), 500


# =================== LOGIN ===================
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        ip = request.remote_addr

        # ⚠️ Vérifier si IP est bloquée
        is_locked = rate_limit_manager.is_ip_locked(ip)
        if is_locked and is_locked[0]:
            security_logger.log_suspicious_activity(
                event_type="BRUTE_FORCE_BLOCKED", details=is_locked[1]
            )
            return jsonify({"error": is_locked[1]}), 429

        data = request.get_json()

        if not data or not data.get("email") or not data.get("password"):
            return jsonify({"error": "Email et mot de passe requis"}), 400

        user = User.query.filter_by(email=data["email"]).first()

        if not user or not check_password_hash(user.password, data["password"]):
            # 📝 Logging tentative échouée + brute force protection
            success, message = rate_limit_manager.record_failed_login(ip)

            security_logger.log_auth_attempt(email=data["email"], success=False)
            security_logger.log_suspicious_activity(
                event_type="FAILED_LOGIN", details=f"Tentative pour {data['email']}"
            )

            if not success:
                return jsonify({"error": message}), 429

            return jsonify({"error": "Email ou mot de passe invalide"}), 401

        # ✅ Réinitialiser les tentatives échouées après succès
        rate_limit_manager.record_successful_login(ip)

        # 📝 Logging succès
        security_logger.log_auth_attempt(email=data["email"], success=True)

        access_token = create_access_token(identity=user.id)

        return (
            jsonify(
                {
                    "message": "Connexion réussie",
                    "access_token": access_token,
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "name": user.name,
                        "is_admin": user.is_admin,
                    },
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET CURRENT USER
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "Utilisateur non trouvé"}), 404

        return (
            jsonify(
                {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "is_admin": user.is_admin,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =================== FORGOT / RESET PASSWORD ===================
@auth_bp.route('/forgot', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json() or {}
        email = data.get('email')
        if not email:
            return jsonify({'error': 'Email requis'}), 400

        user = User.query.filter_by(email=email).first()

        # Always respond with 200 to avoid account enumeration
        if not user:
            return jsonify({'message': 'Si cet email existe, un lien de réinitialisation a été envoyé.'}), 200

        s = _get_serializer()
        token = s.dumps({'user_id': user.id})
        # Build reset link pointing to frontend reset page
        frontend_origin = os.environ.get('FRONTEND_ORIGIN') or ''
        if frontend_origin:
            reset_link = f"{frontend_origin}/reset-password.html?token={token}"
        else:
            reset_link = f"/reset-password.html?token={token}"

        sent, err = _send_reset_email(user.email, reset_link)
        if sent:
            return jsonify({'message': 'Lien de réinitialisation envoyé'}), 200
        else:
            # If mail not configured, in debug return token so dev can test
            if os.environ.get('FLASK_DEBUG', 'False').lower() in ('1','true','yes'):
                return jsonify({'message': 'DEBUG: mail non configuré', 'token': token}), 200
            return jsonify({'message': 'Si cet email existe, un lien de réinitialisation a été envoyé.'}), 200
    except Exception as e:
        return jsonify({'error': 'Erreur interne'}), 500


@auth_bp.route('/reset', methods=['POST'])
def reset_password():
    try:
        data = request.get_json() or {}
        token = data.get('token')
        new_password = data.get('password')
        if not token or not new_password:
            return jsonify({'error': 'Token et nouveau mot de passe requis'}), 400

        # validate password complexity
        ok, msg = validate_password(new_password)
        if not ok:
            return jsonify({'error': f'Mot de passe invalide: {msg}'}), 400

        s = _get_serializer()
        try:
            payload = s.loads(token, max_age=int(os.environ.get('PASSWORD_RESET_TOKEN_EXP', 3600)))
        except SignatureExpired:
            return jsonify({'error': 'Token expiré'}), 400
        except BadSignature:
            return jsonify({'error': 'Token invalide'}), 400

        user_id = payload.get('user_id')
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404

        user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
        db.session.commit()
        return jsonify({'message': 'Mot de passe réinitialisé avec succès'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur interne'}), 500
