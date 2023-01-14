from flask_restx import Namespace, reqparse, Resource

from app import db
from app.model.template import TemplateHan
from app.model.user import User
from app.utils import format_datetime

ns = Namespace("template", description="绘图模版")
parser = reqparse.RequestParser()


@ns.route("/favorite/sfw")
@ns.doc(params={"templateId": "收藏的id", "userId": "用户账号id"})
class SingleTemplate(Resource):
    @staticmethod
    def post():
        parser.add_argument("templateId", help="模版的id", type=int)
        parser.add_argument("userId", help="用户的id", type=int)
        body = parser.parse_args()
        user_id = body["userId"]
        template_id = body["templateId"]
        cur_user = User.query.filter_by(id=user_id).first()
        cur_template = TemplateHan.query.filter_by(id=template_id).first().to_json()
        cur_template['create_time'] = format_datetime(cur_template['create_time'])
        cur_template['update_time'] = format_datetime(cur_template['update_time'])

        if cur_user is None:
            return {"code": 500, "msg": "当前用户不存在", "data": ""}, 200

        try:
            if cur_user.is_favorite(template_id):
                cur_user.del_favorite(template_id)
                db.session.commit()
                return {"code": 200, "msg": "取消收藏{}成功".format(template_id), "data": cur_template}, 200
            else:
                cur_user.add_favorite(template_id)
                db.session.commit()
                return {"code": 200, "msg": "收藏{}成功".format(template_id), "data": cur_template}, 200

        except Exception as e:
            print(e)
            return {"code": 500, "msg": "操作失败", "data": ""}, 200
