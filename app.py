from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import make_response
from flask import abort
from flask import session
from flask import flash


from models import User
from models import Tweet
from models import Comment
from models import Retweet
from treelog import log


app = Flask(__name__)
app.secret_key = 'tree'



# 通过 session 来获取当前登录的用户
def current_user():
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first()
    return user


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
    user = User.query.filter_by(username=u.username).first()
    if user.validate(u):
        log("用户登录成功")
        # 用 make_response 生成响应 并且设置 cookie
        session['user_id'] = user.id
        return redirect(url_for('timeline_view', username=user.username))
    else:
        log("用户登录失败", user)
        return redirect(url_for('login_view'))


# 处理注册的请求  POST
@app.route('/register', methods=['POST'])
def register():
    u = User(request.form)
    if u.valid():
        log("用户注册成功")

        u.hash_password()
        # 保存到数据库
        u.save()
        user = User.query.filter_by(username=u.username).first()
        session['user_id'] = user.id
        return redirect(url_for('timeline_view', username=user.username))
    else:
        flash('注册失败')
        log('注册失败', request.form)
        return redirect(url_for('login_view'))


# 显示某个用户的时间线  GET
@app.route('/timeline/<username>')
def timeline_view(username):
    # 查找 username 对应的用户
    u = User.query.filter_by(username=username).first()
    if u is None:
        abort(404)
    else:
        user = current_user()
        # 我的微博
        tweets = u.tweets
        tweets.sort(key=lambda t: t.created_time, reverse=True)
        # 我关注的人微博
        follower_tweets = u.follower_tweets
        follower_tweets.sort(key=lambda t: t.created_time, reverse=True)
        # 回复我的所有评论
        replies_to_me = Comment.query.filter_by(user_replied=user.username)
        follower_lst = u.follower_lst
        followee_lst = u.followee_lst
        args = {
            'tweets': tweets,
            'user': user,
            'u': u,
            'follower_lst': follower_lst,
            'followee_lst': followee_lst,
            'follower_tweets': follower_tweets,
            'replies_to_me': replies_to_me
        }
        return render_template('timeline.html', **args)


# 处理关注用户函数
@app.route('/follow/<user_id>')
def user_follow(user_id):
    user = User.query.filter_by(id=user_id).first()
    u = current_user()
    if u is None:
        return redirect(url_for('login_view'))
    # 关注人信息,被关注人信息写入表中相应字段
    usr_id = str(user.id) + ','
    u_id = str(u.id) + ','
    u.follower += usr_id
    user.followee += u_id
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
def user_delete(user_id):
    user = current_user()
    if user.role != 1:
        abort(401)
    u = User.query.filter_by(id=user_id).first()
    u.delete()
    return redirect(url_for('users_view'))

##显示更新用户的界面
@app.route('/admin/users/update/<user_id>')
def user_update_view(user_id):
    user = current_user()
    if user is None:
        return redirect(url_for('login_view'))
    elif user.role != 1:
        abort(401)
    else:
        u = User.query.filter_by(id=user_id).first()
        return render_template('user_edit.html', user=u)


# 处理更新用户的请求
@app.route('/admin/users/update/<user_id>', methods=['POST'])
def user_update(user_id):
    user = current_user()
    if user is None:
        return redirect(url_for('login_view'))
    elif user.role != 1:
        abort(401)
    else:
        u = User.query.filter_by(id=user_id).first()
        u.password = request.form.get('password', '')
        u.save()
        return redirect(url_for('users_view'))




# 处理 发送 微博的函数  POST
@app.route('/tweet/add', methods=['POST'])
def tweet_add():
    user = current_user()
    if user is None:
        return redirect(url_for('login_view'))
    else:
        t = Tweet(request.form)
        # 设置是谁发的
        t.user = user
        # 保存到数据库
        t.save()
        log('t.user_id', t.user_id)
        log('t.comments', t.comments)
        return redirect(url_for('timeline_view', username=user.username))


# 显示单条微博的界面
@app.route('/tweets/<tweet_id>')
def tweet_view(tweet_id):
    t = Tweet.query.filter_by(id=tweet_id).first()
    u = current_user()
    if u is None:
        return redirect(url_for('login_view'))
    else:
        log(t.user.username, u.username)
        return render_template('single_tweet_view.html', t=t, u=u)


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
def comment_add(tweet_id):
    user = current_user()
    tweet = Tweet.query.filter_by(id=tweet_id).first()
    u = tweet.user
    print(u)
    if user is None:
        return redirect(url_for('login_view'))
    else:
        c = Comment(request.form)
        # 谁发的
        c.user = user
        c.user_id = user.id
        # 发到哪条微博
        c.tweet = tweet
        c.tweet_id = tweet.id
        # 保存到数据库
        c.save()
        log('c.tweet_id', c.tweet_id)
        log('c.user_id', c.tweet_id)

        return redirect(url_for('tweet_view', tweet_id=tweet.id))


# 显示转发的界面
@app.route('/tweet/retweet/<tweet_id>')
def retweet_add_view(tweet_id):
    user = current_user()
    tweet = Tweet.query.filter_by(id=tweet_id).first()
    if user is None:
        return redirect(url_for('login_view'))
    else:
        return render_template('retweet_add.html', tweet=tweet)


# 处理转发的函数
@app.route('/tweet/retweet/<tweet_id>', methods=['POST'])
def retweet_add(tweet_id):
    user = current_user()
    tweet = Tweet.query.filter_by(id=tweet_id).first()
    u = tweet.user
    print(u)
    if user is None:
        return redirect(url_for('login_view'))
    else:
        r = Retweet(request.form)
        # 谁转发的
        r.user = user
        r.user_id = user.id
        # 转发哪条微博
        r.tweet = tweet
        r.tweet_id = tweet.id
        # 转发微博信息
        t = Tweet(request.form)
        tweet_content_before = '//' + tweet.user.username + ':' + tweet.content
        t.content += tweet_content_before
        t.user = user
        t.user_id = user.id
        r.save()
        t.save()
        # 到本微博为止原始微博转发路线
        tweet_id_str = str(tweet.id) + ','
        t.retweet_from += tweet_id_str
        r.save()
        t.save()

        return redirect(url_for('tweet_view', tweet_id=tweet.id))




# 显示发送回复的界面
@app.route('/tweet/reply/<comment_id>')
def reply_add_view(comment_id):
    user = current_user()
    comment = Comment.query.filter_by(id=comment_id).first()
    if user is None:
        return redirect(url_for('login_view'))
    else:
        return render_template('reply_add.html', comment=comment)


# 处理发送回复的函数
@app.route('/tweet/reply/<comment_id>', methods=['POST'])
def reply_add(comment_id):
        user = current_user()
        comment = Comment.query.filter_by(id=comment_id).first()
        tweet = comment.tweet
        if user is None:
            return redirect(url_for('login_view'))
        else:
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
            return redirect(url_for('tweet_view', tweet_id=tweet.id))


# 查看通知中的回复
@app.route('/reply/view/<comment_id>')
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
    if user is None:
        return redirect(url_for('login_view'))
    else:
        return render_template('notification_view.html', c=c, comment=comment)

# 忽略通知中的回复
@app.route('/reply/discard/<comment_id>')
def notification_discard(comment_id):
    user = current_user()
    comment = Comment.query.filter_by(id=comment_id).first()
    # 回复被忽略, 字段值标记设为1
    comment.reply_viewed = 1
    comment.save()
    if user is None:
        return redirect(url_for('login_view'))
    else:
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