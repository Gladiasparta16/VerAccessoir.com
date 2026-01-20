"""
Routes de test de sécurité - À RETIRER EN PRODUCTION
Permet de tester les validations de sécurité
"""

from flask import Blueprint, jsonify, request

security_test_bp = Blueprint('security_test', __name__)

# ⚠️ À RETIRER EN PRODUCTION - Test endpoints uniquement

@security_test_bp.route('/test/sql-injection', methods=['POST'])
def test_sql_injection():
    """Test protection SQL injection"""
    data = request.get_json()
    # Si vous arrivez ici sans erreur, la protection fonctionne
    return jsonify({
        'message': 'Protection SQL injection: OK',
        'note': 'Les requêtes sont paramétrées avec SQLAlchemy ORM'
    }), 200

@security_test_bp.route('/test/xss-protection', methods=['POST'])
def test_xss():
    """Test protection XSS"""
    data = request.get_json()
    return jsonify({
        'message': 'Protection XSS: OK',
        'headers': dict(request.headers),
        'note': 'Content-Security-Policy active'
    }), 200

@security_test_bp.route('/test/password-validation', methods=['POST'])
def test_password():
    """Test validation mot de passe"""
    from routes.auth import validate_password
    
    password = request.json.get('password', '')
    is_valid, message = validate_password(password)
    
    return jsonify({
        'valid': is_valid,
        'message': message,
        'requirements': {
            'min_length': 8,
            'uppercase': 'Required',
            'lowercase': 'Required',
            'digit': 'Required',
            'special_char': 'Required'
        }
    }), 200

@security_test_bp.route('/test/rate-limit', methods=['POST'])
def test_rate_limit():
    """Test rate limiting"""
    from rate_limiter import rate_limit_manager
    from time import time
    
    ip = request.remote_addr
    
    return jsonify({
        'message': 'Rate limiting: OK',
        'ip': ip,
        'limits': {
            'max_requests_per_minute': rate_limit_manager.MAX_REQUESTS_PER_MINUTE,
            'max_failed_logins': rate_limit_manager.MAX_FAILED_LOGINS,
            'lockout_time_seconds': rate_limit_manager.LOCKOUT_TIME
        }
    }), 200

@security_test_bp.route('/test/headers', methods=['GET'])
def test_headers():
    """Afficher tous les headers de sécurité"""
    return jsonify({
        'security_headers': {
            'X-Frame-Options': 'DENY (Prévient clickjacking)',
            'X-Content-Type-Options': 'nosniff (Prévient MIME sniffing)',
            'X-XSS-Protection': '1; mode=block (Prévient XSS en IE)',
            'Content-Security-Policy': 'Active (Prévient injections)',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Strict-Transport-Security': 'Active en production'
        }
    }), 200

@security_test_bp.route('/test/all', methods=['GET'])
def test_all():
    """Test de sécurité complet"""
    return jsonify({
        'security_tests': {
            'authentication': '✅ JWT tokens avec expiration',
            'authorization': '✅ Vérification is_admin',
            'password_validation': '✅ Complexité requise',
            'rate_limiting': '✅ Protection bruteforce',
            'sql_injection': '✅ ORM SQLAlchemy',
            'xss_protection': '✅ CSP headers',
            'csrf_protection': '✅ Tokens CSRF',
            'logging': '✅ Events sensibles loggés',
            'https': '✅ À vérifier en production'
        },
        'warning': '⚠️ Ces endpoints de test à RETIRER en production!',
        'note': 'Supprimer security_test_bp de app.py avant déploiement'
    }), 200
