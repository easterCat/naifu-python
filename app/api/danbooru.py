import logging
import os
import uuid

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
            new_file_name = uuid.uuid4().hex + '.' + ext
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
    @staticmethod
    def get():
        parser.add_argument("searchText", help="请输入你要查询的tag(可以有多个)", type=str, default='all')
        parser.add_argument("pageSize", help="每页多少个", type=int, default=100)
        parser.add_argument("pageIndex", help="第几页", type=int, default=1)
        params = parser.parse_args()
        page_size = params['pageSize']
        page_index = params['pageIndex']
        tags = params['searchText']
        rate = ' '
        source = r'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags='
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
        url = source + tags + rate
        response = requests.get(url, headers=headers)
        result_list = []

        if response.status_code != 200:
            return {"code": 500, "msg": "gelbooru请求出现错误", "data": ""}, 200

        soup = BeautifulSoup(response.text, "lxml")
        total_count = int(soup.find('posts')['count'])
        total_page = int(round(total_count / page_size))

        if total_count == 0:
            logger.error('没有找到图片，可能是出错了...')
            return {"code": 500, "msg": "没有找到图片，可能是出错了...", "data": ""}, 200

        logger.info(
            f"{url} API访问正常...\n对于tag:{tags}{rate}，有{total_count}张图，{total_page}页"
        )

        page = page_index - 1
        page_response = requests.get(url + '&pid=' + str(page))
        if page_response.status_code == 200:
            get_page_xml = BeautifulSoup(page_response.text, "lxml")
            posts = get_page_xml.find('posts')
            pics = posts.find_all('post')
            for link in pics:
                result_list.append({
                    "id": link.find("id").get_text(),
                    "minify_preview": link.find("preview_url").get_text(),
                    "preview": link.find("file_url").get_text(),
                    "name": link.find("image").get_text(),
                    "sample": link.find("sample").get_text(),
                    "prompt": link.find("tags").get_text(),
                })
            return {"code": 200, "msg": "解析成功", "data": {'list': result_list, 'total': total_count}}, 200


@ns.route("/tags")
class BooruTags(Resource):
    @staticmethod
    def get():
        parser.add_argument("searchText", help="请输入你要查询的tag(可以有多个)", type=str, default='all')
        params = parser.parse_args()
        search_text = params['searchText']
        source = r'http://gelbooru.com/index.php?page=tags&s=list&sort=desc&order_by=index_count'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
        if search_text != '':
            url = f"{source}&tags={search_text}"
        else:
            url = source
        result_list = []
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return {"code": 500, "msg": "获取booru的tags失败", "data": {"tags": result_list, "total": 0}}, 200

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.select_one('table.highlightable')
        rows = table.find_all('tr')
        for row in rows:
            first_td = row.select_one('td:first-child')
            if first_td is None:
                continue
            span_type = first_td.select_one('a').text
            span_count = row.select_one('span.tag-count').text
            if span_type == '':
                continue
            result_list.append({
                "tag_name": span_type.replace(" ", "_"),
                "tag_count": span_count
            })

        return {"code": 200, "msg": "获取tags成功", "data": {"tags": result_list, "total": len(result_list)}}, 200
