// Static sample products for Homme - optiques
(function(){
  const products = [
    { id: 'm-o-1', name: 'Lunettes Optique Homme A', price: 12000, image: 'https://via.placeholder.com/300x200?text=H+O+1', gender:'men', type:'optiques' },
    { id: 'm-o-2', name: 'Lunettes Optique Homme B', price: 14000, image: 'https://via.placeholder.com/300x200?text=H+O+2', gender:'men', type:'optiques' }
  ];

  function render() {
    const container = document.getElementById('products');
    if (!container) return;
    container.innerHTML = products.map(p => `\n      <div class="product-card">\n        <img src="${p.image}" alt="${p.name}">\n        <h3>${p.name}</h3>\n        <p>${p.price} FCFA</p>\n        <button class="btn add-to-cart" data-product-id="${p.id}" data-product-name="${p.name}" data-product-price="${p.price}">Ajouter</button>\n      </div>\n    `).join('');
  }

  document.addEventListener('DOMContentLoaded', render);
})();
