from flask import Flask as _Flask
from json import JSONEncoder as _JSONEncoder, loads

from app.libs.api_exceptions import ServerException


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, str):
            return loads(o)
        raise ServerException()


class Flask(_Flask):
    json_encoder = JSONEncoder


