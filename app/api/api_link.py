import jsonschema
from flask import request

from app import db
from app.model.link import Link
from app.utils import JsonResponse
from . import api


@api.route("/get_links", methods=['GET', 'OPTION'])
def get_links():
    """添加收录网址
    添加收录网址
    ---
    definitions:
      pageIndex:
        type: int
      pageSize:
        type: int
    responses:
      200:
        description: Add link success
        schema:
          $ref: '#/definitions/pageIndex'
          $ref: '#/definitions/pageSize'
        examples:
          rgb: ['red', 'green', 'blue']
    """
    try:
        page_index = request.args.get('pageIndex', 1, type=int)
        page_size = request.args.get('pageSize', 100, type=int)
        pagination = Link.query.paginate(page=page_index, per_page=page_size, error_out=False)
        links = pagination.items
        total = Link.query.count()
        return JsonResponse.success({
            'list': [link.to_json() for link in links],
            'total': total,
        })
    except Link.DoesNotExist:
        return JsonResponse.error({})


@api.route("/add_link", methods=['POST', 'OPTION'])
def add_link():
    schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'href': {'type': 'string'},
            'type': {'type': 'string'},
            'hot': {'type': 'boolean'},
            'icon': {'type': 'string'},
            'desc': {'type': 'string'},
        },
        'required': ['name', 'href', 'type', 'hot']
    }
    req = request.json

    try:
        jsonschema.validate(req, schema)
        add_name = req['name']
        add_href = req['href']
        add_type = req['type']
        add_hot = req['hot']
        add_icon = validate_post_json('icon', req)
        add_desc = validate_post_json('desc', req)
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
                desc=add_desc
            )
            add_one_data(link_data)
            return JsonResponse.success({
                'add': link_data.to_json()
            })
    except jsonschema.ValidationError as e:
        return JsonResponse.error({'msg': e.message})


def validate_post_json(validata_key, validata_dict):
    if validata_key in validata_dict:
        result = str(validata_dict[validata_key])
    else:
        result = ''
    return result


@api.route("/update_link", methods=['POST', 'OPTION'])
def update_link():
    schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'href': {'type': 'string'},
            'type': {'type': 'string'},
            'hot': {'type': 'boolean'},
            'icon': {'type': 'string'},
            'desc': {'type': 'string'},
        },
        'required': ['name', 'href', 'type', 'hot']
    }
    req = request.json

    try:
        jsonschema.validate(req, schema)
        update_id = req['id']
        update_name = str(req['name'])
        update_href = str(req['href'])
        update_type = str(req['type'])
        update_hot = req['hot']
        Link.query.filter_by(id=update_id).update({
            'name': update_name,
            'href': update_href,
            'link_type': update_type,
            'hot': update_hot
        })
        db.session.commit()
        return JsonResponse.success({
            'update': '更新成功'
        })
    except jsonschema.ValidationError as e:
        return JsonResponse.error({'msg': e.message})


@api.route("/delete_link", methods=['POST', 'OPTION'])
def delete_link():
    req = request.get_json()
    delete_id = req['id']
    Link.query.filter_by(id=delete_id).delete()
    db.session.commit()
    return JsonResponse.success({
        'delete': '删除' + str(delete_id) + '成功'
    })


def add_one_data(data):
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
