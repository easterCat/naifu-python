import json
import requests

from flask import render_template
from . import api
from app import db
from app.models import Template, Category, Tag, Link
import pandas as pd


@api.route("/db")
def database_home():
    return render_template('database.html')


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
    json_list = request_json('https://raw.githubusercontent.com/easterCat/nuxt-utils-assets/main/json/templates.json')
    for item in json_list:
        temp = Template(name=item['name'], prompt=item['prompt'], n_prompt=item['nprompt'], step=item['step'],
                        scale=item['scale'], author=item['author'], preview=item['preview'])
        db.session.add(temp)
        db.session.commit()
        print(item)
    return json_list, 200


@api.route("/init_template_more")
def init_template_more():
    total = 0
    nums = [5, 6, 7, 8, 9]

    for num in nums:
        try:
            csv_path = 'app/static/csv/temp' + str(num) + '.csv'
            csv_data9 = pd.read_csv(csv_path)
            for index, item in csv_data9.iterrows():
                print(item['author'])
                temp = Template(name=item['name'], author=item['author'], preview=item['preview'],
                                prompt=item['prompt'],
                                n_prompt=item['n_prompt'], step=item['step'], sampler=item['sampler'],
                                scale=item['scale'],
                                seed=item['seed'], skip=item['skip'], size=item['size'], model=item['model'],
                                path=item['path'], )
                db.session.add(temp)
                db.session.commit()
                total = total + 1
        except Exception as e:
            print('插入数据错误 ==> ', e)
    return 'success,总计' + str(total) + '条', 200


@api.route("/init_category")
def init_category():
    json_list = request_json('https://raw.githubusercontent.com/easterCat/nuxt-utils-assets/main/json/tags.json')
    json_class = json_list['class']
    total = 0
    for item in json_class:
        total = total + 1
        cate = Category(name=item['name'])
        db.session.add(cate)
        db.session.commit()
    return '初始化category成功,共计' + str(total) + '条', 200


@api.route("/init_tag")
def init_tag():
    json_list = request_json('https://raw.githubusercontent.com/easterCat/nuxt-utils-assets/main/json/tags.json')
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
    json_list = request_json('https://raw.githubusercontent.com/easterCat/nuxt-utils-assets/main/json/links.json')
    total = 0
    repeat_total = 0
    for item in json_list:
        find_count = Link.query.filter(Link.name == item['name']).count()
        if find_count > 0:
            repeat_total = repeat_total + 1
        else:
            total = total + 1
            cate = Link(name=item['name'], href=item['href'], link_type=item['type'])
            db.session.add(cate)
            db.session.commit()
    return '初始化link成功,插入' + str(total) + '条' + ',重复' + str(repeat_total) + '条', 200


def request_json(url):
    res = requests.get(url)
    res_list = json.loads(res.text)
    return res_list
