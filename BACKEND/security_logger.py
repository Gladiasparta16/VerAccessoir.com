"""
Système de logging sécurisé pour événements de sécurité
Enregistre les tentatives d'authentification, accès admin, etc.
"""

import logging
import os
from datetime import datetime
from functools import wraps
from flask import request, g

# Créer dossier logs s'il n'existe pas
os.makedirs('logs', exist_ok=True)

# =================== CONFIGURATION LOGGING ===================
class SecurityLogger:
    """Gestionnaire de logs sécurisés"""
    
    def __init__(self):
        self.logger = logging.getLogger('security')
        self.logger.setLevel(logging.INFO)
        
        # File handler pour les logs
        handler = logging.FileHandler('logs/security.log')
        handler.setLevel(logging.INFO)
        
        # Format: [timestamp] [LEVEL] event=xxx ip=xxx user=xxx details=xxx
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_auth_attempt(self, email, success, ip=None):
        """Enregistrer tentative d'authentification"""
        if not ip:
            ip = request.remote_addr if request else 'unknown'
        
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"AUTH_ATTEMPT email={email} status={status} ip={ip}")
    
    def log_admin_action(self, user_id, action, resource, details='', ip=None):
        """Enregistrer action admin"""
        if not ip:
            ip = request.remote_addr if request else 'unknown'
        
        self.logger.info(
            f"ADMIN_ACTION user_id={user_id} action={action} "
            f"resource={resource} details={details} ip={ip}"
        )
    
    def log_suspicious_activity(self, event_type, details, ip=None):
        """Enregistrer activité suspecte"""
        if not ip:
            ip = request.remote_addr if request else 'unknown'
        
        self.logger.warning(
            f"SUSPICIOUS event_type={event_type} details={details} ip={ip}"
        )
    
    def log_api_call(self, method, endpoint, status_code, user_id=None, ip=None):
        """Enregistrer appel API"""
        if not ip:
            ip = request.remote_addr if request else 'unknown'
        
        user_part = f" user_id={user_id}" if user_id else ""
        self.logger.info(
            f"API_CALL method={method} endpoint={endpoint} "
            f"status={status_code}{user_part} ip={ip}"
        )

# Instance globale
security_logger = SecurityLogger()

# =================== DÉCORATEURS ===================
def log_security_event(event_type):
    """Décorateur pour log automatique des événements sécurité"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                result = f(*args, **kwargs)
                return result
            except Exception as e:
                security_logger.log_suspicious_activity(
                    event_type=event_type,
                    details=f"Error: {type(e).__name__}"
                )
                raise
        return decorated_function
    return decorator
