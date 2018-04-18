# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2018/4/9 17:04
@connect : superonesfazai@gmail.com
'''
import sys, json, re
sys.path.append('..')
from pprint import pprint

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

_ = SqlServerMyPageInfoSaveItemPipeline()
_s = _.select_tmall_all_goods_id_url_by_site_6()
# print(_s)

import re
tmp = _s
tmp = [list(item) for item in tmp]
for item in tmp:
    a = re.compile('(.*htm)').findall(item[2])[0]
    b = re.compile('.*htm(.*)').findall(item[2])[0]
    c = a + '?id=' + b
    item[2] = c

# print(tmp)
tmp = [{'goods_id': item[0], 'goods_url': item[2]} for item in tmp]
# print(tmp)

for item in tmp:
    _.update_tmall_goodsurl_by_site_id_6(item=item)