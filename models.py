from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import sql

import hashlib
import time
import shutil

# 数据库的路径
db_path = 'db.sqlite'
# 获取 app 的实例
app = Flask(__name__)
# 这个先不管，其实是 flask 用来加密 session 的东西
app.secret_key = 'random string'
# 配置数据库的打开方式
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///{}'.format(db_path)

db = SQLAlchemy(app)


# 数据库里面的一张表，是一个类
# 它继承自 db.Model
class User(db.Model):
    # 类的属性就是数据库表的字段
    # 这些都是内置的 __tablename__ 是表名
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    gender = db.Column(db.String())
    signature = db.Column(db.String())
    role = db.Column(db.Integer(), default=2)
    follower = db.Column(db.String(), default='' )
    followee = db.Column(db.String(), default='')
    created_time = db.Column(db.DateTime(timezone=True),
                             default=sql.func.now())
    # 这是引用别的表的数据的属性，表明了它关联的东西
    tweets = db.relationship('Tweet', backref='user')
    comments = db.relationship('Comment', backref='user')
    retweets = db.relationship('Retweet', backref='user')

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.gender = form.get('gender', '')
        self.signature = form.get('signature', '')
        self.role = form.get('role', 2)
        self.follow = ''
        self.followed = ''


    def __repr__(self):
        class_name = self.__class__.__name__
        return u'<{}: {}>'.format(class_name, self.id)

    @property
    def follower_lst(self):
        # 去掉字符串末尾逗号,如果有的话
        follower = self.follower[:-1]
        return follower.split(',') if follower is not '' else []

    @property
    def followee_lst(self):
        # 去掉字符串末尾逗号,如果有的话
        followee = self.followee[:-1]
        return followee.split(' ') if followee is not '' else []

    @property
    def follower_tweets(self):
        follower_tweets = []
        for i in self.follower_lst:
            i_user = User.query.filter_by(id=int(i)).first()
            follower_tweets += i_user.tweets
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

    def hash_password(self):
        s = self.password
        m = hashlib.md5()
        m.update(s.encode('utf-8'))
        result = m.hexdigest()
        self.password = result
        return


    def validate(self, user):
        if isinstance(user, User):
            username_equals = self.username == user.username
            password_equals = self.password == user.password
            return username_equals and password_equals
        else:
            return False


class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.DateTime(timezone=True), default=sql.func.now())
    retweet_from = db.Column(db.String(), default='')
    retweet_seen = db.Column(db.Integer(), default=0)
    retweets = db.relationship('Retweet', backref='tweet')
    comments = db.relationship('Comment', backref='tweet')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __init__(self, form):
        self.content = form.get('content', '')

    def __repr__(self):
        class_name = self.__class__.__name__
        return u'<{}: {}>'.format(class_name, self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.DateTime(timezone=True), default=sql.func.now())
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'))
    comment_replied = db.Column(db.Integer())
    user_replied = db.Column(db.String())
    reply_viewed = db.Column(db.Integer(), default=0)

    def __init__(self, form):
        self.content = form.get('content', '')


    def __repr__(self):
        class_name = self.__class__.__name__
        return u'<{}: {}>'.format(class_name, self.id)


    def save(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Retweet(db.Model):
    __tablename__ = 'retweets'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.DateTime(timezone=True), default=sql.func.now())
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'))


    def __init__(self, form):
        self.content = form.get('content', 'repost')


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


# 定义了数据库，如何创建数据库呢？
# 调用 db.create_all()
# 如果数据库文件已经存在了，则啥也不做
# 所以说我们先 drop_all 删除所有表
# 再重新 create_all 创建所有表
def rebuild_db():
    backup_db()
    db.drop_all()
    db.create_all()
    print('rebuild database')


# 第一次运行工程的时候没有数据库
# 所以我们运行 models.py 创建一个新的数据库文件
if __name__ == '__main__':
    rebuild_db()
