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

from . import bp
from ..Model import *
from ..Forms import *
from ..forgetpassVerification import *


@bp.route('/logout')
def Logout():
    logout_user()
    return redirect(url_for('main.twitts'))


@bp.route('/signup', methods=['POST', 'GET'])
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
