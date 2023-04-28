from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restx import Namespace, Resource, reqparse

from app import db
from app.model.role import Role

ns = Namespace("role", description="角色管理")

parser = reqparse.RequestParser()
parser.add_argument("pageIndex", help="当前页数 必填", type=int, default=1, required=True)
parser.add_argument("pageSize", help="每页显示数量 必填", type=int, default=20, required=True)
parser.add_argument(
    "name",
    help="角色名 必填",
    type=str,
    default="",
    required=True,
)
parser.add_argument(
    "role_name",
    help="角色昵称 必填",
    type=str,
    default="",
    required=True,
)


@ns.route("/list")
@ns.doc(
    params={
        "pageIndex": "当前页数",
        "pageSize": "每页显示数量",
    }
)
class RoleResource(Resource):
    @staticmethod
    def get():
        data = parser.parse_args()
        roles = Role.query.paginate(
            page=data["pageIndex"], per_page=data["pageSize"], error_out=False
        )
        total = Role.query.count()
        return jsonify(
            {
                "data": {"roles": [i.to_json() for i in roles], "total": total},
                "msg": "获取角色列表成功",
                "code": 200,
            }
        )

    @staticmethod
    def post():
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        nickname = data["nickname"]
        email = data["email"]

        if User.find_by_username(data["username"]):
            return {
                "data": "",
                "msg": "User {} already exists".format(data["username"]),
                "code": 404,
            }, 200

        new_user = User(
            username=data["username"],
            password=data["password"],
            nickname=data["nickname"],
            email=data["email"],
            password_hash=User.generate_hash(data["password"]),
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(identity=data["username"])
            refresh_token = create_refresh_token(identity=data["username"])

            return {
                "data": {
                    "user": new_user.row2dict(),
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
                "msg": "User {} was created".format(data["username"]),
                "code": 200,
            }, 200
        except Exception as e:
            print(e)
            return {"data": "", "msg": "Something went wrong", "code": 500}, 200
