from app import db




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
