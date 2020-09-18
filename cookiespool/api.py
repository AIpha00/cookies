import json
from flask import Flask, g, render_template
from flask import request, jsonify, make_response
from cookiespool.config import *
from cookiespool.db import *

__all__ = ['app']

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('taobao.html')


def get_conn():
    """
    获取
    :return:
    """
    for website in GENERATOR_MAP:
        if not hasattr(g, website):
            setattr(g, website + '_cookies', eval('RedisClient' + '("cookies", "' + website + '")'))
            setattr(g, website + '_accounts', eval('MongoCli' + '()'))
    return g


@app.route('/<website>/random')
def random(website):
    """
    获取随机的Cookie, 访问地址如 /taobao/random
    :return: 随机Cookie
    """
    g = get_conn()
    cookies = getattr(g, website + '_cookies').random()
    return cookies


@app.route('/<website>/insert')
def insert(website):
    """
    添加用户, 访问地址如 /weibo/add/user/password
    :param website: 站点
    :param username: 用户名
    :param password: 密码
    :return: 
    """
    g = get_conn()
    params = request.args  # 获取请求正文
    encrypt = params.get('encrypt')
    password = params.get('password')
    username = params.get('username')
    getattr(g, website + '_accounts').set(username=username, password=password, encrypt=encrypt, website=website)
    response = make_response(jsonify({'code': True, 'msg': '入库成功'}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/<website>/count')
def count(website):
    """
    获取Cookies总数
    """
    g = get_conn()
    count = getattr(g, website + '_cookies').count()
    return json.dumps({'status': '1', 'count': count})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
