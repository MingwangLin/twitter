from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from models import Tweet
from models import Comment
from flask import session
from api import api
from .decorator import requires_login, requires_admin, current_user
from .notification import comment_At_lst, get_name


# 显示发送评论的界面
@api.route('/tweet/comment/<tweet_id>')
def comment_add_view(tweet_id):
    user = current_user()
    tweet = Tweet.query.filter_by(id=tweet_id).first()
    if user is None:
        return redirect(url_for('login_view'))
    else:
        return render_template('comment_add.html', tweet=tweet)


# 处理发送评论的函数
@api.route('/tweet/comment/<tweet_id>', methods=['POST'])
@requires_login
def comment_add(tweet_id):
    user = current_user()
    tweet = Tweet.query.filter_by(id=tweet_id).first()
    u = tweet.user
    c = Comment(request.form)
    # 谁发的
    c.user = user
    c.user_id = user.id
    # 发到哪条微博
    c.tweet = tweet
    c.tweet_id = tweet.id
    # 保存到数据库
    c.save()
    if '@' in c.content:
        name_lst = get_name(c.content)
        comment_At_lst(lst=name_lst, comment=c)
    return redirect(url_for('tweet_view', tweet_id=tweet.id))


# 显示发送回复的界面
@api.route('/tweet/reply/<comment_id>')
@requires_login
def reply_add_view(comment_id):
    user = current_user()
    comment = Comment.query.filter_by(id=comment_id).first()
    return render_template('reply_add.html', comment=comment)


# 处理发送回复的函数
@api.route('/tweet/reply/<comment_id>', methods=['POST'])
@requires_login
def reply_add(comment_id):
    user = current_user()
    comment = Comment.query.filter_by(id=comment_id).first()
    tweet = comment.tweet
    c = Comment(request.form)
    # 谁发的
    c.user = user
    c.user_id = user.id
    # 发到哪条微博
    c.tweet = tweet
    c.tweet_id = tweet.id
    # 回复哪条评论
    c.comment_replied = comment_id
    # 回复哪位用户
    c.user_replied = comment.user.username
    c.save()
    if '@' in c.content:
        name_lst = get_name(c.content)
        comment_At_lst(lst=name_lst, comment=c)
    return redirect(url_for('tweet_view', tweet_id=tweet.id))
