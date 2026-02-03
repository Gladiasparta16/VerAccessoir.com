// Main JavaScript - Initialisation globale

// Charger les produits au démarrage
document.addEventListener('DOMContentLoaded', async () => {
  // Charger les produits
  await productManager.loadProducts();

  // Rendre les produits si on est sur une page avec une grille
  const productContainer = document.querySelector('.products');
  if (productContainer) {
    // Detecter page d'accueil de façon robuste: présence de la section 'featured'
    const isHome = !!document.querySelector('.featured');
    // Si page d'accueil, afficher uniquement les produits en vedette
    if (isHome) {
      const featured = (productManager.products || []).filter(p => p.featured);
      productManager.renderProducts(productContainer, featured, { hidePrice: true, compact: true });
    } else {
      productManager.renderProducts(productContainer, undefined, { hidePrice: false, compact: false });
    }
  }

  // Initialiser la navigation
  setupNavigation();

  // Mettre à jour l'UI d'authentification
  if (typeof updateAuthUI === 'function') updateAuthUI();

  // Charger le panier
  if (typeof cartManager !== 'undefined' && cartManager.updateCart) cartManager.updateCart();
});

// Configuration de la navigation
function setupNavigation() {
  const navLinks = document.querySelectorAll('.nav a');

  navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      // Enlever la classe active de tous les liens
      navLinks.forEach(l => l.classList.remove('active'));
      // Ajouter la classe active au lien cliqué
      this.classList.add('active');
    });
  });

  // Marquer le lien actif basé sur l'URL
  const currentPath = window.location.pathname;
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (currentPath.includes(href.replace('.html', '')) || 
        (currentPath === '/' && href === 'index.html')) {
      link.classList.add('active');
    }
  });
}

// Animations CSS
const style = document.createElement('style');
style.textContent = `
  @keyframes slideDown {
    from {
      transform: translateX(-50%) translateY(-100%);
      opacity: 0;
    }
    to {
      transform: translateX(-50%) translateY(0);
      opacity: 1;
    }
  }

  @keyframes slideUp {
    from {
      transform: translateX(-50%) translateY(0);
      opacity: 1;
    }
    to {
      transform: translateX(-50%) translateY(-100%);
      opacity: 0;
    }
  }

  @keyframes slideIn {
    from {
      transform: translateX(400px);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }

  @keyframes slideOut {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(400px);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);

// Fonction pour afficher des alertes
function showAlert(message, type = 'info') {
  const alert = document.createElement('div');
  alert.className = `alert alert-${type}`;
  alert.textContent = message;
  alert.style.cssText = `
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 2000;
    padding: 15px 20px;
    border-radius: 8px;
    animation: slideDown 0.3s ease-out;
  `;

  if (type === 'success') {
    alert.style.backgroundColor = '#d4edda';
    alert.style.color = '#155724';
    alert.style.borderLeft = '4px solid #27ae60';
  } else if (type === 'error') {
    alert.style.backgroundColor = '#f8d7da';
    alert.style.color = '#721c24';
    alert.style.borderLeft = '4px solid #e74c3c';
  } else {
    alert.style.backgroundColor = '#d1ecf1';
    alert.style.color = '#0c5460';
    alert.style.borderLeft = '4px solid #3498db';
  }

  document.body.appendChild(alert);

  setTimeout(() => {
    alert.style.animation = 'slideUp 0.3s ease-out';
    setTimeout(() => alert.remove(), 300);
  }, 3000);
}

// Exporter les fonctions globales
window.showAlert = showAlert;

function proceedToPayment() {
  const cart = JSON.parse(localStorage.getItem('cart') || '[]');
  const token = localStorage.getItem('token');

  if (cart.length === 0) {
    showAlert('Votre panier est vide', 'error');
    return;
  }

  if (!token) {
    showAlert('Veuillez vous connecter pour continuer', 'error');
    window.location.href = 'login.html';
    return;
  }

  window.location.href = 'payment.html';
}

window.proceedToPayment = proceedToPayment;
