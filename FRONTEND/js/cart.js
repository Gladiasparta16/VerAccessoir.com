function addToCart(product) {
  let cart;
  try { cart = JSON.parse(localStorage.getItem("cart") || '[]'); } catch (e) { console.error('Erreur parsing cart:', e); cart = []; }
  
  // S'assurer que la propriété quantity est utilisée (pas qty)
  if (!product.quantity && product.qty) {
    product.quantity = product.qty;
    delete product.qty;
  }
  if (!product.quantity) {
    product.quantity = 1;
  }
  
  const existingItem = cart.find(item => item.id === product.id);
  if (existingItem) {
    existingItem.quantity = (existingItem.quantity || 1) + 1;
  } else {
    cart.push(product);
  }
  
  localStorage.setItem("cart", JSON.stringify(cart));
  
  // Mettre à jour le badge
  if (typeof updateCartBadge === 'function') {
    updateCartBadge();
  }
}
