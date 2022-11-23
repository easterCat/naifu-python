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
    id = db.Column('template_id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(80))
    desc = db.Column(db.String(150))

    def __init__(self, name, prompt, author='', desc=''):
        self.name = name
        self.prompt = prompt
        self.author = author
        self.desc = desc
