import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from models import db, User, Product
from werkzeug.security import generate_password_hash

with app.app_context():
    # WARNING: This will recreate the schema and erase existing data in dev DB
    print('Dropping existing tables (if any)')
    db.drop_all()
    db.create_all()
    print('Schema recreated')

    products = [
        Product(
            name='Lunettes Classiques Noires',
            price=15000,
            description='Design élégant et intemporel, parfaites pour tous les jours',
            image_url='https://via.placeholder.com/300x300?text=Classiques+Noires',
            category='classiques',
            stock=20,
            featured=True,
        ),
        Product(
            name='Lunettes Modernes Dorées',
            price=18000,
            description='Monture en métal doré, style contemporain',
            image_url='https://via.placeholder.com/300x300?text=Modernes+Dorees',
            category='modernes',
            stock=15,
            featured=True,
        ),
        Product(
            name='Lunettes Solaires Aviateur',
            price=22000,
            description='Protection UV 100%, lentilles teintées fumées',
            image_url='https://via.placeholder.com/300x300?text=Aviateur',
            category='solaires',
            stock=25,
            featured=True,
        ),
    ]

    db.session.add_all(products)

    # Create admin
    admin = User(
        email='admin@veraccessoire.com',
        password=generate_password_hash('admin123'),
        name='Administrateur',
        is_admin=True,
    )
    db.session.add(admin)
    db.session.commit()
    print('Seeded products and admin')
