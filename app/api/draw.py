import json

import requests
from flask_restx import Namespace, reqparse, Resource

ns = Namespace("draw", description="图片生成")
parser = reqparse.RequestParser()


@ns.route("/ai")
@ns.doc(
    params={
        'init_images': '',
        'prompt': '',
        'seed': '',
        'negative_prompt': '',
        'cfg_scale': '',
        'width': '',
        'height': '',
        'denoising_strength': '',
        'steps': '',
    }
)
class DrawResource(Resource):
    @staticmethod
    def post():
        parser.add_argument("init_images", help="init_images ", type=str, default="")
        parser.add_argument("prompt", help="prompt 必填", type=str, default="", required=True)
        parser.add_argument("seed", help="seed ", type=int, required=True)
        parser.add_argument("negative_prompt", help="negative_prompt ", type=str, default="")
        parser.add_argument("cfg_scale", help="cfg_scale ", type=int, default=12)
        parser.add_argument("width", help="width ", type=str, default="512")
        parser.add_argument("height", help="height ", type=str, default="768")
        parser.add_argument("denoising_strength", help="denoising_strength ", type=float, default=0.6)
        parser.add_argument("steps", help="steps ", type=int, default=28)
        arguments = parser.parse_args()
        data = json.dumps({
            'prompt': arguments['prompt'],
            'seed': arguments['seed'],
            'negative_prompt': arguments['negative_prompt'],
            'cfg_scale': 11,
            'width': 512,
            'height': 768,
            'denoising_strength': 0.6,
            'steps': 28,
        })
        headers = {"api": "42"}
        res = requests.post('https://rryth.elchapo.cn:11000/v2', data=data, headers=headers)
        res_json = res.json()

        if res.status_code == 200:
            return {
                "data": {
                    "images": res_json['images']
                },
                "msg": "生成图片成功",
                "code": 200,
            }, 200
        else:
            return {
                "data": '',
                "msg": "生成图片失败",
                "code": 500,
            }, 200
