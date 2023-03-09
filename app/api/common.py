import base64
import imghdr
import os
import time
import uuid
from pathlib import Path

from flask_restx import Namespace, reqparse, Resource
from image_depot import image_depot, DepotType

ns = Namespace("common", description="通用接口")
parser = reqparse.RequestParser()

ALLOWED_EXTENSIONS = {"txt", "png", "jpg", "xls", "JPG", "PNG", "xlsx", "gif", "GIF"}


# 用于判断文件后缀
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


def save_image(img_data):
    if imghdr.what("", img_data) is None:
        return {"code": 500, "msg": "不支持当前文件格式!", "data": ""}, 200

    temp_path = Path(__file__).parent / "static" / "temp"
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)

    img_url = temp_path / f"{uuid.uuid4()}.png"

    with open(img_url, "wb") as f:
        f.write(img_data)
        if img_url.exists():
            d = image_depot(DepotType.NiuPic)
            if d is None:
                pass
            time.sleep(2)
            imgbb_url = d.upload_file(str(img_url))
            os.remove(img_url)
            if imgbb_url is None:
                return {"code": 500, "msg": "牛图网上传失败!", "data": imgbb_url}, 200
            else:
                return {"code": 200, "msg": "图片上传成功!", "data": [imgbb_url]}, 200
        else:
            return {"code": 500, "msg": "图片保存失败!", "data": ""}, 200


@ns.route("/upload_image")
class UploadImage(Resource):
    @staticmethod
    def post():
        parser.add_argument("files")
        body = parser.parse_args()
        files = body["files"].split(",")
        upload_images = []
        for file in files:
            img_data = base64.b64decode(file)
            res, status = save_image(img_data)
            if status != 200:
                return res, status
            upload_images.extend(res["data"])
        return {"code": 200, "msg": "图片上传成功!", "data": upload_images}, 200
