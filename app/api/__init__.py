from flask import Blueprint, render_template
from flask_restx import Api

from app.utils import DeepDanbooru
from .auth import ns as auth_ns
from .chitu import ns as chitu_ns
from .danbooru import ns as danbooru_ns
from .link import ns as link_ns
from .template import ns as template_ns
from .role import ns as role_ns
from .draw import ns as draw_ns

api = Blueprint("api", __name__, url_prefix="/api")

restful_api = Api(
    api,
    version="1.0",
    title="模版项目的API文档",
    description="模版项目的API文档/api/doc",
    doc='/doc'
)

restful_api.add_namespace(auth_ns)
restful_api.add_namespace(chitu_ns)
restful_api.add_namespace(link_ns)
restful_api.add_namespace(template_ns)
restful_api.add_namespace(danbooru_ns)
restful_api.add_namespace(role_ns)
restful_api.add_namespace(draw_ns)

from . import database, reptile, api_template, translate


@api.route("/")
def api_home():
    return render_template("database.html")


@api.route("/danbooru")
def api_danbooru():
    d = DeepDanbooru()
    d.create_dir()
    d.create_file()
    d.download_tags()
    d.download_file()
    return '下载完毕', 200
