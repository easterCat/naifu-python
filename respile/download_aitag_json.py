import requests
import json
from requests.structures import CaseInsensitiveDict
from string import Template


def init():
    res = requests.get("https://api.aitag.top/tagv2/get_subs")
    tag_json = json.loads(res.content)
    tag_result = tag_json['result']

    for tag in tag_result:
        save_map = {'result': []}
        url = "https://api.aitag.top/tagv2"
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        data = json.dumps({
            'method': 'get_tags_from_sub',
            'sub': tag,
            'page': 1,
        }).encode("utf-8")
        tem_res = requests.post(url, headers=headers, data=data)
        tem_json = json.loads(tem_res.content)
        page_count = tem_json['page_data']['page_count']
        for page in range(1, page_count+1):
            data2 = json.dumps({
                'method': 'get_tags_from_sub',
                'sub': tag,
                'page': page,
            }).encode("utf-8")
            page_res = requests.post(url, headers=headers, data=data2)
            page_json = json.loads(page_res.content)
            page_result = page_json['result']
            save_map['result'] = save_map['result'] + page_result
        for index, item in enumerate(save_map['result']):
            item['index'] = index
        with open("app/static/json/aitag/"+tag+'.json', 'w', encoding='gb2312') as f:
            json.dump(save_map, f)


init()
