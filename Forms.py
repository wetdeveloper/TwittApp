from app import *
class SignupForm(FlaskForm):   
      username = StringField('username', [validators.DataRequired(), validators.Length(max=64)])
      password = PasswordField('password', [validators.DataRequired(),validators.Length(min=8)])
      email = StringField("Email",  validators=[validators.DataRequired()])
      submit=SubmitField('Signup')
      # recaptcha = RecaptchaField()


class LoginForm(FlaskForm):   
      username = StringField('username', [validators.DataRequired(), validators.Length(max=64)])
      password = PasswordField('password', [validators.DataRequired(),validators.Length(min=8)])
      submit=SubmitField('Login')
      # recaptcha = RecaptchaField()

class ForgetPasswordForm(FlaskForm):   
      username = StringField('username', [validators.DataRequired(), validators.Length(max=64)])
      submit=SubmitField('Send Verification Code')
      # recaptcha = RecaptchaField()

class ResetPasswordForm(FlaskForm):
      newPassword=StringField('New password',[validators.DataRequired(), validators.Length(max=64,min=8)])
      verificationCode=StringField('Verification code',[validators.DataRequired(), validators.Length(max=4,min=4)])
      submit=SubmitField('Rest the password')
      # recaptcha = RecaptchaField()
