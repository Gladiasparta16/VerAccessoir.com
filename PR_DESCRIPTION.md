Titre: Corrige badge panier et durcit configuration pour déploiement

Résumé:
- Met à jour le badge du panier pour qu'il s'incrémente immédiatement lors de l'ajout depuis `shop.html`.
- Centralise les headers de sécurité dans `BACKEND/config.py` et rend `DEBUG` configurable via `.env`.
- Ajoute un petit script `tools/compile_all.py` pour vérifier la syntaxe Python.
- Génère un ZIP nettoyé pour partage: `verraaccessoire_share.zip` sur le Bureau.

Fichiers modifiés/ajoutés:
- `FRONTEND/pages/shop.html` (appel `updateCartBadge()` ajouté après `localStorage.setItem`)
- `BACKEND/config.py` (ajout `DEBUG`, ajustement `SECURITY_HEADERS`)
- `BACKEND/app.py` (utilise `SECURITY_HEADERS` depuis la config et `app.run(debug=...)`)
- `tools/compile_all.py` (nouveau)
- `PR_DESCRIPTION.md` (ce fichier)

Instructions de test local:
1. Créer un environnement virtuel et installer les dépendances:
   python -m venv .venv
   .venv\Scripts\activate
   python -m pip install -r BACKEND/requirements.txt
2. Créer un fichier `BACKEND/.env` (ou `BACKEND/.env`) si besoin et définir `SECRET_KEY` et `JWT_SECRET_KEY` pour les tests.
3. Lancer le serveur local: `python BACKEND/app.py` (ou `START.bat`).
4. Ouvrir http://localhost:5000/shop.html, ajouter un produit: le badge doit s'incrémenter immédiatement.

Variables d'environnement recommandées (.env):
- SECRET_KEY=une_clé_forte
- JWT_SECRET_KEY=une_autre_clé
- FLASK_DEBUG=False
- DATABASE_URL=sqlite:///database.db (ou votre URL PostgreSQL en prod)

Notes sécurité & déploiement:
- Ne pas activer `DEBUG` en production.
- Restreindre CORS aux domaines autorisés dans production.
- Stocker secrets dans le gestionnaire d'environnement de votre hébergeur.
- Vérifier les règles CSP/CORS si frontend et backend seront sur domaines différents.

Suivants possibles:
- Ajuster CSP `connect-src` pour le domaine final (par ex. `connect-src 'self' https://mon-frontend.example`).
- Ajouter tests automatisés pour le front (E2E) et pour l'API.

Merci — copier/coller ce contenu comme description de PR si nécessaire.
