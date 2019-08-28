from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import reconstructor
import time

from .base import Base


class Category(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

    def __init__(self):
        self.id = time.time().__int__()

    @property
    @reconstructor
    def field(self):
        return ['id', 'name']


