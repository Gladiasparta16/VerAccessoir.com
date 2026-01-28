// Composant Produits
class ProductManager {
  constructor() {
    this.products = [];
    this.filteredProducts = [];
  }

  async loadProducts() {
    try {
      const response = await fetch('/api/products/');
      this.products = await response.json();
      this.filteredProducts = this.products;
      return this.products;
    } catch (error) {
      console.error('Erreur au chargement des produits:', error);
      // Charger les produits admin depuis localStorage
      const adminProducts = JSON.parse(localStorage.getItem('adminProducts') || '[]');
      if (adminProducts.length > 0) {
        this.products = adminProducts;
        this.filteredProducts = this.products;
        return this.products;
      }
      // Fallback avec produits locaux
      this.products = this.getDefaultProducts();
      this.filteredProducts = this.products;
      return this.products;
    }
  }

  getDefaultProducts() {
    return [
      {
        id: 1,
        name: 'Lunettes Classiques',
        featured: true,
        price: 15000,
        description: 'Lunettes élégantes et intemporelles',
        image: 'INDEX/images/glasses1.jpeg',
        category: 'classiques'
      },
      {
        id: 2,
        name: 'Lunettes Modernes',
        price: 18000,
        description: 'Design contemporain et tendance',
        image: 'INDEX/images/glasses2.jpeg',
        category: 'modernes'
      },
      {
        id: 3,
        name: 'Lunettes Solaires',
        price: 20000,
        description: 'Protection UV et style',
        image: 'INDEX/images/glasses3.jpeg',
        category: 'solaires'
      }
    ];
  }

  renderProducts(container, products = this.filteredProducts, options = {}) {
    if (!container) return;
    const hidePrice = !!options.hidePrice;
    const compact = !!options.compact;

    container.innerHTML = products
      .map(
        product => `
      <div class="product-card ${compact ? 'compact' : ''}">
        <img src="${product.image_url || product.image || 'https://via.placeholder.com/300x300?text=Produit'}" alt="${product.name}" class="product-image">
        <div class="product-content">
          <h4 class="product-title">${product.name}</h4>
          <p class="product-description">${product.description || ''}</p>
          ${hidePrice ? '' : `<p class="product-price">${product.price} FCFA</p>`}
            <button type="button" class="btn btn-primary btn-sm add-to-cart" 
              data-product-id="${String(product.id)}"
              data-product-name="${(product.name || '').replace(/"/g, '&quot;')}"
              data-product-price="${product.price || 0}">
            Ajouter au panier
          </button>
        </div>
      </div>
    `
      )
      .join('');

    // Bind direct click handlers to buttons to ensure add-to-cart works across environments
    try {
      container.querySelectorAll('.add-to-cart').forEach(btn => {
        btn.addEventListener('click', (e) => {
          const t = e.currentTarget;
          const id = String(t.dataset.productId || '');
          const name = t.dataset.productName || '';
          const price = parseFloat(t.dataset.productPrice) || 0;
          if (typeof window.addProductToCart === 'function') {
            window.addProductToCart(id, name, price);
          } else if (window.cartManager && typeof window.cartManager.addItem === 'function') {
            window.cartManager.addItem(id, name, price);
          } else {
            // fallback
            const cart = JSON.parse(localStorage.getItem('cart') || '[]');
            const existing = cart.find(i => String(i.id) === id);
            if (existing) existing.quantity = (existing.quantity || 1) + 1;
            else cart.push({ id, name, price, quantity: 1 });
            localStorage.setItem('cart', JSON.stringify(cart));
            if (typeof window.updateCartBadge === 'function') window.updateCartBadge();
          }
        });
      });
    } catch (err) {
      console.error('bind add-to-cart handlers error', err);
    }
  }

  filterByCategory(category) {
    if (category === 'all') {
      this.filteredProducts = this.products;
    } else {
      this.filteredProducts = this.products.filter(p => p.category === category);
    }
  }

  search(query) {
    const lowerQuery = query.toLowerCase();
    this.filteredProducts = this.products.filter(
      product => product.name.toLowerCase().includes(lowerQuery) ||
                  product.description.toLowerCase().includes(lowerQuery)
    );
  }
}

// Initialiser
const productManager = new ProductManager();
