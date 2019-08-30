# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@connect : superonesfazai@gmail.com
'''

from pprint import pprint
from fzutils.ip_pools import (
    tri_ip_pool,
    IpPools,)

ip_pool = IpPools(type=tri_ip_pool)
proxy_list = (ip_pool.get_proxy_ip_from_ip_pool()).get('https', [])
pprint(proxy_list)
print('len: {}'.format(len(proxy_list)))