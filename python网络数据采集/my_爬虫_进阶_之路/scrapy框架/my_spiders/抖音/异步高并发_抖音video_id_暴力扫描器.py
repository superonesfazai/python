# coding:utf-8

'''
@author = super_fazai
@File    : 异步高并发_抖音video_id_暴力扫描器.py
@Time    : 2018/4/3 16:55
@connect : superonesfazai@gmail.com
'''

import asyncio, time, re, json
from random import randint
from my_aiohttp import MyAiohttp
from asyncio import Semaphore

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

async def fetch_async(num):
    video_id = str(int('65' + 17 * '0') + num)

    url = 'https://www.iesdouyin.com/share/video/' + video_id + '/'

    print(video_id)
    # 公司网测试 [参数如下] 效率较高(mac插网线) 56s
    body = await MyAiohttp.aio_get_url_body(url=url, headers=headers, num_retries=25, timeout=.4)
    # print(body)

    if body == '':
        print('[-] ' + video_id + '\tbody为空str!')
        pass

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

    await asyncio.sleep(.1)

async def run(num):
    global start
    with (await sema):  # 控制下方函数最高并发量
        await fetch_async(num)

if __name__ == '__main__':
    # start = 21002
    concurrency_number = 100      # 并发量
    sema = Semaphore(concurrency_number)
    while True:
        with open('./setting.txt', 'r') as f:
            start = int(f.readline())
        if start > 99999999999999999:
            break

        start_time = time.time()
        # NUMBERS = range(start, 99999999999999999)
        NUMBERS = range(start, start+concurrency_number)

        loop = asyncio.get_event_loop()
        f = asyncio.wait([run(num) for num in NUMBERS])
        result = loop.run_until_complete(f)
        # print(result)
        end_time = time.time()
        print('用时: ', end_time - start_time)
        # loop.close()

        start += concurrency_number

        with open('./setting.txt', 'w') as f:
            f.write(str(start))
