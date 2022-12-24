import jsonschema
from flask import request
from flask_login import login_user, logout_user, login_required

from app import db
from app.model.user import User
from app.utils import JsonResponse
from . import api


@api.route("/register", methods=["POST", "OPTION"])
def register():
    schema = {
        "type": "object",
        "properties": {
            "username": {"type": "string"},
            "password": {"type": "string"},
            "nickname": {"type": "string"},
            "email": {"type": "string"},
        },
        "required": ["username", "password"],
    }
    req = request.json

    try:
        jsonschema.validate(req, schema)
        add_username = req["username"]
        add_password = req["password"]
        add_nickname = validate_post_json("nickname", req)
        add_email = validate_post_json("email", req)
        find_index = User.query.filter_by(username=add_username).count()
        if find_index > 0:
            return JsonResponse.error({"msg": "username is exist"})
        else:
            user_data = User(
                username=add_username,
                password=add_password,
                nickname=add_nickname,
                email=add_email,
            )
            add_one_data(user_data)
            return JsonResponse.success({"register": user_data.to_json()})
    except jsonschema.ValidationError as e:
        return JsonResponse.error({"msg": e.message})


@api.route("/login", methods=["POST", "OPTION"])
def login():
    schema = {
        "type": "object",
        "properties": {
            "username": {"type": "string"},
            "password": {"type": "string"},
            "nickname": {"type": "string"},
            "email": {"type": "string"},
        },
        "required": ["username", "password"],
    }
    req = request.json

    try:
        jsonschema.validate(req, schema)
        add_username = req["username"]
        add_password = req["password"]
        add_nickname = validate_post_json("nickname", req)
        add_email = validate_post_json("email", req)
        user = User.query.filter_by(username=add_username).first()
        if user is not None and user.verify_password(add_password):
            print("用户" + str(add_username) + "登录成功")
            login_user(user)
        return JsonResponse.success({"login": user.to_json()})
    except jsonschema.ValidationError as e:
        return JsonResponse.error({"msg": e.message})


@api.route("/logout", methods=["GET", "OPTION"])
@login_required
def logout():
    try:
        logout_user()
        return JsonResponse.success({})
    except Exception as e:
        print(e)
        return JsonResponse.error({})


@api.route("/update_user_info", methods=["POST", "OPTION"])
@login_required
def update_user_info():
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "href": {"type": "string"},
            "type": {"type": "string"},
            "hot": {"type": "boolean"},
            "icon": {"type": "string"},
            "desc": {"type": "string"},
        },
        "required": ["name", "href", "type", "hot"],
    }
    req = request.json

    try:
        jsonschema.validate(req, schema)
        update_id = req["id"]
        update_name = str(req["name"])
        update_href = str(req["href"])
        update_type = str(req["type"])
        update_hot = req["hot"]
        User.query.filter_by(id=update_id).update(
            {
                "name": update_name,
                "href": update_href,
                "link_type": update_type,
                "hot": update_hot,
            }
        )
        db.session.commit()
        return JsonResponse.success({"update": "更新成功"})
    except jsonschema.ValidationError as e:
        return JsonResponse.error({"msg": e.message})


@api.route("/delete_user", methods=["POST", "OPTION"])
def delete_user():
    req = request.get_json()
    delete_id = req["id"]
    User.query.filter_by(id=delete_id).delete()
    db.session.commit()
    return JsonResponse.success({"delete": "删除" + str(delete_id) + "成功"})


def add_one_data(data):
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


def validate_post_json(validata_key, validata_dict):
    if validata_key in validata_dict:
        result = str(validata_dict[validata_key])
    else:
        result = ""
    return result
