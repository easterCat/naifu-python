from flask import Flask
from flask_bootstrap import Bootstrap4
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import config

app = Flask(__name__)
jwt = JWTManager()
db = SQLAlchemy(session_options={"autoflush": False})
bootstrap = Bootstrap4()
login_manager = LoginManager()
login_manager.session_protection = "strong"


@app.route("/hello")
def hello():
    return "Hello, World!"


def create_app(config_name):
    # 解决上传文件过大413错误
    app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

    # config配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # bs样式
    bootstrap.init_app(app)
    # 用户登录管理
    login_manager.init_app(app)
    # 跨域
    CORS(app, resources={r"/*": {"origins": "*"}})
    # 数据库
    db.init_app(app)
    # 数据库迁移
    Migrate(app, db)
    # jwt
    jwt.init_app(app)
    # blueprint注入
    inject_blueprint(app)

    return app


def inject_blueprint(app):
    # 主程序注入
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    # 路由注入
    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint)
