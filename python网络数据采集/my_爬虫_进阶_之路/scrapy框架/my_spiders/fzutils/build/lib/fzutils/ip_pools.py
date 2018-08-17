# coding:utf-8

'''
@author = super_fazai
@File    : ip_pools.py
@Time    : 2018/7/13 18:31
@connect : superonesfazai@gmail.com
'''

from requests import get
import gc
from random import randint

__all__ = [
    'MyIpPools',
]

class MyIpPools(object):
    def __init__(self, high_conceal=False):
        '''
        :param high_conceal: 是否初始化为高匿代理
        '''
        super(MyIpPools, self).__init__()
        self.high_conceal = high_conceal

    def get_proxy_ip_from_ip_pool(self):
        '''
        从代理ip池中获取到对应ip
        :return: dict类型 {'http': ['http://183.136.218.253:80', ...]}
        '''
        if self.high_conceal:
            base_url = 'http://127.0.0.1:8000/?types=0' # types: 0高匿|1匿名|2透明
        else:
            base_url = 'http://127.0.0.1:8000'
        try:
            result = get(base_url).json()
        except Exception as e:
            print(e)
            return {'http': None}

        result_ip_list = {}
        result_ip_list['http'] = []
        for item in result:
            if item[2] > 7:
                tmp_url = 'http://' + str(item[0]) + ':' + str(item[1])
                result_ip_list['http'].append(tmp_url)
            else:
                delete_url = 'http://127.0.0.1:8000/delete?ip='
                delete_info = get(delete_url + item[0])

        # pprint(result_ip_list)

        return result_ip_list

    def _get_random_proxy_ip(self):
        '''
        随机获取一个代理ip: 格式 'http://175.6.2.174:8088'
        :return:
        '''
        ip_list = self.get_proxy_ip_from_ip_pool().get('http')
        try:
            if isinstance(ip_list, list):
                proxy_ip = ip_list[randint(0, len(ip_list) - 1)]  # 随机一个代理ip
            else:
                raise TypeError
        except Exception:
            print('从ip池获取随机ip失败...正在使用本机ip进行爬取!')
            proxy_ip = False

        return proxy_ip

    def _empty_ip_pools(self):
        '''
        清空ip池
        :return:
        '''
        base_url = 'http://127.0.0.1:8000'
        result = get(base_url).json()

        delete_url = 'http://127.0.0.1:8000/delete?ip='

        for item in result:
            if item[2] < 11:
                delete_info = get(delete_url + item[0])
                print(delete_info.text)

        return None

    def __del__(self):
        gc.collect()
