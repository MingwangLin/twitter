from flask import abort
from flask import jsonify
from flask import session

from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from .treelog import log
from .login import hash_password

from ..models import At, Comment, User, Tweet
from . import api
from .decorator import requires_login, requires_admin, current_user
import random
import string
from .notification import At_lst, get_name



# 显示某个用户的主页  GET
@api.route('/timeline/<username>')
@requires_login
def timeline_view(username):
    # 查找 username 对应的用户
    user = current_user()
    u = User.query.filter_by(username=username).first()
    if u is None:
        abort(404)
    else:

        # 我关注的人微博, 取前20条微博显示
        followee_tweets = u.followee_tweets[:20]
        # 回复我的所有评论
        replies_to_me = Comment.query.filter_by(user_replied=user.username)
        # @我的所有微博
        ats_to_me = At.query.filter_by(reciever_id=user.id).all
        follower_lst = u.follower_lst
        followee_lst = u.followee_lst
        args = {
            'user': user,
            'u': u,
            'follower_lst': follower_lst,
            'followee_lst': followee_lst,
            'followee_tweets': followee_tweets,
            'replies_to_me': replies_to_me,
            'ats_to_me': ats_to_me,
        }
        return render_template('timeline_bs.html', **args)


# 用ajax显示某个用户的时间线  GET
@api.route('/tweets/<username>')
@requires_login
def timeline_ajax(username):
    # 查找 username 对应的用户
    visitor = current_user()
    host = User.query.filter_by(username=username).first()
    if host is None:
        abort(404)
    else:
        args = request.args
        offset = args.get('mytweets_offset', 0)
        offset = int(offset)
        limit = args.get('mytweets_limit', 20)
        limit = int(limit)
        tweets = host.tweets
        tweets.sort(key=lambda t: t.created_time, reverse=True)
        tweets = tweets[offset:offset + limit]
        tweets = [t.json() for t in tweets]
        filtered_tweets = {
            'success':True,
            'host': host.json(),
            'visitor': visitor.json(),
            'tweets': tweets,

        }
        log('filtered_tweets', filtered_tweets)
        return jsonify(filtered_tweets)

# 用ajax显示关注人微博时间线  GET
@api.route('/followee_tweets/<username>')
@requires_login
def timeline_followee(username):
    # 查找 username 对应的用户
    visitor = current_user()
    host = User.query.filter_by(username=username).first()
    if host is None:
        abort(404)
    else:
        args = request.args
        offset = args.get('offset', 0)
        log('offset', offset)
        offset = int(offset)
        limit = args.get('limit', 20)
        limit = int(limit)
        # 我关注的人微博
        followee_tweets = visitor.followee_tweets
        followee_tweets = followee_tweets[offset:offset + limit]
        log('followee_tweets', followee_tweets)
        followee_tweets = [t.json() for t in followee_tweets]
        filtered_tweets = {
            'success':True,
            'host': host.json(),
            'visitor': visitor.json(),
            'followee_tweets': followee_tweets


        }
        log('filtered_tweets', filtered_tweets)
        return jsonify(filtered_tweets)



# 删除用户
@api.route('/admin/users/delete/<user_id>')
@requires_admin
def user_delete(user_id):
    user = current_user()
    u = User.query.filter_by(id=user_id).first()
    u.delete()
    return redirect(url_for('users_view'))


##显示更新用户的界面
@api.route('/admin/users/update/<user_id>')
@requires_login
@requires_admin
def user_update_view(user_id):
    user = current_user()
    u = User.query.filter_by(id=user_id).first()
    return render_template('user_edit.html', user=u)


# 处理更新用户的请求
@api.route('/admin/users/update/<user_id>', methods=['POST'])
@requires_login
@requires_admin
def user_update(user_id):
    user = current_user()
    u = User.query.filter_by(id=user_id).first()
    u.password = request.form.get('password', '')
    u.save()
    return redirect(url_for('users_view'))

def string_generator():
    size = 4
    #chars = string.ascii_uppercase + string.digits
    chars = string.digits

    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


# 自动创建用户
@api.route('/testuser', methods=['GET'])
def user_create():
    form = {
        'username':'游客' + string_generator(),
        'password': string_generator(),
    }
    user = User(form)
    default_list = '1 2'
    # 写入关注人信息
    user.followee = default_list
    user.password = hash_password(user.password)
    # 保存到数据库
    user.save()
    user = User.query.filter_by(username=user.username).first()
    session['user_id'] = user.id
    # 向该用户发送@通知供测试
    words = '欢迎来访'
    content = '@' + user.username + ' ' + words
    form = {
        'content': content
    }
    t = Tweet(form)
    sender_id = '1'
    sender_user = User.query.filter_by(id=sender_id).first()
    t.user = sender_user
    t.save()
    # 根据解析微博得到的@的用户名数组, 生成相应的At实例, 存入数据库
    if '@' in t.content:
        name_lst = get_name(t.content)
        At_lst(lst=name_lst, tweet=t)
    log('t.ats', t.ats)
    created_user = {
        'success': True,
        'user': user.json(),
        'message':'登录成功',

    }
    return jsonify(created_user)

