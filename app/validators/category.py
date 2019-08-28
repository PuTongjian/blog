from wtforms import StringField, IntegerField
from wtforms.validators import Length, ValidationError

from .base import BaseValidator


class CategoryValidator(BaseValidator):
    id = IntegerField()
    name = StringField(validators=[Length(max=20)])

    def validate_id(self, raw):
        if isinstance(raw.data, str):
            try:
                self.id.data = int(raw.data)
            except Exception as err:
                raise ValidationError(message=err)

