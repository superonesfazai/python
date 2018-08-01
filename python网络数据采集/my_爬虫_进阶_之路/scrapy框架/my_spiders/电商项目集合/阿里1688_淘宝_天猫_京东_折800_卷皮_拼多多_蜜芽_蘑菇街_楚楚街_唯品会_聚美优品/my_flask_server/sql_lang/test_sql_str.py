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

from fzutils.sql_utils import pretty_table

_ = SqlServerMyPageInfoSaveItemPipeline()
sql_str = '''
select top 20 ID as id, UserName as user_name, GoodsUrl, CreateTime, MainGoodsID, IsPriceChange
from dbo.GoodsInfoAutoGet
where GETDATE()-CreateTime < 1
order by ID desc;
'''
# sql_str = 'select count(*) from dbo.daren_recommend where site_id=3'
# result = _._select_table(sql_str=sql_str, params=None)
# pprint(result)
# print(result)
pretty_table(cursor=_._get_one_select_cursor(sql_str=sql_str, params=None))

# 更新
# sql_str_2 = 'UPDATE dbo.daren_recommend set share_img_url_list=NULL, goods_id_list=NULL, share_goods_base_info=%s where MainID=579;'
# result = _._update_table(sql_str=sql_str_2, params=params)
# print(result)

