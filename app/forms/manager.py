from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import Email, DataRequired
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField()
    remember_me = BooleanField(label='记住我')
