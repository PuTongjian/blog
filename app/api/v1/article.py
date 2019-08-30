from flask import jsonify, request
from flask_login import login_required
import requests
import json

from app.libs.redprint import RedPrint
from app.libs.cahce import cache
from app.libs.limiter import limiter
from app.libs.api_exceptions import Success, ServerException
from app.models import db, Article
from app.validators import ArticleValidator
from app.view_models import ArticleViewModel, ArticleViewModelCollection


api = RedPrint('article')


@api.route('', methods=['POST'])
@limiter.limit('1/second')
@login_required
def create_article():
    """
        API描述
        Url： POST /v1/article
        描述：创建一篇文章
        :param
        {'category_id': '', 'title': ''}
        :return
        {'id': '', 'title': '', 'category_id': '', 'sharing_status': ''}
    """
    validate = ArticleValidator.create_validator(200).validate_for_api()
    with db.auto_commit():
        article = Article()
        article.set_attrs(**validate.data)
        db.session.add(article)

    article_view_model = ArticleViewModel(model=dict(article), opera_code=200)
    return jsonify(article_view_model)


@api.route('/category', methods=['POST'])
@login_required
def alter_article_category():
    """
        API描述
        Url： POST /v1/article/type
        描述：更改文章所属的模块
        :param
        {'id': '', 'category_id': ''}
        :return
        {'code': '', 'msg': ''}
    """
    validate = ArticleValidator.create_validator(201).validate_for_api()
    with db.auto_commit():
        article = Article.query.filter_by(id=validate.id.data).first_or_404()
        article.category_id = validate.category_id.data

    return Success()


@api.route('/share', methods=['POST'])
@login_required
def alter_article_sharing_status():
    """
        API描述
        Url： POST /v1/article/share
        描述：更改文章的发布状态
        :param
        {'id': '', 'sharing_status': ''}
        :return
        {'code': '', 'msg': ''}
    """
    validator = ArticleValidator.create_validator(203).validate_for_api()
    with db.auto_commit():
        article = Article.query.filter_by(id=validator.id.data).first_or_404()
        article.sharing_status = validator.sharing_status.data

    return Success()


@api.route('/content', methods=['POST'])
@login_required
def update_article_content():
    """
        API描述
        Url： POST /v1/article/content
        描述：更新文章的内容
        :param
        {'id': '', 'title': '', 'content': ''}
        :return
        {'code': '', 'msg': ''}
    """
    validator = ArticleValidator.create_validator(202).validate_for_api()
    with db.auto_commit():
        article = Article.query.filter_by(id=validator.id.data).first_or_404()
        article.title = validator.title.data
        article.content = validator.content.data
        article.get_current_time()

    return Success()


@api.route('/upload_images', methods=['POST'])
@login_required
def upload_images():
    """
        API描述
        Url： POST /v1/article/upload_images
        描述：上传图片 请求第三方接口
        :param
        {'upload_images': ''}
        :return
        {'image_url'}
    """
    resp = requests.post('http://47.103.198.17/upload/upload_images', data={'image': request.data})
    text = json.loads(resp.text)
    return jsonify(text) if resp.status_code == 200 else ServerException()


@api.route('/content/html', methods=['POST'])
def get_article_html_content():
    """
        API描述
        Url： GET /v1/article/content/html
        描述：将markdown文章转化为html
        :param
        {'content': ''}
        :return
        {'html_content':''}
    """
    validator = ArticleValidator.create_validator(104).validate_for_api()
    article = Article()
    article.content = validator.content.data
    article_view = ArticleViewModel(article, 104)
    return jsonify(article_view)


@api.route('', methods=['GET'])
def get_article():
    """
        API描述
        Url： GET /v1/article
        描述：获取文章
        :param
        {'page': '', 'num': '','category_id': ''}
        :return
        {'id': '', 'title': '', 'category_name': '', 'update_time': '', 'page_views': ''}
    """
    validator = ArticleValidator.create_validator(100).validate_for_api()
    data = cache.get(validator.key)
    if data:
        return jsonify(data)

    articles = Article.get_articles_with_paging(validator.page.data, validator.num.data, validator.category_id.data)
    article_collection = ArticleViewModelCollection()
    article_collection.fill(articles.items, 100)
    cache.set(validator.key, article_collection, 60*10)
    return jsonify(article_collection)


@api.route('/all', methods=['GET'])
@login_required
def get_all_article():
    """
        API描述
        Url： GET /v1/article/all
        描述：获取某一模块的全部文章
        :param
        {'category_id': ''}
        :return
        {'id': '', 'title': '', 'category_id', 'sharing_status': ''}
    """
    validator = ArticleValidator.create_validator(102).validate_for_api()

    articles = Article.get_articles_with_category(validator.category_id.data)
    article_collection = ArticleViewModelCollection()
    article_collection.fill(articles, 102)
    return jsonify(article_collection)


@api.route('/content', methods=['GET'])
@login_required
def get_article_content():
    """
        API描述
        Url： GET /v1/article/content
        描述：获取某一文章的内容
        :param
        {'id': ''}
        :return
        {content:''}
    """
    validator = ArticleValidator.create_validator(103).validate_for_api()
    article = Article.query.filter_by(id=validator.id.data).first_or_404()
    article_view = ArticleViewModel(dict(article), 103)
    return jsonify(article_view)


@api.route('', methods=['DELETE'])
@limiter.limit('1/second')
@login_required
def delete_article():
    """
        API描述
        Url： DELETE /v1/article
        描述：删除某一文章
        :param
        {'id': ''}
        :return
        {'code': '', 'msg': ''}
    """
    validator = ArticleValidator.create_validator(300).validate_for_api()
    with db.auto_commit():
        article = Article.query.filter_by(id=validator.id.data).first_or_404()
        article.delete()

    return Success()

