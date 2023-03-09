from datetime import datetime

from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256
from werkzeug.security import check_password_hash

from app import db, login_manager
from app.model.template import TemplateHan, TemplatePersonal
from app.utils import format_datetime
from .role import Role

collections = db.Table(
    'collections',
    db.Column('template_han_id', db.Integer, db.ForeignKey('template_han.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

personals = db.Table(
    'personals',
    db.Column('template_personal_id', db.Integer, db.ForeignKey('template_personal.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    nickname = db.Column(db.String(50), default="")
    collected = db.Column(db.Text(3000), default="")
    avatar = db.Column(db.Text(300), default="")
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    favorites = db.relationship(
        "TemplateHan", secondary=collections, backref=db.backref("user", lazy='dynamic'), lazy='dynamic'
    )
    templates = db.relationship(
        "TemplatePersonal", secondary=personals, backref=db.backref("user", lazy='dynamic'), lazy='dynamic'
    )

    def __init__(self, *args, **kwargs):
        self.set_args(**kwargs)
        if self.role_id is None:
            role = Role.query.filter_by(default=True).first()
            self.role_id = role.get_id()

    def set_args(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_json(self):
        json_data = {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name != "password"
        }
        return json_data

    def row2dict(self):
        d = {}
        for column in self.__table__.columns:
            if column.name != "password":
                d[column.name] = str(getattr(self, column.name))

        favorites = []
        for i in self.favorites.all():
            i = i.to_json()
            i['create_time'] = format_datetime(i['create_time'])
            i['update_time'] = format_datetime(i['update_time'])
            favorites.append(i)
        d['favorites'] = favorites

        templates = []
        for t in self.templates.all():
            t = t.to_json()
            t['create_time'] = format_datetime(t['create_time'])
            t['update_time'] = format_datetime(t['update_time'])
            templates.append(t)
        d['templates'] = templates
        return d

    def verify_password(self, password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """获取用户ID"""
        return self.id

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {"message": "{} row(s) deleted".format(num_rows_deleted)}
        except Exception as e:
            return {"message": "Something went wrong"}

    @staticmethod
    def return_all():
        def to_json(x):
            return {"username": x.username, "password": x.password}

        return {"users": list(map(lambda x: to_json(x), User.query.all()))}

    @staticmethod
    def generate_hash(password):
        p_hash = pbkdf2_sha256.hash(str(password))
        return p_hash

    @staticmethod
    def verify_hash(password, password_hash):
        return pbkdf2_sha256.verify(str(password), password_hash)

    def add_favorite(self, tid):
        t = TemplateHan.query.get(tid)
        self.favorites.append(t)

    def del_favorite(self, tid):
        t = TemplateHan.query.get(tid)
        self.favorites.remove(t)

    def is_favorite(self, tid):
        favorites = self.favorites.all()
        tem_list = list(filter(lambda tem: tem.id == tid, favorites))
        if len(tem_list) > 0:
            return True
        else:
            return False

    def add_template(self, name):
        t = TemplatePersonal.query.filter_by(name=name).first()
        print(t.to_json())
        self.templates.append(t)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
