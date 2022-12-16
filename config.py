import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "11122233"
    JWT_SECRET_KEY = "999888777"
    JWT_BLOCKLIST_TOKEN_CHECKS = ["access", "refresh"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    ENV = "dev"
    DEBUG = True
    # 数据库
    HOSTNAME = "localhost"
    PORT = 3306
    USERNAME = "root"
    PASSWORD = "123456789"
    DATABASE = "novalai"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class TestConfig(Config):
    ENV = "test"
    DEBUG = True
    # 数据库
    HOSTNAME = "localhost"
    PORT = 3306
    USERNAME = "root"
    PASSWORD = "123456789"
    DATABASE = "novalai"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class ProductionConfig(Config):
    ENV = "prod"
    DEBUG = False
    # 数据库
    HOSTNAME = "134.195.211.222"
    PORT = 3306
    USERNAME = "root"
    PASSWORD = "Jp940612"
    DATABASE = "novalai"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    "development": DevelopmentConfig,
    "testing": TestConfig,
    "production": ProductionConfig,
}
