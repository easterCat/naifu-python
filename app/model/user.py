from datetime import datetime

from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256
from werkzeug.security import check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    nickname = db.Column(db.String(50), default="")
    collected = db.Column(db.Text(3000), default="")
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __init__(self, *args, **kwargs):
        self.set_args(**kwargs)
        if self.role_id is None:
            role = Role.query.filter_by(default=True).first()
            self.role_id = role.get_id()

    def set_args(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }

        return {'users': list(map(lambda x: to_json(x), User.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        p_hash = pbkdf2_sha256.hash(str(password))
        return p_hash

    @staticmethod
    def verify_hash(password, password_hash):
        return pbkdf2_sha256.verify(str(password), password_hash)

    def to_json(self):
        json_data = {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name != 'password'
        }
        return json_data

    def row2dict(self):
        d = {}
        for column in self.__table__.columns:
            if column.name != 'password':
                d[column.name] = str(getattr(self, column.name))

        return d

    def verify_password(self, password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """获取用户ID"""
        return self.id


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    role_name = db.Column(db.String(64), unique=True, index=True)
    default = db.Column(db.Boolean, default=False, index=True)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        self.set_args(**kwargs)

    def set_args(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_json(self):
        json_data = {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
        }
        return json_data

    def get_id(self):
        """获取用户ID"""
        return self.id


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
