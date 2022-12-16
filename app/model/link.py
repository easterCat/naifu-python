from app import db


class Link(db.Model):
    __tablename__ = 'link'
    id = db.Column('link_id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    href = db.Column(db.String(230), nullable=False)
    link_type = db.Column(db.String(50))
    hot = db.Column(db.Boolean())
    icon = db.Column(db.String(230))
    desc = db.Column(db.Text(300))

    def __init__(self, name, href, link_type, hot=False, icon='', desc=''):
        super(Link, self).__init__()
        self.name = name
        self.href = href
        self.link_type = link_type
        self.icon = icon
        self.hot = hot
        self.desc = desc

    def to_json(self):
        json_data = {
            'id': self.id,
            'href': self.href,
            'name': self.name,
            'link_type': self.link_type,
            'icon': self.icon,
            'hot': self.hot,
            'desc': self.desc,
        }
        return json_data
