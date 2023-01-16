from datetime import datetime

from app import db


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    role_name = db.Column(db.String(64), unique=True, index=True)
    default = db.Column(db.Boolean, default=False, index=True)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __init__(self, *args, **kwargs):
        self.set_args(**kwargs)

    def set_args(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_json(self):
        json_data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return json_data

    def get_id(self):
        """获取用户ID"""
        return self.id
