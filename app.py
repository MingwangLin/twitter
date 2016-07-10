import time
from flask import redirect
from flask import url_for
from flask import Flask
from api import api
from flask import render_template


app = Flask(__name__)
app.secret_key = 'tree'

app.register_blueprint(api)


@app.template_filter('format_time')
def format_time(timestamp):
    t = timestamp
    format = '%Y/%m/%d %H:%M'
    t = time.localtime(timestamp)
    ft = time.strftime(format, t)
    return ft


@app.route('/')
def index():
    return redirect(url_for('login_view'))


# 显示登录界面的函数  GET
@app.route('/login')
def login_view():
    return render_template('login.html')


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
