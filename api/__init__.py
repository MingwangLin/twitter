from flask import Blueprint

api = Blueprint('ap', __name__)

from . import login, user, decorator, notification, tweet, retweet, comment, follow



