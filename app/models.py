from sqlalchemy import false

from app import db


class Template(db.Model):
    __tablename__ = 'template'
    id = db.Column('template_id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    prompt = db.Column(db.Text(3000), nullable=False)
    n_prompt = db.Column(db.Text(3000), )
    step = db.Column(db.String(50), )
    scale = db.Column(db.String(50))
    author = db.Column(db.String(50))
    preview = db.Column(db.String(150))
    desc = db.Column(db.String(150))
    category = db.Column(db.String(100))

    def __init__(self, name, prompt, n_prompt='', step='', scale='', author='', preview='', desc='', category=''):
        self.name = name
        self.prompt = prompt
        self.n_prompt = n_prompt
        self.step = step
        self.scale = scale
        self.author = author
        self.preview = preview
        self.desc = desc
        self.category = category


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
