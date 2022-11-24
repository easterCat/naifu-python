from flask import Blueprint

api = Blueprint('api', __name__, static_folder='static')

from app.api import translate, database