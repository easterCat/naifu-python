import logging
import os
import time
import urllib.request

import requests
from bs4 import BeautifulSoup
from deepdanbooru_onnx import DeepDanbooru
from flask import request
from flask_restx import Namespace, reqparse, Resource
from loguru import logger

ns = Namespace("danbooru", description="deepdanbooru图片分析")
parser = reqparse.RequestParser()

ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@ns.route("/upload")
class DanbooruResource(Resource):
    @staticmethod
    def post():
        temp_path = os.path.abspath(os.path.join(__file__, "../..", "static/temp"))
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)

        upload_file = request.files['file']

        if upload_file and allowed_file(upload_file.filename):
            file_name = upload_file.filename
            ext = file_name.rsplit(".", 1)[1]
            unix_time = int(time.time())
            new_file_name = str(unix_time) + '.' + ext
            save_path = temp_path + '/' + new_file_name
            upload_file.save(save_path)
            return {"code": 200, "msg": "上传成功", "data": {
                "file_name": new_file_name,
                "file_path": '/temp/' + new_file_name
            }}, 200
        else:
            return {"code": 500, "msg": "不支持当前文件格式", "data": ""}, 200


@ns.route("/analysis")
class DanbooruAnalysis(Resource):
    @staticmethod
    def post():
        static_path = os.path.abspath(os.path.join(__file__, "../..", "static"))
        temp_path = os.path.abspath(os.path.join(__file__, "../..", "static/temp"))
        req = request.get_json()
        image_name = str(req["name"])

        try:
            danbooru = DeepDanbooru(
                model_path=static_path + "/danbooru/deepdanbooru.onnx",
                tags_path=static_path + "/danbooru/tags.txt"
            )
            save_path = temp_path + '/' + image_name
            result = danbooru(save_path)
            tag_list = []
            for key, value in result.items():
                tag_list.append({
                    'key': str(key),
                    'value': str(value)
                })

            return {"code": 200, "msg": "解析成功", "data": {
                'tags': tag_list
            }}, 200
        except Exception as e:
            logging.error(e)
            return {"code": 500, "msg": "解析{}出现错误".format(image_name), "data": ""}, 200


@ns.route("/list")
class BooruList(Resource):
    # https://github.com/yukishirataco/animepics-pest/blob/master/start.py
    @staticmethod
    def get():
        parser.add_argument("searchText", help="请输入你要查询的tag(可以有多个)", type=str, default='')
        parser.add_argument("pageSize", help="每页多少个", type=int, default=100)
        parser.add_argument("pageIndex", help="第几页", type=int, default=1)
        params = parser.parse_args()
        tags = params['searchText']
        rate = ' '
        source = r'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags='
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
        url = source + tags + rate
        r = requests.get(url, headers=headers)
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        d_list = []
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "lxml")
            num = int(soup.find('posts')['count'])
            max_page = int(round(num / params['pageSize']))
            # 查看页面上有多少图片，以100张图一页的话有多少图
            count = 0
            logger.info(
                url + 'API访问正常...\n对于tag:' + tags + rate + ',有' + str(num) + '张图，' + str(max_page) + '页')
            if num == 0:
                logger.error('没有找到图片，可能是出错了...')
                return {"code": 500, "msg": "没有找到图片，可能是出错了...", "data": ""}, 200
            else:
                page = params['pageIndex'] - 1
                # 爬取所有页面的图，所以在每一页都要找到图片
                pages = requests.get(url + '&pid=' + str(page))
                if pages.status_code == 200:
                    get_page_xml = BeautifulSoup(pages.text, "lxml")
                    posts = get_page_xml.find('posts')
                    pics = posts.find_all('post')
                    for link in pics:
                        d_list.append({
                            "id": link.find("id").get_text(),
                            "minify_preview": link.find("preview_url").get_text(),
                            "preview": link.find("file_url").get_text(),
                            "name": link.find("image").get_text(),
                            "sample": link.find("sample").get_text(),
                            "prompt": link.find("tags").get_text(),
                        })
                        count = count + 1
                    return {"code": 200, "msg": "解析成功", "data": {'list': d_list, 'total': num}}, 200
        else:
            return {"code": 500, "msg": "gelbooru出现错误", "data": ""}, 200
