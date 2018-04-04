# coding:utf-8

'''
@author = super_fazai
@File    : 抖音video_id_暴力扫描器.py
@Time    : 2018/4/3 15:15
@connect : superonesfazai@gmail.com
'''

import re, json
from my_requests import MyRequests
from pprint import pprint
import time
from random import randint
from time import sleep

headers = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'cache-control': 'max-age=0',
}

params = (
    ('region', 'CN'),
    # ('mid', '6539782714772916996'),
    ('titleType', 'title'),
    ('timestamp', str(time.time().__round__()) + str(randint(100, 999))),
    ('utm_campaign', 'client_share'),
    ('app', 'aweme'),
    ('utm_medium', 'aweme_ios'),
    ('iid', '29797177823'),
    ('utm_source', 'weixin'),
    ('tt_from', 'weixin'),
    # ('uid', '93453836807'),
    ('did', '29797177823'),
)

'''
6539816136194657540
6515248147944934152
6529398170412125454
6539925645483314440
6539801701493247235
6540274931093998861
6540136173849808142
6538985783276080391
6516458290216439053
6540176819398642948
6539817464413293828
6528367736416898311
6540116161948814606
6539296609774079246
6519785860471196936
'''

douyin_path = '/Users/afa/myFiles/my_spider_logs/抖音/video_id.txt'

def deal_with_data(video_id, body):
    if body == '':
        print('[-] ' + video_id + '\tbody为空str!')
        return False

    try:
        data = re.compile(r'var data = (.*);require').findall(body)[0]
        # pprint(data)
    except IndexError:
        data = '[{}]'

    try:
        data = json.loads(data)
        # pprint(data)
        # print(data)
    except Exception as e:
        data = [{}]
        print(e)

    if data == []:
        print('[-] ' + video_id)
    else:
        if data.get('status', {}) != {}:
            print('[+] ' + video_id)
            with open(douyin_path, 'a') as f:
                f.write(video_id + '\n')
        else:
            print('[-] ' + video_id)

    return True

def run_forever():
    with open('./setting.txt', 'r') as f:
        start = int(f.readline())

    for index in range(start, 99999999999999999):
        if index % 50 == 0:
            with open('./setting.txt', 'w') as f:
                f.write(str(index))
            print('*** 短暂休眠...')
            sleep(2)

        video_id = str(int('65' + 17*'0') + index)

        url = 'https://www.iesdouyin.com/share/video/' + video_id + '/'
        body = MyRequests.get_url_body(url=url, headers=headers, params=params)
        # print(body)

        if deal_with_data(video_id=video_id, body=body) is False:
            continue
        else:
            pass

        sleep(.2)

run_forever()