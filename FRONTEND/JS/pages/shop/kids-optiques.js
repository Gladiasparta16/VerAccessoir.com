// Static sample products for Enfant - optiques
(function(){
  const products = [
    { id: 'k-o-1', name: 'Lunettes Optique Enfant A', price: 9500, image: 'https://via.placeholder.com/300x200?text=K+O+1', gender:'kids', type:'optiques' }
  ];

  function render() {
    const container = document.getElementById('products');
    if (!container) return;
    container.innerHTML = products.map(p => `\n      <div class="product-card">\n        <img src="${p.image}" alt="${p.name}">\n        <h3>${p.name}</h3>\n        <p>${p.price} FCFA</p>\n        <button class="btn add-to-cart" data-product-id="${p.id}" data-product-name="${p.name}" data-product-price="${p.price}">Ajouter</button>\n      </div>\n    `).join('');
  }

  document.addEventListener('DOMContentLoaded', render);
})();
