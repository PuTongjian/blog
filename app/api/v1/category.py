from flask import jsonify
from flask_login import login_required

from app.libs.redprint import RedPrint
from app.libs.limiter import limiter
from app.libs.api_exceptions import Success
from app.validators import CategoryValidator
from app.models import db, Category, Article


api = RedPrint('category')


@api.route('', methods=['POST'])
@limiter.limit('1/second')
@login_required
def create_category():
    """
        API描述
        Url： POST /v1/category
        描述：根据名称创建一个模块
        :param
        {'name': ''}
        :return
        {'id': '', 'name': ''}
    """
    validate = CategoryValidator().validate_for_api()
    with db.auto_commit():
        category = Category()
        category.name = validate.name.data
        db.session.add(category)
    return jsonify(category)


@api.route('/name', methods=['POST'])
@limiter.limit('1/second')
@login_required
def rename_category():
    """
        API描述
        Url： POST /v1/category/name
        描述：更改某一模块的标题
        :param
        {'id': '', 'name': ''}
        :return
        {'code': '', msg: ''}
    """
    validate = CategoryValidator().validate_for_api()
    category = Category.query.filter_by(id=validate.id.data).first_or_404()
    with db.auto_commit():
        category.name = validate.name.data
    return Success()


@api.route('', methods=['GET'])
def get_category():
    """
        API描述
        Url： GET /v1/category
        描述：获取所有模块
        :param
        {}
        :return
        [{id: '', name: ''}]
    """
    category = Category.query.filter_by().all()
    return jsonify(category)


@api.route('', methods=['DELETE'])
@limiter.limit('1/second')
@login_required
def delete_category():
    """
        API描述
        Url： DELETE /v1/category
        描述：删除某一模块，并删除该模块下的所有文章
        :param
        {'id': ''}
        :return
        {'code': '', msg: ''}
    """
    validate = CategoryValidator().validate_for_api()
    category = Category.query.filter_by(id=validate.id.data).first_or_404()
    with db.auto_commit():
        category.delete()
        Article.query.filter_by(category_id=category.id).update({Article.status: 0})
    return Success()
