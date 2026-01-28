from app import app
from models import db, User, Product, Order, OrderItem
from werkzeug.security import generate_password_hash
import os

with app.app_context():
    db.create_all()
    print("Database initialized")

    # Vérifier si produits existent déjà
    if Product.query.first() is None:
        products = [
            Product(
                name="Lunettes Classiques Noires",
                price=15000,
                description="Design élégant et intemporel, parfaites pour tous les jours",
                image_url="https://via.placeholder.com/300x300?text=Classiques+Noires",
                category="classiques",
                stock=20,
                featured=True,
            ),
            Product(
                name="Lunettes Modernes Dorées",
                price=18000,
                description="Monture en métal doré, style contemporain",
                image_url="https://via.placeholder.com/300x300?text=Modernes+Dorees",
                category="modernes",
                stock=15,
                featured=True,
            ),
            Product(
                name="Lunettes Solaires Aviateur",
                price=22000,
                description="Protection UV 100%, lentilles teintées fumées",
                image_url="https://via.placeholder.com/300x300?text=Aviateur",
                category="solaires",
                stock=25,
                featured=True,
            ),
            Product(
                name="Lunettes Vintage Marron",
                price=16500,
                description="Style vintage avec monture épaisse, très tendance",
                image_url="https://via.placeholder.com/300x300?text=Vintage+Marron",
                category="vintage",
                stock=12,
            ),
            Product(
                name="Lunettes Cat-Eye Rose",
                price=17000,
                description="Forme chat, monture rose pastel, look rétro",
                image_url="https://via.placeholder.com/300x300?text=Cat-Eye+Rose",
                category="fashion",
                stock=18,
            ),
            Product(
                name="Lunettes Sportives Neon",
                price=19000,
                description="Verres photochromiques, parfait pour le sport",
                image_url="https://via.placeholder.com/300x300?text=Sportives",
                category="sport",
                stock=14,
            ),
            Product(
                name="Lunettes Carrées Transparentes",
                price=14000,
                description="Monture transparente, tendance actuelle",
                image_url="https://via.placeholder.com/300x300?text=Carrees",
                category="classiques",
                stock=22,
            ),
            Product(
                name="Lunettes Hexagonales Dorées",
                price=20000,
                description="Forme géométrique unique, très stylé",
                image_url="https://via.placeholder.com/300x300?text=Hexagonales",
                category="fashion",
                stock=10,
            ),
            Product(
                name="Lunettes Clubmaster Noir/Or",
                price=21000,
                description="Combinaison classe noir et or, look premium",
                image_url="https://via.placeholder.com/300x300?text=Clubmaster",
                category="classiques",
                stock=16,
            ),
            Product(
                name="Lunettes Oversize Tortoise",
                price=18500,
                description="Monture oversize motif écaille, très chic",
                image_url="https://via.placeholder.com/300x300?text=Oversize",
                category="fashion",
                stock=19,
            ),
        ]

        db.session.add_all(products)
        db.session.commit()
        print(f"✓ {len(products)} produits ajoutés")

    # Optional: create initial admin account only if specified via environment
    admin_email = os.environ.get("INITIAL_ADMIN_EMAIL")
    admin_password = os.environ.get("INITIAL_ADMIN_PASSWORD")
    if admin_email and admin_password:
        if User.query.filter_by(email=admin_email).first() is None:
            admin = User(
                email=admin_email,
                password=generate_password_hash(admin_password),
                name="Administrateur",
                is_admin=True,
            )
            db.session.add(admin)
            db.session.commit()
            print(f"✓ Administrateur créé: {admin_email} (from env)")
    else:
        print("Info: INITIAL_ADMIN_EMAIL not set — skipping creation of default admin.")

    # Optional: create test user only if environment requests it
    test_user_email = os.environ.get("INITIAL_TEST_USER_EMAIL")
    test_user_password = os.environ.get("INITIAL_TEST_USER_PASSWORD")
    if test_user_email and test_user_password:
        if User.query.filter_by(email=test_user_email).first() is None:
            user = User(
                email=test_user_email,
                password=generate_password_hash(test_user_password),
                name="Client Test",
                is_admin=False,
            )
            db.session.add(user)
            db.session.commit()
            print(f"✓ Utilisateur créé: {test_user_email} (from env)")
    else:
        print("Info: INITIAL_TEST_USER_EMAIL not set — skipping creation of test user.")

    print("\n✓ Base de données initialisée avec succès!")

    # S'assurer que certains produits sont marqués comme 'featured' si présents
    try:
        featured_names = [
            "Lunettes Classiques Noires",
            "Lunettes Modernes Dorées",
            "Lunettes Solaires Aviateur",
        ]
        for p in Product.query.filter(Product.name.in_(featured_names)).all():
            if not getattr(p, 'featured', False):
                p.featured = True
        db.session.commit()
        print("✓ Mise à jour des produits vedette effectuée")
    except Exception:
        db.session.rollback()
