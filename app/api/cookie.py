from flask import make_response, request
from . import api

@api.route("/set_cookies")
def set_cookie():
    resp = make_response("success")
    resp.set_cookie("w3cshool", "w3cshool", max_age=3600)
    return resp

@api.route("/get_cookies")
def get_cookie():
    cookie_1 = request.cookies.get("w3cshool")
    return cookie_1

@api.route("/delete_cookies")
def delete_cookie():
    resp = make_response("del success")
    resp.delete_cookie("w3cshool")
    return resp
