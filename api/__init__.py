from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')

from . import login, user, decorator, notification, tweet, retweet, comment, follow

