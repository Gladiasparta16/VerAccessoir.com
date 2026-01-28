#!/usr/bin/env python
"""
Script de configuration automatique pour VerAccessoire
Initialise la base de données et prépare l'environnement
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Créer et configurer l'environnement"""
    print("🔧 Configuration de l'environnement...")
    
    # Créer le dossier BACKEND s'il n'existe pas
    backend_path = Path(__file__).parent
    
    # Créer .env s'il n'existe pas
    env_file = backend_path / '.env'
    if not env_file.exists():
        env_content = """FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=dev-secret-key-2024-veraccessoire
JWT_SECRET_KEY=jwt-secret-key-2024-veraccessoire
DATABASE_URL=sqlite:///data.db
PORT=5000
HOST=0.0.0.0
"""
        env_file.write_text(env_content)
        print("✅ Fichier .env créé")
    else:
        print("✅ Fichier .env existant")

def init_database():
    """Initialiser la base de données"""
    print("\n📦 Initialisation de la base de données...")
    
    os.chdir(Path(__file__).parent)
    sys.path.insert(0, str(Path(__file__).parent))
    
    try:
        from app import create_app
        from models import db
        
        app = create_app()
        with app.app_context():
            db.create_all()
            print("✅ Tables créées avec succès")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    return True

def check_dependencies():
    """Vérifier que les dépendances sont installées"""
    print("\n📚 Vérification des dépendances...")
    
    required = [
        'flask',
        'flask_cors',
        'flask_sqlalchemy',
        'flask_jwt_extended',
        'python-dotenv'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} manquant")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️ Installez les paquets manquants avec:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    return True

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║        🎨 VerAccessoire - Configuration Initial           ║
    ║                                                           ║
    ║  Site e-commerce de lunettes avec API Flask moderne      ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Vérifier les dépendances
    if not check_dependencies():
        print("\n⚠️ Installez d'abord les dépendances:")
        print("pip install -r requirements.txt")
        return False
    
    # Configurer l'environnement
    setup_environment()
    
    # Initialiser la base de données
    if not init_database():
        return False
    
    print("""
    
    ✅ Configuration terminée!
    
    🚀 Pour démarrer le serveur, exécutez:
    
    cd BACKEND
    python app.py
    
    Puis accédez à: http://localhost:5000/
    
    📝 URLs importantes:
    - Accueil: http://localhost:5000/
    - Boutique: http://localhost:5000/pages/shop.html
    - Panier: http://localhost:5000/pages/cart.html
    - Admin: http://localhost:5000/pages/admin.html
    - API Health: http://localhost:5000/api/health
    
    """)
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
