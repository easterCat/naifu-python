import jsonschema
from flask_restx import Namespace, reqparse, Resource

from app import db
from app.model.link import Link
from app.utils import JsonResponse

ns = Namespace("link", description="收录网站")
parser = reqparse.RequestParser()
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


@ns.route("/list", methods=["GET", "POST", "PUT", "DELETE"])
@ns.doc(
    params={
        "pageIndex": "pageIndex 当前第几页",
        "pageSize": "pageSize 每页多少条数据",
    }
)
class LinkResource(Resource):
    @staticmethod
    def get():

        parser.add_argument("pageIndex", default=1, type=int, required=True)
        parser.add_argument("pageSize", default=100, type=int, required=True)
        params = parser.parse_args()
        page_index = params['pageIndex']
        page_size = params['pageSize']
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
        }, 200

    @staticmethod
    def post():
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

    @staticmethod
    def put():
        parser.add_argument("id", type=int, required=True)
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
            return {"code": 200, "msg": "更新id={}成功".format(update_id), "data": ""}, 200
        except jsonschema.ValidationError as e:
            return {"code": 500, "msg": "更新失败", "data": ""}, 200

    @staticmethod
    def delete():
        parser.add_argument("id", help="删除的id", type=int, required=True)
        body = parser.parse_args()
        link_id = body["id"]
        cur_link = Link.query.filter_by(id=link_id).first()
        if cur_link is None:
            return {"code": 500, "msg": "对应id的网站不存在", "data": ""}, 200
        else:
            db.session.delete(cur_link)
            db.session.commit()
            return {"code": 200, "msg": "成功删除id={}".format(link_id), "data": ""}, 200


def add_one_data(data):
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
