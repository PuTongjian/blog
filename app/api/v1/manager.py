from flask_login import login_required

from app.libs.redprint import RedPrint
from app.validators import ManagerValidator
from app.models import Manager, db
from app.libs.api_exceptions import Success


api = RedPrint('manager')


@api.route('/authorization', methods=['POST'])
def authorization():
    """
        API描述
        Url： POST /v1/manager/authorization
        描述：根据名称创建一个模块
        :param
        {'email': '', 'password': '', 'nickname': '', authorization_code: ''}
        :return
        {'code': '', msg: ''}
    """
    validator = ManagerValidator().validate_for_api()

    with db.auto_commit():
        manager = Manager.register(**validator.data)
        db.session.add(manager)

    return Success(201)


@api.route('/is_active', methods=['POST'])
@login_required
def is_active():
    """
        API描述
        Url： POST /v1/manager/is_active
        描述：判断用户是否登录
        :param
        {}
        :return
        {}
    """
    return Success()



