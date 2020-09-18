import json
import requests
from requests.exceptions import ConnectionError
from cookiespool.db import *
from login.taobao.login import UsernameLogin


class ValidTester(object):
    """
    对cookie的生命周期进行检测
    """
    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = MongoCli()

    def test(self, username, cookies):
        raise NotImplementedError

    def run(self):
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)


class TaobaoValidTester(ValidTester):
    def __init__(self, website='taobao'):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):
        print('正在测试Cookies', '用户名', username)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('Cookies不合法', username)
            self.cookies_db.delete(username)
            print('删除Cookies', username)
            return
        try:
            res_username, status = UsernameLogin(username, '').test_cookies_login(cookies)
            if status:
                print('Cookies有效', res_username)
            else:
                print('Cookies失效', username)
                self.cookies_db.delete(username)
                print('删除Cookies', username)
        except ConnectionError as e:
            print('发生异常', e.args)


if __name__ == '__main__':
    TaobaoValidTester().run()
