from flask import abort
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from .treelog import log
from ..models import At, Comment, User
from . import api
from .decorator import requires_login, requires_admin, current_user


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
        follower_tweets = u.follower_tweets[:20]
        follower_tweets.sort(key=lambda t: t.created_time, reverse=True)
        # 回复我的所有评论
        replies_to_me = Comment.query.filter_by(user_replied=user.username)
        # @我的所有微博
        ats_to_me = At.query.filter_by(reciever_id=user.id)
        follower_lst = u.follower_lst
        followee_lst = u.followee_lst
        args = {
            'user': user,
            'u': u,
            'follower_lst': follower_lst,
            'followee_lst': followee_lst,
            'follower_tweets': follower_tweets,
            'replies_to_me': replies_to_me,
            'ats_to_me': ats_to_me,
        }
        return render_template('timeline_bs.html', **args)


# 用ajax显示某个用户的时间线  GET
@api.route('/tweets/json/<username>')
@requires_login
def timeline_ajax(username):
    # 查找 username 对应的用户
    visitor = current_user()
    host = User.query.filter_by(username=username).first()
    if host is None:
        abort(404)
    else:
        args = request.args
        offset = args.get('offset', 0)
        offset = int(offset)
        limit = args.get('limit', 20)
        limit = int(limit)
        tweets = host.tweets
        tweets.sort(key=lambda t: t.created_time, reverse=True)
        tweets = tweets[offset:offset + limit]
        tweets = [t.json() for t in tweets]
        filtered_tweets = {
            'host': host.json(),
            'visitor': visitor.json(),
            'tweets': tweets,

        }
        log('filtered_tweets', filtered_tweets)
        return jsonify(filtered_tweets)

# 用ajax显示关注人微博时间线  GET
@api.route('/followee_tweets/json/<username>')
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
        offset = int(offset)
        limit = args.get('limit', 20)
        limit = int(limit)
        # 我关注的人微博
        followee_tweets = visitor.follower_tweets[offset:offset + limit]
        followee_tweets.sort(key=lambda t: t.created_time, reverse=True)
        followee_tweets = [t.json() for t in followee_tweets]
        filtered_tweets = {
            'follower_tweets': followee_tweets

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
