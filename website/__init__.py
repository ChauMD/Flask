from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] =  '123'
#app.config['SQLALCHEMY_DATABASE_URI']= f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI']= f'postgres://lpkmfjwayhvoka:bae127a5b9629a5d7d1c8fe9934cae2dfb176c5830106b309862680158cec66b@ec2-54-211-255-161.compute-1.amazonaws.com:5432/deoei8ls1t9bai'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
# tell about database from models
    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view= 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created database!')
