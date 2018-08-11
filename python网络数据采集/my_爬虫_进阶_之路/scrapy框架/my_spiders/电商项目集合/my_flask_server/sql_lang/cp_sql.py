# coding:utf-8

'''
@author = super_fazai
@File    : cp_sql.py
@Time    : 2018/7/24 10:03
@connect : superonesfazai@gmail.com
'''

# server数据插入失败 -> 运行此sql_str
error_insert_sql_str = '''
select UserName, CreateTime, GoodsID, GoodsName, ConvertTime, MainGoodsID
from dbo.GoodsInfoAutoGet 
where GoodsID=%s
'''