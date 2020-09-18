# Redis数据库地址
REDIS_HOST = 'localhost'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = None

# Redis数据库地址
MONGO_HOST = 'localhost'

# MONGO端口
MONGO_PORT = 27017

# mongo用户
MONGO_USER = 'root'

# MONGO密码，如无填None
MONGO_PASSWORD = None

# Mongo DB, 用于存放用户名和密码
MONGO_DB = 'taobao_crypto'

# Mongo table, 用于存放用户名和密码
MONGO_TABLE = 'pw_encrypt'


# 产生器使用的浏览器
BROWSER_TYPE = None

# 产生器类，如扩展其他站点，请在此配置
GENERATOR_MAP = {
    'taobao': 'TaobaoCookiesGenerator'
}

# 测试类，如扩展其他站点，请在此配置
TESTER_MAP = {
    'taobao': 'TaobaoValidTester'
}

TEST_URL_MAP = {
    'taobao': 'https://s.taobao.com/search?q=nike&bcoffset=-3&ntoffset=-3&p4ppushleft=1%2C48&s=1'
}

# 产生器循环周期
GET_CYCLE = 120

# 验证器循环周期
TEST_CYCLE = 120

# API地址和端口
API_HOST = '0.0.0.0'
API_PORT = 5000

# 产生器开关，模拟登录添加Cookies
GENERATOR_PROCESS = True
# 验证器开关，循环检测数据库中Cookies是否可用，不可用删除
VALID_PROCESS = False
# API接口服务
API_PROCESS = False
