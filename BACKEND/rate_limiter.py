"""
Gestionnaire de rate limiting et bruteforce protection
"""

from time import time

class RateLimitManager:
    """Gère le rate limiting avec protection contre bruteforce"""
    
    def __init__(self):
        self.request_history = {}
        self.failed_logins = {}
        self.MAX_REQUESTS_PER_MINUTE = 100
        self.MAX_FAILED_LOGINS = 5
        self.LOCKOUT_TIME = 900  # 15 minutes
    
    def record_failed_login(self, ip):
        """Enregistrer une tentative de connexion échouée"""
        current_time = time()
        
        if ip not in self.failed_logins:
            self.failed_logins[ip] = {'count': 0, 'lockout_until': 0}
        
        # Si la période de lockout est terminée, réinitialiser
        if current_time >= self.failed_logins[ip]['lockout_until']:
            self.failed_logins[ip] = {'count': 0, 'lockout_until': 0}
        
        self.failed_logins[ip]['count'] += 1
        
        # Si trop d'essais échoués, bloquer
        if self.failed_logins[ip]['count'] >= self.MAX_FAILED_LOGINS:
            self.failed_logins[ip]['lockout_until'] = current_time + self.LOCKOUT_TIME
            return False, f"Trop de tentatives échouées. Compte bloqué pour {self.LOCKOUT_TIME}s."
        
        return True, None
    
    def record_successful_login(self, ip):
        """Réinitialiser les tentatives échouées après succès"""
        if ip in self.failed_logins:
            self.failed_logins[ip] = {'count': 0, 'lockout_until': 0}
    
    def is_ip_locked(self, ip):
        """Vérifier si une IP est bloquée"""
        current_time = time()
        
        if ip not in self.failed_logins:
            return False
        
        if current_time < self.failed_logins[ip]['lockout_until']:
            remaining = int(self.failed_logins[ip]['lockout_until'] - current_time)
            return True, f"IP bloquée. Réessayez dans {remaining}s."
        
        return False

rate_limit_manager = RateLimitManager()
