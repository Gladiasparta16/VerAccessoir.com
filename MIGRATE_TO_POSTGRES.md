Migration SQLite -> PostgreSQL
=================================

Options recommandées pour migrer les données et tester localement.

1) Méthode rapide (recommandée si vous pouvez installer pgloader)

- Installer pgloader (Linux/macOS): https://pgloader.io/
- Exemple de commande:
  pgloader sqlite:///path/to/database.db postgresql://user:pass@host:5432/dbname

2) Méthode via Docker (tester tout localement avec docker-compose)

- Modifier `BACKEND/.env` pour utiliser DATABASE_URL=postgresql://verra_user:change_me@db:5432/verra_db
- Lancer les services:
  docker-compose up --build -d
- Initialiser la base (après que Postgres soit prêt):
  docker-compose exec web python init_db.py

3) Méthode manuelle CSV (si pgloader impossible)

- Exporter chaque table SQLite en CSV, créer les tables équivalentes sur Postgres, puis importer via COPY.

4) Remarques

- Vérifier les IDs / séquences (serial) après migration.
- Tester /api/health, /api/products et l'inscription/connexion.
- En production: ne pas utiliser les credentials d'exemple et activer sauvegardes automatiques.
