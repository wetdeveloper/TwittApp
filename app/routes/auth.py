from werkzeug.security import check_password_hash, generate_password_hash

from flask import (
    request,
    render_template,
    redirect,
    url_for,
    session,
    jsonify,
)

from flask_login import (
    current_user,
    login_user,
    logout_user,
)

from . import auth_bp
from ..Model import *
from ..Forms import *
from ..forgetpassVerification import *


@auth_bp.route('/logout')
def Logout():
    logout_user()
    return redirect(url_for('main.twitts'))


@auth_bp.route('/signup', methods=['POST', 'GET'])
def Signup():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = generate_password_hash(form.password.data)
            email = form.email.data

            user = User.query.filter_by(username=username).first()

            if not user:
                try:
                    user = User(username, password, email)
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)
                except BaseException as e:
                    return str(e)
                else:
                    return redirect(url_for("main.twitts"))

            return "This username is already taken.try another."

        return str(form.errors)

    return render_template("signup.html", form=form)
@auth_bp.route('/home/login',methods=['POST','GET'])
def Login():
    form=LoginForm()
    if request.method=='POST':
        if form.validate_on_submit():
            username=form.username.data
            password=form.password.data
            # user=User.query.filter_by(username=username).filter_by(password=password).first()
            user=User.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password,password):
                    login_user(user)
                    return redirect(url_for('main.twitts'))
                return "Wrong Password"
            else:
                return redirect(url_for('auth.Login',message='No user matches taken username and password. \n try again. '))
        return str(form.errors)
    elif request.method=='GET':
        message=''
        if current_user.is_authenticated:
            return redirect(url_for('main.twitts',login_message="You're already logged in.first logout then try to login via other account"))
        if 'message' in request.args:
            message=request.args['message']
        return render_template('login.html',message=message,form=form)


@auth_bp.route('/home/login/forgetpassword/',methods=["GET","POST"])
def ForgetPassword():
    form=ForgetPasswordForm()
    if request.method=="GET":
        if current_user.is_authenticated:
            return jsonify({
                "message":"You are already a user.log out to login twice!"
            })
        return render_template("forgetpassword.html",form=form)
    elif request.method=="POST":
        if form.validate_on_submit():
            username=form.username.data
            user=User.query.filter_by(username=username).first()
            if user:
                emailAddress=user.email
                session["verification"]={}
                session["verification"]["verificationCode"]=[str(random.randint(0,9)) for i in range(4)]
                session["verification"]["verificationCode"]="".join(session["verification"]["verificationCode"])
                session["verification"]["emailAddress"]=emailAddress
                mailVerCode(emailAddress,session["verification"]["verificationCode"])
                return redirect(url_for("auth.ResetPassword"))
            else:
                return jsonify({
                    "message":"User is not found"
                })
        else:
            return str(form.errors)
@auth_bp.route('/home/login/forgetpassword/resetpassword',methods=['GET','POST'])
def ResetPassword():
    form=ResetPasswordForm()
    if request.method=='GET':
        if current_user.is_authenticated:
            return jsonify({
                "message":"You are already a user.log out to login twice!"
            })
        else:
            if not("verification" in session):
                return redirect(url_for('auth.ForgetPassword'))
            else:
                return render_template('reset-password.html',form=form)
    elif request.method=='POST':
        if form.validate_on_submit():
            if session["verification"]["verificationCode"]==form.verificationCode.data:
                User.query.filter_by(email=session["verification"]["emailAddress"]).first().password=form.newPassword.data
                del session["verification"]
                return jsonify({
                    "message":"Password is Changed!"
                })
            else:
                del session["verification"]
                return redirect(url_for("auth.ForgetPassword"))


