from getpass import getpass
import os
from app import app
from models import db, User
from werkzeug.security import generate_password_hash


def create_admin(email, password, name="Administrateur"):
    with app.app_context():
        if User.query.filter_by(email=email).first():
            print(f"User with email {email} already exists.")
            return
        user = User(email=email, password=generate_password_hash(password), name=name, is_admin=True)
        db.session.add(user)
        db.session.commit()
        print(f"Admin created: {email}")


def main():
    email = os.environ.get('INITIAL_ADMIN_EMAIL') or input('Admin email: ').strip()
    if not email:
        print('Email is required')
        return
    password = os.environ.get('INITIAL_ADMIN_PASSWORD')
    if not password:
        password = getpass('Admin password (will not echo): ')
    if not password:
        print('Password is required')
        return
    create_admin(email, password)


if __name__ == '__main__':
    main()
