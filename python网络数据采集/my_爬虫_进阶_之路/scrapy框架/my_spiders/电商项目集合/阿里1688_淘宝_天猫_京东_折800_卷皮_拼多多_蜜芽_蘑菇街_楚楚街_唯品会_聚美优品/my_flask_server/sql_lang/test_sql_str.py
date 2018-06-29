# coding:utf-8

'''
@author = super_fazai
@File    : test_sql_str.py
@Time    : 2018/6/14 07:41
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from pprint import pprint
from json import dumps
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

_ = SqlServerMyPageInfoSaveItemPipeline()
# sql_str = 'select gather_url, MainID from dbo.daren_recommend where site_id=2 and MainID is not null'
sql_str = 'select GoodsID from dbo.GoodsInfoAutoGet where SiteID=2 and GoodsID=%s'
params = ('556812068095',)
result = _._select_table(sql_str=sql_str, params=params)
# pprint(result)
print(result)

# 更新
# sql_str_2 = 'UPDATE dbo.daren_recommend set share_img_url_list=NULL, goods_id_list=NULL, share_goods_base_info=%s where MainID=579;'
# result = _._update_table(sql_str=sql_str_2, params=params)
# print(result)

