from models import Retweet

from models import Tweet
from flask import render_template
from flask import redirect
from treelog import log
from flask import url_for
from models import User
from flask import Blueprint
from flask import request
from flask import session
from flask import jsonify
from .user import current_user
from flask import session
from .decorator import requires_login, requires_admin, current_user
from api import api
from .notification import At_lst, get_name


# 显示转发的界面
@api.route('/tweet/retweet/<tweet_id>')
@requires_login
def retweet_add_view(tweet_id):
    user = current_user()
    tweet = Tweet.query.filter_by(id=tweet_id).first()
    # 用户转发微博时, 微博写入文本框供用户编辑,最右微博在文本框中隐藏以防被编辑。
    if '//@' in tweet.content:
        content_shown = '//@' + tweet.user.username + ':' + tweet.content.rpartition('//@')[0]
    else:
        content_shown = ''
    return render_template('retweet_add.html', tweet=tweet, content_shown=content_shown)


# 处理转发的函数
# 用户转发微博时, 原微博写入文本框供用户编辑,最右微博在文本框中隐藏以防被编辑。
# 转发微博存入数据库之前添加最右微博
@api.route('/tweet/retweet/<tweet_id>', methods=['POST'])
@requires_login
def retweet_add(tweet_id):
    user = current_user()
    # 被转发微博
    tweet = Tweet.query.filter_by(id=tweet_id).first()
    # 转发微博实例
    t = Tweet(request.form)
    c = tweet.content
    # 存入数据库之前添加添加最右微博
    if '//@' in c:
        # 最右微博内容
        tweet_first_content = c.rpartition(':')[2]
        log('tweet_first_content', tweet_first_content)
        content = t.content + '//@' + tweet_first_content
        # 转发最右微博 实例
        r = Retweet(request.form)
        r.content = content
        r.user = user
        r.user_id = user.id
        tweet_first = Tweet.query.filter_by(content=tweet_first_content).first()
        log('tweet_first', tweet_first)
        r.tweet = tweet_first
        r.tweet_id = tweet_first.id
        r.save()
        log('tweet_first', tweet_first.retweets)

    else:
        content = t.content + '//@' + tweet.user.username + ':' + c
    t.user = user
    t.content = content
    t.save()
    name_lst = get_name(t.content)
    At_lst(lst=name_lst, tweet=t)
    r = Retweet(request.form)
    r.user = user
    r.user_id = user.id
    r.tweet = tweet
    r.tweet_id = tweet.id
    r.save()
    return redirect(url_for('api.tweet_view', tweet_id=t.id))
