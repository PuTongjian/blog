from app import create_app
from app.libs.api_exceptions import APIException, HTTPException
from werkzeug.exceptions import NotFound


app = create_app()


@app.errorhandler(Exception)
def handle_error(err):
    if isinstance(err, APIException):
        return err
    if isinstance(err, HTTPException):
        return NotFound()
    else:
        return APIException()


if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'], threaded=app.config['THREAD'])
