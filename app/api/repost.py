from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify
from flask import url_for
from . import api
from .treelog import log
from ..models import Repost, Tweet
from .decorator import requires_login, current_user
from .notification import At_lst, get_name


# 用ajax处理转发的函数
@api.route('/repost/add/<tweet_id>', methods=['POST'])
@requires_login
def add_repost(tweet_id):
    visitor = current_user()
    form = request.get_json()
    log('form', form)
    t = Tweet(form)
    # 设置是谁发的
    t.user = visitor
    tweet_reposted = Tweet.query.filter_by(id=tweet_id).first()
    c = tweet_reposted.content
    t.content = t.content + '//@' + tweet_reposted.user.username + ':' + c
    # 保存到数据库
    t.save()
    log('t1', t)
    log('t2', tweet_reposted)
    r = Repost(t.id, tweet_id)
    r.save()
    log('r', r)
    r = {
        'success': True,
        'tweet': t.json(),
        'user': visitor.json(),
    }
    # 获取微博中@的用户名, 生成相应的At实例, 存入数据库
    if '@' in t.content:
        name_lst = get_name(t.content)
        At_lst(lst=name_lst, tweet=t)
    return jsonify(r)


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
        r = Repost(request.form)
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
    r = Repost(request.form)
    r.user = user
    r.user_id = user.id
    r.tweet = tweet
    r.tweet_id = tweet.id
    r.save()
    return redirect(url_for('api.tweet_view', tweet_id=t.id))


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

# 用ajax显示转发微博
# @api.route('/reposts/<tweet_id>')
# @requires_login
# def timeline_reposts(tweet_id):
#     tweet = Tweet.query.filter_by(id=tweet_id).first()
#     args = request.args
#     page = args.get('page', 1, type=int)
#     log('p', request.args)
#     pagination = Tweet.query. \
#         join(Repost, Repost.reposted_id == Tweet.id) \
#         .filter(Repost.repost_id == tweet.id).order_by(
#         Tweet.created_time.desc()).paginate(
#         page, error_out=False)
#     reposts = pagination.items
#     log('f', reposts)
#     reposts = [i.json() for i in reposts]
#     reposts_perpage = {
#         'success': True,
#         'reposts': reposts
#
#     }
#     log('reposts_perpage', reposts_perpage)
#     return jsonify(reposts_perpage)
