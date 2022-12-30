import logging
import os
import time

from deepdanbooru_onnx import DeepDanbooru
from flask import request
from flask_restx import Namespace, reqparse, Resource

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
                "file_path": '/static/temp/' + new_file_name
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
