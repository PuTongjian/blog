from wtforms import StringField, IntegerField
from wtforms.validators import Length, NumberRange
import base64

from .base import BaseValidator
from app.libs.enums import ArticleOperaEnum


validator_parameter = {
    'id': IntegerField(default=None),
    'category_id': StringField(default=None),
    'content': StringField(),
    'page': IntegerField(validators=[NumberRange(min=0)], default=1),
    'num': IntegerField(validators=[NumberRange(min=1)], default=1),
    'sharing_status': IntegerField(validators=[NumberRange(min=1, max=2)]),
    'title': StringField(validators=[Length(min=1, max=30)])
}

validator = {
    ArticleOperaEnum.create_article.name: ['category_id', 'title'],
    ArticleOperaEnum.alter_article_category.name: ['id', 'category_id'],
    ArticleOperaEnum.alter_article_share_status.name: ['id', 'sharing_status'],
    ArticleOperaEnum.update_article_content.name: ['id', 'title', 'content'],
    ArticleOperaEnum.get_articles.name: ['page', 'num', 'category_id'],
    ArticleOperaEnum.get_article_content.name: ['id'],
    ArticleOperaEnum.get_article_html_content.name: ['content'],
    ArticleOperaEnum.get_all_articles.name: ['category_id'],
    ArticleOperaEnum.delete_article.name: ['id'],
}


class ArticleValidator(BaseValidator):
    @classmethod
    def create_validator(cls, opera_code: int):
        [delattr(cls, key)for key in validator_parameter.keys() if hasattr(cls, key)]
        name = ArticleOperaEnum(opera_code).name
        for key in validator[name]:
            if key in validator_parameter.keys():
                setattr(cls, key, validator_parameter[key])
        return cls()

    @property
    def key(self):
        return base64.b64encode(str(self.data).encode())



