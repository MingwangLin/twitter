import hashlib
import time
from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import make_response
from flask import abort
from flask import session
from flask import flash
from functools import wraps
from models import User
from models import Tweet
from models import Comment
from models import At
from treelog import log


app = Flask(__name__)
app.secret_key = 'tree'


@app.template_filter('format_time')
def format_time(timestamp):
    t = timestamp
    format = '%Y/%m/%d %H:%M'
    t = time.localtime(timestamp)
    ft = time.strftime(format, t)
    return ft


# 通过 session 来获取当前登录的用户
def current_user():
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first()
    return user


def hash_password(pwd):
    m = hashlib.md5()
    m.update(pwd.encode('utf-8'))
    result = m.hexdigest()
    return result


def requires_login(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        # f 是被装饰的函数
        # 所以下面两行会先于被装饰的函数内容调用
        user = current_user()
        if current_user() is None:
            return redirect(url_for('login_view'))
        return f(*args, **kwargs)
    return wrapped


def requires_admin(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        # f 是被装饰的函数
        # 所以下面两行会先于被装饰的函数内容调用
        print('debug, requires_login')
        user = current_user()
        if user.role != 1:
            # return abort(401)
            return abort(404)
        return f(*args, **kwargs)

    return wrapped


@app.route('/')
def index():
    return redirect(url_for('login_view'))


# 显示登录界面的函数  GET
@app.route('/login')
def login_view():
    return render_template('login.html')


# 处理登录请求  POST
@app.route('/login', methods=['POST'])
def login():
    u = User(request.form)
    u.password = hash_password(u.password)
    user = User.query.filter_by(username=u.username).first()
    if user.validate(u):
        log("用户登录成功")
        # 用 make_response 生成响应 并且设置 cookie
        session['user_id'] = user.id
        return redirect(url_for('timeline_view', username=user.username))
    else:
        flash('登陆失败')
        log("用户登录失败", user)
        return redirect(url_for('login_view'))


# 处理注册的请求  POST
@app.route('/register', methods=['POST'])
def register():
    u = User(request.form)
    usr = User.query.filter_by(username=u.username).first()
    if u.valid() and usr is None:
        log("用户注册成功")
        u.password = hash_password(u.password)
        # 保存到数据库
        u.save()
        user = User.query.filter_by(username=u.username).first()
        session['user_id'] = user.id
        return redirect(url_for('timeline_view', username=user.username))
    else:
        flash('注册失败')
        return redirect(url_for('login_view'))


# 显示某个用户的时间线  GET
@app.route('/timeline/<username>')
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
        retweet_from = Tweet.query.filter_by(retweet_from=user.username)
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


# 处理关注用户函数
@app.route('/follow/<user_id>')
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
    return redirect(url_for('timeline_view', username=user.username ))


# 处理取消关注用户函数
@app.route('/unfollow/<user_id>')
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
    return redirect(url_for('timeline_view', username=user.username ))


#显示所有用户信息
@app.route('/admin/users')
def users_view():
    users = User.query.all()
    return render_template('users_view.html', users=users)


#删除用户
@app.route('/admin/users/delete/<user_id>')
@requires_admin
def user_delete(user_id):
    user = current_user()
    u = User.query.filter_by(id=user_id).first()
    u.delete()
    return redirect(url_for('users_view'))


##显示更新用户的界面
@app.route('/admin/users/update/<user_id>')
@requires_login
@requires_admin
def user_update_view(user_id):
    user = current_user()
    u = User.query.filter_by(id=user_id).first()
    return render_template('user_edit.html', user=u)



# 处理更新用户的请求
@app.route('/admin/users/update/<user_id>', methods=['POST'])
@requires_login
@requires_admin
def user_update(user_id):
    user = current_user()
    u = User.query.filter_by(id=user_id).first()
    u.password = request.form.get('password', '')
    u.save()
    return redirect(url_for('users_view'))


# 显示单条微博的界面
@app.route('/tweets/<tweet_id>')
@requires_login
def tweet_view(tweet_id):
    t = Tweet.query.filter_by(id=tweet_id).first()
    u = current_user()
    return render_template('single_tweet_view.html', t=t, u=u)


# 解析微博/评论内容,得到所有@的用户名
def get_name(s):
    # 用'//@'切片, 得到转发微博中用户原创内容
    if '//@' in s:
        s = s.partition('//@')[0]
    #内容后面加上' ', 方便解析
    # 得到所有@的用户名
    name_lst = []
    s += ' '
    while s.find('@') != -1:
        i = s.find('@')
        j = s.find(' ', i)
        log(i, j)
        name_lst.append(s[i+1:j])
        s = s[j+1:]
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


# 显示转发的界面
@app.route('/tweet/retweet/<tweet_id>')
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


# 处理 发送 微博的函数  POST
@app.route('/tweet/add', methods=['POST'])
def tweet_add():
    user = current_user()
    t = Tweet(request.form)
    # 设置是谁发的
    t.user = user
    # 保存到数据库
    t.save()
    # 获取微博中@的用户名
    if '@' in t.content:
        name_lst = get_name(t.content)
        At_lst(lst=name_lst, tweet=t)
    return redirect(url_for('timeline_view', username=user.username))


# 处理转发的函数
@app.route('/tweet/retweet/<tweet_id>', methods=['POST'])
@requires_login
def retweet_add(tweet_id):
    user = current_user()
    tweet = Tweet.query.filter_by(id=tweet_id).first()
    t = Tweet(request.form)
    # 用户转发微博时, 原微博写入文本框供用户编辑,最右微博在文本框中隐藏以防被编辑。
    # 转发微博存入数据库之前添加添加最右微博
    if '//@' in tweet.content:
        content = t.content + tweet.content.rpartition('//@')[1] + tweet.content.rpartition('//@')[2]
    else:
        content = t.content + '//@' + tweet.user.username + ':' + tweet.content
    t.user = user
    t.content = content
    t.retweet_from = tweet.id
    t.save()
    name_lst = get_name(t.content)
    At_lst(lst=name_lst, tweet=t)
    return redirect(url_for('tweet_view', tweet_id=t.id))


# 显示发送评论的界面
@app.route('/tweet/comment/<tweet_id>')
def comment_add_view(tweet_id):
    user = current_user()
    tweet = Tweet.query.filter_by(id=tweet_id).first()
    if user is None:
        return redirect(url_for('login_view'))
    else:
        return render_template('comment_add.html', tweet=tweet)


# 处理发送评论的函数
@app.route('/tweet/comment/<tweet_id>', methods=['POST'])
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
@app.route('/tweet/reply/<comment_id>')
@requires_login
def reply_add_view(comment_id):
    user = current_user()
    comment = Comment.query.filter_by(id=comment_id).first()
    return render_template('reply_add.html', comment=comment)


# 处理发送回复的函数
@app.route('/tweet/reply/<comment_id>', methods=['POST'])
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


# 查看通知中的回复
@app.route('/reply/view/<comment_id>')
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
@app.route('/reply/discard/<comment_id>')
@requires_login
def notification_discard(comment_id):
    user = current_user()
    comment = Comment.query.filter_by(id=comment_id).first()
    # 回复被忽略, 字段值标记设为1
    comment.reply_viewed = 1
    comment.save()
    return redirect(url_for('timeline_view', username=user.username))

# 查看微博中的@
@app.route('/tweet/at/view/<a_id>')
@requires_login
def tweet_at_view(a_id):
    user = current_user()
    a = At.query.filter_by(id=a_id).first()
    # @被查看后, 字段值标记为1
    a.at_viewed = 1
    a.save()
    return render_template('at_view.html', a=a, c=None)


# 忽略微博中的@
@app.route('/tweet/at/discard/<a_id>')
@requires_login
def tweet_at_discard(a_id):
    user = current_user()
    a = At.query.filter_by(id=a_id).first()
    # 回复被忽略, 字段值标记设为1
    a.at_viewed = 1
    a.save()
    return redirect(url_for('timeline_view', username=user.username))


# 查看评论中的@
@app.route('/comment/at/view/<a_id>')
@requires_login
def comment_at_view(a_id):
    a = At.query.filter_by(id=a_id).first()
    c = Comment.query.filter_by(id=a.comment_id).first()
    # @被查看后, 字段值标记为1
    a.at_viewed = 1
    a.save()
    return render_template('at_view.html', a=a, c=c)


# 忽略评论中的@
@app.route('/comment/at/discard/<a_id>')
@requires_login
def comment_at_discard(a_id):
    user = current_user()
    a = At.query.filter_by(id=a_id).first()
    # 回复被忽略, 字段值标记设为1
    a.at_viewed = 1
    a.save()
    return redirect(url_for('timeline_view', username=user.username))

# 显示 更新 微博的界面
@app.route('/tweet/update/<tweet_id>')
def tweet_update_view(tweet_id):
    t = Tweet.query.filter_by(id=tweet_id).first()
    if t is None:
        abort(404)
    # 获取当前登录的用户, 如果用户没登录或者用户不是这条微博的主人, 就返回 401 错误
    user = current_user()
    if user is None or user.id != t.user_id:
        abort(401)
    else:
        return render_template('tweet_edit.html', tweet=t)


# 处理 更新 微博的请求
@app.route('/tweet/update/<tweet_id>', methods=['POST'])
def tweet_update(tweet_id):
    t = Tweet.query.filter_by(id=tweet_id).first()
    if t is None:
        abort(404)
    # 获取当前登录的用户, 如果用户没登录或者用户不是这条微博的主人, 就返回 401 错误
    user = current_user()
    if user is None or user.id != t.user_id:
        abort(401)
    else:
        t.content = request.form.get('content', '')
        t.save()
        return redirect(url_for('timeline_view', username=user.username))


# 处理 删除 微博的请求
@app.route('/tweet/delete/<tweet_id>')
def tweet_delete(tweet_id):
    t = Tweet.query.filter_by(id=tweet_id).first()
    if t is None:
        abort(404)
    # 获取当前登录的用户, 如果用户没登录或者用户不是这条微博的主人, 就返回 401 错误
    user = current_user()
    if user is None or user.id != t.user_id:
        abort(401)
    else:
        t.delete()
        return redirect(url_for('timeline_view', username=user.username))


if __name__ == '__main__':
    host, port = '127.0.0.1', 5000
    args = {
        'host': host,
        'port': port,
        'debug': True,
    }
    app.run(**args)

# 数据库有个功能叫做索引
# 索引就是一个 字段：id 的字典
# 这样你就能够通过 字段 查找到 id
# 然后实现 O(1) 的快速查询