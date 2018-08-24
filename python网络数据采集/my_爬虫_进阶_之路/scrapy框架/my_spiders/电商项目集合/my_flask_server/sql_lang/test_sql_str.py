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
select top 200 id, head_img_url
from dbo.sina_weibo
where sina_type = 'bilibili'
'''
pretty_table(cursor=_._get_one_select_cursor(sql_str=sql_str, params=None))

# 更新
# sql_str_2 = 'UPDATE dbo.daren_recommend set share_img_url_list=NULL, goods_id_list=NULL, share_goods_base_info=%s where MainID=579;'
# result = _._update_table(sql_str=sql_str_2, params=params)
# print(result)

# 删除
# delete_sql = 'delete from dbo.sina_weibo where id=%s'
# while True:
#     id = input('请输入要删除的id:').replace(';', '')
#     res = _._delete_table(sql_str=delete_sql, params=(id,))
#     print(res)

