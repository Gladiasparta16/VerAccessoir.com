// Configuration du site - À personnaliser
const SITE_CONFIG = {
  // Infos de contact
  contact: {
    phone: "+225 0787985182",        // Numéro WhatsApp principal
    email: "info@veraccessoire.com",
    address: "ABIDJAN, Côte d'Ivoire",
    hours: "Lun-Sam: 9h-18h | Dim: Fermé"
  },

  // Réseaux sociaux
  social: {
    whatsapp: "https://wa.me/2250787985182",
    instagram: "https://instagram.com/veraccessoire",
    facebook: "https://facebook.com/veraccessoire",
    tiktok: "https://tiktok.com/@veraccessoire",
    twitter: "https://twitter.com/veraccessoire"
  },

  // Info entreprise
  company: {
    name: "VerAccessoire",
    tagline: "Des lunettes qui révèlent ton style",
    description: "La meilleure plateforme de vente de lunettes en ligne au Senegal"
  },

  // Moyens de paiement (numéros marchands)
  payment: {
    orangeMoney: "0787985182",    // Numéro Orange Money marchand
    moovMoney: "700000002",      // Numéro Moov Money marchand
    mtnMoney: "700000003",       // Numéro MTN Money marchand
    wave: "https://app.wave.com/send/business/VERACCESSOIRE"  // Lien Wave
  }
};

// Initialiser la configuration par défaut si elle n'existe pas
function initializeConfig() {
  const saved = localStorage.getItem('siteConfig');
  
  if (!saved) {
    const defaultConfig = {
      adminEmail: 'admin@veraccessoire.com',
      adminPassword: 'admin123',
      social: {
        facebook: '#',
        instagram: '#',
        whatsapp: '#'
      },
      siteName: 'VerAccessoire',
      tagline: 'Le chic à portée de clic'
    };
    
    localStorage.setItem('siteConfig', JSON.stringify(defaultConfig));
  }
}

// Appeler l'initialisation au chargement
initializeConfig();

// Exporter pour utilisation
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SITE_CONFIG;
}
