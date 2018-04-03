# coding:utf-8

'''
@author = super_fazai
@File    : 抖音_附近的人.py
@Time    : 2018/4/2 22:04
@connect : superonesfazai@gmail.com
'''

# 附近的人的接口
# https://api.amemv.com/aweme/v1/nearby/feed/?iid=29797177823&device_id=48592631504&os_api=18&app_name=aweme&channel=App%20Store&idfa=DA8C3A83-C08C-4881-86A8-1E67849F5BB2&device_platform=iphone&build_number=17805&vid=855FEC75-BEB7-45A5-BE6A-2699A6864BAC&openudid=c33813d872541f3bfc4ca174d9fbc5e708dd9ec5&device_type=iPhone7,1&app_version=1.7.8&version_code=1.7.8&os_version=11.0&screen_width=1242&aid=1128&ac=WIFI&count=20&feed_style=1&mas=006bb027c8cf2c54b445f26aefd87301a68ba304517abba0e08727&as=a165336cd3ad2a17429392&ts=1522677715

import requests
import json
from pprint import pprint
import time

cookies = {
    'install_id': '29797177823',
    'odin_tt': 'c53dd298a0e92adf64e9303da9ab2efbe0cbef78e6737970d9adb9b207d0758ac4b9c183d9d96c3b84f3e4eedb68c12d',
    'sessionid': '16fc74a57b38e96fc93bf967a6ccd76a',
    'sid_guard': '16fc74a57b38e96fc93bf967a6ccd76a%7C1522509051%7C2592000%7CMon%2C+30-Apr-2018+15%3A10%3A51+GMT',
    'sid_tt': '16fc74a57b38e96fc93bf967a6ccd76a',
    'ttreq': '1$494b0ed8e828b687a808d93e101fac11837708e6',
    'uid_tt': '9e0f14ca7575e68526e07408631cd322',
}

headers = {
    'Host': 'api.amemv.com',
    'Accept': '*/*',
    'User-Agent': 'Aweme/1.7.8 (iPhone; iOS 11.0; Scale/3.00)',
    'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
}

params = (
    ('iid', '29797177823'),
    ('device_id', '48592631504'),
    ('os_api', '18'),
    ('app_name', 'aweme'),
    ('channel', 'App Store'),
    ('idfa', 'DA8C3A83-C08C-4881-86A8-1E67849F5BB2'),
    ('device_platform', 'iphone'),
    ('build_number', '17805'),
    ('vid', '855FEC75-BEB7-45A5-BE6A-2699A6864BAC'),
    ('openudid', 'c33813d872541f3bfc4ca174d9fbc5e708dd9ec5'),
    ('device_type', 'iPhone7,1'),
    ('app_version', '1.7.8'),
    ('version_code', '1.7.8'),
    ('os_version', '11.0'),
    ('screen_width', '1242'),
    ('aid', '1128'),
    ('ac', 'WIFI'),
    ('count', '20'),
    ('feed_style', '1'),
    ('mas', '00091bb0192f7f76cca5221e6ad1aa541a5cc186d72840dd2f26a8'),  # 变
    # ('as', 'a12593fc5e6b1a59e25917'),   # 变(可无)
    ('ts', '1522678206'),   # 变
    # ('ts', str(time.time().__round__())),  # 变
)

response = requests.get('https://api.amemv.com/aweme/v1/nearby/feed/', headers=headers, params=params)
body = response.content.decode('utf-8')
# print(body)

try:
    data = json.loads(body).get('aweme_list', [])
except:
    print('json转换失败!')

pprint(body)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://api.amemv.com/aweme/v1/nearby/feed/?iid=29797177823&device_id=48592631504&os_api=18&app_name=aweme&channel=App%20Store&idfa=DA8C3A83-C08C-4881-86A8-1E67849F5BB2&device_platform=iphone&build_number=17805&vid=855FEC75-BEB7-45A5-BE6A-2699A6864BAC&openudid=c33813d872541f3bfc4ca174d9fbc5e708dd9ec5&device_type=iPhone7,1&app_version=1.7.8&version_code=1.7.8&os_version=11.0&screen_width=1242&aid=1128&ac=WIFI&count=20&feed_style=1&mas=00091bb0192f7f76cca5221e6ad1aa541a5cc186d72840dd2f26a8&as=a12593fc5e6b1a59e25917&ts=1522678206', headers=headers, cookies=cookies)
