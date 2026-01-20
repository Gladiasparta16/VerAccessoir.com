"""
Sécurité CSRF - Protection contre les attaques Cross-Site Request Forgery
Génère et valide des tokens CSRF pour toutes les opérations sensibles
"""

import secrets
import hashlib
from flask import session, request
from functools import wraps


class CSRFProtection:
    """Gestion de la protection CSRF"""
    
    @staticmethod
    def generate_csrf_token():
        """Génère un token CSRF unique"""
        if '_csrf_token' not in session:
            session['_csrf_token'] = secrets.token_urlsafe(32)
        return session['_csrf_token']
    
    @staticmethod
    def validate_csrf_token(token):
        """Valide un token CSRF"""
        if '_csrf_token' not in session:
            return False
        return secrets.compare_digest(session['_csrf_token'], token)
    
    @staticmethod
    def csrf_protect():
        """Décorateur pour protéger une route contre CSRF"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Les requêtes GET/HEAD/OPTIONS ne nécessitent pas de validation
                if request.method in ['GET', 'HEAD', 'OPTIONS']:
                    return f(*args, **kwargs)
                
                # Pour POST/PUT/DELETE, vérifier le token CSRF
                token = request.form.get('_csrf_token')
                if not token:
                    token = request.headers.get('X-CSRF-Token')
                
                if not token or not CSRFProtection.validate_csrf_token(token):
                    return {'error': 'CSRF token missing or invalid'}, 403
                
                return f(*args, **kwargs)
            return decorated_function
        return decorator


def init_csrf(app):
    """
    Initialise la protection CSRF pour l'application Flask
    """
    app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # JS ne peut pas accéder
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Protection CSRF native
    
    @app.before_request
    def csrf_protect():
        """Génère un token CSRF au premier accès"""
        CSRFProtection.generate_csrf_token()
    
    @app.context_processor
    def inject_csrf_token():
        """Injecte le token CSRF dans les templates"""
        return {'csrf_token': CSRFProtection.generate_csrf_token()}
