from flask import Blueprint

from . import article, manager, index


def create_blueprint() -> Blueprint:
    blueprint = Blueprint('views', __name__)

    index.views.register(blueprint)
    manager.views.register(blueprint)
    article.views.register(blueprint)

    return blueprint


view_bp = create_blueprint()
