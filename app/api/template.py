from flask import request, make_response
from . import api
from app.utils import JsonRep
from app.models import Template
from app import db


@api.route("/set_ip", methods=['GET', 'OPTION'])
def set_ip():
    ip = request.remote_addr
    res = make_response('success')
    res.set_cookie('ip', ip)
    return JsonRep.success({
        'ip': ip
    })


@api.route("/get_templates", methods=['GET', 'OPTION'])
async def get_templates():
    ip = request.remote_addr
    page_index = request.args.get('pageIndex', 1, type=int)
    page_size = request.args.get('pageSize', 100, type=int)

    try:
        pagination = Template.query.paginate(page=page_index, per_page=page_size, error_out=False)
        total = Template.query.count()
        templates = pagination.items
    except Exception as e:
        print('查询出现异常 ==>', e)
        return JsonRep.error({})

    return JsonRep.success({
        'list': [i.to_json() for i in templates],
        'total': total,
    })


@api.route("/add_template", methods=['POST', 'OPTION'])
def add_template():
    req = request.get_json()
    add_name = str(req['name'])
    add_href = str(req['href'])
    add_type = str(req['type'])
    add_hot = req['hot']
    find_index = Template.query.filter_by(name=add_name).count()
    if find_index > 0:
        return JsonRep.error({})
    else:
        template_data = Template(name=add_name)
        add_one_data(template_data)
        return JsonRep.success({
            'add': template_data.to_json()
        })


@api.route("/update_template", methods=['POST', 'OPTION'])
def update_template():
    req = request.get_json()
    update_id = req['id']
    update_name = str(req['name'])
    update_href = str(req['href'])
    update_type = str(req['type'])
    update_hot = req['hot']
    update_data = Template.query.filter_by(id=update_id).update({
        'name': update_name,
        'href': update_href,
        'template_type': update_type,
        'hot': update_hot
    })
    db.session.commit()
    return JsonRep.success({
        'update': '更新成功'
    })


@api.route("/delete_template", methods=['POST', 'OPTION'])
def delete_template():
    req = request.get_json()
    delete_id = req['id']
    delete_data = Template.query.filter_by(id=delete_id).delete()
    db.session.commit()
    return JsonRep.success({
        'delete': '删除' + str(delete_id) + '成功'
    })


@api.route("/like_template_by_id", methods=['POST', 'OPTION'])
def like_template_by_id():
    ip = request.remote_addr
    req = request.get_json()
    like_id = req['id']
    like_data = Template.query.filter_by(id=like_id).first()
    address = like_data.like_address
    if address.find(str(ip)) == -1:
        if address == '':
            like_data.like_address = '' + ip
        else:
            like_data.like_address = like_data.like_address + ',' + ip
        like_data.like = like_data.like + 1
        db.session.commit()
        return JsonRep.success({
            'like': '喜爱' + str(like_id) + '成功'
        })
    else:
        return JsonRep.success({
            'like': '已添加喜爱'
        })


def add_one_data(data):
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
