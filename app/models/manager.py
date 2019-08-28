from sqlalchemy import Column, String, SmallInteger
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager

from .base import Base
from app.libs.api_exceptions import ClientException

login_manager = LoginManager()


class Manager(Base, UserMixin):
    email = Column(String(30), primary_key=True)
    _password = Column('password', String(128), nullable=False)
    nickname = Column(String(20), nullable=False)
    permission = Column(SmallInteger, nullable=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, password):
        if not check_password_hash(self.password, password):
            raise ClientException(code=401, msg='密码或用户名错误')

    def get_id(self):
        try:
            return str(self.email)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    @classmethod
    def register(cls, **kwargs):
        manager = cls()
        manager.set_attrs(**kwargs)
        manager.permission = 1

        return manager

    @classmethod
    def login(cls, email, password):
        manager = cls.query.filter_by(email=email).first_or_404()
        manager.check_password(password)

        return manager


@login_manager.user_loader
def load_user(user_id):
    return Manager.query.get(user_id)
