from flask import render_template
from flask import redirect
from treelog import log
from flask import url_for
from models import User
from flask import session
from .decorator import requires_login, requires_admin, current_user
from api import api


# 处理关注用户函数
@api.route('/follow/<user_id>')
@requires_login
def user_follow(user_id):
    u = current_user()
    if current_user() is None:
        return redirect(url_for('login_view'))
    user = User.query.filter_by(id=user_id).first()
    # 关注人信息,被关注人信息写入表中相应字段
    usr_id = str(user.id) + ' '
    u_id = str(u.id) + ' '
    u.follower += usr_id
    user.followee += u_id
    u.save()
    user.save()
    return redirect(url_for('timeline_view', username=user.username))


# 处理取消关注用户函数
@api.route('/unfollow/<user_id>')
@requires_login
def user_unfollow(user_id):
    u = current_user()
    user = User.query.filter_by(id=user_id).first()
    # 关注人信息,被关注人信息从表中相应字段删除
    usr_id = str(user.id) + ' '
    u_id = str(u.id) + ' '
    u.follower = u.follower.strip(usr_id)
    user.followee = user.followee.strip(u_id)
    u.save()
    user.save()
    return redirect(url_for('timeline_view', username=user.username))


# 显示所有用户信息
@api.route('/admin/users')
def users_view():
    users = User.query.all()
    return render_template('users_view.html', users=users)
