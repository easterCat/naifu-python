from flask import Blueprint, render_template

api = Blueprint("api", __name__)

from . import api_translate, database, api_link, reptile, api_template, chitu, api_auth


@api.route("/")
def api_home():
    return render_template("database.html")
