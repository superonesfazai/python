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

# douyin_path = '/root/myFiles/my_spider_logs/抖音/user_id.txt'
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
    setting_file_name = './setting_2.txt'
    while True:
        with open(setting_file_name, 'r') as f:
            start = int(f.readline())
        if start > 99999999999:
            break

        start_time = time.time()
        # NUMBERS = range(start, 999999999)
        NUMBERS = range(start, start + concurrency_number)

        loop = asyncio.get_event_loop()
        # f = [run(num) for num in NUMBERS]
        # loop.run_until_complete(asyncio.wait(f))

        # 下面2行替换成上面2行, 增大了10个的并发量
        tasks = [asyncio.ensure_future(run(num)) for num in NUMBERS]
        loop.run_until_complete(asyncio.wait(tasks))

        end_time = time.time()
        print('用时: ', end_time - start_time)
        # loop.close()

        start += concurrency_number

        with open(setting_file_name, 'w') as f:
            f.write(str(start))

if __name__ == '__main__':
    concurrency_number = 120  # 并发量
    sema = Semaphore(concurrency_number)
    main()
