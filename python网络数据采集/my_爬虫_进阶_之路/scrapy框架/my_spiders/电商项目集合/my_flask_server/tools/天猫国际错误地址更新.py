# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2018/4/9 17:04
@connect : superonesfazai@gmail.com
'''

"""
不能多次运行
"""

import sys, json, re
sys.path.append('..')
from pprint import pprint

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

_ = SqlServerMyPageInfoSaveItemPipeline()
sql_str = r'select GoodsID, SiteID, GoodsUrl from dbo.GoodsInfoAutoGet where SiteID=6 order by ID desc'
_s = _._select_table(sql_str=sql_str)
# print(_s)

import re
tmp = _s
tmp = [list(item) for item in tmp]
for item in tmp:
    if re.compile('\?id=').findall(item[2]) == []:
        a = re.compile('(.*htm)').findall(item[2])[0]
        b = re.compile('.*htm(.*)').findall(item[2])[0]
        c = a + '?id=' + b
        item[2] = c

# print(tmp)
tmp = [{'goods_id': item[0], 'goods_url': item[2]} for item in tmp]
# print(tmp)

sql_str = r'update dbo.GoodsInfoAutoGet set GoodsUrl=%s where GoodsID = %s'
for item in tmp:
    _._update_table(sql_str=sql_str, params=(item['goods_url'], item['goods_id']))