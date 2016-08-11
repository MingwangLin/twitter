from . import db
from . import ReprMixin
import time

class Repost(db.Model, ReprMixin):
    __tablename__ = 'reposts'
    repost_id = db.Column(db.Integer, db.ForeignKey('tweets.id'),
                            primary_key=True)
    reposted_id = db.Column(db.Integer, db.ForeignKey('tweets.id'),
                            primary_key=True)
    created_time = db.Column(db.Integer(), default=0)

    def __init__(self, repost_tweet, reposted_tweet):
        super(Repost, self).__init__()
        self.repost_id = reposted_tweet.id
        self.reposted_id = reposted_tweet.id
        self.created_time = int(time.time())

    def json(self):
        d = {
        'reposter_id': self.reposter_id,
        'reposted_id': self.reposted_id,
        'created_time': self.created_time,
        }
        return d

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()
