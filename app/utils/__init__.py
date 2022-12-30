import logging
import os.path
import sys

import requests
from PIL import Image
from flask import jsonify


def progress_bar(current, total):
    print("\r", end="")
    print(f"当前已处理: {current} : {total} ", "▋" * (int(current / total * 30)), end="")
    if current == total:
        print(" 处理完毕")
    sys.stdout.flush()


class JsonResponse:
    def __init__(self, data):
        self.data = data

    @classmethod
    def success(cls, data):
        return jsonify({"msg": "success", "code": 200, "data": data})

    @classmethod
    def error(cls, data):
        if hasattr(data, "msg"):
            msg = data["msg"]
        else:
            msg = "error"
        return jsonify({"msg": msg, "code": 500, "data": data})


class CompressImage:
    def __init__(self, static_path, dir_name, quality):
        self.static_path = static_path
        self.dir_name = dir_name
        self.quality = quality

    def compress_image(self):
        all_images = os.listdir(self.static_path + self.dir_name)
        total = 0
        for image_name in all_images:
            old_size = self.get_image_size(self.get_current_image_path(image_name))
            img = Image.open(self.get_current_image_path(image_name))
            x, y = img.size
            if x > 300:
                min_x = 300
                min_y = int(y * min_x / x)
                min_img = img.resize((min_x, min_y), Image.ANTIALIAS)
                min_img.save(self.get_out_path(image_name), quality=self.quality)
                new_size = self.get_image_size(self.get_out_path(image_name))
                total = total + 1
                print("压缩前大小" + str(old_size) + "-" + "压缩后大小" + str(new_size))
            else:
                img.save(self.get_out_path(image_name), quality=80)
                new_size = self.get_image_size(self.get_out_path(image_name))
                total = total + 1
                print("压缩前大小" + str(old_size) + "-" + "压缩后大小" + str(new_size))
        return total

    @staticmethod
    def get_image_size(image_path):
        size = os.path.getsize(image_path)
        return size / 1024

    def get_current_image_path(self, image_name):
        out_path = self.static_path + self.dir_name + "/"
        if not os.path.exists(out_path):
            print("图片存储目录不存在")
            os.makedirs(out_path)
            print(str(out_path) + "图片存储目录创建成功")
        return out_path + image_name

    def get_out_path(self, image_name):
        out_path = self.static_path + "min_" + self.dir_name + "/"
        if not os.path.exists(out_path):
            print("压缩图片存储目录不存在")
            os.makedirs(out_path)
            print(str(out_path) + "压缩图片存储目录创建成功")
        return out_path + image_name


class DeepDanbooru:
    def __init__(self):
        self.model_url = "https://huggingface.co/chinoll/deepdanbooru/resolve/main/deepdanbooru.onnx"
        self.tags_url = "https://huggingface.co/chinoll/deepdanbooru/resolve/main/tags.txt"
        self.base_path = 'app/static/danbooru'
        self.file_path = self.base_path + '/deepdanbooru.onnx'
        self.tags_path = self.base_path + '/tags.txt'

    def create_dir(self):
        if not os.path.exists(self.base_path):
            logging.warning("danbooru文件夹不存在")
            os.makedirs(self.base_path)

    def create_file(self):
        if not os.path.exists(self.file_path):
            logging.warning("deepdanbooru.onnx文件不存在")
            with open(self.file_path, 'a+', encoding='utf-8') as f:
                f.write("")

    def download_file(self):
        try:
            url = self.model_url
            r = requests.get(url, stream=True)
            print(r)
            size = 0
            chunk_size = 1024
            content_size = int(r.headers['content-length'])
            if r.status_code == 200:
                print('开始下载,已下载:{size:.2f} MB'.format(size=content_size / chunk_size / 1024))
                with open(self.file_path, "wb") as file:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if chunk:
                            file.write(chunk)
                            size += len(chunk)
                            print('\r' + '下载进度:%s%.2f%%' % (
                                '>' * int(size * 50 / content_size), float(size / content_size * 100)), end=' ')
        except:
            logging.error("下载danbooru出现错误")

    def download_tags(self):
        try:
            url = self.tags_url
            r = requests.get(url, stream=True)
            size = 0
            chunk_size = 1024
            content_size = int(r.headers['content-length'])
            if r.status_code == 200:
                print('开始下载,已下载:{size:.2f} MB'.format(size=content_size / chunk_size / 1024))
                with open(self.tags_path, "wb") as file:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if chunk:
                            file.write(chunk)
                            size += len(chunk)
                            print('\r' + '下载进度:%s%.2f%%' % (
                                '>' * int(size * 50 / content_size), float(size / content_size * 100)), end=' ')
        except:
            logging.error("下载danbooru出现错误")
