// Panier - Cart Manager
class CartManager {
  constructor() {
    this.updateCart();
    this.setupEventListeners();
  }

  setupEventListeners() {
    document.addEventListener('click', (e) => {
      // Support clicks on buttons and their inner elements
      const addBtn = (e.target.closest && e.target.closest('.add-to-cart')) || e.target;
      if (addBtn && addBtn.classList && addBtn.classList.contains('add-to-cart')) {
        const productId = String(addBtn.dataset.productId || '');
        const productName = addBtn.dataset.productName || '';
        const productPrice = parseFloat(addBtn.dataset.productPrice) || 0;
        console.debug && console.debug('cart click detected:', { productId, productName, productPrice });
        this.addItem(productId, productName, productPrice);
        return;
      }

      const rm = (e.target.closest && e.target.closest('.btn-remove')) || e.target;
      if (rm && rm.classList && rm.classList.contains('btn-remove')) {
        const id = rm.dataset.id;
        this.removeItem(String(id));
      }
    });
  }

  addItem(id, name, price, quantity = 1) {
    id = String(id);
    const cart = this.getCart();
    const item = cart.find(item => String(item.id) === id);

    if (item) {
      item.quantity += quantity;
    } else {
      cart.push({ id, name, price, quantity, image: '' });
    }

    this.saveCart(cart);
    this.showNotification(`${name} ajouté au panier!`);
    this.updateCart();
  }

  removeItem(id) {
    const cart = this.getCart().filter(item => item.id !== id);
    this.saveCart(cart);
    this.updateCart();
  }

  updateQuantity(id, quantity) {
    const cart = this.getCart();
    const item = cart.find(i => i.id === id);
    if (!item) return;
    item.quantity = Math.max(0, quantity);
    if (item.quantity === 0) this.removeItem(id);
    else { this.saveCart(cart); this.updateCart(); }
  }

  getCart() {
    try { return JSON.parse(localStorage.getItem('cart') || '[]'); } catch(e) { return []; }
  }

  saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
    this.updateCartBadge();
  }

  clearCart() {
    localStorage.removeItem('cart');
    this.updateCart();
  }

  updateCart() {
    this.updateCartBadge();
    this.updateCartDisplay();
  }

  updateCartBadge() {
    const cart = this.getCart();
    const totalItems = cart.reduce((sum, item) => sum + (item.quantity || 0), 0);
    document.querySelectorAll('.cart-badge').forEach(badge => {
      badge.textContent = totalItems;
      try { badge.style.display = totalItems > 0 ? 'flex' : 'none'; } catch(e) { /* ignore */ }
    });
  }

  updateCartDisplay() {
    const cartContainer = document.querySelector('.cart-container');
    if (!cartContainer) return;
    const cart = this.getCart();
    const cartItems = document.querySelector('.cart-items');
    if (cart.length === 0) {
      if (cartItems) cartItems.innerHTML = '<p class="text-center text-muted">Votre panier est vide</p>';
      return;
    }
    if (!cartItems) return;
    cartItems.innerHTML = cart.map(item => `
      <div class="cart-item">
        <img src="${item.image || 'https://via.placeholder.com/100'}" alt="${item.name}" class="cart-item-image">
        <div class="cart-item-details">
          <h4 class="cart-item-title">${item.name}</h4>
          <p class="cart-item-price">${item.price} FCFA</p>
          <div class="quantity-control">
            <button class="qty-btn qty-minus" data-id="${item.id}">-</button>
            <input type="number" class="qty-input" value="${item.quantity}" data-id="${item.id}" readonly>
            <button class="qty-btn qty-plus" data-id="${item.id}">+</button>
          </div>
        </div>
        <button class="btn-remove" data-id="${item.id}" style="background: #e74c3c; color: white; padding: 8px 12px; border-radius: 4px; cursor: pointer;">✕</button>
      </div>
    `).join('');
    this.setupQuantityHandlers();
    this.updateCartSummary();
  }

  setupQuantityHandlers() {
    document.querySelectorAll('.qty-btn').forEach(btn => {
      btn.removeEventListener('click', btn._cm_handler);
      const handler = (e) => {
        const id = e.target.dataset.id;
        const input = document.querySelector(`.qty-input[data-id="${id}"]`);
        let quantity = parseInt(input.value || '0', 10);
        if (e.target.classList.contains('qty-plus')) quantity++;
        if (e.target.classList.contains('qty-minus') && quantity > 1) quantity--;
        this.updateQuantity(id, quantity);
      };
      btn.addEventListener('click', handler);
      btn._cm_handler = handler;
    });
    document.querySelectorAll('.btn-remove').forEach(btn => {
      btn.removeEventListener('click', btn._cm_rm);
      const rm = (e) => { this.removeItem(e.target.dataset.id); };
      btn.addEventListener('click', rm);
      btn._cm_rm = rm;
    });
  }

  updateCartSummary() {
    const summary = document.querySelector('.cart-summary');
    if (!summary) return;
    const cart = this.getCart();
    const subtotal = cart.reduce((sum, item) => sum + (item.price || 0) * (item.quantity || 0), 0);
    const tax = subtotal * 0.1;
    const total = subtotal + tax;
    const totalItems = cart.reduce((sum, item) => sum + (item.quantity || 0), 0);
    summary.innerHTML = `
      <div class="summary-row"><span>Articles:</span><span>${totalItems}</span></div>
      <div class="summary-row"><span>Sous-total:</span><span>${subtotal.toFixed(0)} FCFA</span></div>
      <div class="summary-row"><span>TVA (10%):</span><span>${tax.toFixed(0)} FCFA</span></div>
      <div class="summary-row total"><span>Total:</span><span>${total.toFixed(0)} FCFA</span></div>
      <button class="btn btn-primary" style="width: 100%; margin-top: var(--spacing-lg);" onclick="proceedToPayment()">💳 Procéder au paiement</button>
    `;
  }

  showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `position: fixed; top: 80px; right: 20px; background: #27ae60; color: white; padding: 15px 20px; border-radius: 8px; z-index: 2000; animation: slideIn 0.3s ease-out;`;
    document.body.appendChild(notification);
    setTimeout(() => { notification.style.animation = 'slideOut 0.3s ease-out'; setTimeout(() => notification.remove(), 300); }, 3000);
  }
}

// Initialiser et exposer l'instance
const cartManager = new CartManager();
try { window.cartManager = cartManager; } catch (e) { /* ignore */ }
