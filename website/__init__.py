from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_mailman import Mail
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from datetime import datetime, date

# Initialize extensions globally
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load environment variables from .env file
    load_dotenv()

    # App Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_super_secret_key_default')
    
    # Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f"sqlite:///{os.environ.get('SQLITE_DB', 'qbc.db')}")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Flask-Mailman Configuration
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 465))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'False').lower() == 'true'
    app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'True').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', os.environ.get('MAIL_USERNAME'))

    # Initialize extensions with the app
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(id):
        from .models import User
        return User.query.get(int(id))

    # Register blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Create database tables and default admin if they don't exist
    with app.app_context():
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if not path.exists(db_path):
            db.create_all()
            print("Created Database tables!")
        else:
            print("Database tables already exist.")

        from .models import User
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'adminpassword')

        if not User.query.filter_by(is_admin=True).first():
            print("No admin user found. Creating a default admin user.")
            default_admin = User(
                email=admin_email,
                full_name='Admin QBC',
                # Removed method='sha256'
                password=generate_password_hash(admin_password), 
                qualification='N/A',
                dob=date(2000, 1, 1),
                is_admin=True,
                is_verified=True
            )
            db.session.add(default_admin)
            db.session.commit()
            print(f"Default admin user created: Email={admin_email}, Password={admin_password}")

    return app

