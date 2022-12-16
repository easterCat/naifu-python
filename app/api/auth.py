from flask import Blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from flask_restful import Api, Resource, reqparse

from app import db, jwt
from app.model.user import User, RevokedTokenModel

bp = Blueprint("auth", __name__)
restful_api = Api(bp)
parser = reqparse.RequestParser()


class UserRegistration(Resource):
    def post(self):
        parser.add_argument(
            "username", help="This field cannot be blank", required=True
        )
        parser.add_argument(
            "password", help="This field cannot be blank", required=True
        )
        parser.add_argument(
            "nickname", help="This field cannot be blank", required=False
        )
        parser.add_argument("email", help="This field cannot be blank", required=False)
        data = parser.parse_args()

        if User.find_by_username(data["username"]):
            return {"message": "User {} already exists".format(data["username"])}

        new_user = User(
            username=data["username"],
            password=data["password"],
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
        except:
            return {"data": "", "msg": "Something went wrong", "code": 500}, 500


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
            return {"message": "User {} does't exist".format(data["username"])}

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
            return {"data": "", "msg": "错误令牌", "code": 500}, 500


class UserLogoutAccess(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {"code": 200, "msg": "访问令牌已被撤销", "data": ""}
        except:
            return {"code": 500, "msg": "出问题了", "data": ""}, 500


class UserLogoutRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        jti = get_jwt()["jti"]
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {"message": "刷新令牌已被撤销"}
        except:
            return {"message": "出问题了"}, 500


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {
            "code": 200,
            "msg": "access_token已更新",
            "data": {"access_token": access_token},
        }


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


restful_api.add_resource(UserRegistration, "/api/auth/registration")
restful_api.add_resource(UserLogin, "/api/auth/login")
restful_api.add_resource(UserLogoutAccess, "/api/auth/logout/access")
restful_api.add_resource(UserLogoutRefresh, "/api/auth/logout/refresh")
restful_api.add_resource(TokenRefresh, "/api/auth/token/refresh")
restful_api.add_resource(AllUsers, "/api/auth/users")
