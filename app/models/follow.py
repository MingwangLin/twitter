from . import db
from . import ReprMixin

import time

class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    created_time = db.Column(db.Integer(), default=0)


    def __init__(self, follower, followed):
        super(Follow, self).__init__()
        self.follower_id = follower.id
        self.followed_id = followed.id
        self.created_time = int(time.time())

    def json(self):
        d = {
        'follower_id': self.follower_id,
        'followee_id': self.followee_id,
        'created_time': self.created_time,
        }
        return d

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()
