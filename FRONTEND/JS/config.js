// Configuration du site — personnalisez depuis le backend ou via variables d'environnement
const SITE_CONFIG = {
  contact: {
    phone: "+225 0787985182",
    email: "info@veraccessoire.com",
    address: "ABIDJAN, Côte d'Ivoire",
    hours: "Lun-Sam: 9h-18h | Dim: Fermé"
  },
  social: {
    whatsapp: "https://wa.me/2250787985182",
    instagram: "https://instagram.com/veraccessoire",
    facebook: "https://facebook.com/veraccessoire"
  },
  company: {
    name: "VerAccessoire",
    tagline: "Des lunettes qui révèlent ton style",
    description: "La meilleure plateforme de vente de lunettes en ligne"
  },
  payment: {
    orangeMoney: "",
    moovMoney: "",
    mtnMoney: "",
    wave: ""
  }
};

// Init siteConfig localStorage only with non-sensitive defaults
function initializeConfig() {
  const saved = localStorage.getItem('siteConfig');
  if (!saved) {
    const defaultConfig = {
      social: {
        facebook: '#',
        instagram: '#',
        whatsapp: '#'
      },
      siteName: SITE_CONFIG.company.name,
      tagline: SITE_CONFIG.company.tagline
    };
    localStorage.setItem('siteConfig', JSON.stringify(defaultConfig));
  }
}

initializeConfig();

if (typeof module !== 'undefined' && module.exports) {
  module.exports = SITE_CONFIG;
}
