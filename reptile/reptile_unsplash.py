import requests


class DownloadUnsplash(object):

    def __init__(self):
        self.target = 'https://unsplash.com/napi/photos?per_page=12&page=3&xp=search-quality-boosting%3Acontrol'
        self.images = []

    def download(self):
        print("开始下载")
        req = requests.get(url=self.target)
        print(req.text)


if __name__ == '__main__':
    d = DownloadUnsplash()
    d.download()
