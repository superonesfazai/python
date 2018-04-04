# coding:utf-8

'''
@author = super_fazai
@File    : 异步高并发_获取抖音用户主页所有视频链接.py
@Time    : 2018/4/4 13:47
@connect : superonesfazai@gmail.com
'''

import re, asyncio, json, time
from my_aiohttp import MyAiohttp
from asyncio import Semaphore

headers = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'cache-control': 'max-age=0',
    'authority': 'www.douyin.com',
    # 'cookie': '_ba=BA0.2-20180330-5199e-OeUxtvwJvy5ElpWGFLId; _ga=GA1.2.390071767.1522391891; sso_login_status=1; tt_webid=6540458660484122126; __tea_sdk__user_unique_id=10_; _gid=GA1.2.1237547268.1522819200; __tea_sdk__ssid=e88eef4a-ec1f-497d-b2c7-301239bfdc67; login_flag=d6ee54ffebe3021c3fb67ff863970736; sessionid=7bdfd0e36df78f38c25abd13f0eff3cc; uid_tt=644e532b271dae498b62c659de17afdf; sid_tt=7bdfd0e36df78f38c25abd13f0eff3cc; sid_guard="7bdfd0e36df78f38c25abd13f0eff3cc|1522819290|2591999|Fri\\054 04-May-2018 05:21:29 GMT"',
}

douyin_path = '/Users/afa/myFiles/my_spider_logs/抖音/user_id.txt'

async def deal_with_data(user_id, body):
    '''
    处理数据
    :param user_id:
    :param body:
    :return:
    '''
    if body == '':
        print('[-] ' + user_id + '\tbody为空str!')
        return False

    try:
        data = json.loads(body)
        # pprint(data)
        # print(data)
    except Exception as e:
        data = {}
        print(e)

    if data.get('aweme_list', []) != []:
        print('[+] ' + user_id + ' [+]')
        with open(douyin_path, 'a') as f:
            f.write(user_id + '\n')
    else:
        print('[-] ' + user_id)

    return True

async def fetch_async(num):
    user_id = str(int(num))

    url = 'https://www.douyin.com/aweme/v1/aweme/post/'

    params = (
        ('user_id', user_id),
        ('max_cursor', '0'),
        ('count', '20'),
    )

    print(user_id)
    # 公司网测试 [参数如下] 效率较高(mac插网线) 56s
    body = await MyAiohttp.aio_get_url_body(url=url, headers=headers, params=params, num_retries=25, timeout=.3)
    # print(body)

    await deal_with_data(user_id, body)
    await asyncio.sleep(.1)

async def run(num):
    global start
    with (await sema):  # 控制下方函数最高并发量
        await fetch_async(num)

def main():
    while True:
        with open('./setting_2.txt', 'r') as f:
            start = int(f.readline())
        if start > 99999999999:
            break

        start_time = time.time()
        # NUMBERS = range(start, 999999999)
        NUMBERS = range(start, start + concurrency_number)

        loop = asyncio.get_event_loop()
        f = asyncio.wait([run(num) for num in NUMBERS])
        result = loop.run_until_complete(f)
        # print(result)
        end_time = time.time()
        print('用时: ', end_time - start_time)
        # loop.close()

        start += concurrency_number

        with open('./setting_2.txt', 'w') as f:
            f.write(str(start))

if __name__ == '__main__':
    concurrency_number = 110  # 并发量
    sema = Semaphore(concurrency_number)
    main()

'''
63386731255
66909301390
75942572681
67743208078
57790573431
80082422210
76496630960
75012418312
78297212610
3945072861
58847741205
67782762800
94707885141
88216594360
58813130905
69911221370
69724222848
60690378433
84945939089
96443791545
78781024955
57921024042
69724222848
61044440345
61885527450
71545770640
70846350561
58732428252
62797833029
59441622616
59469281770
59571614656
58397867830
74183443399
61645476527
94495692182
58947317715
72416915819
63545846781
95411093755
59149589176
88211355663
60701719666
54732891751
83848958189
95617072438
12357694588
91722165108
94518703655
58402665611
84349047467
86346749976
73475117725
58543051410
87195370547
69322498246
66570258203
75886879356
62459149388
58835034008
77512002736
82065929939
69579396488
59482337368
95153769133
71192476814
59146907291
59027089834
63815698410
62090131445
59611884846
58893121102
78372282836
69772216136
57578754935
59611884846
58893121102
60761262772
70951616850
62870510063
69387089021
58958068057
'''
