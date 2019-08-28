from wtforms import Form
from flask import request

from app.libs.api_exceptions import ClientException


class BaseValidator(Form):
    def __init__(self):

        args = request.args
        data = request.get_json()

        super(BaseValidator, self).__init__(args, data=data)

    def validate_for_api(self):
        valid = super(BaseValidator, self).validate()

        if not valid:
            raise ClientException(msg=self.errors)

        return self
