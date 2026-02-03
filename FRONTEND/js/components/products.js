// Composant Produits
class ProductManager {
  constructor() {
    this.products = [];
    this.filteredProducts = [];
  }

  escapeHTML(str) {
    if (str === undefined || str === null) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  async loadProducts() {
    try {
      // Use APIClient which has a robust fallback to local backend if needed
      const products = await APIClient.getProducts();
      this.products = Array.isArray(products) ? products : [];
      this.filteredProducts = this.products;
      return this.products;
    } catch (error) {
      console.error('Erreur au chargement des produits:', error);
      // Charger les produits admin depuis localStorage (sûr si storage util présent)
      const adminProducts = (window.storage && typeof window.storage.getJSON === 'function') ? window.storage.getJSON('adminProducts', []) : [];
      if (adminProducts && adminProducts.length > 0) {
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
        image: 'assets/images/products/glasses-classic.svg',
        category: 'classiques'
      },
      {
        id: 2,
        name: 'Lunettes Modernes',
        price: 18000,
        description: 'Design contemporain et tendance',
        image: 'assets/images/products/glasses-elegant.svg',
        category: 'modernes'
      },
      {
        id: 3,
        name: 'Lunettes Solaires',
        price: 20000,
        description: 'Protection UV et style',
        image: 'assets/images/products/sunglasses.svg',
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
      <div class="product-card ${compact ? 'compact' : ''}" data-category="${product.category || ''}">
        <img src="${product.image_url || product.image || 'https://via.placeholder.com/300x300?text=Produit'}" alt="${product.name}" class="product-image">
        <div class="product-content">
          <h4 class="product-title">${this.escapeHTML(product.name)}</h4>
          <p class="product-description">${this.escapeHTML(product.description || '')}</p>
          ${hidePrice ? '' : `<p class="product-price">${product.price} FCFA</p>`}
            <button type="button" class="btn btn-primary btn-sm add-to-cart" 
              data-product-id="${String(product.id)}"
              data-product-name="${this.escapeHTML(product.name)}"
              data-product-price="${product.price || 0}">
            Ajouter au panier
          </button>
        </div>
      </div>
    `
      )
      .join('');

    // add-to-cart buttons are handled globally by `cartManager` document listener
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

// Auto-load products when a '.products' container exists on the page
document.addEventListener('DOMContentLoaded', () => {
  const container = document.querySelector('.products');
  if (!container) return;
  productManager.loadProducts().then(() => {
    // If the products container is inside a featured section (homepage), render compact tiles
    const compact = !!container.closest('.featured');
    productManager.renderProducts(container, undefined, { compact });
    // ensure cart badge is updated if cartManager exists
    try { if (window.cartManager) window.cartManager.updateCart(); } catch (e) { /* ignore */ }
  });
});
