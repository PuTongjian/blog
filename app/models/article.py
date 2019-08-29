from sqlalchemy import Column, String, Integer, Text, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship, reconstructor
import time

from .base import Base, db
from app.libs.enums import ShareStatus
from app.libs.api_exceptions import ClientException


class Article(Base):
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    title = Column(String(30), nullable=False)
    update_time = Column(Integer, nullable=False)
    page_views = Column(Integer, default=0)
    content = Column(Text, default=' ')
    sharing_status = Column(SmallInteger, default=1)
    category = relationship('Category')

    def __init__(self):
        self.get_current_time()
        self.id = self.update_time
        self.sharing_status = ShareStatus.private.value

    def get_current_time(self):
        self.update_time = time.time().__int__()

    def increase_page_views(self):
        with db.auto_commit():
            self.page_views += 1

    @classmethod
    def get_articles_with_paging(cls, page: int, num: int, category_id: int = None):
        if category_id:
            return cls.query.filter_by(category_id=category_id, sharing_status=ShareStatus.shared.value).paginate(page, num)
        return cls.query.filter_by().paginate(page, num)

    @classmethod
    def get_articles_with_category(cls, category_id):
        if not category_id:
            raise ClientException()
        return cls.query.filter_by(category_id=category_id).all()

    @property
    @reconstructor
    def field(self):
        return ['id', 'title', 'update_time', 'page_views', 'content', 'sharing_status', 'category']


