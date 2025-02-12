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

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')