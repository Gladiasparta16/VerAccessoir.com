// Bootstrap global helpers: assure que `productManager`, `cartManager`, et `updateCartBadge` existent
(function(){
  try {
    // ProductManager
    if (typeof window.productManager === 'undefined' && typeof ProductManager !== 'undefined') {
      window.productManager = new ProductManager();
    }

    // CartManager
    if (typeof window.cartManager === 'undefined' && typeof CartManager !== 'undefined') {
      window.cartManager = new CartManager();
    }

    // updateCartBadge fallback (if cart-badge.js missing)
    if (typeof window.updateCartBadge !== 'function') {
      window.updateCartBadge = function() {
        try {
          const cart = JSON.parse(localStorage.getItem('cart') || '[]');
          const totalItems = cart.reduce((sum, item) => sum + (item.quantity || 1), 0);
          document.querySelectorAll('.cart-badge').forEach(b => { b.textContent = totalItems; });
        } catch (e) {
          console.error('updateCartBadge error', e);
        }
      };
      // run once
      window.addEventListener('storage', window.updateCartBadge);
      document.addEventListener('DOMContentLoaded', window.updateCartBadge);
    }

    // Helper to add product from API-rendered buttons
    if (typeof window.addProductToCart !== 'function') {
      window.addProductToCart = function(id, name, price) {
        const cart = JSON.parse(localStorage.getItem('cart') || '[]');
        const existing = cart.find(i => i.id === id);
        if (existing) existing.quantity = (existing.quantity || 1) + 1;
        else cart.push({ id, name, price, quantity: 1 });
        localStorage.setItem('cart', JSON.stringify(cart));
        if (window.cartManager && typeof window.cartManager.updateCart === 'function') window.cartManager.updateCart();
        if (typeof window.updateCartBadge === 'function') window.updateCartBadge();
      };
    }

    // Simple addToCart for older pages
    if (typeof window.addToCart !== 'function') {
      window.addToCart = function(product) {
        const cart = JSON.parse(localStorage.getItem('cart') || '[]');
        const existing = cart.find(i => i.id === product.id);
        if (existing) existing.quantity = (existing.quantity || 1) + 1;
        else cart.push(product);
        localStorage.setItem('cart', JSON.stringify(cart));
        if (window.cartManager && typeof window.cartManager.updateCart === 'function') window.cartManager.updateCart();
        if (typeof window.updateCartBadge === 'function') window.updateCartBadge();
      };
    }

    // Global cart click handler: delegate clicks to cart page
    document.addEventListener('click', function(e) {
      try {
        const btn = e.target.closest('.cart-icon, .icon-btn, [data-role="cart"]');
        if (btn) {
          // If element is an anchor with href, let it behave normally
          if (btn.tagName && btn.tagName.toLowerCase() === 'a' && btn.getAttribute('href')) return;
          window.location.href = '/cart.html';
        }
      } catch (err) { /* ignore */ }
    });
  } catch (err) {
    console.error('bootstrap.js init error', err);
  }
})();
