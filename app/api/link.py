import jsonschema
from flask import request
from app import db
from app.model.link import Link
from app.utils import JsonResponse
from flask_restx import Namespace, reqparse, Resource

ns = Namespace("link", description="收录网站")
parser = reqparse.RequestParser()


@ns.route("/", methods=["GET", "POST", "PUT", "DELETE"])
@ns.doc(
    params={
        "pageIndex": "pageIndex 当前第几页",
        "pageSize": "pageSize 每页多少条数据",
    }
)
class LinkResource(Resource):
    def get(self):
        parser.add_argument(
            "pageIndex",
            help="default value is 1",
            required=False,
            type=int,
            default=1,
        )
        parser.add_argument(
            "pageSize",
            help="default value is 100",
            required=False,
            type=int,
            default=100,
        )
        data = parser.parse_args()
        page_index = data["pageIndex"]
        page_size = data["pageSize"]
        pagination = Link.query.paginate(
            page=page_index, per_page=page_size, error_out=False
        )
        links = pagination.items
        total = Link.query.count()
        return {
            "code": 200,
            "msg": "列表查询成功",
            "data": {
                "list": [link.to_json() for link in links],
                "total": total,
            },
        }

    def post(self):
        parser.add_argument("name", default="", type=str, required=True)
        parser.add_argument("href", default="", type=str, required=True)
        parser.add_argument("type", default="", type=str, required=True)
        parser.add_argument("hot", default=0, type=int, required=True)
        parser.add_argument("icon", default="", type=str, required=False)
        parser.add_argument("desc", default="", type=str, required=False)
        body = parser.parse_args()

        try:
            add_name = body["name"]
            add_href = body["href"]
            add_type = body["type"]
            add_hot = body["hot"]
            add_icon = body["icon"]
            add_desc = body["desc"]
            find_index = Link.query.filter_by(name=add_name).count()
            if find_index > 0:
                return JsonResponse.error({})
            else:
                link_data = Link(
                    name=add_name,
                    href=add_href,
                    link_type=add_type,
                    hot=add_hot,
                    icon=add_icon,
                    desc=add_desc,
                )
                add_one_data(link_data)
                return JsonResponse.success({"add": link_data.to_json()})
        except jsonschema.ValidationError as e:
            return JsonResponse.error({"msg": e.message})

    def put(self):
        parser.add_argument("name", default="", type=str, required=True)
        parser.add_argument("href", default="", type=str, required=True)
        parser.add_argument("type", default="", type=str, required=True)
        parser.add_argument("hot", default=0, type=int, required=True)
        parser.add_argument("icon", default="", type=str, required=False)
        parser.add_argument("desc", default="", type=str, required=False)
        body = parser.parse_args()

        try:
            update_id = body["id"]
            update_name = str(body["name"])
            update_href = str(body["href"])
            update_type = str(body["type"])
            update_hot = body["hot"]

            Link.query.filter_by(id=update_id).update(
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


@ns.route("/<int:id>")
@ns.doc(params={"id": "删除对应id的收录值"})
class SingleLink(Resource):
    def delete(self, id):
        link = Link.query.filter_by(id=id).first()
        if link is None:
            return {"code": 200, "msg": "对应id的网站不存在", "data": ""}
        else:
            db.session.delete(link)
            db.session.commit()
            return {"code": 200, "msg": "成功删除id={}".format(id), "data": ""}


def add_one_data(data):
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
