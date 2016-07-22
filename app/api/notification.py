from flask import redirect
from flask import render_template
from flask import url_for

from .treelog import log
from ..models import At, Comment, User
from . import api
from .decorator import requires_login, current_user


# 解析微博/评论内容,得到所有@的用户名/
def get_name(s):
    # 用'//@'切片, 得到微博中用户原创内容
    if '//@' in s:
        s = s.partition('//@')[0]
    # 内容后面加上' ', 方便解析
    # 得到所有@的用户名
    name_lst = []
    s += ' '
    while s.find('@') != -1:
        i = s.find('@')
        j = s.find(' ', i)
        log(i, j)
        name_lst.append(s[i + 1:j])
        s = s[j + 1:]
    return name_lst


# 根据解析微博得到的@的用户名数组, 生成相应的At实例, 存入数据库
def At_lst(lst, tweet):
    for i in lst:
        u = User.query.filter_by(username=i).first()
        if u is not None:
            a = At()
            a.tweet = tweet
            a.tweet_id = tweet.id
            a.user = u
            a.reciever_id = u.id
            a.save()
    return


# 根据解析评论得到的@的用户名数组, 生成相应的At实例, 存入数据库
def comment_At_lst(lst, comment):
    for i in lst:
        u = User.query.filter_by(username=i).first()
        if u is not None:
            a = At()
            a.comment = comment
            a.comment_id = comment.id
            a.user = u
            a.reciever_id = u.id
            a.save()
    return


# 查看通知中的回复
@api.route('/reply/view/<comment_id>')
@requires_login
def notification_view(comment_id):
    user = current_user()
    # 回复的评论
    comment = Comment.query.filter_by(id=comment_id).first()
    # 被回复的评论
    c_id = comment.comment_replied
    c = Comment.query.filter_by(id=c_id).first()
    # 回复被查看后, 字段值标记为1
    comment.reply_viewed = 1
    comment.save()
    return render_template('notification_view.html', c=c, comment=comment)


# 忽略通知中的回复
@api.route('/reply/discard/<comment_id>')
@requires_login
def notification_discard(comment_id):
    user = current_user()
    comment = Comment.query.filter_by(id=comment_id).first()
    # 回复被忽略, 字段值标记设为1
    comment.reply_viewed = 1
    comment.save()
    return redirect(url_for('timeline_view', username=user.username))


# 查看微博中的@
@api.route('/tweet/at/view/<a_id>')
@requires_login
def tweet_at_view(a_id):
    user = current_user()
    a = At.query.filter_by(id=a_id).first()
    # @被查看后, 字段值标记为1
    a.at_viewed = 1
    a.save()
    return render_template('at_view.html', a=a, c=None)


# 忽略微博中的@
@api.route('/tweet/at/discard/<a_id>')
@requires_login
def tweet_at_discard(a_id):
    user = current_user()
    a = At.query.filter_by(id=a_id).first()
    # 回复被忽略, 字段值标记设为1
    a.at_viewed = 1
    a.save()
    return redirect(url_for('timeline_view', username=user.username))


# 查看评论中的@
@api.route('/comment/at/view/<a_id>')
@requires_login
def comment_at_view(a_id):
    a = At.query.filter_by(id=a_id).first()
    c = Comment.query.filter_by(id=a.comment_id).first()
    # @被查看后, 字段值标记为1
    a.at_viewed = 1
    a.save()
    return render_template('at_view.html', a=a, c=c)


# 忽略评论中的@
@api.route('/comment/at/discard/<a_id>')
@requires_login
def comment_at_discard(a_id):
    user = current_user()
    a = At.query.filter_by(id=a_id).first()
    # 回复被忽略, 字段值标记设为1
    a.at_viewed = 1
    a.save()
    return redirect(url_for('timeline_view', username=user.username))
