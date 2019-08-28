from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import current_app

default_limits = ['2/second', '200/hour', '500/day']


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=default_limits,
)


@limiter.request_filter
def limiter_filter():
    dont_filter = get_remote_address() in (current_app.config.get('WHITE_LIST') or ())
    if not current_app.config['DEBUG'] or dont_filter:
        return True


