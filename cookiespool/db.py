import random
import redis
from pymongo import MongoClient
from cookiespool.config import *


class RedisClient(object):
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化Redis连接
        :param host: 地址
        :param port: 端口
        :param password: 密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        self.type = type
        self.website = website

    def name(self):
        """
        获取Hash的名称
        :return: Hash名称
        """
        return "{type}:{website}".format(type=self.type, website=self.website)

    def set(self, username, value):
        """
        设置键值对
        :param username: 用户名
        :param value: 密码或Cookies
        :return:
        """
        return self.db.hset(self.name(), username, value)

    def get(self, username):
        """
        根据键名获取键值
        :param username: 用户名
        :return:
        """
        return self.db.hget(self.name(), username)

    def delete(self, username):
        """
        根据键名删除键值对
        :param username: 用户名
        :return: 删除结果
        """
        return self.db.hdel(self.name(), username)

    def count(self):
        """
        获取数目
        :return: 数目
        """
        return self.db.hlen(self.name())

    def random(self):
        """
        随机得到键值，用于随机Cookies获取
        :return: 随机Cookies
        """
        print(self.name())
        return random.choice(self.db.hvals(self.name()))

    def usernames(self):
        """
        获取所有账户信息
        :return: 所有用户名
        """
        return self.db.hkeys(self.name())

    def all(self):
        """
        获取所有键值对
        :return: 用户名和密码或Cookies的映射表
        """
        return self.db.hgetall(self.name())


class MongoCli(object):
    connect = None

    def __init__(self, host=MONGO_HOST, port=MONGO_PORT, user='root', password=None, db=MONGO_DB, table=MONGO_TABLE):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.table = table

    def get_connect(self):
        """
        返回连接
        :return:
        """
        if self.connect:
            return self.connect
        try:
            self.connect = MongoClient(host=self.host, port=self.port)
            if self.user and self.password:
                self.connect[self.db].authenticate(self.user, self.password)
            return self.connect
        except Exception as e:
            print(e)
        return False

    def conn(self):
        """
        建立链接
        :return:
        """
        return self.get_connect()[self.db][self.table]

    def set(self, **kwargs):
        """
        写入用户名和密码以及加密值
        :param kwargs:
        :return:
        """
        return self.conn().insert_one(dict(kwargs))

    def get(self, username):
        """
        根据键名获取键值
        :param username: 用户名
        :return:
        """
        return self.conn().find_one({'username': username})

    def delete(self, username):
        """
        根据键名删除键值对
        :param username: 用户名
        :return: 删除结果
        """
        return self.conn().delete_one({'username': username})

    def count(self):
        """
        获取数目
        :return: 数目
        """
        return self.conn().count()

    def usernames(self):
        """
        获取所有账户信息
        :return: 所有用户名
        """
        return self.conn().find({}, {'username': 1})

    def all(self):
        """
        获取所有键值对
        :return: 用户名和密码或Cookies的映射表
        """
        return self.conn().find({})


if __name__ == '__main__':
    mon_conn = MongoCli()
    print('count: ' + str(mon_conn.count()))
    for name in mon_conn.usernames():
        print(name.get('username'))

    for i in mon_conn.all():
        print(i)

    # conn = RedisClient('accounts', 'weibo')
    # result = conn.set('hell2o', 'sss3s')
    # print(result)
