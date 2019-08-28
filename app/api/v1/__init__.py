from flask import Blueprint

from . import article, category, manager


def create_blueprint() -> Blueprint:
    blueprint = Blueprint('v1', __name__, url_prefix='/v1')

    article.api.register(blueprint)
    category.api.register(blueprint)
    manager.api.register(blueprint)

    return blueprint


v1_bp = create_blueprint()



