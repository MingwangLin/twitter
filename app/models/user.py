from . import db
from . import ReprMixin

import time

class User(db.Model, ReprMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    role = db.Column(db.Integer(), default=2)
    follower = db.Column(db.String(), default='')
    followee = db.Column(db.String(), default='')
    created_time = db.Column(db.Integer(), default=0)
    tweets = db.relationship('Tweet', backref='user')
    comments = db.relationship('Comment', backref='user')
    ats = db.relationship('At', backref='user')

    @staticmethod
    def user_by_name(username):
        return User.query.filter_by(username=username).first()

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.created_time = int(time.time())

    def __repr__(self):
        class_name = self.__class__.__name__
        return u'<{}: {}>'.format(class_name, self.id)

    @property
    def followee_lst(self):
        # 去掉字符串首尾空格
        followee = self.followee.strip()
        return followee.split() if followee is not '' else []

    @property
    def follower_lst(self):
        follower = self.follower.strip()
        return follower.split() if follower is not '' else []

    @property
    def followee_tweets(self):
        followee_tweets = []
        for i in self.followee_lst:
            user = User.query.filter_by(id=int(i)).first()
            followee_tweets += user.tweets
        followee_tweets.sort(key=lambda t: t.created_time, reverse=True)
        return followee_tweets

    def json(self):
        # Model 是延迟载入的, 如果没有引用过数据, 就不会从数据库中加载
        # 引用一下 id 这样数据就从数据库中载入了
        self.id
        d = {k: v for k, v in self.__dict__.items() if k not in self.blacklist()}
        return d

    def blacklist(self):
        b = [
            '_sa_instance_state',
            'password',
            'tweets'
        ]
        return b

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


