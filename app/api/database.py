import json
from . import api
from app.models import Template
from app import db
import os


@api.route("/table")
def database():
    db.create_all()
    return '创建成功', 200


@api.route("/insert")
def insert():
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
