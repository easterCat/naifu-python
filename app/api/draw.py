import json
import os

import requests
from flask_restx import Namespace, reqparse, Resource

ns = Namespace("draw", description="图片生成")
parser = reqparse.RequestParser()


@ns.route('/list')
@ns.doc()
class DrawListResource(Resource):
    @staticmethod
    def get():
        data = []
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        static_dir = os.path.join(parent_dir, "static")
        for filename in os.listdir(static_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(static_dir, filename)
                with open(file_path, 'r', encoding='u8') as json_file:
                    json_data = json.load(json_file)
                    data.extend(json_data)
        return {"data": {"result_urls": data}, "msg": "服务器列表获取成功", "code": 200}, 200


@ns.route("/ai")
@ns.doc(params={
    'init_images': '', 'prompt': '', 'seed': '', 'negative_prompt': '', 'cfg_scale': '', 'width': '',
    'height': '', 'denoising_strength': '', 'steps': ''
})
class DrawResource(Resource):
    @staticmethod
    def post():
        parser.add_argument("init_images", help="init_images ", type=str, default="")
        parser.add_argument("prompt", help="prompt 必填", type=str, default="", required=True)
        parser.add_argument("seed", help="seed ", type=int)
        parser.add_argument("negative_prompt", help="negative_prompt ", type=str, default="")
        parser.add_argument("cfg_scale", help="cfg_scale ", type=int, default=8)
        parser.add_argument("width", help="width ", type=str, default="512")
        parser.add_argument("height", help="height ", type=str, default="768")
        parser.add_argument("denoising_strength", help="denoising_strength ", type=float, default=0.6)
        parser.add_argument("steps", help="steps ", type=int, default=28)
        parser.add_argument("n_samples", help="n_samples ", type=int, default=3)
        parser.add_argument("postUrl", help="postUrl ", type=str, default="")

        arguments = parser.parse_args()

        if arguments['postUrl']:
            url = arguments['postUrl'] + '/sdapi/v1/txt2img'
        else:
            url = 'https://rryth.elchapo.cn:11000/v2'

        data = json.dumps({
            'prompt': arguments['prompt'],
            'negative_prompt': arguments['negative_prompt'],
            'cfg_scale': int(arguments['cfg_scale']),
            'width': int(arguments['width']),
            'height': int(arguments['height']),
            'denoising_strength': 0.6,
            'steps': int(arguments['steps']),
            'n_iter': int(arguments['n_samples']),
        })
        headers = {"api": "42", "Content-Type": "application/json"}
        res = requests.post(url, data=data, headers=headers)
        res_json = res.json()
        if res.status_code == 200:
            return {"data": {"images": res_json['images']}, "msg": "生成图片成功", "code": 200, }, 200
        else:
            return {"data": '', "msg": "生成图片失败", "code": 500, }, 200


@ns.route('/test')
@ns.doc()
class TestDrawServer(Resource):
    @staticmethod
    def get():
        response = requests.post('http://127.0.0.1:9999/test', headers={'X-Requested-With': 'XMLHttpRequest'})
        json_data = response.json()
        if response.status_code == 200:
            return {"data": {"result_urls": json_data}, "msg": "验证服务成功", "code": 200, }, 200
        else:
            return {"data": {"result_urls": []}, "msg": "验证服务失败", "code": 500, }, 200
