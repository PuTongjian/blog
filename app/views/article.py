from flask import render_template
from flask_login import login_required

from app.libs.redprint import RedPrint
from app.libs.cahce import cache
from app.models import Article
from app.view_models import ArticleViewModel

views = RedPrint('article')


@views.route('', methods=['GET'])
@cache.cached(timeout=60*60*24*7, key_prefix='article')
def article():
    return render_template('article.html')


@views.route('/detail/<int:article_id>', methods=['GET'])
@cache.cached(timeout=60*10, key_prefix='article_detail')
def article_detail(article_id):
    article = Article.query.filter_by(id=article_id).first_or_404()
    article.increase_page_views()
    article_view_model = ArticleViewModel(dict(article), 101)
    return render_template('article_detail.html', article=article_view_model)


@views.route('/writer', methods=['GET'])
@login_required
@cache.cached(timeout=60*60*24*7, key_prefix='article_editor')
def article_editor():
    return render_template('article_editor.html')
