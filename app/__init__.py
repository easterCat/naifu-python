from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 跨域
    CORS(app)
    # 数据库
    db.init_app(app)

    # 主程序注入
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 路由注入
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
