from treelog import log
from models import User
from flask import request
from flask import session
from flask import jsonify
from flask import redirect
from flask import url_for
from flask import render_template

from . import api

import hashlib


def hash_password(pwd):
    m = hashlib.md5()
    m.update(pwd.encode('utf-8'))
    result = m.hexdigest()
    return result

@api.route('/')
def index():
    return redirect(url_for('api.login_view'))


# 显示登录界面的函数  GET
@api.route('/login')
def login_view():
    return render_template('login.html')


# 处理登录请求  POST
@api.route('/login', methods=['POST'])
def login():
    account = request.get_json()
    log('account', account)
    u = User(account)
    u.password = hash_password(u.password)
    user = User.query.filter_by(username=u.username).first()
    r = {
        'success': True,
        'message': '登录成功',
        'code': '成功',
        'data': {

        }
    }
    if user.validate(u):
        log("用户登录成功")
        # 用 make_response 生成响应 并且设置 cookie
        session['user_id'] = user.id
        r['data'] = '/timeline/{}'.format(user.username)
    else:
        r['success'] = False
        r['message'] = '登录失败'
    return jsonify(r)


# 处理注册的请求  POST
@api.route('/register', methods=['POST'])
def register():
    account = request.get_json()

    data = request.get_data()
    '''
    json_string = data.decode('utf-8')
    d = json.loads(json_string)
    log('json_string', json_string)
    log('d', d)
    '''
    log('account', account)
    log('data', data)

    u = User(account)
    usr = User.query.filter_by(username=u.username).first()
    r = {
        'success': True,
        'message': '注册成功',
        'code': '成功',
        'data': {

        }
    }
    if u.valid() and usr is None:
        log("用户注册成功")
        u.password = hash_password(u.password)
        # 保存到数据库
        u.save()
        user = User.query.filter_by(username=u.username).first()
        session['user_id'] = user.id
        r['data'] = '/timeline/{}'.format(u.username)
    else:
        r['success'] = False
        r['message'] = '注册失败'
    return jsonify(r)
