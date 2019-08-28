from flask import render_template

from app.libs.redprint import RedPrint
from app.libs.cahce import cache

views = RedPrint('index', url_prefix='/')


@views.route('/', methods=['GET'])
@views.route('index', methods=['GET'])
@cache.cached(timeout=60*60*24*7, key_prefix='index')
def index():
    return render_template('index.html')



