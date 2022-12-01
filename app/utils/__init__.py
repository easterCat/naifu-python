import os.path
from PIL import Image

from flask import jsonify


class JsonResponse:
    def __init__(self, data):
        self.data = data

    @classmethod
    def success(cls, data):
        return jsonify({
            'msg': 'success',
            'code': 200,
            'data': data
        })

    @classmethod
    def error(cls, data):
        return jsonify({
            'msg': 'error',
            'code': 500,
            'data': data
        })


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
                print('压缩前大小' + str(old_size) + '-' + '压缩后大小' + str(new_size))
            else:
                img.save(self.get_out_path(image_name), quality=80)
                new_size = self.get_image_size(self.get_out_path(image_name))
                total = total + 1
                print('压缩前大小' + str(old_size) + '-' + '压缩后大小' + str(new_size))
        return total

    @staticmethod
    def get_image_size(image_path):
        size = os.path.getsize(image_path)
        return size / 1024

    def get_current_image_path(self, image_name):
        out_path = self.static_path + self.dir_name + '/'
        if not os.path.exists(out_path):
            print('图片存储目录不存在')
            os.makedirs(out_path)
        return out_path + image_name

    def get_out_path(self, image_name):
        out_path = self.static_path + 'min_' + self.dir_name + '/'
        if not os.path.exists(out_path):
            print('压缩图片存储目录不存在')
            os.makedirs(out_path)
        return out_path + image_name
