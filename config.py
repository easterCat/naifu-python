import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'this is secret key'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # 数据库
    # HOSTNAME = "localhost"
    HOSTNAME = "134.195.211.222"
    PORT = 3306
    USERNAME = 'root'
    # PASSWORD = '123456789'
    PASSWORD = 'Jp940612'
    DATABASE = 'novalai'
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class ProductionConfig(Config):
    # 数据库
    HOSTNAME = "localhost"
    PORT = 3306
    USERNAME = 'root'
    PASSWORD = '123456789'
    DATABASE = 'novalai'
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
