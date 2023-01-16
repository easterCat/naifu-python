import os

import pandas as pd
import requests


def upload_image(dir_name):
    print("当前目录" + dir_name)
    total = 0
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../app/", "static/media/article/", dir_name))
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    df = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "../app/", "static/csv/temp9.csv")))
    df_list = df.values.tolist()
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            search_index = find_index_in_list(df_list, file)
            files = {
                'image': ('image', open(path + "/" + file, 'rb')),
            }
            res = requests.post("https://api.imgbb.com/1/upload", data={
                "key": "ae9007d87ab99b8db40e2cb1fa07f0c1"
                       "",
                "name": file,
            }, files=files)

            if res.status_code == 200:
                res_json = res.json()
                data = res_json['data']
                df_list[search_index].append(data['url'])
                total = total + 1
                if total >= 3:
                    df1 = pd.DataFrame(
                        data=df_list,
                        columns=[
                            "index",
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
                            "imgbb_url",
                        ],
                    )
                    df1.to_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "../app/", "static/csv/temp99.csv")))
    df1 = pd.DataFrame(
        data=df_list,
        columns=[
            "index",
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
            "imgbb_url",
        ],
    )
    df1.to_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "../app/", "static/csv/temp99.csv")))
    print('总计' + str(total))  # 打印结果


def find_index_in_list(df_list, file_name):
    for (index, item) in enumerate(df_list):
        if file_name in item[3]:
            return index


# upload_image("min_hanwang_20230106")
upload_image("original_20221209")
