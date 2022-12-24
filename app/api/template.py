from flask import Blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from flask_restx import Namespace, reqparse, Resource
from app import db, jwt
from app.model.user import User, RevokedTokenModel
from app.model.template import TemplateHan

ns = Namespace("template", description="绘图模版")
parser = reqparse.RequestParser()


@ns.route("/favorite/<int:id>")
@ns.doc(params={"id": "收藏的id", "userId": "用户账号id"})
class SingleTemplate(Resource):
    def post(self, id):
        parser.add_argument("userId", help="用户的id", type=int)
        body = parser.parse_args()
        user_id = body["userId"]
        template = TemplateHan.query.filter_by(id=id).first()
        user = User.query.filter_by(id=user_id).first()

        if template is None:
            return {"code": 200, "msg": "收藏的模版不存在", "data": ""}
        else:
            if user.collected.find(str(id)) == -1:
                if user.collected == "":
                    user.collected = user.collected + str(id)
                else:
                    user.collected = user.collected + "," + str(id)
                db.session.add(user)
                db.session.commit()
                return {"code": 200, "msg": "收藏{}成功".format(id), "data": ""}
            else:
                user.collected.replace(str(id) + ",", "")
                db.session.add(user)
                db.session.commit()
                return {"code": 200, "msg": "取消收藏成功", "data": ""}
