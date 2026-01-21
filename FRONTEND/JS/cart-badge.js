// Fichier partagé pour gérer le badge du panier sur toutes les pages
function updateCartBadge() {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    const totalItems = cart.reduce((sum, item) => sum + (item.quantity || 1), 0);
    document.querySelectorAll('.cart-badge').forEach(badge => {
        badge.textContent = totalItems;
        try { badge.style.display = totalItems > 0 ? 'flex' : 'none'; } catch(e) { /* ignore */ }
    });
}

// Met à jour le badge au chargement et sur changement de stockage
document.addEventListener('DOMContentLoaded', updateCartBadge);
window.addEventListener('storage', updateCartBadge);
