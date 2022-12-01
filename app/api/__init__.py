from flask import Blueprint

api = Blueprint('api', __name__)

from app.api import translate, database, link, reptile, template
