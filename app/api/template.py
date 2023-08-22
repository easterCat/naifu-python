import uuid

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, reqparse, Resource
from loguru import logger

from app import db
from app.model.template import TemplateHan, TemplatePersonal
from app.model.user import User
from app.utils import format_datetime

ns = Namespace("template", description="绘图模版")
parser = reqparse.RequestParser()


@ns.route("/favorite/sfw")
@ns.doc(params={"templateId": "收藏的id", "userId": "用户账号id"})
class SingleTemplate(Resource):
    @staticmethod
    @jwt_required()
    def post():
        parser.add_argument("templateId", help="模版的id", type=int)
        parser.add_argument("userId", help="用户的id", type=int)
        body = parser.parse_args()
        user_id = body["userId"]
        template_id = body["templateId"]

        cur_user = User.query.filter_by(id=user_id).first()
        if cur_user is None:
            return {"code": 500, "msg": "当前用户不存在", "data": ""}, 200

        cur_template = TemplateHan.query.filter_by(id=template_id).first()
        if cur_template is None:
            return {"code": 500, "msg": "模版不存在", "data": ""}, 200

        cur_template_json = format_template(cur_template.to_json())

        try:
            if cur_user.is_favorite(template_id):
                cur_user.del_favorite(template_id)
                db.session.commit()
                return {
                    "code": 200,
                    "msg": f"取消收藏{template_id}成功",
                    "data": cur_template_json,
                }, 200
            else:
                cur_user.add_favorite(template_id)
                db.session.commit()
                return {
                    "code": 200,
                    "msg": f"收藏{template_id}成功",
                    "data": cur_template_json,
                }, 200

        except Exception as e:
            logger.error(e)
            return {"code": 500, "msg": "操作失败", "data": ""}, 200


def format_template(template_json):
    template_json["create_time"] = format_datetime(template_json["create_time"])
    template_json["update_time"] = format_datetime(template_json["update_time"])
    return template_json


@ns.route("/personal")
class PersonalTemplate(Resource):
    @staticmethod
    @jwt_required()
    def post():
        parser.add_argument("prompt", help="模版的标签", type=str)
        parser.add_argument("n_prompt", help="模版的负面标签", type=str)
        parser.add_argument("size", help="模版的大小", type=str)
        parser.add_argument("scale", help="模版的扩散值", type=str)
        parser.add_argument("sampler", help="模版的渲染器", type=str)
        parser.add_argument("step", help="模版的步数", type=str)
        parser.add_argument("images", help="模版的预览图", type=str)

        body = parser.parse_args()
        image_list = body["images"].split(",")
        current_username = get_jwt_identity()
        current_user = User.query.filter_by(username=current_username).first()
        name = uuid.uuid4()

        try:
            new_tem = TemplatePersonal(
                name=name,
                author=current_username,
                prompt=body["prompt"],
                n_prompt=body["n_prompt"],
                size=body["size"],
                scale=body["scale"],
                sampler=body["sampler"],
                step=body["step"],
                images=body["images"],
                min_imgbb_url=image_list[0],
                imgbb_url=image_list[0],
            )
            db.session.add(new_tem)
            db.session.commit()
            current_user.add_template(name)
            new_tem_json = new_tem.to_json()
            return {"code": 200, "msg": "发布成功", "data": {"add": new_tem_json}}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(e)
            return {"code": 500, "msg": "发布失败", "data": ""}, 200


@ns.route("/han")
class HanTemplate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("pageIndex", help="当前页数", type=int, default=1)
    parser.add_argument("pageSize", help="每页数据数", type=int, default=10)
    parser.add_argument("searchTag", help="搜索关键词", type=str)

    def get(self):
        args = self.parser.parse_args()
        page_size = args.get("pageSize", 10)
        page_index = args.get("pageIndex", 1)
        search_tag = args.get("searchTag", "")

        query = TemplateHan.query

        if search_tag is not None:
            query = query.filter(TemplateHan.prompt.contains(search_tag))

        try:
            pagination = query.order_by(TemplateHan.id.desc()).paginate(
                page=page_index, per_page=page_size, error_out=False
            )
            total = query.count()
            templates = pagination.items

            return {
                "code": 200,
                "msg": "数据查询成功",
                "data": {
                    "list": [template.to_json() for template in templates],
                    "total": total,
                },
            }, 200
        except Exception as e:
            logger.error("查询出现异常 ==>", e)
            return {"code": 500, "msg": "查询出现异常", "data": ""}, 200
