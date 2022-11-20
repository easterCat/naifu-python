from flask import Blueprint

api = Blueprint('api', __name__)

from . import helloworld,login, student, translate
