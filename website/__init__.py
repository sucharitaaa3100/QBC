from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mailman import Mail
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
mail = Mail()  

DB_NAME = "qbc.db"

from .models import User  # Import the User model

def create_database(app):
    with app.app_context():
        if not path.exists('instance/' + DB_NAME):
            db.create_all()
            print("Created Database!")

            # Check if admin user already exists
            admin_user = User.query.filter_by(email="admin_qbc@fastmail.com").first()
            if not admin_user:
                print("Creating default admin user...")
                admin = User(
                    email="qbc_admin@fastmail.com",
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


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'shahid'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    app.config['MAIL_SERVER'] = 'smtp.fastmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'qbc_admin@fastmail.com'  # Replace with your email
    app.config['MAIL_PASSWORD'] = '342b6h558h6z2w57'  # Replace with your email password
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    
    db.init_app(app)
    mail.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect to login page if not authenticated

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Fetch user from the database

    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Quiz, Question, Score, Chapter, Subject
    
    create_database(app)
    
    return app


