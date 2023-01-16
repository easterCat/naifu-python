import base64
import io
import json

import requests
from PIL import Image
from image_depot import image_depot, DepotType


def init():
    with open("/Users/lilin/Desktop/naifu-python/app/static/json/tags.json", "r") as tags:
        res_json = json.load(tags)
        category_list = res_json['class']
        for category in category_list:
            prompt_list = category['data']
            for prompt in prompt_list:
                en = prompt['en']
                req2_data = {
                    'cfg_scale': 12,
                    'denoising_strength': 0.6,
                    'height': "512",
                    'init_images': "",
                    'n_samples': 1,
                    'negative_prompt': "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry",
                    'prompt': "masterpiece, best quality, 1girl, ({})".format(en),
                    'sampler': "k_euler_ancestral",
                    'seed': 3179801653,
                    'steps': 28,
                    'width': "512",
                }
                res2 = requests.post('http://localhost:5000/api/draw/ai', data=req2_data)
                res2_json = json.loads(res2.content)
                base64_str = res2_json['data']['images'][0]
                img = Image.open(io.BytesIO(base64.decodebytes(bytes(base64_str, "utf-8"))))
                img.save('/Users/lilin/Desktop/naifu-python/app/static/temp/aaa.png')

                d = image_depot(DepotType.NiuPic)
                imgbb_url = d.upload_file('/Users/lilin/Desktop/naifu-python/app/static/temp/aaa.png')
                prompt['preview'] = imgbb_url
                print(prompt)
        save_json = json.dumps(res_json, ensure_ascii=False)
        with open("/Users/lilin/Desktop/naifu-python/app/static/json/tags.json", "w") as write_file:
            write_file.write(save_json)


init()
