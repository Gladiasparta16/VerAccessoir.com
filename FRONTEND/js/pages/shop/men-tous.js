// Combine Homme solaires + optiques
(function(){
  const products = [
    { id: 'm-s-1', name: 'Lunettes Soleil Homme A', price: 15000, image: 'https://via.placeholder.com/300x200?text=H+S+1', gender:'men', type:'solaire' },
    { id: 'm-s-2', name: 'Lunettes Soleil Homme B', price: 18000, image: 'https://via.placeholder.com/300x200?text=H+S+2', gender:'men', type:'solaire' },
    { id: 'm-o-1', name: 'Lunettes Optique Homme A', price: 12000, image: 'https://via.placeholder.com/300x200?text=H+O+1', gender:'men', type:'optiques' }
  ];

  function render() {
    const container = document.getElementById('products');
    if (!container) return;
    container.innerHTML = products.map(p => `\n      <div class="product-card">\n        <img src="${p.image}" alt="${p.name}">\n        <h3>${p.name}</h3>\n        <p>${p.price} FCFA</p>\n        <button class="btn add-to-cart" data-product-id="${p.id}" data-product-name="${p.name}" data-product-price="${p.price}">Ajouter</button>\n      </div>\n    `).join('');
  }

  document.addEventListener('DOMContentLoaded', render);
})();
