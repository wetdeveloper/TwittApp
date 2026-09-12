# app/__init__.py

import os

from flask import Flask
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
admin = Admin(name="TwittApp Admin", template_mode="bootstrap3")
bootstrap = Bootstrap()
moment = Moment()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__, template_folder="static")

    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY",
        "dev-secret-key"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Db.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.Login"

    bootstrap.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)
    admin.init_app(app)

    CORS(app)

    with app.app_context():
        from . import Model

    from .routes import (
    auth_bp,
    users_bp,
    tweets_bp,
    comments_bp,
    social_bp,
    messages_bp,
    misc_bp,
)
    print("Routes imported successfully")
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(tweets_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(social_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(misc_bp)
    # admin.init_app(app)

    return app
