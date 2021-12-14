from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager
from flask_restful import Api


db = SQLAlchemy()
DB_NAME = "project.sqlite3"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abulaman'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    api = Api(app)


    from .api import UserAPI, DeckAPI, CardAPI
    
    api.add_resource(UserAPI, '/api/user', '/api/user/<string:username>')
    api.add_resource(DeckAPI, '/api/deck/<string:username>')
    api.add_resource(CardAPI, '/api/<string:username>/<string:deck>/card', '/api/card/<string:card_id>','/api/<string:deck>')

    from .views import views

    app.register_blueprint(views, url_prefix="/")

    from .models import User, Deck, Card

    create_db(app)

    login_manager = LoginManager()
    login_manager.login_view = "views.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return  app, api

def create_db(app):
    if not path.exists("FlashyPep/"+ DB_NAME):
        db.create_all(app=app)
    print('DATABASE ALREADY EXISTS')