# coding:utf-8

'''
@author = super_fazai
@File    : aiguangjie.py
@Time    : 2017/12/4 20:57
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

import requests
import re
import json
import gc, os
from random import randint
from pprint import pprint
from settings import IS_BACKGROUND_RUNNING

from fzutils.internet_utils import get_random_pc_ua
from fzutils.linux_utils import daemon_init

class AiGuangJie(object):
    def __init__(self):
        # * requests模拟ajax请求 *
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/json,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'guang.taobao.com',
            'User-Agent': get_random_pc_ua(),      # 随机一个请求头
            # 'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://guang.taobao.com/',  # 必须的参数
        }

    def get_goods_info_list(self):
        '''
        测试二: 模拟ajax爱逛街pc端接口
        '''
        # tmp_url = 'https://guang.taobao.com/street/ajax/get_guang_list.json?_input_charset=utf-8&cpage=1&start=1'
        # cpage为1到30页
        tmp_url = 'https://guang.taobao.com/street/ajax/get_guang_list.json?_input_charset=utf-8&cpage=1'

        # 设置代理ip
        self.proxies = self.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]

        tmp_proxies = {
            'http': self.proxy,
        }
        # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))

        try:
            response = requests.get(tmp_url, headers=self.headers, proxies=tmp_proxies, timeout=10)
            body = response.content.decode('utf-8')
            # print(body)
        except Exception:
            print('requests.get()请求超时....')
            print('body为空!')
            body = '{}'

        is_success = False
        data = {}
        try:
            data = json.loads(body)
            if data.get('success') == 1:
                is_success = True
            data = data.get('data', {}).get('data', [])
            # pprint(data)
        except:
            print('json.loads转换data时出错, 此处跳过!')

        if is_success and data != []:
            # 清洗data
            for item in data:
                # print(item.get('title'))
                # print(item.get('userNick'))
                for item2 in item.get('items', []):
                    item2['itemTags'] = []
            print(len(data))
            pprint(data)

        else:
            print('data数据获取失败!')
            return []

    def get_proxy_ip_from_ip_pool(self):
        '''
        从代理ip池中获取到对应ip
        :return: dict类型 {'http': ['http://183.136.218.253:80', ...]}
        '''
        base_url = 'http://127.0.0.1:8000'
        result = requests.get(base_url).json()

        result_ip_list = {}
        result_ip_list['http'] = []
        for item in result:
            if item[2] > 7:
                tmp_url = 'http://' + str(item[0]) + ':' + str(item[1])
                result_ip_list['http'].append(tmp_url)
            else:
                delete_url = 'http://127.0.0.1:8000/delete?ip='
                delete_info = requests.get(delete_url + item[0])
        # pprint(result_ip_list)
        return result_ip_list

    def __del__(self):
        gc.collect()

def just_fuck_run():
    # while True:
    print('一次大更新即将开始'.center(30, '-'))
    tmp = AiGuangJie()
    tmp.get_goods_info_list()
    try:
        del tmp
    except:
        pass
    gc.collect()
    print('一次大更新完毕'.center(30, '-'))

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')  # 在调用daemon_init函数前是可以使用print到标准输出的，调用之后就要用把提示信息通过stdout发送到日志系统中了
    daemon_init()  # 调用之后，你的程序已经成为了一个守护进程，可以执行自己的程序入口了
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    # time.sleep(10)  # daemon化自己的程序之后，sleep 10秒，模拟阻塞
    just_fuck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        just_fuck_run()
