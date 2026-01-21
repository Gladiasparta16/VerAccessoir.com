from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User
from security_logger import security_logger
from rate_limiter import rate_limit_manager
import re

auth_bp = Blueprint("auth", __name__)


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
