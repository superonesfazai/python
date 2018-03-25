# coding:utf-8

'''
@author = super_fazai
@File    : my_ip_pools.py
@Time    : 2017/12/23 15:11
@connect : superonesfazai@gmail.com
'''

import requests
import gc

__all__ = [
    'MyIpPools',
]

class MyIpPools(object):
    def __init__(self):
        super().__init__()

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