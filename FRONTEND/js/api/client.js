// API Configuration
// Use `window.API_BASE_URL` when provided by hosting env, else default to current origin
const API_BASE_URL = (window.API_BASE_URL || (window.location.origin + '/api'));

class APIClient {
  static async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    };

    // Ajouter le token JWT s'il existe
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
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
    return window.storage.getJSON('cart', []);
  }

  static saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
  }

  static clearCart() {
    localStorage.removeItem('cart');
  }

  static getCartTotal(products) {
    const cart = this.getCart();
    return cart.reduce((total, item) => {
      const product = products.find(p => p.id === item.id);
      return total + (product ? product.price * item.quantity : 0);
    }, 0);
  }

