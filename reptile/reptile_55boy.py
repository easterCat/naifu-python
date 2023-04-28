import json
import sys

import requests
from bs4 import BeautifulSoup


class Download55Boy(object):
    def __init__(self):
        self.server = 'https://55boy.com'
        self.links = []
        self.types = []
        self.total = 78

    def download(self):
        self.get_download_page()
        self.get_download_content()
        self.save_links_to_json()

    def get_download_page(self):
        for page in range(1, self.total):
            bf = self.request_html('{0}/page/{1}/'.format(self.server, page))
            html_a = bf.find_all('a', class_='ele-box')
            for a in html_a:
                self.links.append({
                    'link_title': a.get('title'),
                    'link_page': a.get('href'),
                })
        print("页面爬取完毕")

    def get_download_content(self):
        print("开始获取详情")
        length = len(self.links)
        for index, link in enumerate(self.links):
            sys.stdout.write("\r当前进度: {0}/{1}".format(index, length))
            sys.stdout.flush()
            bf = self.request_html(link['link_page'])
            # 获取访问地址
            div_links = bf.find('div', class_="links")
            html_a = div_links.find_all('a')
            href = html_a[0].get('href')
            # 获取描述详情
            desc = bf.find('div', class_="desc")
            html_p = desc.find('p')
            text = ''
            if html_p is not None:
                text = html_p.text
            # 获取分类
            html_box = bf.find('div', class_='ms')
            html_box_p = html_box.find_all('p')[5]
            html_box_p_a = html_box_p.find_all("a")[1]
            link_type = ''
            if html_box_p_a is not None:
                link_type = html_box_p_a.text

            link['link_url'] = href
            link['link_desc'] = text
            link['link_type'] = link_type

    def save_links_to_json(self):
        try:
            with open("55boy.json", 'w', encoding='utf-8') as f:
                json.dump(self.links, f, ensure_ascii=False)
            with open("55boy_type.json", 'w', encoding='utf-8') as f2:
                for item in self.links:
                    if item['link_type'] not in self.types:
                        self.types.append(item['link_type'])
                json.dump(self.types, f2, ensure_ascii=False)
        except IOError as e:
            print(e)
        print("保存json成功")

    @staticmethod
    def request_html(target):
        req = requests.get(url=target)
        html = req.text
        bf = BeautifulSoup(html, 'lxml')
        return bf


if __name__ == '__main__':
    d = Download55Boy()
    d.download()
