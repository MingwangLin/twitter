from flask import abort
from flask import jsonify
from flask import session

from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from .treelog import log
from .login import hash_password

from ..models import At, Comment, User, Tweet, Follow
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
    visitor = current_user()
    host = User.query.filter_by(username=username).first()
    if host is None:
        abort(404)
    else:
        args = {
            'visitor': visitor,
            'host': host,
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
        # args = request.args
        # offset = args.get('offset', 0)
        # offset = int(offset)
        # limit = args.get('limit', 20)
        # limit = int(limit)
        # tweets = host.tweets
        # tweets.sort(key=lambda t: t.created_time, reverse=True)
        # tweets = tweets[offset:offset + limit]
        # tweets = [t.json() for t in tweets]
        args = request.args
        page = args.get('page', 1, type=int)
        log('p', request.args)
        pagination = Tweet.query.filter_by(user_id=host.id).order_by(
            Tweet.created_time.desc()).paginate(
            page, error_out=False)
        tweets = pagination.items
        log('items', tweets)
        tweets = [i.json() for i in tweets]
        filtered_tweets = {
            'success': True,
            'host': host.json(),
            'visitor': visitor.json(),
            'tweets': tweets,

        }
        # log('filtered_tweets', filtered_tweets)
        return jsonify(filtered_tweets)


# 用ajax显示关注人微博时间线  GET
@api.route('/followedtweets/<username>')
@requires_login
def timeline_followed(username):
    # 查找 username 对应的用户
    visitor = current_user()
    host = User.query.filter_by(username=username).first()
    if host is None:
        abort(404)
    else:
        args = request.args
        page = args.get('page', 1, type=int)
        log('p', request.args)
        pagination = Tweet.query. \
            join(Follow, Follow.followed_id == Tweet.user_id) \
            .filter(Follow.follower_id == visitor.id).order_by(
            Tweet.created_time.desc()).paginate(
            page, error_out=False)
        followed_tweets = pagination.items
        log('f', followed_tweets)
        tweets = [i.json() for i in followed_tweets]
        filtered_tweets = {
            'success': True,
            'host': host.json(),
            'visitor': visitor.json(),
            'tweets': tweets

        }
        log('filtered_tweets', filtered_tweets)
        return jsonify(filtered_tweets)

# 用ajax上传用户头像
@api.route('/upload/avatars', methods=['POST'])
@requires_login
def upload_avatars():
    user = current_user()
    # uploaded 是上传时候的文件名
    file = request.files.get('uploaded')
    log('upload, ', request.files)
    r = {
        'success': True,
        'code': '成功',
        'data': {

        }
    }
    if file:
        filename = file.filename
        log('filename, ', filename)
        path = '/static/avatars/' + filename
        abs_path = '/Users/linmingwang/twitter/app' + path
        file.save(abs_path)
        user.avatar = path
        user.save()
        r['data'] = '/timeline/{}'.format(user.username)
    else:
        r['success'] = False
    return jsonify(r)



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
    # chars = string.ascii_uppercase + string.digits
    chars = string.digits

    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


# 自动创建用户
@api.route('/testuser', methods=['GET'])
def user_create():
    form = {
        'username': '游客' + string_generator(),
        'password': string_generator(),
    }
    user = User(form)
    # 写入关注人信息
    user.password = hash_password(user.password)
    # 保存到数据库
    user.save()
    user = User.query.filter_by(username=user.username).first()
    admin = User.query.filter_by(id=1).first()
    f = Follow(user, admin)
    f.save()
    session['user_id'] = user.id
    # 向该用户发送@通知供测试
    words = 'welcome!'
    content = '@' + user.username + ' ' + words
    form = {
        'content': content
    }
    t = Tweet(form)
    sender_id = '1'
    sender_user = User.query.filter_by(id=sender_id).first()
    # t.user = sender_user
    t.user_id = sender_id
    t.save()
    # 根据解析微博得到的@的用户名数组, 生成相应的At实例, 存入数据库
    name_lst = get_name(t.content)
    At_lst(lst=name_lst, tweet=t)
    log('t.ats', t.ats)
    created_user = {
        'success': True,
        'user': user.json(),
        'message': '登录成功',
    }
    return jsonify(created_user)
