"""
    APIException Class
    继承HTTPException类，重写部分方法，使在请求API时，返回的数据类型未Json
"""

from werkzeug.exceptions import HTTPException
import json


class APIException(HTTPException):
    code = 500
    msg = 'Expected error'

    default = {
        500: 'Expected error'
    }

    def __init__(self, code: int = None, msg: str = None, response=None):
        if code and code in self.default.keys():
            self.code = code
            self.msg = self.default[code]
        if msg:
            self.msg = msg
        self.response = response

        super(APIException, self).__init__(description=msg, response=response)

    def get_body(self, environ=None) -> str:
        """Get the HTML body."""
        body = {
            'code': self.code,
            'msg': self.msg
        }

        return json.dumps(body)

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [("Content-Type", "application/json")]


class Success(APIException):
    """
        Success Class
        API请求成功的状态信息
    """
    code = 200
    msg = 'Request success'

    default = {
        200: 'Request success',
        201: 'The request was successful and the server created a new resource',
        202: 'The server has accepted the request but has not processed it'
    }


class ClientException(APIException):
    """
        ClientException Class
        服务器内部错误
    """
    code = 400
    msg = 'The client request has a syntax error and cannot be understood by the server.'

    default = {
        400: 'The client request has a syntax error and cannot be understood by the server.',
        401: 'Request unauthorized',
        403: 'Request is forbidden',
        404: 'Not Found'
    }


class ServerException(APIException):
    """
        ServerException Class
        服务器内部错误
    """
    code = 500
    msg = 'Server encountered an error'

    default = {
        500: 'Server encountered an error'
    }

