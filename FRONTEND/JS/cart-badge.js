// Fichier partagé pour gérer le badge du panier sur toutes les pages
function updateCartBadge() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const totalItems = cart.reduce((sum, item) => sum + (item.quantity || 1), 0);
    
    document.querySelectorAll('.cart-badge').forEach(badge => {
        badge.textContent = totalItems;
    });
}

// Met à jour le badge au chargement
document.addEventListener('DOMContentLoaded', updateCartBadge);

// Synchronise si le panier change dans un autre onglet
window.addEventListener('storage', updateCartBadge);
// Fichier partagé pour gérer le badge du panier sur toutes les pages
function updateCartBadge() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const totalItems = cart.reduce((sum, item) => sum + (item.quantity || 1), 0);
    
    document.querySelectorAll('.cart-badge').forEach(badge => {
        badge.textContent = totalItems;
    });
}

// Met à jour le badge au chargement
document.addEventListener('DOMContentLoaded', updateCartBadge);

// Synchronise si le panier change dans un autre onglet
window.addEventListener('storage', updateCartBadge);
