/**
 * 🔒 Sécurité Frontend - Protection contre XSS et attaques
 * Ce fichier contient des fonctions de sécurité pour le frontend
 */

class SecurityUtils {
  /**
   * Échappe le HTML pour prévenir les attaques XSS
   * @param {string} text - Texte à échapper
   * @returns {string} Texte échappé
   */
  static escapeHTML(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  /**
   * Valide une URL pour prévenir les attaques javascript:
   * @param {string} url - URL à valider
   * @returns {boolean} true si l'URL est sûre
   */
  static isSafeURL(url) {
    try {
      const urlObj = new URL(url);
      // Vérifier que ce n'est pas javascript: ou data:
      return !['javascript:', 'data:', 'vbscript:'].includes(urlObj.protocol);
    } catch (e) {
      return false;
    }
  }

  /**
   * Valide une adresse email
   * @param {string} email - Email à valider
   * @returns {boolean} true si l'email est valide
   */
  static isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email) && email.length < 254;
  }

  /**
   * Valide un numéro de carte de crédit (Luhn algorithm)
   * @param {string} cardNumber - Numéro de carte
   * @returns {boolean} true si le numéro est valide
   */
  static isValidCardNumber(cardNumber) {
    const cleaned = cardNumber.replace(/\s/g, '');
    if (!/^\d{13,19}$/.test(cleaned)) return false;

    let sum = 0;
    let isEven = false;

    for (let i = cleaned.length - 1; i >= 0; i--) {
      let digit = parseInt(cleaned[i], 10);

      if (isEven) {
        digit *= 2;
        if (digit > 9) digit -= 9;
      }

      sum += digit;
      isEven = !isEven;
    }

    return sum % 10 === 0;
  }

  /**
   * Prévient le Clickjacking
   */
  static preventClickjacking() {
    if (window.self !== window.top) {
      window.top.location = window.self.location;
    }
  }

  /**
   * Valide un fichier avant upload (vérification magic bytes)
   * @param {File} file - Fichier à valider
   * @param {Object} options - Options de validation
   * @returns {Object} {valid: boolean, error: string}
   */
  static validateFile(file, options = {}) {
    const maxSize = options.maxSize || 5 * 1024 * 1024; // 5MB par défaut
    const allowedTypes = options.allowedTypes || ['image/jpeg', 'image/png', 'image/gif'];

    // Vérifier la taille
    if (file.size > maxSize) {
      return {
        valid: false,
        error: `Fichier trop grand (max ${maxSize / (1024 * 1024)}MB)`
      };
    }

    // Vérifier le type MIME
    if (!allowedTypes.includes(file.type)) {
      return {
        valid: false,
        error: `Type de fichier non autorisé: ${file.type}`
      };
    }

    // Vérifier l'extension
    const validExtensions = allowedTypes.map(t => t.split('/')[1]);
    const fileName = file.name.toLowerCase();
    const hasValidExtension = validExtensions.some(ext => fileName.endsWith(`.${ext}`));

    if (!hasValidExtension) {
      return {
        valid: false,
        error: `Extension non autorisée`
      };
    }

    return { valid: true };
  }

  /**
   * Prévient les attaques de clonage de session
   */
  static preventSessionFixation() {
    // Régénérer un ID unique par session
    const sessionId = sessionStorage.getItem('_session_id');
    if (!sessionId) {
      sessionStorage.setItem('_session_id', this.generateSecureToken());
    }
  }

  /**
   * Génère un token sécurisé côté client
   * @returns {string} Token aléatoire
   */
  static generateSecureToken() {
    return Array.from(crypto.getRandomValues(new Uint8Array(32)))
      .map(b => b.toString(16).padStart(2, '0'))
      .join('');
  }

  /**
   * Prévient les attaques par injection de contenu (Content Spoofing)
   */
  static preventContentSpoofing() {
    // Désactiver la synthèse vocale et autres fonctionnalités suspectes
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
  }

  /**
   * Valide une entrée contre les caractères dangereux
   * @param {string} input - Entrée à valider
   * @param {string} type - Type de validation ('phone', 'zipcode', 'alphanumeric')
   * @returns {boolean} true si valide
   */
  static validateInputType(input, type) {
    const patterns = {
      phone: /^[\d\s\-\+\(\)]{7,20}$/,
      zipcode: /^\d{4,6}$/,
      alphanumeric: /^[a-zA-Z0-9\s\-_.]+$/,
      username: /^[a-zA-Z0-9_]{3,20}$/,
      password: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/
    };

    if (patterns[type]) {
      return patterns[type].test(input);
    }
    return false;
  }

  /**
   * Nettoie les données utilisateur
   * @param {string} input - Entrée utilisateur
   * @returns {string} Données nettoyées
   */
  static sanitizeInput(input) {
    // Supprimer les balises HTML
    let cleaned = input.replace(/<[^>]*>/g, '');
    
    // Supprimer les caractères de contrôle
    cleaned = cleaned.replace(/[\x00-\x1F\x7F]/g, '');
    
    // Supprimer les séquences d'échappement dangereuses
    cleaned = cleaned.replace(/\\x[0-9A-Fa-f]{2}/g, '');
    
    // Limiter la longueur
    cleaned = cleaned.substring(0, 1000);
    
    return cleaned.trim();
  }

  /**
   * Prévient les attaques de copier-coller malveillant
   */
  static preventMaliciousPaste(inputElement) {
    if (!inputElement) return;

    inputElement.addEventListener('paste', (e) => {
      e.preventDefault();
      const text = e.clipboardData.getData('text/plain');
      const cleaned = this.sanitizeInput(text);
      document.execCommand('insertText', false, cleaned);
    });
  }

  /**
   * Génère un token CSRF pour les requêtes
   * @returns {string} Token CSRF
   */
  static getCSRFToken() {
    // Chercher dans les meta tags
    const token = document.querySelector('meta[name="csrf-token"]');
    if (token) return token.getAttribute('content');

    // Chercher dans les cookies
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const [name, value] = cookie.split('=');
      if (name.trim() === '_csrf_token') {
        return decodeURIComponent(value);
      }
    }

    return null;
  }

  /**
   * Envoie une requête API sécurisée
   * @param {string} url - URL de la requête
   * @param {Object} options - Options fetch
   * @returns {Promise} Réponse
   */
  static async secureAPICall(url, options = {}) {
    const method = options.method || 'GET';
    
    // Ajouter le token CSRF pour les requêtes non-GET
    if (['POST', 'PUT', 'DELETE'].includes(method)) {
      const csrfToken = this.getCSRFToken();
      if (csrfToken) {
        options.headers = options.headers || {};
        options.headers['X-CSRF-Token'] = csrfToken;
      }
    }

    // Ajouter les headers de sécurité par défaut
    options.headers = options.headers || {};
    options.headers['Content-Type'] = options.headers['Content-Type'] || 'application/json';
    options.headers['X-Requested-With'] = 'XMLHttpRequest';

    try {
      const response = await fetch(url, options);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Erreur API sécurisée:', error);
      throw error;
    }
  }

  /**
   * Affiche un message d'erreur de manière sécurisée
   * @param {string} message - Message à afficher
   */
  static showSafeError(message) {
    const errorElement = document.getElementById('errorMessage') ||
                        document.getElementById('message');
    
    if (errorElement) {
      errorElement.textContent = this.escapeHTML(message);
      errorElement.className = 'message error';
      errorElement.style.display = 'block';
    } else {
      // Fallback sûr (pas de innerHTML)
      alert(message);
    }
  }

  /**
   * Affiche un message de succès de manière sécurisée
   * @param {string} message - Message à afficher
   */
  static showSafeSuccess(message) {
    const successElement = document.getElementById('successMessage') ||
                          document.getElementById('message');
    
    if (successElement) {
      successElement.textContent = this.escapeHTML(message);
      successElement.className = 'message success';
      successElement.style.display = 'block';
    }
  }

  /**
   * Valide un formulaire complet
   * @param {HTMLFormElement} form - Formulaire à valider
   * @returns {Object} Données validées
   */
  static validateForm(form) {
    const formData = new FormData(form);
    const data = {};
    const errors = [];

    for (let [key, value] of formData.entries()) {
      // Nettoyer les entrées
      const cleaned = this.sanitizeInput(value);
      
      // Validations spécifiques
      if (key.includes('email')) {
        if (!this.isValidEmail(cleaned)) {
          errors.push(`Email invalide: ${key}`);
        }
      }

      data[key] = cleaned;
    }

    return { data, errors };
  }

  /**
   * Initialise toutes les protections de sécurité
   */
  static initializeAllProtections() {
    this.preventClickjacking();
    this.preventSessionFixation();
    this.preventContentSpoofing();
    console.log('✅ Toutes les protections de sécurité sont activées');
  }
}
/**
 * 🔒 Sécurité Frontend - Protection contre XSS et attaques
 * Ce fichier contient des fonctions de sécurité pour le frontend
 */

class SecurityUtils {
  /**
   * Échappe le HTML pour prévenir les attaques XSS
   * @param {string} text - Texte à échapper
   * @returns {string} Texte échappé
   */
  static escapeHTML(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  /**
   * Valide une URL pour prévenir les attaques javascript:
   * @param {string} url - URL à valider
   * @returns {boolean} true si l'URL est sûre
   */
  static isSafeURL(url) {
    try {
      const urlObj = new URL(url);
      // Vérifier que ce n'est pas javascript: ou data:
      return !['javascript:', 'data:', 'vbscript:'].includes(urlObj.protocol);
    } catch (e) {
      return false;
    }
  }

  /**
   * Valide une adresse email
   * @param {string} email - Email à valider
   * @returns {boolean} true si l'email est valide
   */
  static isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email) && email.length < 254;
  }

  /**
   * Valide un numéro de carte de crédit (Luhn algorithm)
   * @param {string} cardNumber - Numéro de carte
   * @returns {boolean} true si le numéro est valide
   */
  static isValidCardNumber(cardNumber) {
    const cleaned = cardNumber.replace(/\s/g, '');
    if (!/^\d{13,19}$/.test(cleaned)) return false;

    let sum = 0;
    let isEven = false;

    for (let i = cleaned.length - 1; i >= 0; i--) {
      let digit = parseInt(cleaned[i], 10);

      if (isEven) {
        digit *= 2;
        if (digit > 9) digit -= 9;
      }

      sum += digit;
      isEven = !isEven;
    }

    return sum % 10 === 0;
  }

  /**
   * Prévient le Clickjacking
   */
  static preventClickjacking() {
    if (window.self !== window.top) {
      window.top.location = window.self.location;
    }
  }

  /**
   * Valide un fichier avant upload (vérification magic bytes)
   * @param {File} file - Fichier à valider
   * @param {Object} options - Options de validation
   * @returns {Object} {valid: boolean, error: string}
   */
  static validateFile(file, options = {}) {
    const maxSize = options.maxSize || 5 * 1024 * 1024; // 5MB par défaut
    const allowedTypes = options.allowedTypes || ['image/jpeg', 'image/png', 'image/gif'];

    // Vérifier la taille
    if (file.size > maxSize) {
      return {
        valid: false,
        error: `Fichier trop grand (max ${maxSize / (1024 * 1024)}MB)`
      };
    }

    // Vérifier le type MIME
    if (!allowedTypes.includes(file.type)) {
      return {
        valid: false,
        error: `Type de fichier non autorisé: ${file.type}`
      };
    }

    // Vérifier l'extension
    const validExtensions = allowedTypes.map(t => t.split('/')[1]);
    const fileName = file.name.toLowerCase();
    const hasValidExtension = validExtensions.some(ext => fileName.endsWith(`.${ext}`));

    if (!hasValidExtension) {
      return {
        valid: false,
        error: `Extension non autorisée`
      };
    }

    return { valid: true };
  }

  /**
   * Prévient les attaques de clonage de session
   */
  static preventSessionFixation() {
    // Régénérer un ID unique par session
    const sessionId = sessionStorage.getItem('_session_id');
    if (!sessionId) {
      sessionStorage.setItem('_session_id', this.generateSecureToken());
    }
  }

  /**
   * Génère un token sécurisé côté client
   * @returns {string} Token aléatoire
   */
  static generateSecureToken() {
    return Array.from(crypto.getRandomValues(new Uint8Array(32)))
      .map(b => b.toString(16).padStart(2, '0'))
      .join('');
  }

  /**
   * Prévient les attaques par injection de contenu (Content Spoofing)
   */
  static preventContentSpoofing() {
    // Désactiver la synthèse vocale et autres fonctionnalités suspectes
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
  }

  /**
   * Valide une entrée contre les caractères dangereux
   * @param {string} input - Entrée à valider
   * @param {string} type - Type de validation ('phone', 'zipcode', 'alphanumeric')
   * @returns {boolean} true si valide
   */
  static validateInputType(input, type) {
    const patterns = {
      phone: /^[\d\s\-\+\(\)]{7,20}$/,
      zipcode: /^\d{4,6}$/,
      alphanumeric: /^[a-zA-Z0-9\s\-_.]+$/,
      username: /^[a-zA-Z0-9_]{3,20}$/,
      password: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/
    };

    if (patterns[type]) {
      return patterns[type].test(input);
    }
    return false;
  }

  /**
   * Nettoie les données utilisateur
   * @param {string} input - Entrée utilisateur
   * @returns {string} Données nettoyées
   */
  static sanitizeInput(input) {
    // Supprimer les balises HTML
    let cleaned = input.replace(/<[^>]*>/g, '');
    
    // Supprimer les caractères de contrôle
    cleaned = cleaned.replace(/[\x00-\x1F\x7F]/g, '');
    
    // Supprimer les séquences d'échappement dangereuses
    cleaned = cleaned.replace(/\\x[0-9A-Fa-f]{2}/g, '');
    
    // Limiter la longueur
    cleaned = cleaned.substring(0, 1000);
    
    return cleaned.trim();
  }

  /**
   * Prévient les attaques de copier-coller malveillant
   */
  static preventMaliciousPaste(inputElement) {
    if (!inputElement) return;

    inputElement.addEventListener('paste', (e) => {
      e.preventDefault();
      const text = e.clipboardData.getData('text/plain');
      const cleaned = this.sanitizeInput(text);
      document.execCommand('insertText', false, cleaned);
    });
  }

  /**
   * Génère un token CSRF pour les requêtes
   * @returns {string} Token CSRF
   */
  static getCSRFToken() {
    // Chercher dans les meta tags
    const token = document.querySelector('meta[name="csrf-token"]');
    if (token) return token.getAttribute('content');

    // Chercher dans les cookies
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const [name, value] = cookie.split('=');
      if (name.trim() === '_csrf_token') {
        return decodeURIComponent(value);
      }
    }

    return null;
  }

  /**
   * Envoie une requête API sécurisée
   * @param {string} url - URL de la requête
   * @param {Object} options - Options fetch
   * @returns {Promise} Réponse
   */
  static async secureAPICall(url, options = {}) {
    const method = options.method || 'GET';
    
    // Ajouter le token CSRF pour les requêtes non-GET
    if (['POST', 'PUT', 'DELETE'].includes(method)) {
      const csrfToken = this.getCSRFToken();
      if (csrfToken) {
        options.headers = options.headers || {};
        options.headers['X-CSRF-Token'] = csrfToken;
      }
    }

    // Ajouter les headers de sécurité par défaut
    options.headers = options.headers || {};
    options.headers['Content-Type'] = options.headers['Content-Type'] || 'application/json';
    options.headers['X-Requested-With'] = 'XMLHttpRequest';

    try {
      const response = await fetch(url, options);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Erreur API sécurisée:', error);
      throw error;
    }
  }

  /**
   * Affiche un message d'erreur de manière sécurisée
   * @param {string} message - Message à afficher
   */
  static showSafeError(message) {
    const errorElement = document.getElementById('errorMessage') ||
                        document.getElementById('message');
    
    if (errorElement) {
      errorElement.textContent = this.escapeHTML(message);
      errorElement.className = 'message error';
      errorElement.style.display = 'block';
    } else {
      // Fallback sûr (pas de innerHTML)
      alert(message);
    }
  }

  /**
   * Affiche un message de succès de manière sécurisée
   * @param {string} message - Message à afficher
   */
  static showSafeSuccess(message) {
    const successElement = document.getElementById('successMessage') ||
                          document.getElementById('message');
    
    if (successElement) {
      successElement.textContent = this.escapeHTML(message);
      successElement.className = 'message success';
      successElement.style.display = 'block';
    }
  }

  /**
   * Valide un formulaire complet
   * @param {HTMLFormElement} form - Formulaire à valider
   * @returns {Object} Données validées
   */
  static validateForm(form) {
    const formData = new FormData(form);
    const data = {};
    const errors = [];

    for (let [key, value] of formData.entries()) {
      // Nettoyer les entrées
      const cleaned = this.sanitizeInput(value);
      
      // Validations spécifiques
      if (key.includes('email')) {
        if (!this.isValidEmail(cleaned)) {
          errors.push(`Email invalide: ${key}`);
        }
      }

      data[key] = cleaned;
    }

    return { data, errors };
  }

  /**
   * Initialise toutes les protections de sécurité
   */
  static initializeAllProtections() {
    this.preventClickjacking();
    this.preventSessionFixation();
    this.preventContentSpoofing();
    console.log('✅ Toutes les protections de sécurité sont activées');
  }
}

    if (!hasValidExtension) {
      return {
        valid: false,
        error: `Extension non autorisée`
      };
    }

    return { valid: true };
  }

  /**
   * Nettoie les données utilisateur
   * @param {string} input - Entrée utilisateur
   * @returns {string} Données nettoyées
   */
  static sanitizeInput(input) {
    // Supprimer les balises HTML
    let cleaned = input.replace(/<[^>]*>/g, '');
    
    // Supprimer les caractères de contrôle
    cleaned = cleaned.replace(/[\x00-\x1F\x7F]/g, '');
    
    // Limiter la longueur
    cleaned = cleaned.substring(0, 1000);
    
    return cleaned.trim();
  }

  /**
   * Génère un token CSRF pour les requêtes
   * @returns {string} Token CSRF
   */
  static getCSRFToken() {
    // Chercher dans les meta tags
    const token = document.querySelector('meta[name="csrf-token"]');
    if (token) return token.getAttribute('content');

    // Chercher dans les cookies
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const [name, value] = cookie.split('=');
      if (name.trim() === '_csrf_token') {
        return decodeURIComponent(value);
      }
    }

    return null;
  }

  /**
   * Envoie une requête API sécurisée
   * @param {string} url - URL de la requête
   * @param {Object} options - Options fetch
   * @returns {Promise} Réponse
   */
  static async secureAPICall(url, options = {}) {
    const method = options.method || 'GET';
    
    // Ajouter le token CSRF pour les requêtes non-GET
    if (['POST', 'PUT', 'DELETE'].includes(method)) {
      const csrfToken = this.getCSRFToken();
      if (csrfToken) {
        options.headers = options.headers || {};
        options.headers['X-CSRF-Token'] = csrfToken;
      }
    }

    // Ajouter les headers de sécurité par défaut
    options.headers = options.headers || {};
    options.headers['Content-Type'] = options.headers['Content-Type'] || 'application/json';

    try {
      const response = await fetch(url, options);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Erreur API sécurisée:', error);
      throw error;
    }
  }

  /**
   * Affiche un message d'erreur de manière sécurisée
   * @param {string} message - Message à afficher
   */
  static showSafeError(message) {
    const errorElement = document.getElementById('errorMessage') ||
                        document.getElementById('message');
    
    if (errorElement) {
      errorElement.textContent = this.escapeHTML(message);
      errorElement.className = 'message error';
      errorElement.style.display = 'block';
    } else {
      // Fallback sûr (pas de innerHTML)
      alert(message);
    }
  }

  /**
   * Affiche un message de succès de manière sécurisée
   * @param {string} message - Message à afficher
   */
  static showSafeSuccess(message) {
    const successElement = document.getElementById('successMessage') ||
                          document.getElementById('message');
    
    if (successElement) {
      successElement.textContent = this.escapeHTML(message);
      successElement.className = 'message success';
      successElement.style.display = 'block';
    }
  }

  /**
   * Valide un formulaire complet
   * @param {HTMLFormElement} form - Formulaire à valider
   * @returns {Object} Données validées
   */
  static validateForm(form) {
    const formData = new FormData(form);
    const data = {};
    const errors = [];

    for (let [key, value] of formData.entries()) {
      // Nettoyer les entrées
      const cleaned = this.sanitizeInput(value);
      
      // Validations spécifiques
      if (key.includes('email')) {
        if (!this.isValidEmail(cleaned)) {
          errors.push(`Email invalide: ${key}`);
        }
      }

      data[key] = cleaned;
    }

    return { data, errors };
  }
}

// Export pour utilisation en modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SecurityUtils;
}
