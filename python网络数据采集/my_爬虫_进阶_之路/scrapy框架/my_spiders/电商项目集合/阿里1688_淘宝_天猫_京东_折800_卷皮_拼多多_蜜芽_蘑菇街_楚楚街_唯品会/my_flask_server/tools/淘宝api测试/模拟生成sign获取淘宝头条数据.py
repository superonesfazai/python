import execjs
import time
import requests
from random import randint

# 打开js源文件
with open('./get_h_func.js', 'r') as f:
    js = f.read()

js_parser = execjs.compile(js)  #  编译js得到python解析对象

t = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位

# 构造请求参数a
a = 'undefined&' + t + '&12574478&{"app":"tbc","version":"17.0","userType":1}'

# 获取sign
sign = js_parser.call('h', a)

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'
}

base_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.hlservice.columntab.list/2.0/'

params = {
    "jsv": "2.4.2",
    "appKey": "12574478",
    "t": t,
    "sign": sign,
    "api": "mtop.taobao.hlservice.columntab.list",
    "v": " 2.0",
    "AntiCreep": "true",
    "timeout": "5000",
    "type": "jsonp",
    "dataType": "jsonp",
    "callback": "mtopjsonp1",
    "data": '{"app":"tbc","version":"17.0","userType"": "1}',
}

s = requests.session()

res = s.get(url=base_url, params=params, headers=headers)

tk = res.cookies['_m_h5_tk']

tk = tk.split('_')[0]

print(res.text)
print(s.cookies.items())
print(tk)

list_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.hlservice.feed.list/1.0/'

t = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位

# 构造请求参数a
a = tk + '&' + t + '&12574478&{"app":"tbc","version":"17.0","userType":1,"action":"1","columnId":"10"}'

# 获取sign
sign = js_parser.call('h', a)

# 构建请求参数
params = {
    "jsv": "2.4.2",
    "appKey": "12574478",
    "t": t,
    "sign": sign,
    "api": "mtop.taobao.hlservice.columntab.list",
    "v": " 2.0",
    "AntiCreep": "true",
    "timeout": "5000",
    "type": "jsonp",
    "dataType": "jsonp",
    "callback": "mtopjsonp2",
    "data": '{"app":"tbc","version":"17.0","userType":1,"action":"1","columnId":"10"}',
}

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1",
}

res = s.get(url=list_url, params=params, headers=headers)

print(res.text)