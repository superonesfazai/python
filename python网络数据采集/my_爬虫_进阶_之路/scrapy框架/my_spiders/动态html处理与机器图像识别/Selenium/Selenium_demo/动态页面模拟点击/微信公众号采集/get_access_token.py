# coding:utf-8

'''
@author = super_fazai
@File    : get_access_token.py
@connect : superonesfazai@gmail.com
'''

import requests
import time

start_time = time.time()

def get_new_access_token():
    my_weixin_opener_info = {
        'appid': 'wx8xxxxxxx5b8',
        'AppSecret': 'xxxxxxxxxxxxxxxxxxx'
    }

    get_access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'\
        .format(my_weixin_opener_info['appid'], my_weixin_opener_info['AppSecret'])

    response = requests.get(get_access_token_url)
    access_token = response.json().get('access_token')      # 注意有限时间为7200s
    # print(access_token)
    with open('access_token.txt', 'w') as file:
        file.writelines(access_token)

def get_users_lists(access_token):
    # https://api.weixin.qq.com/cgi-bin/user/get?access_token=ACCESS_TOKEN
    users_lists_url = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token={}&next_openid=NEXT_OPENID'.format(access_token)
    response = requests.get(users_lists_url)
    print(response.json())


get_new_access_token()
with open('./access_token.txt', 'r') as file:
    access_token = file.readline()
# print(access_token)
get_users_lists(access_token)   # return -> {'errcode': 48001, 'errmsg': 'api unauthorized hint: [Fst0kA0797vr31!]'}
                                # 表示接口权限不够，因为是个人公众号所有不具备权限(获取用户列表的权限)