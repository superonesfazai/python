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
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from fzutils.sql_utils import pretty_table

_ = SqlServerMyPageInfoSaveItemPipeline()
sql_str = '''
use Gather;
select MainGoodsID, goods_url, is_delete, create_time, modfiy_time, ConvertTime, goods_id, miaosha_begin_time, miaosha_end_time
from dbo.juanpi_xianshimiaosha 
where MainGoodsID='129216' 
or MainGoodsID='129215'
or MainGoodsID='129214'
or MainGoodsID='129213'
'''
pretty_table(cursor=_._get_one_select_cursor(sql_str=sql_str, params=None))

# 更新
# sql_str_2 = 'UPDATE dbo.daren_recommend set share_img_url_list=NULL, goods_id_list=NULL, share_goods_base_info=%s where MainID=579;'
# result = _._update_table(sql_str=sql_str_2, params=params)
# print(result)

