# VerAccessoire - Site de Vente de Lunettes 👓

Un site e-commerce moderne et complet pour la vente de lunettes de qualité.

## 📁 Structure du Projet

```
VerAccessoire/
├── FRONTEND/
│   ├── index.html                 # Page d'accueil
│   ├── pages/
│   │   ├── shop.html              # Boutique
│   │   ├── cart.html              # Panier
│   │   ├── about.html             # À propos
│   │   └── contact.html           # Contact
│   ├── css/
│   │   ├── styles.css             # Styles principaux
│   │   └── variables.css          # Variables CSS
│   ├── js/
│   │   ├── main.js                # Logique principale
│   │   ├── api/
│   │   │   └── client.js          # Client API
│   │   └── components/
│   │       ├── products.js        # Gestion des produits
│   │       └── cart.js            # Gestion du panier
│   └── assets/
│       ├── images/                # Images des produits
│       └── icons/                 # Icônes
│
└── BACKEND/
    ├── app.py                     # Application Flask
    ├── config.py                  # Configuration
    ├── models.py                  # Modèles de données
    ├── init_db.py                 # Initialisation BD
    ├── requirements.txt           # Dépendances
    └── routes/
        ├── products.py            # Routes produits
        ├── auth.py                # Routes authentification
        ├── orders.py              # Routes commandes
        └── admin.py               # Routes admin
```

## 🚀 Installation et Démarrage

### Backend

1. **Installer les dépendances:**
```bash
cd BACKEND
pip install -r requirements.txt
```

2. **Initialiser la base de données:**
```bash
python init_db.py
```

3. **Démarrer le serveur:**
```bash
python app.py
```

Le serveur sera accessible à `http://localhost:5000`

### Frontend

1. **Ouvrir dans un navigateur:**
Ouvrir le fichier `FRONTEND/index.html` dans un navigateur.

Ou pour un serveur local:
```bash
# Avec Python 3
python -m http.server 8000 --directory FRONTEND

# Puis accéder à http://localhost:8000
```

## 📚 API Documentation

### Authentification

#### Register
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"
}
```

#### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

### Produits

#### Récupérer tous les produits
```bash
GET /api/products
```

#### Récupérer un produit
```bash
GET /api/products/:id
```

#### Créer un produit (Admin)
```bash
POST /api/products
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Lunettes Classiques",
  "price": 15000,
  "description": "Description du produit",
  "image_url": "url_image",
  "category": "classiques",
  "stock": 10
}
```

### Commandes

#### Créer une commande
```bash
POST /api/orders
Authorization: Bearer <token>
Content-Type: application/json

{
  "items": [
    {"product_id": 1, "quantity": 2}
  ],
  "total_amount": 30000
}
```

#### Récupérer les commandes de l'utilisateur
```bash
GET /api/orders
Authorization: Bearer <token>
```

## 🎨 Caractéristiques

- ✅ Design moderne et responsive
- ✅ Système de panier fonctionnel
- ✅ Authentification sécurisée JWT
- ✅ Gestion des produits
- ✅ Gestion des commandes
- ✅ Interface admin
- ✅ Support multi-navigateur
- ✅ Optimisé pour mobiles

## 🛠️ Technologies Utilisées

### Frontend
- HTML5
- CSS3 (Variables, Flexbox, Grid)
- Vanilla JavaScript (ES6+)
- Fetch API

### Backend
- Python 3
- Flask
- Flask-CORS
- Flask-SQLAlchemy
- Flask-JWT-Extended
- SQLite

## 📱 Pages et Fonctionnalités

### Accueil
- Affichage des produits en vedette
- Section statistiques
- Call-to-action vers la boutique

### Boutique
- Liste complète des produits
- Affichage du prix et description
- Bouton "Ajouter au panier"

### Panier
- Vue d'ensemble des articles
- Modification des quantités
- Calcul du total
- Procédure de paiement

### À Propos
- Présentation de la marque
- Valeurs et mission
- Raisons de choisir VerAccessoire

### Contact
- Formulaire de contact
- Informations de contact
- Horaires d'ouverture

## 🔐 Sécurité

- JWT pour l'authentification
- Hachage des mots de passe
- CORS configuré
- Protection des routes admin

## 📝 Variables CSS Personnalisables

Modifiez `css/variables.css` pour adapter les couleurs, espacements et typographie:

```css
:root {
  --color-primary: #ff6a00;
  --color-primary-dark: #e55a00;
  --spacing-lg: 24px;
  /* ... */
}
```

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à proposer des améliorations.

## 📄 Licence

Ce projet est sous licence MIT.

## 📧 Support

Pour toute question ou problème, contactez-nous à: info@veraccessoire.com

---

**VerAccessoire** - Des lunettes qui révèlent ton style 👓
