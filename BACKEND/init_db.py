from app import app
from models import db, User, Product, Order, OrderItem
from werkzeug.security import generate_password_hash

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
            ),
            Product(
                name="Lunettes Modernes Dorées",
                price=18000,
                description="Monture en métal doré, style contemporain",
                image_url="https://via.placeholder.com/300x300?text=Modernes+Dorees",
                category="modernes",
                stock=15,
            ),
            Product(
                name="Lunettes Solaires Aviateur",
                price=22000,
                description="Protection UV 100%, lentilles teintées fumées",
                image_url="https://via.placeholder.com/300x300?text=Aviateur",
                category="solaires",
                stock=25,
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

    # Créer utilisateur admin de test
    if User.query.filter_by(email="admin@veraccessoire.com").first() is None:
        admin = User(
            email="admin@veraccessoire.com",
            password=generate_password_hash("admin123"),
            name="Administrateur",
            is_admin=True,
        )
        db.session.add(admin)
        db.session.commit()
        print("✓ Administrateur créé: admin@veraccessoire.com / admin123")

    # Créer utilisateur client de test
    if User.query.filter_by(email="test@example.com").first() is None:
        user = User(
            email="test@example.com",
            password=generate_password_hash("test123"),
            name="Client Test",
            is_admin=False,
        )
        db.session.add(user)
        db.session.commit()
        print("✓ Utilisateur créé: test@example.com / test123")

    print("\n✓ Base de données initialisée avec succès!")
