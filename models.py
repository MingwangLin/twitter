from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import sql
from . import ReprMixin


import time
import shutil


db_path = 'db.sqlite'
app = Flask(__name__)
app.secret_key = 'random string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class User(db.Model, ReprMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    role = db.Column(db.Integer(), default=2)
    follower = db.Column(db.String(), default='')
    followee = db.Column(db.String(), default='')
    created_time = db.Column(db.Integer(), default=0)
    # 这是引用别的表的数据的属性，表明了它关联的东西
    tweets = db.relationship('Tweet', backref='user')
    comments = db.relationship('Comment', backref='user')
    ats = db.relationship('At', backref='user')

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.created_time = int(time.time())

    def __repr__(self):
        class_name = self.__class__.__name__
        return u'<{}: {}>'.format(class_name, self.id)

    @property
    def follower_lst(self):
        # 去掉字符串首尾空格
        follower = self.follower.strip()
        return follower.split() if follower is not '' else []

    @property
    def followee_lst(self):
        followee = self.followee.strip()
        return followee.split() if followee is not '' else []

    @property
    def follower_tweets(self):
        follower_tweets = []
        for i in self.follower_lst:
            user = User.query.filter_by(id=int(i)).first()
            follower_tweets += user.tweets
        return follower_tweets

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    # 验证注册用户的合法性
    def valid(self):
        username_len = len(self.username) >= 1
        password_len = len(self.password) >= 1
        return username_len and password_len

    def validate(self, user):
        if isinstance(user, User):
            username_equals = self.username == user.username
            password_equals = self.password == user.password
            return username_equals and password_equals
        else:
            return False


class Tweet(db.Model, ReprMixin):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.Integer(), default=0)
    comments = db.relationship('Comment', backref='tweet')
    retweets = db.relationship('Retweet', backref='tweet')

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
        extra = dict(
            user_id=self.user_id,
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


class Comment(db.Model, ReprMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.Integer(), default=0)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'))
    comment_replied = db.Column(db.Integer())
    user_replied = db.Column(db.String())
    reply_viewed = db.Column(db.Integer(), default=0)
    ats = db.relationship('At', backref='comment')

    def __init__(self, form):
        super(Comment, self).__init__()
        self.content = form.get('content', '')
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

class Retweet(db.Model, ReprMixin):
    __tablename__ = 'retweets'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.Integer(), default=0)
    tweet_id = db.Column(db.Integer(), db.ForeignKey('tweets.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __init__(self, form):
        super(Retweet, self).__init__()
        self.content = form.get('content', '')
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


def backup_db():
    backup_path = '{}.{}'.format(time.time(), db_path)
    shutil.copyfile(db_path, backup_path)


def rebuild_db():
    backup_db()
    db.drop_all()
    db.create_all()
    print('rebuild database')


if __name__ == '__main__':
    rebuild_db()
