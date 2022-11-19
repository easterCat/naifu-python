from flask import jsonify, request
from . import api
import asyncio
# https://github.com/sevenc-nanashi/async-google-trans-new/tree/main/async_google_trans_new
from async_google_trans_new import AsyncTranslator


@api.route("/translate", methods=['POST'])
async def translate():
    if request.method == 'POST':
        # 1=>en to zh, 2=>zh to en
        req = request.get_json()
        type = str(req['type'])
        text = req['text']
        print(text)
        tText = ''
        g = AsyncTranslator()
        if type == '1':
            print('英转中')
            tText = await g.translate(text, 'zh-cn')
        if type == '2':
            print('中转英')
            tText = await g.translate(text, 'en')

        return jsonify({
            'msg': 'success',
            'code': 200,
            'data': {
                'text': text,
                'type': type,
                'translateText': tText,
            }
        })
