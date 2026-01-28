// Static sample products for Enfant - solaires
(function(){
  const products = [
    { id: 'k-s-1', name: 'Lunettes Soleil Enfant A', price: 9000, image: 'https://via.placeholder.com/300x200?text=K+S+1', gender:'kids', type:'solaire' },
    { id: 'k-s-2', name: 'Lunettes Soleil Enfant B', price: 10000, image: 'https://via.placeholder.com/300x200?text=K+S+2', gender:'kids', type:'solaire' }
  ];

  function render() {
    const container = document.getElementById('products');
    if (!container) return;
    container.innerHTML = products.map(p => `\n      <div class="product-card">\n        <img src="${p.image}" alt="${p.name}">\n        <h3>${p.name}</h3>\n        <p>${p.price} FCFA</p>\n        <button class="btn add-to-cart" data-product-id="${p.id}" data-product-name="${p.name}" data-product-price="${p.price}">Ajouter</button>\n      </div>\n    `).join('');
  }

  document.addEventListener('DOMContentLoaded', render);
})();
