import datetime
import random
import uuid
import os
from flask import Flask,render_template,url_for,request,redirect,jsonify,session
from flask_login import login_user,LoginManager,current_user,logout_user
from flask_sessionstore import Session
from flask_wtf import FlaskForm ,CSRFProtect,RecaptchaField,Recaptcha
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from wtforms import PasswordField,StringField, validators,SubmitField
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from sqlalchemy.engine import Engine
from sqlalchemy import event,create_engine,or_,desc
from flask_bootstrap import Bootstrap  
from flask_login import UserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_moment import Moment 
from flask_cors import CORS
# import pytest

app=Flask(__name__, template_folder='static')

CORS(app)
app.app_context().push()
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.config['WTF_CSRF_SECRET_KEY']='wtffdjfksdjfksjg;jgkdlsgh'

# app.config['service_email_address']="your mail address"
# app.config['service_email_appPassword']='abcdefghhhhhhh" #Like gmail app password

login_manager=LoginManager()
login_manager.init_app(app)

# app.config['RECAPTCHA_USE_SSL']= False
# app.config['RECAPTCHA_PUBLIC_KEY']= '6Lc5wpMgAAAAAGkyxQ7ks_6xanfvZgB3dcyz8eYN'
# app.config['RECAPTCHA_PRIVATE_KEY']='6Lc5wpMgAAAAAIAWAhI6EFGhlytXDFgPG5A1XBrf'
# app.config['RECAPTCHA_PARAMETERS']={'hl': 'zh', 'render': 'explicit'}
# app.config['RECAPTCHA_DATA_ATTRS ']={'theme': 'dark'}
# recaptcha = RecaptchaField(app)

Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Db.db'
db = SQLAlchemy(app)

csrf=CSRFProtect(app)
app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'
app.config['SESSION_SQLALCHEMY'] = db
# app.config['SESSION_TYPE'] = 'sqlalchemy'
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if type(dbapi_connection) is sqlite3.Connection:  # play well with other DB backends
       cursor = dbapi_connection.cursor()
       cursor.execute("PRAGMA foreign_keys=ON")
       cursor.close()

admin=Admin(app,name='My App',template_mode='bootstrap3')
engine=create_engine('sqlite:///DB.db')

moment=Moment(app)


if __name__ == "__main__":
    #Session(app)
    app.run(debug='True')

