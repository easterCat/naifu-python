import json
from . import api
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import os


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def requests_img(img_name, img_url, proxy, headers):
    r = requests.get(img_url, headers=headers, stream=True, proxies={"http": "http://{}".format(proxy)})
    if r.status_code == 200:
        save_path = 'app/static' + img_name
        find_index = save_path.rfind('/')
        static_path = save_path[0:find_index]
        if not os.path.exists(static_path):
            os.makedirs(static_path)
        with open(save_path, 'wb') as f:
            f.write(r.content)
            print('下载完成' + save_path)
            return save_path
    del r


@api.route("/reptile")
def reptile():
    ua = UserAgent().random
    headers = {
        'User-Agent': ua}
    url = 'https://www.ptsearch.info/home/?page='
    proxy = get_proxy().get("proxy")
    print('当前代理的地址 ==> ', proxy)
    total_page = 251
    current_page = 241
    retry_count = 5
    total_list = []
    while retry_count > 0:
        try:
            while current_page < total_page:
                # 使用代理访问
                str_html = requests.get(url + str(current_page), headers=headers,
                                        proxies={"http": "http://{}".format(proxy)})
                soup = BeautifulSoup(str_html.text, 'lxml')
                data = soup.select('body > main > div.container > div.outer_card > a')
                for item in data:
                    result = get_detail(str(item.get('href')), headers, proxy)
                    try:
                        result['page'] = current_page
                        total_list.append(result)
                    except Exception as e:
                        print('插入result出现错误 ==> ', e)
                current_page = current_page + 1
            try:
                df1 = pd.DataFrame(data=total_list,
                                   columns=['name', 'author', 'img', 'preview', 'prompt', 'n_prompt', 'step', 'sampler',
                                            'scale', 'seed', 'skip', 'size', 'model', 'path', 'page'])
                df1.to_csv('app/static/csv/temp9.csv')
            except Exception as e:
                print('插入csv数据出现错误 ==> ', e)
            return 'success' + str(len(total_list)) + '条', 200
        except Exception as e:
            print('代理重试 ==> ', e)
            retry_count -= 1
    # 删除代理池中代理
    delete_proxy(proxy)
    print('爬取出现错误')
    return json.dumps(total_list), 200


def get_detail(detail_id, headers, proxy):
    result = {}
    prefix = 'https://www.ptsearch.info'
    str_html = requests.get(prefix + str(detail_id), headers=headers,
                            proxies={"http": "http://{}".format(proxy)})
    soup = BeautifulSoup(str_html.text, 'lxml')
    name = soup.select('body > main > div.container > h1')
    author = soup.select('body > main > div.container > div:nth-child(4) > div > a > p')
    img = soup.select('body > main > div.container > div.form_class_max_800px > img')
    preview = 'https://www.ptsearch.info' + img[0].get('src')
    no_exif = soup.select_one('body > main > div.container > div.form_class_max_800px > div.text-center > button')

    result = {
        'name': str(name[0].get_text()),
        'author': str(author[0].get_text()),
        'img': str(img[0].get('src')),
        'preview': str(preview),
        'prompt': 'None',
        'n_prompt': 'None',
        'step': 'None',
        'sampler': 'None',
        'scale': 'None',
        'seed': 'None',
        'skip': 'None',
        'size': 'None',
        'model': 'None',
        'path': 'None',
    }

    save_path = requests_img(str(img[0].get('src')), str(preview), proxy, headers)

    if save_path is not None:
        result['path'] = save_path

    if no_exif is not None:
        return result
    else:
        try:
            children = soup.select(
                "body > main > div.container > div:nth-child(7) > table > tbody > tr > td:nth-child(1)")
            for index, value in enumerate(children):
                text = value.get_text()

                if text == 'parameters':
                    prompt = soup.select_one(
                        "body > main > div.container > div:nth-child(7) > table > tbody > tr:nth-child(" + str(
                            index + 1) + ") > td:nth-child(2)")
                    result['prompt'] = str(prompt.contents[0])

                if text == 'negative_prompt':
                    prompt = soup.select_one(
                        "body > main > div.container > div:nth-child(7) > table > tbody > tr:nth-child(" + str(
                            index + 1) + ") > td:nth-child(2)")
                    result['n_prompt'] = str(prompt.contents[0])

                if text == 'step':
                    prompt = soup.select_one(
                        "body > main > div.container > div:nth-child(7) > table > tbody > tr:nth-child(" + str(
                            index + 1) + ") > td:nth-child(2)")
                    result['step'] = str(prompt.contents[0])

                if text == 'sampler':
                    prompt = soup.select_one(
                        "body > main > div.container > div:nth-child(7) > table > tbody > tr:nth-child(" + str(
                            index + 1) + ") > td:nth-child(2)")
                    result['sampler'] = str(prompt.contents[0])

                if text == 'cfg_scale':
                    prompt = soup.select_one(
                        "body > main > div.container > div:nth-child(7) > table > tbody > tr:nth-child(" + str(
                            index + 1) + ") > td:nth-child(2)")
                    result['scale'] = str(prompt.contents[0])

                if text == 'seed':
                    prompt = soup.select_one(
                        "body > main > div.container > div:nth-child(7) > table > tbody > tr:nth-child(" + str(
                            index + 1) + ") > td:nth-child(2)")
                    result['seed'] = str(prompt.contents[0])

                if text == 'clip_skip':
                    prompt = soup.select_one(
                        "body > main > div.container > div:nth-child(7) > table > tbody > tr:nth-child(" + str(
                            index + 1) + ") > td:nth-child(2)")
                    result['skip'] = str(prompt.contents[0])

                if text == 'size':
                    prompt = soup.select_one(
                        "body > main > div.container > div:nth-child(7) > table > tbody > tr:nth-child(" + str(
                            index + 1) + ") > td:nth-child(2)")
                    result['size'] = str(prompt.contents[0])

                if text == 'model_hash':
                    prompt = soup.select_one(
                        "body > main > div.container > div:nth-child(7) > table > tbody > tr:nth-child(" + str(
                            index + 1) + ") > td:nth-child(2)")
                    result['model'] = str(prompt.contents[0])

        except Exception as e:
            print('赋值result错误 ==> :', e)

        return result
