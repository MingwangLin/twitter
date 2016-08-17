from . import db
from . import ReprMixin
from .user import User
from .tweet import Tweet


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

    def json(self):
        sender_id = Tweet.query.filter_by(id=self.tweet_id).first().user_id
        t= Tweet.query.filter_by(id=self.tweet_id).first()
        comments_length = len(Tweet.query.filter_by(id=self.tweet_id).first().comments)
        sender_name = User.query.filter_by(id=sender_id).first().username
        avatar_path = User.query.filter_by(id=sender_id).first().avatar
        tweet_content = Tweet.query.filter_by(id=self.tweet_id).first().content
        extra = dict(
            reciever_id = self.reciever_id,
            tweet_id = self.tweet_id,
            sender_name = sender_name,
            tweet_content = tweet_content,
            comments_length = comments_length,
            avatar_path = avatar_path,
            t = t.json()
        )
        d = {k: v for k, v in self.__dict__.items() if k not in self.blacklist()}
        d.update(extra)
        return d

    def blacklist(self):
        b = [
            '_sa_instance_state',
        ]
        return b
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
