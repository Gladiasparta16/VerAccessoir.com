"""
Simple migration runner for SQLite: checks and adds missing columns.
Run via: .venv\Scripts\python.exe tools\run_migrations.py
"""
import os, sys
# Ensure repo root is on sys.path so we can import BACKEND modules
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root)
# Also add BACKEND dir so imports in BACKEND/app.py find local modules like config, models
sys.path.insert(0, os.path.join(root, 'BACKEND'))
import sqlite3
import os

DB_PATH = os.environ.get('DATABASE_URL', 'sqlite:///database.db').replace('sqlite:///', '')
MIGRATIONS = [
    {
        "id": "20260203_add_featured_to_product",
        "sql": "ALTER TABLE product ADD COLUMN featured BOOLEAN DEFAULT 0",
        "check": "SELECT name FROM pragma_table_info('product') WHERE name='featured'"
    }
]

if not os.path.exists(DB_PATH):
    print('Database file not found, nothing to migrate:', DB_PATH)
else:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for m in MIGRATIONS:
        try:
            cur.execute(m['check'])
            res = cur.fetchone()
            if res is None:
                print(f"Applying migration {m['id']}")
                cur.execute(m['sql'])
                conn.commit()
                print('Migration applied')
            else:
                print(f"Migration {m['id']} already applied")
        except Exception as e:
            print(f"Migration {m['id']} failed: {e}")
    cur.close()
    conn.close()

