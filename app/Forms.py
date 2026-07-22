
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField


class SignupForm(FlaskForm):   
    username = StringField('username', [DataRequired(), Length(max=64)])
    password = PasswordField('password', [DataRequired(), Length(min=8)])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField('Signup')


class LoginForm(FlaskForm):   
    username = StringField('username', [DataRequired(), Length(max=64)])
    password = PasswordField('password', [DataRequired(), Length(min=8)])
    submit = SubmitField('Login')


class ForgetPasswordForm(FlaskForm):   
    username = StringField('username', [DataRequired(), Length(max=64)])
    submit = SubmitField('Send Verification Code')


class ResetPasswordForm(FlaskForm):
    newPassword = StringField('New password', [DataRequired(), Length(min=8, max=64)])
    verificationCode = StringField('Verification code', [DataRequired(), Length(min=4, max=4)])
    submit = SubmitField('Reset the password')


class ProfPicUploadForm(FlaskForm):
    uploadbox = FileField()
    submit = SubmitField('Upload')
