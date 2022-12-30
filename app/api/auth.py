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

ns = Namespace("auth", description="账号管理")
parser = reqparse.RequestParser()


@ns.route("/registration")
@ns.doc(
    params={
        "username": "用户名",
        "password": "密码",
        "nickname": "",
        "email": "",
    }
)
class UserRegistration(Resource):
    def post(self):
        parser.add_argument(
            "username",
            help="用户名 必填",
            type=str,
            default="",
            required=True,
        )
        parser.add_argument(
            "password",
            help="密码 必填",
            type=str,
            default="",
            required=True,
        )
        parser.add_argument(
            "nickname",
            help="昵称 非必填",
            type=str,
            default="",
            required=False,
        )
        parser.add_argument(
            "email",
            help="邮箱 非必填",
            type=str,
            default="",
            required=False,
        )
        data = parser.parse_args()

        if User.find_by_username(data["username"]):
            return {
                "data": "",
                "msg": "User {} already exists".format(data["username"]),
                "code": 200,
            }

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
            }
        except Exception as e:
            print(e)
            return {"data": "", "msg": "Something went wrong", "code": 500}, 200


@ns.route("/login")
class UserLogin(Resource):
    def post(self):
        parser.add_argument(
            "username", help="username field cannot be blank", required=True
        )
        parser.add_argument(
            "password", help="password field cannot be blank", required=True
        )
        parser.add_argument(
            "nickname", help="nickname field cannot be blank", required=False
        )
        parser.add_argument("email", help="email field cannot be blank", required=False)
        data = parser.parse_args()
        current_user = User.find_by_username(data["username"])

        if not current_user:
            return {"data": "", "msg": "用户{}不存在".format(data["username"]), "code": 500}, 200

        if User.verify_hash(data["password"], current_user.password_hash):
            access_token = create_access_token(identity=data["username"])
            refresh_token = create_refresh_token(identity=data["username"])
            return {
                "data": {
                    "user": current_user.row2dict(),
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
                "msg": "Logged in as {}".format(current_user.username),
                "code": 200,
            }
        else:
            return {"data": "", "msg": "错误令牌", "code": 500}, 200


@ns.route("/logout/access")
class UserLogoutAccess(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {"code": 200, "msg": "访问令牌已被撤销", "data": ""}, 200
        except:
            return {"code": 500, "msg": "出问题了", "data": ""}, 200


@ns.route("/logout/refresh")
class UserLogoutRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        jti = get_jwt()["jti"]
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {"code": 200, "msg": "刷新令牌已被撤销", "data": ""}, 200
        except:
            return {"code": 500, "msg": "出问题了", "data": ""}, 200


@ns.route("/token/refresh")
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {
            "code": 200,
            "msg": "access_token已更新",
            "data": {"access_token": access_token},
        }, 200


@ns.route("/users")
class AllUsers(Resource):
    def get(self):
        return User.return_all()

    def delete(self):
        return User.delete_all()


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, decrypted_token):
    jti = decrypted_token["jti"]
    return RevokedTokenModel.is_jti_blacklisted(jti)


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return {"code": 20001, "msg": "access_token已过期", "data": ""}, 200


@jwt.unauthorized_loader
def my_unauthorized_token_callback(jwt_header):
    return {"code": 20002, "msg": "缺少必要Authorization请求头", "data": ""}, 200


@jwt.revoked_token_loader
def my_revoked_token_callback(jwt_header, jwt_payload):
    return {"code": 20003, "msg": "令牌已被撤销", "data": ""}, 200
