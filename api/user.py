from flask import abort
from models import Comment
from models import At
from flask import render_template
from flask import redirect
from treelog import log
from flask import url_for
from models import User
from flask import request
from flask import jsonify
from flask import session
from .decorator import requires_login, requires_admin, current_user
from api import api


# 显示某个用户的时间线  GET
@api.route('/timeline/<username>')
@requires_login
def timeline_view(username):
    # 查找 username 对应的用户
    user = current_user()
    u = User.query.filter_by(username=username).first()
    if u is None:
        abort(404)
    else:
        # 我的微博
        tweets = u.tweets
        tweets.sort(key=lambda t: t.created_time, reverse=True)
        # 我关注的人微博
        follower_tweets = u.follower_tweets
        follower_tweets.sort(key=lambda t: t.created_time, reverse=True)
        # 回复我的所有评论
        replies_to_me = Comment.query.filter_by(user_replied=user.username)
        # @我的所有微博
        ats_to_me = At.query.filter_by(reciever_id=user.id)
        follower_lst = u.follower_lst
        followee_lst = u.followee_lst
        args = {
            'tweets': tweets,
            'user': user,
            'u': u,
            'follower_lst': follower_lst,
            'followee_lst': followee_lst,
            'follower_tweets': follower_tweets,
            'replies_to_me': replies_to_me,
            'ats_to_me': ats_to_me,
        }
        return render_template('timeline.html', **args)


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
