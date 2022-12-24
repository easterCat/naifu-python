import json
import os
import random
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from app import db
from app.model.template import TemplateHan, TemplateNoval
from app.utils import CompressImage
from . import api

proxy_list = [
    "148.76.97.250:80",
    "51.15.242.202:8888",
    "162.240.75.37:80",
]


@api.route("/reptile_hanwang")
def reptile_hanwang():
    return reptile_hanwang()


@api.route("/reptile_noval")
def reptile_noval():
    return reptile_noval()


def reptile_noval():
    # 爬取小飞机中某个绘图库
    total = 0
    options = create_header_options()
    total_page = 10000
    current_page = 1
    retry_count = 4
    total_list = []
    img_prefix = "https://novel.pyhdxy.top"
    while retry_count > 0:
        try:
            while current_page < total_page:
                url = "https://novel.pyhdxy.top/data"
                response = requests.get(url=url, headers={}, proxies=options["proxies"])
                time.sleep(random.random() * 6)
                json_list = json.loads(response.content)
                json_result = json_list["result"]
                for item in json_result:
                    p = item["image"].split("/")[-1]
                    find = TemplateNoval.query.filter_by(name=p).first()
                    if find is None:
                        print(str(p) + "不存在,开始添加")
                        soup = BeautifulSoup(item["cfg"], "lxml")
                        soup_json = soup.select_one("body > p:nth-child(1)")
                        text = soup_json.get_text()
                        jss = json.loads(text)

                        if hasattr(jss, "model_hash"):
                            model = jss["model_hash"]
                        else:
                            model = ""

                        download_images(
                            p,
                            img_prefix + item["image"],
                            options["proxies"],
                            {},
                            "app/static/media/article/noval/",
                        )

                        total += 1
                        print(total)
                        tem_instance = TemplateNoval(
                            name=p,
                            preview="http://www.ptg.life/static/media/article/noval/"
                            + p,
                            path="static/media/article/noval/" + p,
                            step=jss["steps"],
                            prompt=jss["tag"],
                            n_prompt=jss["uc"],
                            model=model,
                            sampler=jss["mode"],
                            desc=str(jss),
                        )
                        db.session.add(tem_instance)
                        db.session.commit()
                    else:
                        print(str(p) + "已存在")

                current_page = current_page + 1
            return "success" + str(total) + "条", 200
        except Exception as e:
            print("代理重试 ==> ", e)
            retry_count -= 1
    # 删除代理池中代理
    # delete_proxy(options['proxy'])
    print("爬取出现错误")
    return json.dumps(total_list), 200


def reptile_hanwang():
    save_csv_path = "app/static/csv/temp11.csv"
    options = create_header_options()
    total_page = 2
    current_page = 1
    retry_count = 4
    total_list = []
    while retry_count > 0:
        try:
            while current_page < total_page:
                url = options["url"] + str(current_page)
                print("开始=>", url)
                str_html = requests.get(
                    url, headers=options["headers"], proxies=options["proxies"]
                )
                soup = BeautifulSoup(str_html.text, "lxml")
                data = soup.select("body > main > div.container > div.outer_card > a")
                for item in data:
                    result = get_html_detail(
                        str(item.get("href")), options["headers"], options["proxy"]
                    )
                    try:
                        result["page"] = current_page
                        total_list.append(result)
                    except Exception as e:
                        print("插入result出现错误 ==> ", e)
                current_page = current_page + 1
            try:
                df1 = pd.DataFrame(
                    data=total_list,
                    columns=[
                        "name",
                        "author",
                        "img",
                        "preview",
                        "prompt",
                        "n_prompt",
                        "step",
                        "sampler",
                        "scale",
                        "seed",
                        "skip",
                        "size",
                        "model",
                        "path",
                        "page",
                    ],
                )
                df1.to_csv(save_csv_path)
            except Exception as e:
                print("插入csv数据出现错误 ==> ", e)
            return "success" + str(len(total_list)) + "条", 200
        except Exception as e:
            print("代理重试 ==> ", e)
            retry_count -= 1
    # delete_proxy(options['proxy'])
    print("爬取出现错误")
    return json.dumps(total_list), 200


@api.route("/reptile/http2")
def reptile_http2():
    options = create_http2_header_options()
    user_proxy = ""

    for p in proxy_list:
        proxies = {"http": "http://{}".format(p)}
        s = requests.get(
            options["url"], verify=False, headers=options["headers"], proxies=proxies
        )
        sp = BeautifulSoup(s.text, "lxml")

        if "403 Forbidden" in str(sp):
            print("失败的=>", p)
        else:
            print("成功的=>", p)
            return str(sp), 200
    return user_proxy, 200


@api.route("/reptile/compress")
def reptile_image_compress():
    total = CompressImage(
        static_path="app/static/media/article/", dir_name="noval", quality=30
    ).compress_image()
    return (
        "压缩图片完毕,总计处理图片"
        + str(total)
        + "张"
        + " - "
        + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
        200,
    )


@api.route("/reptile/check_template_image")
def check_template_image():
    total = 0
    error_list = []
    try:
        tems = TemplateHan.query.all()
        for i in tems:
            item = i.to_json()
            view = "app" + item["path"]
            if os.path.isfile(view):
                total = total + 1
                print(total)
            else:
                error_list.append(view)
    except Exception as e:
        print("插入数据错误 ==> ", e)
    return (
        "success,总计" + str(total) + "条" + "success,总计" + json.dumps(error_list) + "条",
        200,
    )


@api.route("/reptile/database")
def reptile_database():
    total = 0

    # 韩网旧数据倒序入库
    # try:
    #     tems = Template.query.order_by(Template.id.desc()).all()
    #     for i in tems:
    #         item = i.to_json()
    #         tem_instance = TemplateHan(name=str(item['name']).strip(), author=str(item['author']).strip(),
    #                                    preview=item['preview'],
    #                                    prompt=str(item['prompt']).strip(), prompt_zh=str(item['prompt_zh']).strip(),
    #                                    n_prompt=str(item['n_prompt']).strip(),
    #                                    n_prompt_zh=str(item['n_prompt_zh']).strip(),
    #                                    step=str(item['step']).strip(),
    #                                    sampler=str(item['sampler']).strip(),
    #                                    scale=str(item['scale']).strip(),
    #                                    seed=str(item['seed']).strip(), skip=str(item['skip']).strip(),
    #                                    size=str(item['size']).strip(),
    #                                    model=str(item['model']).strip(),
    #                                    path=item['path'], desc=str(item['desc']).strip(), like=item['like'],
    #                                    like_address=item['like_address'], category=item['category'],
    #                                    create_time=datetime.now(),
    #                                    update_time=datetime.now())
    #         print(item['id'])
    #         db.session.add(tem_instance)
    #         db.session.commit()
    #         total = total + 1
    # except Exception as e:
    #     print('插入数据错误 ==> ', e)
    # return 'success,总计' + str(total) + '条', 200

    # 新数据入库
    nums = [10]
    for num in nums:
        try:
            csv_path = "app/static/csv/temp" + str(num) + ".csv"
            csv_data = pd.read_csv(csv_path)
            csv_json = csv_data.to_json(orient="records")
            csv_list = json.loads(csv_json)
            for item in reversed(csv_list):
                tem_instance = TemplateHan(
                    name=item["name"],
                    author=item["author"],
                    preview=item["preview"],
                    prompt=item["prompt"] or "",
                    n_prompt=item["n_prompt"],
                    step=item["step"],
                    sampler=item["sampler"],
                    scale=item["scale"],
                    seed=item["seed"],
                    skip=item["skip"],
                    size=item["size"],
                    model=item["model"],
                    path="/static"
                    + item["img"].replace("/original/", "/original_20221209/"),
                )
                # db.session.add(tem_instance)
                # db.session.commit()
                total = total + 1
                print(total)
        except Exception as e:
            print("插入数据错误 ==> ", e)
    return "success,总计" + str(total) + "条", 200


@api.route("/reptile/replace_url")
def reptile_replace_url():
    # total = 0
    # templates = TemplateHan.query.all()
    # for item in templates:
    #     jj = item.to_json()
    #     pp = jj['path'].replace('app', '')
    #     pp2 = jj['preview'].replace('https://www.ptsearch.info', 'http://www.ptg.life/static')
    #     db.session.query(TemplateHan).filter_by(id=jj['id']).update({
    #         'path': pp,
    #         'preview': pp2,
    #     })
    #     db.session.commit()
    #     total = total + 1
    #     print(total)
    # return '替换成完毕,总计处理图片' + str(total) + '张' + ' - ' + str(
    #     time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), 200

    total = 0
    templates = TemplateHan.query.all()
    for item in templates:
        jj = item.to_json()
        if "/original_20221209/" in jj["path"]:
            pp2 = jj["preview"].replace("/original/", "/original_20221209/")
            db.session.query(TemplateHan).filter_by(id=jj["id"]).update(
                {
                    "preview": pp2,
                }
            )
            db.session.commit()
            total = total + 1
            print(total)
    return (
        "替换成完毕,总计处理图片"
        + str(total)
        + "张"
        + " - "
        + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
        200,
    )


def create_http2_header_options():
    test_url = "http://httpbin.org/get"
    prompt_url = "https://www.ptsearch.info/home/?page=1"
    url = test_url
    proxy = "127.0.0.1:8888"
    headers = {
        "Cookie": "OUTFOX_SEARCH_USER_ID = -1916336379 @ 10.169.0.84;JSESSIONID = aaaF3jqgNCov6fQWqZs1w;OUTFOX_SEARCH_USER_ID_NCOO = 885890211.5426716;___rl__test__cookies = 1569052795328",
        "Host": "fanyi.youdao.com",
        "Origin": "http://fanyi.youdao.com",
        "Referer": "http://fanyi.youdao.com/",
        "authority": "www.ptsearch.info",
        "method": "GET",
        "path": "/home/?page=1",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "sec-ch-ua": 'Not A;Brand";v="99", "Chromium";v="108", "Google Chrome";v="108',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Unknown",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "cross-site",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 PTST/221205.203134",
    }

    proxies = {
        "http": proxy,
    }
    options = {
        "url": url,
        "proxies": proxies,
        "headers": headers,
        "proxy": proxy,
    }
    return options


def create_header_options():
    ua = UserAgent().random
    url = "https://www.ptsearch.info/home/?page="
    proxy = random.choice(proxy_list)
    headers = {
        "User-Agent": ua,
        # "Host": "novel.pyhdxy.top",
        # "Origin": "novel.pyhdxy.top",
        # "authority": "novel.pyhdxy.top",
        # "method": "GET",
        # "path": "/data",
        # "scheme": "https",
        # "accept": "application/json, text/javascript, */*; q=0.01",
        # "accept-encoding": "gzip, deflate, br",
        # "accept-language": "zh-CN,zh;q=0.9",
        # "referer": "https://novel.pyhdxy.top/",
        # "sec-ch-ua-mobile": "?0",
        # "sec-ch-ua-platform": "macOS",
        # "sec-fetch-dest": "empty",
        # "sec-fetch-mode": "cors",
        # "sec-fetch-site": "same-origin",
        # "x-requested-with": "XMLHttpRequest",
    }
    proxies = {"http": "http://{}".format(proxy)}
    print("当前代理的地址 ==> ", proxy)
    options = {
        "url": url,
        "proxies": proxies,
        "headers": headers,
        "proxy": proxy,
    }
    return options


def random_header_options():
    ua = UserAgent().random
    url = "https://www.ptsearch.info/home/?page="
    proxy = get_proxy()
    headers = {
        "User-Agent": ua,
        "Host": "novel.pyhdxy.top",
        "Origin": "novel.pyhdxy.top",
        "authority": "novel.pyhdxy.top",
        "method": "GET",
        "path": "/home/?page=1",
        "scheme": "https",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "referer": "https://novel.pyhdxy.top/",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "macOS",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
    }
    proxies = {"http": "http://{}".format(proxy)}
    print("当前代理的地址 ==> ", proxy)
    options = {
        "url": url,
        "proxies": proxies,
        "headers": headers,
        "proxy": proxy,
    }
    return options


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def download_images(img_name, img_url, proxies, headers, save_p):
    print(requests.get)
    r = requests.get(
        img_url,
        headers=headers,
        stream=True,
        proxies=proxies,
    )
    print(r)
    time.sleep(random.random() * 3)
    if r.status_code == 200:
        # "app/static/media/article/original_20221219/"
        save_path = save_p + img_name
        find_index = save_path.rfind("/")
        static_path = save_path[0:find_index]
        if not os.path.exists(static_path):
            os.makedirs(static_path)
        with open(save_path, "wb") as f:
            f.write(r.content)
            print("下载完成" + save_path)
            return save_path
    del r


def get_html_detail(detail_id, headers, proxy):
    prefix = "https://www.ptsearch.info"
    str_html = requests.get(
        prefix + str(detail_id),
        headers=headers,
        proxies={"http": "http://{}".format(proxy)},
    )

    soup = BeautifulSoup(str_html.text, "lxml")
    name = soup.select("body > main > div.container > h1")
    author = soup.select("body > main > div.container > div:nth-child(4) > div > a > p")
    img = soup.select("body > main > div.container > div.form_class_max_800px > img")
    preview = "https://www.ptsearch.info" + img[0].get("src")
    no_exif = soup.select_one(
        "body > main > div.container > div.form_class_max_800px > div.text-center > button"
    )

    result = {
        "name": str(name[0].get_text()).strip(),
        "author": str(author[0].get_text()).strip(),
        "img": str(img[0].get("src")).strip(),
        "preview": str(preview).strip(),
        "prompt": "None",
        "n_prompt": "None",
        "step": "None",
        "sampler": "None",
        "scale": "None",
        "seed": "None",
        "skip": "None",
        "size": "None",
        "model": "None",
        "path": "None",
    }

    save_path = download_images(
        str(img[0].get("src")),
        str(preview),
        proxy,
        headers,
        'app/static/media/article/noval/"',
    )

    if save_path is not None:
        result["path"] = save_path

    if no_exif is not None:
        return result
    else:
        try:
            children = soup.select(
                "body > main > div.container > div:nth-child(7) > table > tbody > tr > td:nth-child(1)"
            )
            for index, value in enumerate(children):
                text = value.get_text()

                if text == "parameters":
                    prompt = soup.select_one(
                        "body > main > div.container > div:nth-child(7) > table > tbody > tr:nth-child("
                        + str(index + 1)
                        + ") > td:nth-child(2)"
                    )
                    result["prompt"] = str(prompt.contents[0]).strip()

                if text == "negative_prompt":
                    prompt = soup.select_one(
                        "body > main > div.container > div:nth-child(7) > table > tbody > tr:nth-child("
                        + str(index + 1)
                        + ") > td:nth-child(2)"
                    )
                    result["n_prompt"] = str(prompt.contents[0]).strip()

                if text == "step":
                    prompt = soup.select_one(
                        "body > main > div.container > div:nth-child(7) > table > tbody > tr:nth-child("
                        + str(index + 1)
                        + ") > td:nth-child(2)"
                    )
                    result["step"] = str(prompt.contents[0]).strip()

                if text == "sampler":
                    prompt = soup.select_one(
                        "body > main > div.container > div:nth-child(7) > table > tbody > tr:nth-child("
                        + str(index + 1)
                        + ") > td:nth-child(2)"
                    )
                    result["sampler"] = str(prompt.contents[0]).strip()

                if text == "cfg_scale":
                    prompt = soup.select_one(
                        "body > main > div.container > div:nth-child(7) > table > tbody > tr:nth-child("
                        + str(index + 1)
                        + ") > td:nth-child(2)"
                    )
                    result["scale"] = str(prompt.contents[0]).strip()

                if text == "seed":
                    prompt = soup.select_one(
                        "body > main > div.container > div:nth-child(7) > table > tbody > tr:nth-child("
                        + str(index + 1)
                        + ") > td:nth-child(2)"
                    )
                    result["seed"] = str(prompt.contents[0]).strip()

                if text == "clip_skip":
                    prompt = soup.select_one(
                        "body > main > div.container > div:nth-child(7) > table > tbody > tr:nth-child("
                        + str(index + 1)
                        + ") > td:nth-child(2)"
                    )
                    result["skip"] = str(prompt.contents[0]).strip()

                if text == "size":
                    prompt = soup.select_one(
                        "body > main > div.container > div:nth-child(7) > table > tbody > tr:nth-child("
                        + str(index + 1)
                        + ") > td:nth-child(2)"
                    )
                    result["size"] = str(prompt.contents[0]).strip()

                if text == "model_hash":
                    prompt = soup.select_one(
                        "body > main > div.container > div:nth-child(7) > table > tbody > tr:nth-child("
                        + str(index + 1)
                        + ") > td:nth-child(2)"
                    )
                    result["model"] = str(prompt.contents[0]).strip()

        except Exception as e:
            print("赋值result错误 ==> :", e)

        print("单数据", result)
        return result
