Instructions de test rapide

1) Créer un environnement Python et l'activer

Windows (PowerShell):
```
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2) Installer les dépendances
```
cd BACKEND
pip install -r requirements.txt
```

3) Créer `BACKEND/.env` à partir de `BACKEND/.env.example` et remplir les valeurs

4) Initialiser la base de données (créera comptes de test)
```
python init_db.py
```

5) Lancer l'application
```
python app.py
```

Accéder à http://localhost:5000

Notes:
- Ne partagez pas `BACKEND/.env` par email en clair. Demandez au collègue de créer son propre `.env` à partir de `.env.example`.
- Le ZIP fourni exclut `.venv`, `logs`, `instance`, `.git` et fichiers temporaires.

Docker / PostgreSQL (optionnel)
- Pour tester avec Postgres via Docker, exécute à la racine :
	- `docker-compose up --build -d`
	- attendre que Postgres soit prêt, puis : `docker-compose exec web python init_db.py`
	- l'application sera accessible sur `http://localhost:5000`

Ne laisse jamais de secrets réels dans `BACKEND/.env` si tu partages le projet.
