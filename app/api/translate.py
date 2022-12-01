from flask import jsonify, request
from . import api
import asyncio
# https://github.com/sevenc-nanashi/async-google-trans-new/tree/main/async_google_trans_new
from async_google_trans_new import AsyncTranslator
from app.utils import JsonResponse


@api.route("/translate", methods=['POST'])
async def translate():
    if request.method == 'POST':
        req = request.get_json()
        translate_type = str(req['type'])
        text = req['text']
        g = AsyncTranslator()
        if translate_type == '1':
            print('英转中')
            translate_text: str = (await g.translate(text, 'zh-cn')).strip()
            return JsonResponse.success({
                'text': text,
                'type': translate_type,
                'translateText': translate_text,
            })
        if translate_type == '2':
            print('中转英')
            translate_text: str = (await g.translate(text, 'en')).strip()
            return JsonResponse.success({
                'text': text,
                'type': translate_type,
                'translateText': translate_text,
            })

        return JsonResponse.error({
            'text': '',
            'type': '',
            'translateText': '',
        })
