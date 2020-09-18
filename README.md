### 来源github上的项目，进行修改

# CookiesPool


## 安装

```
pip3 install -r requirements.txt
```

## 基础配置 

### 接口基本配置

```python
# Redis数据库地址
REDIS_HOST = 'localhost'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = None

# 产生器使用的浏览器
BROWSER_TYPE = 'Chrome'

# 产生器类，如扩展其他站点，请在此配置
GENERATOR_MAP = {
    'taobao': 'TaobaoCookiesGenerator'
}

# 检测类，如扩展其他站点，请在此配置
TESTER_MAP = {
    'taobao': 'TaobaoValidTester'
}


# 产生器和验证器循环周期
CYCLE = 120

# API地址和端口
API_HOST = '0.0.0.0'
API_PORT = 5000

```

### 进程开关

在config.py修改

```python
# 产生器开关，模拟登录添加Cookies
GENERATOR_PROCESS = True
# 验证器开关，循环检测数据库中Cookies是否可用，不可用删除
VALID_PROCESS = True
# API接口服务
API_PROCESS = True
```


## 运行

```
python3 run.py
```
