# coding:utf-8

'''
@author = super_fazai
@File    : test_tm_m.py
@connect : superonesfazai@gmail.com
'''

"""
测试tm m
"""

from sys import path as sys_path
sys_path.append('..')

from multiplex_code import get_tm_m_body_data
from pprint import pprint

goods_id = '547031679260'
data = get_tm_m_body_data(goods_id=goods_id)
pprint(data)