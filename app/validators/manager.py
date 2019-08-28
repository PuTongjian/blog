from wtforms.validators import Email, DataRequired, Length
from wtforms import StringField
from flask import current_app

from .base import BaseValidator
from app.libs.api_exceptions import ClientException


class ManagerValidator(BaseValidator):
    email = StringField(validators=[Email()])
    password = StringField(validators=[DataRequired()])
    nickname = StringField(validators=[Length(min=1, max=20)])
    authorization_code = StringField(validators=[DataRequired()])

    def validate_authorization_code(self, field):
        authorization_code = current_app.config['AUTHORIZATION_CODE']
        if field.data != authorization_code:
            raise ClientException(401)
