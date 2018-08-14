# coding:utf-8

'''
@author = super_fazai
@File    : site_id.py
@Time    : 2017/10/27 21:00
@connect : superonesfazai@gmail.com
'''

"""
site_id对应的站点对象
"""

_1 = '淘宝'
_2 = '阿里'
_3 = '天猫'
_4 = '天猫超市'
_5 = '聚划算'
_6 = '天猫国际'
_7 = '京东'
_8 = '京东超市'
_9 = '京东全球购'
_10 = '京东大药房'
_11 = '折800'
_12 = '卷皮'
_13 = '拼多多'
_14 = '折800秒杀'
_15 = '卷皮秒杀'
_16 = '拼多多秒杀'
_17 = '折800拼团'
_18 = '卷皮拼团'
_19 = '淘宝天天特价'
_20 = '蜜芽秒杀'
_21 = '蜜芽拼团'
_22 = '蘑菇街秒杀'
_23 = '蘑菇街拼团'
_24 = '楚楚街秒杀'
_25 = '唯品会'
_26 = '聚美优品秒杀'
_27 = '聚美优品拼团'
_28 = '淘抢购'
_29 = '网易考拉'
_30 = '网易严选'
_31 = '小米有品'

"""
常用查询sql_str
"""
# 查询某个商品是否已录入
sql_str = '''
use Gather;
select UserName, CreateTime, GoodsName, GoodsID, ConvertTime, MainGoodsID
from dbo.GoodsInfoAutoGet 
where GoodsID='';
'''

# 查询最新入录的商品
sql_str_2 = '''
use Gather;
select top 20 ID, UserName, GoodsUrl, CreateTime, MainGoodsID, IsPriceChange
from dbo.GoodsInfoAutoGet 
where GETDATE()-CreateTime < 1
order by ID desc;
'''

