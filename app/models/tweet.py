from . import db
from . import ReprMixin
from .user import User
from .repost import Repost

import time


class Tweet(db.Model, ReprMixin):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.Integer(), default=0)
    comments = db.relationship('Comment', backref='tweet')
    reposted = db.relationship('Repost',
                               foreign_keys=[Repost.repost_id],
                               backref=db.backref('repost', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    reposts = db.relationship('Repost',
                              foreign_keys=[Repost.reposted_id],
                              backref=db.backref('reposted', lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')
    ats = db.relationship('At', backref='tweet')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, form):
        super(Tweet, self).__init__()
        self.content = form.get('content', '')
        self.created_time = int(time.time())

    def __repr__(self):
        class_name = self.__class__.__name__
        return u'<{}: {}>'.format(class_name, self.id)

    def json(self):
        extra = {
                'user_id': self.user_id,
                'user_name': User.query.filter_by(id=self.user_id).first().username,
                'comments': [i.json() for i in self.comments],
                'avatar': User.query.filter_by(id=self.user_id).first().avatar,
                'original_tweet': []
            }
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
