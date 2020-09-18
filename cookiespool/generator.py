import json
from cookiespool.db import RedisClient, MongoCli
from login.taobao.login import UsernameLogin


class CookiesGenerator(object):
    def __init__(self, website='default'):
        """
        父类, 初始化一些对象
        :param website: 名称
        """
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = MongoCli()

    def __del__(self):
        pass

    def init(self):
        """
        初始化登陆时参数信息
        :return:
        """
        pass

    def new_cookies(self, username, password=''):
        """
        新生成Cookies，子类需要重写
        :param username: 用户名
        :param password: 密码
        :return:
        """
        raise NotImplementedError

    def process_cookies(self, cookies):
        """
        处理Cookies
        :param cookies:
        :return:
        """
        dict = {}
        for cookie in cookies:
            dict[cookie['name']] = cookie['value']
        return dict

    def run(self):
        """
        运行, 得到所有账户, 然后顺次模拟登录
        :return:
        """
        accounts_usernames = self.accounts_db.usernames()
        cookies_usernames = self.cookies_db.usernames()

        for username in accounts_usernames:
            if not username in cookies_usernames:
                username = username.get('username', '')
                print('正在生成Cookies', '账号', username)
                result = self.new_cookies(username)
                # 成功获取
                if result.get('status') == 1:
                    cookies = result.get('content')
                    print('成功获取到Cookies', cookies)
                    if self.cookies_db.set(username, json.dumps(cookies)):
                        print('成功保存Cookies')
                # 密码错误，移除账号
                elif result.get('status') == 2:
                    print(result.get('content'))
                    if self.accounts_db.delete(username):
                        print('成功删除账号')
                else:
                    print(result.get('content'))
        else:
            print('所有账号都已经成功获取Cookies')


class TaobaoCookiesGenerator(CookiesGenerator):
    def __init__(self, website='taobao'):
        """
        初始化操作
        :param website: 站点名称
        :param browser: 使用的浏览器
        """
        CookiesGenerator.__init__(self, website)
        self.website = website

    def new_cookies(self, username, password=''):
        """
        生成Cookies
        :param username: 用户名
        :param password: 密码
        :return: 用户名和Cookies
        """
        ua = '122#ozks+EarEEax2EpZMEpMEJponDJE7SNEEP7rEJ+/FT0gEFQLpo7iEDpWnDEeK51HpyGZp9hBuDEEJFOPpC76EJponDJL7gNpEPXZpJRgu4Ep+FQLpoGUEJLWn4yP7SQEEyuLpERLWrvsprzJBmeCMvAXHXG44W3XVYY/RZQChsxtrEtE94MDpKQ9WmMed95Eb4RCQwKTMNzi4SrNJV35xfmIvxAWAuOSg31VdbUT8oL6JnMRh1K/PgfbD5WGynJxiabEDtVZ8CL6J4IERzTb+cv2E5pxdSX1ulIbkZcqoF+UJN2ryBfmqMvpDEpxnSp1uOIEELXZ8oLiJDEEyF3mqW32E5pangp4ul0EDLVr8CpUw8EEyB7wqMfpEp1eq9v1wgFWVDuIuoi7pTx9zM3fwnk3pA9nE3M+KJKrlNrOYWhTgnokY1d47qGuRf5ZZLWjDkYkUaWMC7NEePiwJlmZPGRB3FJ3R1FTRALc8aeI3xg3b+FzQ5pIm6RSshOA75UHCTblbGzc8Tflhv5YU8NZY3Cf/LFivBEaU2vrJGvvQWoNl2rW3RmTsHI5nbY+B6weqnhq5D5iTQjczmKLVXawuwK9aS1jaRAmxm7CKu5mqr27bAkuR4CEw4evCrdTQoetOn4hdzvI/GYW8YeQ3UA0tFtJXRbtKsczWHMLDnX36azjCT/H2Et2KFg0WTTBepMNs+MoSLYzWIzlXaGD+/q5okbp7j66FZoNXdgGL6vUgEVu7RTHdLyUjc3YMQcBBBox8Hiniih043CmJNcCjSLQ2RZYGrLV39r4Na9KEk5IRr/LhzZGpuMZEvXAGMxhZKcu6OnX/UjMjo7KG9Vop5QWx4XQTlOSPdhfcSIvfn07Wi8cGbAwXCVB1x8f84O74g02T1eAGlMgGZqG8QiWtotkg6uyEDuKKshQj6eCXv4uNh37vjaD1s/ABW33ysSLSbGRIUppinCh/aJykWd3VnYd/ZvMLi41EEtZ8kFvW140ojkxuh0TMWYrgKmPMwuAOIc8+EXXgKFLJcpSAwKkISPoRJGg+2G8ZmfDKkSVPQLVEUio6hJ+7ybacdyAOU+5f09hIb+kSh5Pn4EjnQ9uaroCP0dizOIJShr1ZiDEbLndZrbNtkmUxjnzF6SDcbCd5lfeNApuzg4Ul4DG7Y2+BajqSkEa3+4meWc9W/Vgcme+bSCGA9oDUzK8j3ZRLq8g7O9Ni8WZssWVIgkL5bYh6H8cAWhJOW7HuTPlPxbKYWeQ7jGH02fFXY68i8yQxUnTQHdj49EDb6lYcqIN/QBKbsUBNaco7cWmn77No31OPSCj3xKQYwjBV4CJEZSdL6NONA4gYiXXp4X3KeT4zJyN7mceQu2HUmzwHizaWdhxV5V3KSTJOK+Shbw4F0mAQbhclqHJHEhocHVTqFROa1MX1Fo/NwfJiVDzN34tbVQ3pi8Y7+7LnqqMmKCbQMw1SSh4DkZROU0nLgOsAEUOtc+3K/Xake1UeWHMQ180HP48xntAqbaLeBAVNsaK8eSR8MLTnwEm14fM1Ts9o2tUoiunQXajZ+CeSqvYfVDli1Res0GkZlcXMDAmU5NKq/+V7rLdr+Wn+pysDgFgbsRvDJZvcJREMRFABpTTp8J='
        return UsernameLogin(username, ua).login()


if __name__ == '__main__':
    generator = TaobaoCookiesGenerator()
    generator.run()
