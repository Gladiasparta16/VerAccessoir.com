// API Configuration
// Use `window.API_BASE_URL` when provided by hosting env, else default to current origin
const DEFAULT_API_BASE = (window.API_BASE_URL || (window.location.origin + '/api'));
const API_FALLBACK = 'http://127.0.0.1:5000/api';
let API_BASE_URL = DEFAULT_API_BASE;

class APIClient {
  static async request(endpoint, options = {}) {
    // Helper to perform fetch and validate JSON content-type
    const tryFetch = async (base) => {
      const url = `${base}${endpoint}`;
      const config = {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          ...options.headers
        },
        ...options
      };

      // Ajouter le token JWT s'il existe
      const token = localStorage.getItem('token');
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(url, config);
      const contentType = response.headers.get('Content-Type') || '';

      // If not OK or not JSON (HTML error page), throw to allow fallback
      if (!response.ok || contentType.indexOf('application/json') === -1) {
        const text = await response.text();
        const err = new Error(`API Error: ${response.status} for ${url}`);
        err.status = response.status;
        err.body = text;
        err.contentType = contentType;
        throw err;
      }

      return await response.json();
    };

    try {
      return await tryFetch(API_BASE_URL);
    } catch (err) {
      console.warn('Primary API failed, attempting fallback:', err.message);
      try {
        API_BASE_URL = API_FALLBACK; // switch to fallback for subsequent requests
        return await tryFetch(API_BASE_URL);
      } catch (err2) {
        console.error('Fallback API also failed:', err2);
        throw err2;
      }
    }
  }

  // Produits
  static getProducts() {
    return this.request('/products');
  }

  static getProduct(id) {
    return this.request(`/products/${id}`);
  }

  // Authentification
  static login(email, password) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
  }

  static register(email, password, name) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password, name })
    });
  }

  static logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  // Commandes
  static createOrder(items, totalPrice) {
    return this.request('/orders', {
      method: 'POST',
      body: JSON.stringify({ items, totalPrice })
    });
  }

  static getOrders() {
    return this.request('/orders');
  }

  static getOrder(id) {
    return this.request(`/orders/${id}`);
  }

  // Panier
  static addToCart(productId, quantity = 1) {
    const cart = this.getCart();
    const item = cart.find(item => item.id === productId);
    
    if (item) {
      item.quantity += quantity;
    } else {
      cart.push({ id: productId, quantity });
    }
    
    this.saveCart(cart);
    return cart;
  }

  static removeFromCart(productId) {
    const cart = this.getCart();
    const filtered = cart.filter(item => item.id !== productId);
    this.saveCart(filtered);
    return filtered;
  }

  static getCart() {
    if (window.storage && typeof window.storage.getJSON === 'function') {
      return window.storage.getJSON('cart', []);
    }
    // Fallback
    try {
      const raw = localStorage.getItem('cart');
      return raw ? JSON.parse(raw) : [];
    } catch (e) {
      return [];
    }
  }

  static saveCart(cart) {
    if (window.storage && typeof window.storage.setJSON === 'function') {
      return window.storage.setJSON('cart', cart);
    }
    try {
      localStorage.setItem('cart', JSON.stringify(cart));
    } catch (e) {}
  }

  static clearCart() {
    if (window.storage && typeof window.storage.setJSON === 'function') {
      return window.storage.setJSON('cart', []);
    }
    try {
      localStorage.removeItem('cart');
    } catch (e) {}
  }

  static getCartTotal(products) {
    const cart = this.getCart();
    return cart.reduce((total, item) => {
      const product = products.find(p => p.id === item.id);
      return total + (product ? product.price * item.quantity : 0);
    }, 0);
  }

