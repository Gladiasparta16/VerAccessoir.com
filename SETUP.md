## 🚀 COMMENT DÉMARRER LE SITE

### Le plus facile (Windows)
1. Double-cliquez sur **START.bat**
2. Attendez 30 secondes
3. Le site s'ouvre automatiquement sur http://localhost:5000

### Ou depuis PowerShell
```powershell
.\.venv\Scripts\Activate.ps1
python BACKEND/app.py
```

---

## ✅ TEST RAPIDE

Vérifiez que tout fonctionne :

1. **Accueil** → Les produits s'affichent
2. **Boutique** → Cliquez "Ajouter au panier"
3. **Panier (🛒)** → Article apparaît
4. **S'inscrire** → Créez un compte
5. **Admin** (http://localhost:5000/pages/admin-login.html)
    - NOTE: par sécurité, aucun compte admin par défaut n'est créé.
    - Pour créer un administrateur initial, définissez les variables d'environnement dans `BACKEND/.env` ou via votre hébergeur:
      - `INITIAL_ADMIN_EMAIL` et `INITIAL_ADMIN_PASSWORD` (optionnel)
    - Ou utilisez la fonctionnalité d'administration pour créer un compte via l'interface (si disponible).

---

## 📦 Fichiers Importants

| Fichier | Fonction |
|---------|----------|
| `START.bat` | Lance le serveur |
| `BACKEND/app.py` | API principale |
| `FRONTEND/index.html` | Page d'accueil |
| `BACKEND/requirements.txt` | Dépendances Python |

---

## ❌ SI ERREUR

**"ModuleNotFoundError"** → Recréer le venv :
```powershell
Remove-Item -Recurse -Force ".venv"
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r BACKEND/requirements.txt
python BACKEND/app.py
```

**Port 5000 occupé** → Changer dans `BACKEND/app.py` ligne 189 :
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Changez 5000 à 8000
```

---

## 📋 DONNÉES

- **Produits** : Base de données SQLite (instance/data.db)
- **Panier** : localStorage du navigateur
- **Utilisateurs** : BD SQLite chiffrés

**Réinitialiser la BD** : Supprimer `instance/` puis relancer
