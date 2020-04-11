from flask import Blueprint

api = Blueprint('api', __name__, template_folder='../static')

from . import login, user, decorator, notification, tweet, repost, comment, follow
