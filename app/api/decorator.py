from functools import wraps

from flask import abort
from flask import redirect
from flask import session
from flask import url_for

from ..models import User
from .treelog import log


# 通过 session 来获取当前登录的用户
def current_user():
    user_id = session['user_id']
    log('user__id', user_id)
    user = User.query.filter_by(id=user_id).first()
    log('user', user)
    return user

#  比如处理发表评论、发表微博的那些路由函数，都需要验证当前登录的用户是哪个用户，验证的程序都是一样的，如果每个路由函数都写一遍的话，整个程序会很臃肿，而且不利于修改和维护。
# 这时候就可以把这个验证程序抽象出来，写成一个装饰器，然后用这个装饰器把其他需要用到这个验证程序的路由函数包起来。这样整个程序的结构就会很简明。
def requires_login(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        # f 是被装饰的函数
        # 所以下面两行会先于被装饰的函数内容调用
        user = current_user()
        if user is None:
            return redirect(url_for('api.login_view'))
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
