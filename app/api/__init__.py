from flask import Blueprint

api = Blueprint('api', __name__, static_folder='static')

from . import login, student, translate, database, helloworld
