# coding:utf-8

'''
@author = super_fazai
@File    : test_get_db_goods_from_redis.py
@connect : superonesfazai@gmail.com
'''

"""
测试从redis取数据
"""

from sys import path as sys_path
sys_path.append('..')

from multiplex_code import get_waited_2_update_db_data_from_redis_server
from pprint import pprint

res = get_waited_2_update_db_data_from_redis_server(spider_name='tm0')
# pprint(res)

tmp = [[item[1], item[16]] for item in res]
pprint(tmp)