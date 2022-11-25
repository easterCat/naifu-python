from flask import request
from . import api
from app.utils import JsonRep
from app.models import Link
from app import db


@api.route("/get_links", methods=['GET', 'OPTION'])
async def get_links():
    page_index = request.args.get('pageIndex', 1, type=int)
    page_size = request.args.get('pageSize', 100, type=int)

    try:
        pagination = Link.query.paginate(page=page_index, per_page=page_size, error_out=False)
        total = Link.query.count()
    except Link.DoesNotExist:
        return JsonRep.error({})

    links = pagination.items
    return JsonRep.success({
        'list': [link.to_json() for link in links],
        'total': total,
    })


@api.route("/add_link", methods=['POST', 'OPTION'])
def add_link():
    req = request.get_json()
    add_name = str(req['name'])
    add_href = str(req['href'])
    add_type = str(req['type'])
    add_hot = req['hot']
    find_index = Link.query.filter_by(name=add_name).count()
    if find_index > 0:
        return JsonRep.error({})
    else:
        link_data = Link(name=add_name, href=add_href, link_type=add_type, hot=add_hot)
        add_one_data(link_data)
        return JsonRep.success({
            'add': link_data.to_json()
        })


@api.route("/update_link", methods=['POST', 'OPTION'])
def update_link():
    req = request.get_json()
    update_id = req['id']
    update_name = str(req['name'])
    update_href = str(req['href'])
    update_type = str(req['type'])
    update_hot = req['hot']
    update_data = Link.query.filter_by(id=update_id).update({
        'name': update_name,
        'href': update_href,
        'link_type': update_type,
        'hot': update_hot
    })
    db.session.commit()
    return JsonRep.success({
        'update': '更新成功'
    })


@api.route("/delete_link", methods=['POST', 'OPTION'])
def delete_link():
    req = request.get_json()
    delete_id = req['id']
    delete_data = Link.query.filter_by(id=delete_id).delete()
    db.session.commit()
    return JsonRep.success({
        'delete': '删除' + str(delete_id) + '成功'
    })


def add_one_data(data):
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
