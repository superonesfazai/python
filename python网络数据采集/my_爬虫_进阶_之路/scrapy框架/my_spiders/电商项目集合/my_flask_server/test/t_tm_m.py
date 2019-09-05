# coding:utf-8

'''
@author = super_fazai
@File    : t_tm_m.py
@connect : superonesfazai@gmail.com
'''

"""
测试tm m
"""

from sys import path as sys_path
sys_path.append('..')

from multiplex_code import get_tm_m_body_data
from tmall_parse_2 import TmallParse
from pprint import pprint

# todo 注意部分商品预售，当前无法购买, 不更新, 待其状态正常后会更新
goods_id = '43988580669'
# data = get_tm_m_body_data(goods_id=goods_id)
# pprint(data)
pc_url = 'https://detail.tmall.com/item.htm?id={}'.format(goods_id)
phone_url = 'https://detail.m.tmall.com/item.htm?id={}'.format(goods_id)
print('pc_url: {}, phone_url: {}'.format(pc_url, phone_url))

tm = TmallParse(is_real_times_update_call=True)
goods_id = tm.get_goods_id_from_url(tmall_url=pc_url)
ori_data = tm.get_goods_data(goods_id=goods_id)
# pprint(ori_data)
data = tm.deal_with_data()
pprint(data)

try:del tm
except:pass