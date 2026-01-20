"""
🔒 Protections de Sécurité Avancées
Contient les protections contre les failles courantes
"""

from functools import wraps
from flask import request, jsonify, session
import hashlib
import hmac
from datetime import datetime, timedelta

class AdvancedSecurity:
    """
    Classe pour les protections de sécurité avancées
    """
    
    # Dictionnaire pour tracker les tentatives échouées
    failed_attempts = {}
    
    # Dictionnaire pour tracker les sessions suspectes
    suspicious_sessions = {}
    
    @staticmethod
    def log_security_event(event_type, ip, details=""):
        """Enregistrer les événements de sécurité"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {event_type} | IP: {ip} | {details}"
        print(f"🔒 SECURITY: {log_message}")
        
        # En production, écrire dans un fichier
        try:
            with open('logs/security.log', 'a') as f:
                f.write(log_message + '\n')
        except:
            pass
    
    @staticmethod
    def validate_input_length(data, max_length=10000):
        """Prévenir les attaques d'injection par payload massif"""
        total_length = sum(len(str(v)) for v in data.values() if v)
        if total_length > max_length:
            return False, "Payload trop volumineux"
        return True, ""
    
    @staticmethod
    def detect_sql_injection_patterns(input_string):
        """Détecter les patterns SQL Injection courants"""
        if not isinstance(input_string, str):
            return False
        
        dangerous_patterns = [
            "' OR '",
            "' OR 1=1",
            "'; DROP TABLE",
            "UNION SELECT",
            "exec(",
            "execute(",
            "script",
            "javascript:",
            "<iframe",
            "<script",
            "onclick=",
            "onerror=",
        ]
        
        input_lower = input_string.lower()
        for pattern in dangerous_patterns:
            if pattern.lower() in input_lower:
                return True
        
        return False
    
    @staticmethod
    def detect_xss_patterns(input_string):
        """Détecter les patterns XSS courants"""
        if not isinstance(input_string, str):
            return False
        
        xss_patterns = [
            "<script",
            "javascript:",
            "onerror=",
            "onclick=",
            "onload=",
            "onmouseover=",
            "<iframe",
            "<img",
            "<svg",
            "data:text/html",
        ]
        
        input_lower = input_string.lower()
        for pattern in xss_patterns:
            if pattern.lower() in input_lower:
                return True
        
        return False
    
    @staticmethod
    def detect_brute_force_attack(ip_address, max_attempts=5, time_window=60):
        """Détecter et prévenir les attaques par brute force"""
        current_time = datetime.now()
        
        if ip_address not in AdvancedSecurity.failed_attempts:
            AdvancedSecurity.failed_attempts[ip_address] = []
        
        # Nettoyer les anciennes tentatives
        AdvancedSecurity.failed_attempts[ip_address] = [
            attempt_time for attempt_time in AdvancedSecurity.failed_attempts[ip_address]
            if (current_time - attempt_time).total_seconds() < time_window
        ]
        
        # Vérifier si trop de tentatives
        if len(AdvancedSecurity.failed_attempts[ip_address]) >= max_attempts:
            AdvancedSecurity.log_security_event(
                "BRUTE_FORCE_DETECTED",
                ip_address,
                f"{len(AdvancedSecurity.failed_attempts[ip_address])} tentatives"
            )
            return True, "Trop de tentatives échouées"
        
        return False, ""
    
    @staticmethod
    def record_failed_attempt(ip_address):
        """Enregistrer une tentative échouée"""
        if ip_address not in AdvancedSecurity.failed_attempts:
            AdvancedSecurity.failed_attempts[ip_address] = []
        
        AdvancedSecurity.failed_attempts[ip_address].append(datetime.now())
    
    @staticmethod
    def reset_failed_attempts(ip_address):
        """Réinitialiser les tentatives échouées après succès"""
        if ip_address in AdvancedSecurity.failed_attempts:
            del AdvancedSecurity.failed_attempts[ip_address]
    
    @staticmethod
    def detect_session_hijacking(session_id, user_agent, ip_address):
        """Détecter les tentatives de détournement de session"""
        if session_id not in AdvancedSecurity.suspicious_sessions:
            AdvancedSecurity.suspicious_sessions[session_id] = {
                'user_agent': user_agent,
                'ip': ip_address,
                'timestamp': datetime.now()
            }
            return False, ""
        
        stored_data = AdvancedSecurity.suspicious_sessions[session_id]
        
        # Vérifier si l'agent utilisateur a changé (indicateur possible de hijacking)
        if stored_data['user_agent'] != user_agent:
            AdvancedSecurity.log_security_event(
                "SESSION_HIJACKING_ATTEMPT",
                ip_address,
                f"User-Agent changé: {stored_data['user_agent']} -> {user_agent}"
            )
            return True, "Session compromise détectée"
        
        # Vérifier si l'IP a changé (indicateur possible de hijacking)
        if stored_data['ip'] != ip_address:
            AdvancedSecurity.log_security_event(
                "SESSION_HIJACKING_ATTEMPT",
                ip_address,
                f"IP changée: {stored_data['ip']} -> {ip_address}"
            )
            return True, "IP change détectée"
        
        return False, ""
    
    @staticmethod
    def generate_integrity_hash(data, secret_key):
        """Générer un hash d'intégrité pour les données"""
        message = str(data).encode('utf-8')
        return hmac.new(secret_key.encode('utf-8'), message, hashlib.sha256).hexdigest()
    
    @staticmethod
    def verify_integrity_hash(data, hash_value, secret_key):
        """Vérifier le hash d'intégrité"""
        expected_hash = AdvancedSecurity.generate_integrity_hash(data, secret_key)
        return hmac.compare_digest(expected_hash, hash_value)
    
    @staticmethod
    def sanitize_filename(filename):
        """Nettoyer les noms de fichiers pour prévenir directory traversal"""
        # Supprimer les chemins dangereux
        filename = filename.replace('..', '')
        filename = filename.replace('./', '')
        filename = filename.replace('.\\', '')
        filename = filename.replace('/', '')
        filename = filename.replace('\\', '')
        
        # Garder seulement les caractères autorisés
        import re
        filename = re.sub(r'[^\w\s\-\.]', '', filename)
        
        return filename
    
    @staticmethod
    def validate_content_type(content_type, allowed_types):
        """Valider le Content-Type d'une requête"""
        if not content_type:
            return False
        
        # Extraire le type sans les paramètres (e.g., "application/json; charset=utf-8")
        actual_type = content_type.split(';')[0].strip()
        
        return actual_type in allowed_types


# Décorateurs pour les protections courantes

def require_json_content_type(f):
    """Décorateur pour vérifier que le contenu est JSON"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not AdvancedSecurity.validate_content_type(
            request.content_type,
            ['application/json']
        ):
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        return f(*args, **kwargs)
    return decorated_function


def require_no_injection(f):
    """Décorateur pour vérifier les injections SQL/XSS"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Vérifier tous les paramètres
        data = request.get_json() or {}
        
        for key, value in data.items():
            if isinstance(value, str):
                # Vérifier SQL Injection
                if AdvancedSecurity.detect_sql_injection_patterns(value):
                    AdvancedSecurity.log_security_event(
                        "SQL_INJECTION_ATTEMPT",
                        request.remote_addr,
                        f"Paramètre: {key}"
                    )
                    return jsonify({'error': 'Invalid input detected'}), 400
                
                # Vérifier XSS
                if AdvancedSecurity.detect_xss_patterns(value):
                    AdvancedSecurity.log_security_event(
                        "XSS_ATTEMPT",
                        request.remote_addr,
                        f"Paramètre: {key}"
                    )
                    return jsonify({'error': 'Invalid input detected'}), 400
        
        return f(*args, **kwargs)
    return decorated_function


def require_payload_limit(max_size=10000):
    """Décorateur pour limiter la taille du payload"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json() or {}
            is_valid, error_msg = AdvancedSecurity.validate_input_length(data, max_size)
            
            if not is_valid:
                AdvancedSecurity.log_security_event(
                    "PAYLOAD_TOO_LARGE",
                    request.remote_addr,
                    error_msg
                )
                return jsonify({'error': error_msg}), 413
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def track_brute_force(attempt_type="login"):
    """Décorateur pour tracker les tentatives brute force"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip = request.remote_addr
            
            # Vérifier brute force
            is_brute_force, error_msg = AdvancedSecurity.detect_brute_force_attack(ip)
            if is_brute_force:
                return jsonify({'error': error_msg}), 429
            
            # Enregistrer la tentative
            try:
                result = f(*args, **kwargs)
                
                # Si succès (status 200), réinitialiser
                if isinstance(result, tuple) and result[1] == 200:
                    AdvancedSecurity.reset_failed_attempts(ip)
                else:
                    AdvancedSecurity.record_failed_attempt(ip)
                
                return result
            except Exception as e:
                AdvancedSecurity.record_failed_attempt(ip)
                raise e
        
        return decorated_function
    return decorator


def log_api_call(action="API_CALL"):
    """Décorateur pour logger les appels API"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = getattr(request, 'user', 'unknown')
            method = request.method
            path = request.path
            
            AdvancedSecurity.log_security_event(
                f"{action}",
                request.remote_addr,
                f"{method} {path}"
            )
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
