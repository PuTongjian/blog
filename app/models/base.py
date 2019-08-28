from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery as _BaseQuery
from contextlib import contextmanager
from sqlalchemy import Column, SmallInteger

from app.libs.api_exceptions import ClientException


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise ClientException()


class BaseQuery(_BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(BaseQuery, self).filter_by(**kwargs)

    def first_or_404(self, description=None):
        rv = self.first()
        if rv is None:
            raise ClientException(code=404, msg=description)
        return rv

    def get_or_404(self, ident, description=None):
        rv = self.get(ident)
        if rv is None:
            raise ClientException(code=404, msg=description)
        return rv


db = SQLAlchemy(query_class=BaseQuery)


class Base(db.Model):
    __abstract__ = True

    status = Column(SmallInteger, default=1)

    def delete(self):
        self.status = 0

    def set_attrs(self, **attrs):
        for key, val in attrs.items():
            if hasattr(self, key):
                setattr(self, key, val)

    def keys(self):
        return self.field

    def __getitem__(self, item):
        return getattr(self, item)

