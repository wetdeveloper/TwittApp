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
    login_manager.login_view = "login"

    bootstrap.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)
    admin.init_app(app)

    CORS(app)

    with app.app_context():
        from . import Model

    from . import routes
    print("Routes imported successfully")
    app.register_blueprint(routes.bp)
    # admin.init_app(app)

    return app
