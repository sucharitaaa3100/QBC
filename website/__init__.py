from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mailman import Mail

db = SQLAlchemy()
DB_NAME = "qbc.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'shahid'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    from .models import User, Quiz, Question, Score, Chapter, Subject
    create_database(app)
    return app

from werkzeug.security import generate_password_hash
from .models import User 
def create_database(app):
    with app.app_context():
        if not path.exists('website/' + DB_NAME):
            db.create_all()
            print("Created Database!")

            # Check if admin user already exists
            admin_user = User.query.filter_by(email="admin_qbc@fastmail.com").first()
            if not admin_user:
                print("Creating default admin user...")
                admin = User(
                    email="admin_qbc@fastmail.com",
                    password=generate_password_hash("admin@123"),
                    full_name="Admin QBC",
                    is_admin=True,
                    is_verified=True
                )
                db.session.add(admin)
                db.session.commit()
                print("Admin user created!")

        else:
            print("Database already exists!")