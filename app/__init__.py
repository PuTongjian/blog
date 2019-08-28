from app.models import db, login_manager
from app.api.v1 import v1_bp
from app.views import view_bp
from app.app import Flask
from app.libs.cahce import cache
from app.libs.limiter import limiter


def register_blueprint(app: Flask):
    app.register_blueprint(v1_bp)
    app.register_blueprint(view_bp)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('app.config.settings')
    app.config.from_object('app.config.secure')

    login_manager.init_app(app=app)
    login_manager.login_view = 'views.login'
    login_manager.login_message = '请登录'

    db.init_app(app=app)
    db.create_all(app=app)

    cache.init_app(app=app, config={'CACHE_TYPE': 'simple'})
    limiter.init_app(app=app)

    register_blueprint(app=app)

    return app
