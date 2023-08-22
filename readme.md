# 版本

使用flask做prompt工具网站的后台

- python 3.8.15

## 创建虚拟环境

```commandline
python -m venv tag_venv 
source ./tag_venv/bin/activate
pip install -r requirements.txt
```

## 创建requirements.txt

- 使用freeze

```commandline
pip freeze > requirements.txt .
```

- 使用pipreqs

```commandline
pip install pipreqs
pipreqs --encoding utf-8 ./ --force
or
pipreqs ./ --force
```

## 同步数据库变更

```commandline
flask db init
export FLASK_APP=manage.py
flask db migrate -m 'change'
flask db upgrade
```

## gunicorn启动

```bazaar
gunicorn --config gunicorn.conf.py app:app
```

## 学习文档

- [w3cschool Flask 概述](https://www.w3cschool.cn/flask/flask_overview.html)
- [Flask Web Development github教程实例](https://github.com/miguelgrinberg/flasky)
- [docs Python 教程](https://docs.python.org/zh-cn/3/tutorial/index.html)
- [runoob Python 基础教程](https://www.runoob.com/python/python-tutorial.html)
- [nginx启动、退出、重启](https://juejin.cn/post/6844903941545656333)
- [Nginx location 正则](https://www.jianshu.com/p/403bab8fc34d)
- [Ubuntu安装MySQL8.0](https://www.cnblogs.com/shizhe99/p/14514642.html)
- [免费的代理地址](http://free-proxy.cz/en/proxylist/country/JP/all/ping/level2)
- [计算机相关技术资料整理](https://github.com/EZLippi/practical-programming-books)
- [DeepDanbooru是动漫风格的女孩图像标签估计系统](https://github.com/KichangKim/DeepDanbooru)
- [NGINX 配置](https://www.digitalocean.com/community/tools/nginx?global.app.lang=zhCN)
- [pip install deepdanbooru-onnx](https://github.com/chinoll/deepdanbooru_onnx)