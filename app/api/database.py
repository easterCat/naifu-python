import json

import requests
from flask import render_template

from app import db
from app.model.link import Link
from app.model.models import Category, Tag
from app.model.template import TemplateTest, TemplateStable
from app.model.user import Role
from . import api


@api.route("/db")
def database_home():
    return render_template("database.html")


@api.route("/create_table")
def create_table():
    db.create_all()
    return "创建数据表成功", 200


@api.route("/insert_data")
def insert_data():
    u = TemplateTest(name="cat", prompt="hello,world,")
    db.session.add(u)
    db.session.commit()


@api.route("/init_role")
def init_role():
    total = 0
    role_lists = [
        {"name": "管理员", "role_name": "Admin"},
        {"name": "开发者", "role_name": "Developer"},
        {"name": "贡献者", "role_name": "Contributor"},
        {"name": "游客", "role_name": "Guest"},
    ]
    for item in role_lists:
        if item["role_name"] == "Guest":
            temp = Role(name=item["name"], role_name=item["role_name"], default=True)
        else:
            temp = Role(name=item["name"], role_name=item["role_name"])
        db.session.add(temp)
        db.session.commit()
        total += 1
    return "success" + str(total), 200


@api.route("/init_template")
def init_template():
    json_list = request_json(
        "https://raw.githubusercontent.com/easterCat/nuxt-utils-assets/main/json/templates.json"
    )
    for item in json_list:
        temp = TemplateStable(
            name=item["name"],
            prompt=item["prompt"],
            n_prompt=item["nprompt"],
            step=item["step"],
            scale=item["scale"],
            author=item["author"],
            preview=item["preview"],
        )
        db.session.add(temp)
        db.session.commit()
        print(item)
    return json_list, 200


@api.route("/init_category")
def init_category():
    json_list = request_json(
        "https://raw.githubusercontent.com/easterCat/nuxt-utils-assets/main/json/tags.json"
    )
    json_class = json_list["class"]
    total = 0
    for item in json_class:
        total = total + 1
        cate = Category(name=item["name"])
        db.session.add(cate)
        db.session.commit()
    return "初始化category成功,共计" + str(total) + "条", 200


@api.route("/init_tag")
def init_tag():
    json_list = request_json(
        "https://raw.githubusercontent.com/easterCat/nuxt-utils-assets/main/json/tags.json"
    )
    json_class = json_list["class"]
    total = 0
    for item in json_class:
        json_datas = item["data"]
        for data in json_datas:
            total = total + 1
            cate = Tag(zh=data["zh"], en=data["en"], category=item["name"])
            db.session.add(cate)
            db.session.commit()
    return "初始化tag成功,共计" + str(total) + "条", 200


@api.route("/init_link")
def init_link():
    json_list = request_json(
        "https://raw.githubusercontent.com/easterCat/nuxt-utils-assets/main/json/links.json"
    )
    total = 0
    repeat_total = 0
    for item in json_list:
        find_count = Link.query.filter(Link.name == item["name"]).count()
        if find_count > 0:
            repeat_total = repeat_total + 1
        else:
            total = total + 1
            cate = Link(name=item["name"], href=item["href"], link_type=item["type"])
            db.session.add(cate)
            db.session.commit()
    return "初始化link成功,插入" + str(total) + "条" + ",重复" + str(repeat_total) + "条", 200


def request_json(url):
    res = requests.get(url)
    res_list = json.loads(res.text)
    return res_list
