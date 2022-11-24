import json
import os
from . import api
from app import db
from app.models import Template, Category, Tag, Link


@api.route("/create_table")
def create_table():
    db.create_all()
    return '创建数据表成功', 200


@api.route("/insert_data")
def insert_data():
    u = Template(name='cat', prompt='hello,world,')
    db.session.add(u)
    db.session.commit()


@api.route("/init_template")
def init_template():
    path = os.path.abspath('app/static/json/templates.json')
    print(path)
    with open(path) as f:
        json_list = json.load(f)
        for item in json_list:
            temp = Template(name=item['name'], prompt=item['prompt'], n_prompt=item['nprompt'], step=item['step'],
                            scale=item['scale'], author=item['author'], preview=item['preview'])
            db.session.add(temp)
            db.session.commit()
            print(item)
        return json_list, 200


@api.route("/init_category")
def init_category():
    path = os.path.abspath('app/static/json/tags.json')
    print(path)
    with open(path) as f:
        json_list = json.load(f)
        json_class = json_list['class']
        for item in json_class:
            cate = Category(name=item['name'])
            db.session.add(cate)
            db.session.commit()
        return json_class, 200


@api.route("/init_tag")
def init_tag():
    path = os.path.abspath('app/static/json/tags.json')
    print(path)
    with open(path) as f:
        json_list = json.load(f)
        json_class = json_list['class']
        total = 0
        for item in json_class:
            json_datas = item['data']
            for data in json_datas:
                total = total + 1
                cate = Tag(zh=data['zh'], en=data['en'], category=item['name'])
                db.session.add(cate)
                db.session.commit()
        return '初始化tag成功,共计' + str(total) + '条', 200


@api.route("/init_link")
def init_link():
    path = os.path.abspath('app/static/json/links.json')
    print(path)
    with open(path) as f:
        json_list = json.load(f)
        total = 0
        for item in json_list:
            total = total + 1
            cate = Link(name=item['name'], href=item['href'], link_type=item['type'])
            db.session.add(cate)
            db.session.commit()
        return '初始化link成功,共计' + str(total) + '条', 200
