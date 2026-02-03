// Bootstrap global helpers: ensure `productManager`, `cartManager`, and `updateCartBadge` exist
(function(){
  try {
    // Instantiate managers if available
    if (typeof window.productManager === 'undefined' && typeof ProductManager !== 'undefined') {
      window.productManager = new ProductManager();
    }
    if (typeof window.cartManager === 'undefined' && typeof CartManager !== 'undefined') {
      window.cartManager = new CartManager();
    }

    // updateCartBadge fallback (if cart-badge.js missing)
    if (typeof window.updateCartBadge !== 'function') {
      window.updateCartBadge = function() {
        try {
          let cart;
          try { cart = JSON.parse(localStorage.getItem('cart') || '[]'); } catch (e) { console.error('Erreur parsing cart:', e); cart = []; }
          const totalItems = cart.reduce((sum, item) => sum + (item.quantity || 1), 0);
          document.querySelectorAll('.cart-badge').forEach(b => { b.textContent = totalItems; });
        } catch (e) {
          console.error('updateCartBadge error', e);
        }
      };
      window.addEventListener('storage', window.updateCartBadge);
      document.addEventListener('DOMContentLoaded', window.updateCartBadge);
    }

    // Add product to cart (API-rendered buttons)
    if (typeof window.addProductToCart !== 'function') {
      window.addProductToCart = function(id, name, price) {
        id = String(id);
        let cart;
        try { cart = JSON.parse(localStorage.getItem('cart') || '[]'); } catch (e) { console.error('Erreur parsing cart:', e); cart = []; }
        const existing = cart.find(i => String(i.id) === id);
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
        let cart;
        try { cart = JSON.parse(localStorage.getItem('cart') || '[]'); } catch (e) { console.error('Erreur parsing cart:', e); cart = []; }
        const existing = cart.find(i => String(i.id) === String(product.id));
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
          if (btn.tagName && btn.tagName.toLowerCase() === 'a' && btn.getAttribute('href')) return;
          window.location.href = '/pages/cart.html';
        }
      } catch (err) { /* ignore */ }
    });

  } catch (err) {
    console.error('bootstrap.js init error', err);
  }
})();
