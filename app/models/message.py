from . import db
from . import ReprMixin

import time

class At(db.Model, ReprMixin):
    __tablename__ = 'ats'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer(), default=0)
    reciever_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    at_viewed = db.Column(db.Integer(), default=0)

    def __init__(self):
        super(At, self).__init__()
        self.created_time = int(time.time())

    def __repr__(self):
        class_name = self.__class__.__name__
        return u'<{}: {}>'.format(class_name, self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()