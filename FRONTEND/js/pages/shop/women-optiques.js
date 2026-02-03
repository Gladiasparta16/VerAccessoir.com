// Static sample products for Femme - optiques
(function(){
  const products = [
    { id: 'w-o-1', name: 'Lunettes Optique Femme A', price: 13000, image: 'https://via.placeholder.com/300x200?text=W+O+1', gender:'women', type:'optiques' },
    { id: 'w-o-2', name: 'Lunettes Optique Femme B', price: 15000, image: 'https://via.placeholder.com/300x200?text=W+O+2', gender:'women', type:'optiques' }
  ];

  function render() {
    const container = document.getElementById('products');
    if (!container) return;
    container.innerHTML = products.map(p => `\n      <div class="product-card">\n        <img src="${p.image}" alt="${p.name}">\n        <h3>${p.name}</h3>\n        <p>${p.price} FCFA</p>\n        <button class="btn add-to-cart" data-product-id="${p.id}" data-product-name="${p.name}" data-product-price="${p.price}">Ajouter</button>\n      </div>\n    `).join('');
  }

  document.addEventListener('DOMContentLoaded', render);
})();
