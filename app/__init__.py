from flask import Flask
from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)

    # 跨域
    CORS(app)

    # 数据库
    #
    # HOMENAME = "localhost"
    # PORT = 3306
    # USERNAME = 'root'
    # PASSWORD = '123456789'
    # DATABASE = 'novalai'
    # app.config[
    #     'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOMENAME}:{PORT}/{DATABASE}?charset=utf8"
    # db = SQLAlchemy(app)
    #
    # with app.app_context():
    #     with db.engine.connect() as conn:
    #         rs = conn.execute("select 1")
    #         print(rs.fetchone())

    # 路由注入
    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
