// Panier - Cart Manager
class CartManager {
  constructor() {
    this.updateCart();
    this.setupEventListeners();
  }

  setupEventListeners() {
    // Déléguer les événements d'ajout au panier
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('add-to-cart')) {
        const productId = e.target.dataset.productId;
        const productName = e.target.dataset.productName;
        const productPrice = parseFloat(e.target.dataset.productPrice);
        this.addItem(productId, productName, productPrice);
      }
    });
  }

  addItem(id, name, price, quantity = 1) {
    const cart = this.getCart();
    const item = cart.find(item => item.id === id);

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
    const item = cart.find(item => item.id === id);
    if (item) {
      item.quantity = Math.max(0, quantity);
      if (item.quantity === 0) {
        this.removeItem(id);
      } else {
        this.saveCart(cart);
        this.updateCart();
      }
    }
  }

  getCart() {
    const cart = localStorage.getItem('cart');
    return cart ? JSON.parse(cart) : [];
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
    const badge = document.querySelector('.cart-badge');
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);

    if (badge) {
      badge.textContent = totalItems;
      badge.style.display = totalItems > 0 ? 'flex' : 'none';
    }
  }

  updateCartDisplay() {
    const cartContainer = document.querySelector('.cart-container');
    if (!cartContainer) return;

    const cart = this.getCart();
    const cartItems = document.querySelector('.cart-items');

    if (cart.length === 0) {
      if (cartItems) {
        cartItems.innerHTML = '<p class="text-center text-muted">Votre panier est vide</p>';
      }
      return;
    }

    // Afficher les articles du panier
    if (cartItems) {
      cartItems.innerHTML = cart
        .map(
          item => `
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
      `
        )
        .join('');

      // Ajouter les événements de quantité
      this.setupQuantityHandlers();
    }

    // Mettre à jour le résumé
    this.updateCartSummary();
  }

  setupQuantityHandlers() {
    document.querySelectorAll('.qty-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.target.dataset.id;
        const input = document.querySelector(`.qty-input[data-id="${id}"]`);
        let quantity = parseInt(input.value);

        if (e.target.classList.contains('qty-plus')) {
          quantity++;
        } else if (e.target.classList.contains('qty-minus') && quantity > 1) {
          quantity--;
        }

        this.updateQuantity(id, quantity);
      });
    });

    document.querySelectorAll('.btn-remove').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.target.dataset.id;
        this.removeItem(id);
      });
    });
  }

  updateCartSummary() {
    const summary = document.querySelector('.cart-summary');
    if (!summary) return;

    const cart = this.getCart();
    const subtotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const tax = subtotal * 0.1; // 10% TVA
    const total = subtotal + tax;
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);

    summary.innerHTML = `
      <div class="summary-row">
        <span>Articles:</span>
        <span>${totalItems}</span>
      </div>
      <div class="summary-row">
        <span>Sous-total:</span>
        <span>${subtotal.toFixed(0)} FCFA</span>
      </div>
      <div class="summary-row">
        <span>TVA (10%):</span>
        <span>${tax.toFixed(0)} FCFA</span>
      </div>
      <div class="summary-row total">
        <span>Total:</span>
        <span>${total.toFixed(0)} FCFA</span>
      </div>
      <button class="btn btn-primary" style="width: 100%; margin-top: var(--spacing-lg);" onclick="proceedToPayment()">
        💳 Procéder au paiement
      </button>
    `;
  }

  showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
      position: fixed;
      top: 80px;
      right: 20px;
      background: #27ae60;
      color: white;
      padding: 15px 20px;
      border-radius: 8px;
      z-index: 2000;
      animation: slideIn 0.3s ease-out;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
      notification.style.animation = 'slideOut 0.3s ease-out';
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  }
}

// Initialiser le gestionnaire de panier
const cartManager = new CartManager();
