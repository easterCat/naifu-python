from flask import request, make_response

from app import db
from app.model.template import TemplateHan, TemplateChitu, TemplateNoval
from app.utils import JsonResponse
from . import api


@api.route("/set_ip", methods=["GET", "OPTION"])
def set_ip():
    ip = request.remote_addr
    res = make_response("success")
    res.set_cookie("ip", ip)
    return JsonResponse.success({"ip": ip})


@api.route("/get_templates", methods=["GET", "OPTION"])
async def get_templates():
    page_index = request.args.get("pageIndex", 1, type=int)
    page_size = request.args.get("pageSize", 50, type=int)
    search_tag = request.args.get("searchTag")

    query = TemplateHan.query
    if search_tag is not None:
        query = query.filter(TemplateHan.prompt.contains(search_tag))

    try:
        pagination = query.order_by(TemplateHan.id.desc()).paginate(
            page=page_index, per_page=page_size, error_out=False
        )
        total = query.count()
        templates = pagination.items

    except Exception as e:
        print("查询出现异常 ==>", e)
        return JsonResponse.error({})

    return JsonResponse.success(
        {
            "list": [i.to_json() for i in templates],
            "total": total,
        }
    )


@api.route("/get_templates_noval", methods=["GET", "OPTION"])
async def get_templates_noval():
    page_index = request.args.get("pageIndex", 1, type=int)
    page_size = request.args.get("pageSize", 50, type=int)
    query = TemplateNoval.query
    try:
        pagination = query.paginate(
            page=page_index, per_page=page_size, error_out=False
        )
        total = query.count()
        templates = pagination.items
    except Exception as e:
        print("查询出现异常 ==>", e)
        return JsonResponse.error({})
    return JsonResponse.success(
        {
            "list": [i.to_json() for i in templates],
            "total": total,
        }
    )


@api.route("/get_templates_chitu", methods=["GET", "OPTION"])
async def get_templates_chitu():
    page_index = request.args.get("pageIndex", 1, type=int)
    page_size = request.args.get("pageSize", 100, type=int)
    query = TemplateChitu.query
    try:
        pagination = query.paginate(
            page=page_index, per_page=page_size, error_out=False
        )
        total = query.count()
        templates = pagination.items
    except Exception as e:
        print("查询出现异常 ==>", e)
        return JsonResponse.error({})

    return JsonResponse.success(
        {
            "list": [i.to_json() for i in templates],
            "total": total,
        }
    )


@api.route("/add_template", methods=["POST", "OPTION"])
def add_template():
    req = request.get_json()
    add_name = str(req["name"])
    add_href = str(req["href"])
    add_type = str(req["type"])
    add_hot = req["hot"]
    find_index = TemplateHan.query.filter_by(name=add_name).count()
    if find_index > 0:
        return JsonResponse.error({})
    else:
        template_data = TemplateHan(name=add_name)
        db.session.add(template_data)
        db.session.commit()
        return JsonResponse.success({"add": template_data.to_json()})


@api.route("/update_template", methods=["POST", "OPTION"])
def update_template():
    req = request.get_json()
    update_id = req["id"]
    update_name = str(req["name"])
    update_href = str(req["href"])
    update_type = str(req["type"])
    update_hot = req["hot"]
    TemplateHan.query.filter_by(id=update_id).update(
        {
            "name": update_name,
            "href": update_href,
            "template_type": update_type,
            "hot": update_hot,
        }
    )
    db.session.commit()
    return JsonResponse.success({"update": "更新成功"})


@api.route("/delete_template", methods=["POST", "OPTION"])
def delete_template():
    req = request.get_json()
    delete_id = req["id"]
    delete_data = TemplateHan.query.filter_by(id=delete_id).delete()
    db.session.commit()
    return JsonResponse.success({"delete": "删除" + str(delete_id) + "成功"})


@api.route("/like_template_by_id", methods=["POST", "OPTION"])
def like_template_by_id():
    ip = request.remote_addr
    req = request.get_json()
    like_id = req["id"]
    like_data = TemplateHan.query.filter_by(id=like_id).first()
    # address = like_data.like_address
    # if address.find(str(ip)) == -1:
    #     if address == "":
    #         like_data.like_address = "" + ip
    #     else:
    #         like_data.like_address = like_data.like_address + "," + ip
    #     like_data.like = like_data.like + 1
    #     db.session.commit()
    #     return JsonResponse.success({"like": "喜爱" + str(like_id) + "成功"})
    # else:
    #     return JsonResponse.success({"like": "已添加喜爱"})
