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

'''批量更改'''
# update_sql = 'update dbo.GoodsInfoAutoGet set SKUInfo=%s, p_info_change=1 where GoodsID=%s'
#
# from time import sleep
# from json import dumps
#
# from fzutils.common_utils import json_2_dict
# from fzutils.time_utils import fz_set_timeout
# from fzutils.cp_utils import format_price_info_list
#
# pipeline = SqlServerMyPageInfoSaveItemPipeline()
# sql_str = '''
# select top 100 GoodsID, SiteID, SKUInfo
# from dbo.GoodsInfoAutoGet
# where (p_info_change is null or p_info_change=0) and SKUInfo != '[]'
# '''
# def change_sku_info():
#     global pipeline
#     @fz_set_timeout(6)
#     def oo(goods_id, sku_info, site_id):
#         is_new = False
#         for item in sku_info:       # 新的不格式化
#             if item.get('unique_id') is not None:
#                 is_new = True
#                 break
#
#         if is_new:
#             pass
#         else:
#             sku_info = format_price_info_list(sku_info, site_id=site_id)
#         # print(sku_info)
#         try:
#             pipeline._update_table(
#                 sql_str=update_sql,
#                 params=(
#                     dumps(sku_info, ensure_ascii=False),
#                     goods_id,
#                 )
#             )
#         except:
#             pass
#
#     index = 0
#     while True:
#         try:
#             res = pipeline._select_table(sql_str=sql_str)
#         except TypeError:
#             sleep(5)
#             continue
#
#         if res == []:
#             break
#
#         if res is None:
#             sleep(5)
#             continue
#
#         if index % 200 == 0:
#             pipeline = SqlServerMyPageInfoSaveItemPipeline()
#
#         for item in res:
#             print('index == {0}'.format(index))
#             try:
#                 oo(goods_id=item[0], sku_info=json_2_dict(json_str=item[2]), site_id=item[1])
#             except:
#                 print('遇到错误跳过!出错goods_id={0}'.format(item[0]))
#                 continue
#             index += 1
#
#     print('全部操作完成!')
#
# change_sku_info()