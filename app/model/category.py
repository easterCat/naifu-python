from app import db


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column('category_id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50))
    desc = db.Column(db.String(150))
    nsfw = db.Column(db.String(10))

    def __init__(self, name, author, desc='', nsfw='0'):
        self.name = name
        self.author = author
        self.desc = desc
        self.nsfw = nsfw
