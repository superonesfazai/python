# coding:utf-8

'''
@author = super_fazai
@File    : 随机获取新user_id.py
@Time    : 2018/4/7 10:05
@connect : superonesfazai@gmail.com
'''

import requests, json, time
from pprint import pprint
from random import randint
from time import sleep
from my_requests import MyRequests

def get_random_user_id_list():
    # cookies = {
    #     'install_id': '29797177823',
    #     'odin_tt': 'c53dd298a0e92adf64e9303da9ab2efbe0cbef78e6737970d9adb9b207d0758ac4b9c183d9d96c3b84f3e4eedb68c12d',
    #     'sessionid': '16fc74a57b38e96fc93bf967a6ccd76a',
    #     'sid_guard': '16fc74a57b38e96fc93bf967a6ccd76a%7C1522509051%7C2592000%7CMon%2C+30-Apr-2018+15%3A10%3A51+GMT',
    #     'sid_tt': '16fc74a57b38e96fc93bf967a6ccd76a',
    #     'ttreq': '1$494b0ed8e828b687a808d93e101fac11837708e6',
    #     'uid_tt': '9e0f14ca7575e68526e07408631cd322',
    # }

    headers = {
        'Host': 'aweme.snssdk.com',
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
        ('count', '30'),    # 变
        ('cursor', '30'),   # 游标位置
        # ('mas', '00648f2f9c5b661213d05736e23eea622bf96d64dd09f6e283ea97'),
        # ('as', 'a12512fc4e4aaa76481324'),
        # ('ts', '1523066542'),
        ('ts', str(time.time().__round__()) + str(randint(100, 999))),
    )

    url = 'https://aweme.snssdk.com/aweme/v1/category/list/'
    body = MyRequests.get_url_body(url=url, headers=headers, params=params)
    # print(body)

    try:
        data = json.loads(body).get('category_list', [])
        # pprint(data)
        print('count数:', len(data))
    except:
        data = {}
        print('error')

    aweme_list = [item.get('aweme_list') for item in data]
    # pprint(aweme_list)

    user_id_list = []
    for item in aweme_list:
        if isinstance(item, list):
            for i in item:
                user_id_list.append(i.get('author_user_id', ''))
        else:
            user_id_list.append(item.get('author_user_id', ''))

    user_id_list = sorted(list(set(user_id_list)))
    user_id_list = [item for item in user_id_list if item not in all_user_id_list]
    # pprint(user_id_list)

    return user_id_list

def save_data(douyin_path, user_id_list):
    with open(douyin_path, 'a') as f:
        for item in user_id_list:
            if item == '':
                continue
            print('[+] %s' % str(item))
            f.write(str(item) + '\n')
            all_user_id_list.append(item)   # 更新

    # print('写入完毕!')
    return None

def get_all_user_id(file_path):
    all_user_id_list = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            line = line.replace('\n', '')
            if line == '':
                continue
            all_user_id_list.append(int(line))

    all_user_id_list = sorted(list(set(all_user_id_list)))

    return all_user_id_list

def main():
    while True:
        user_id_list = get_random_user_id_list()
        save_data(douyin_path, user_id_list)
        sleep(1)

if __name__ == '__main__':
    douyin_path = '/Users/afa/myFiles/my_spider_logs/抖音/user_id.txt'
    all_user_id_list = get_all_user_id(file_path=douyin_path)
    main()

