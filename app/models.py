from sqlalchemy import false

from app import db


class Template(db.Model):
    __tablename__ = 'template'
    id = db.Column('template_id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120))
    preview = db.Column(db.Text(300))
    prompt = db.Column(db.Text(3000), nullable=False)
    prompt_zh = db.Column(db.Text(3000))
    n_prompt = db.Column(db.Text(3000))
    n_prompt_zh = db.Column(db.Text(3000))
    step = db.Column(db.String(60))
    sampler = db.Column(db.String(80))
    scale = db.Column(db.String(60))
    seed = db.Column(db.String(60))
    skip = db.Column(db.String(60))
    size = db.Column(db.String(60))
    model = db.Column(db.String(80))
    path = db.Column(db.Text(300))
    desc = db.Column(db.String(150))
    like = db.Column(db.Integer)
    like_address = db.Column(db.Text(3000))
    category = db.Column(db.String(80))

    def __init__(self, name, prompt, author='', preview='', prompt_zh='', n_prompt='', n_prompt_zh='', step='',
                 sampler='',
                 scale='', desc='', seed='', skip='', size='', model='', path='', like=0, like_address='',
                 category=''):
        self.name = name
        self.author = author
        self.preview = preview
        self.prompt = prompt
        self.prompt_zh = prompt_zh
        self.n_prompt = n_prompt
        self.n_prompt_zh = n_prompt_zh
        self.step = step
        self.sampler = sampler
        self.seed = seed
        self.scale = scale
        self.skip = skip
        self.size = size
        self.model = model
        self.path = path
        self.like = like
        self.like_address = like_address
        self.desc = desc
        self.category = category

    def to_json(self):
        server = 'http://www.ptg.life/static/'
        # server = 'http://172.18.234.34:5000/static/'
        if 'original_i2i' in self.preview:
            minify_preview = self.preview.replace('https://www.ptsearch.info/media/article/original_i2i/',
                                                  server + 'media/article/min_original_i2i/')
        else:
            minify_preview = self.preview.replace('https://www.ptsearch.info/media/article/original/',
                                                  server + 'media/article/min_original/')

        if 'original_i2i' in self.preview:
            preview = self.preview.replace('https://www.ptsearch.info/media/article/original_i2i/',
                                           server + 'media/article/original_i2i/')
        else:
            preview = self.preview.replace('https://www.ptsearch.info/media/article/original/',
                                           server + 'media/article/original/')

        json_data = {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'preview': preview,
            'minify_preview': minify_preview,
            'prompt': self.prompt,
            'prompt_zh': self.prompt_zh,
            'n_prompt': self.n_prompt,
            'n_prompt_zh': self.n_prompt_zh,
            'step': self.step,
            'sampler': self.sampler,
            'seed': self.seed,
            'scale': self.scale,
            'skip': self.skip,
            'size': self.size,
            'model': self.model,
            'path': self.path,
            'like': self.like,
            # 'like_address': self.like_address,
            'desc': self.desc,
            'category': self.category,
        }
        return json_data


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column('category_id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50))
    desc = db.Column(db.String(150))
    nsfw = db.Column(db.String(10))

    def __init__(self, name, author='', desc='', nsfw='0'):
        self.name = name
        self.author = author
        self.desc = desc
        self.nsfw = nsfw


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column('tag_id', db.Integer, primary_key=True, autoincrement=True)
    zh = db.Column(db.String(150), nullable=False)
    en = db.Column(db.String(180), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50))
    desc = db.Column(db.String(150))
    nsfw = db.Column(db.String(10))

    def __init__(self, zh, en, category, author='', desc='', nsfw='0'):
        self.zh = zh
        self.en = en
        self.category = category
        self.author = author
        self.desc = desc
        self.nsfw = nsfw


class Link(db.Model):
    __tablename__ = 'link'
    id = db.Column('link_id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    href = db.Column(db.String(230), nullable=False)
    link_type = db.Column(db.String(50))
    hot = db.Column(db.Boolean())

    def __init__(self, name, href, link_type, hot=False):
        super(Link, self).__init__()
        self.name = name
        self.href = href
        self.link_type = link_type
        self.hot = hot

    def to_json(self):
        json_data = {
            'id': self.id,
            'href': self.href,
            'name': self.name,
            'link_type': self.link_type,
            'hot': self.hot,
        }
        return json_data
