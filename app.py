from force_venv import *
import datetime,time
import random
import uuid
import os, subprocess
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



login_manager=LoginManager()
login_manager.init_app(app)



Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Db.db'
db = SQLAlchemy(app)

csrf=CSRFProtect(app)
app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'
app.config['SESSION_SQLALCHEMY'] = db

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if type(dbapi_connection) is sqlite3.Connection:  # play well with other DB backends
       cursor = dbapi_connection.cursor()
       cursor.execute("PRAGMA foreign_keys=ON")
       cursor.close()

admin=Admin(app,name='My App',template_mode='bootstrap3')
engine=create_engine('sqlite:///DB.db')

moment=Moment(app)


if __name__ == '__main__':
 
    PORT = 5000
    
    print(f"🔄 آزاد کردن پورت {PORT} ...")
    
    # روش مناسب برای مانجارو (با ss)
    try:
        # پیدا کردن PID فرآیند روی پورت
        result = subprocess.run(
            f"ss -tlnp | grep :{PORT}", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        if result.stdout:
            # استخراج PID
            pid_line = result.stdout.strip().split('\n')[0]
            if 'pid=' in pid_line:
                pid = pid_line.split('pid=')[1].split(',')[0]
                subprocess.run(f"kill -9 {pid}", shell=True)
                print(f"   Process {pid} killed")
                time.sleep(1.5)
            else:
                print("   Process found but PID extraction failed")
    except:
        pass
    
    print(f"🚀 Starting Flask on port {PORT}")
    app.run(debug=True)
