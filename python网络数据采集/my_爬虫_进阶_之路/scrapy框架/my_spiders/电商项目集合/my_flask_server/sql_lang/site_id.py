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
_32 = '蜜芽'

"""
常用查询sql_str
"""
# 查询某个商品是否已录入
sql_str = '''
select UserName, CreateTime, GoodsName, GoodsID, ConvertTime, MainGoodsID
from dbo.GoodsInfoAutoGet 
where GoodsID='';
'''

# 查询最新入录的商品
sql_str_2 = '''
select top 20 ID, UserName, GoodsUrl, CreateTime, MainGoodsID, IsPriceChange
from dbo.GoodsInfoAutoGet 
where GETDATE()-CreateTime < 1
order by ID desc;
'''

# 查询某个goods的信息变动
sql_str_3 = '''
select top 10 GoodsID, SiteID, SKUInfo, PriceChangeInfo, IsPriceChange, sku_info_trans_time, is_spec_change, spec_trans_time, is_stock_change, stock_change_info
from dbo.GoodsInfoAutoGet
where GoodsID=''
'''

# 知道PID。查询当前被死锁的表
sql_str_4 = '''
select request_session_id spid, OBJECT_NAME(resource_associated_entity_id) tablename
from sys.dm_tran_locks 
where resource_type='OBJECT'
'''

# 死锁解锁
sql_str_5 = '''
declare @spid  int 
Set @spid = 57             --锁表进程
declare @sql varchar(1000)
set @sql='kill '+cast(@spid  as varchar)
exec(@sql)
'''

# 秒杀取值(修改方案: 全按第一类来)(over)
sql_str_6 = '''
-- 秒杀取值
-- 第一类
-- price:normal_price, taobao_price:detail_price(就是秒杀价)
select top 4 price, taobao_price, sku_Info, miaosha_begin_time, miaosha_end_time
from dbo.chuchujie_xianshimiaosha
order by id DESC

-- price:normal_price, taobao_price:detail_price(就是秒杀价)
select top 4 price, taobao_price, sku_Info, miaosha_begin_time, miaosha_end_time
from dbo.juanpi_xianshimiaosha
order by id DESC

-- price:normal_price, taobao_price:detail_price(就是秒杀价)
select top 4 price, taobao_price, sku_Info, miaosha_begin_time, miaosha_end_time
from dbo.mogujie_xianshimiaosha
order by id DESC

-- 第二类
-- price:detail_price, taobao_price:秒杀价, if detail_price == price set detail_price = taobao_price
select top 4 price, taobao_price, sku_Info, miaosha_begin_time, miaosha_end_time
from dbo.zhe_800_xianshimiaosha
order by id DESC

-- price:detail_price, taobao_price:秒杀价, if detail_price == price set detail_price = taobao_price
select top 4 price, taobao_price, sku_Info, miaosha_begin_time, miaosha_end_time
from dbo.jumeiyoupin_xianshimiaosha
order by id DESC

-- 第三类
-- price:秒杀价, taobao_price:秒杀价, 不对比, 直接设置 set detail_price = taobao_price
select top 4 price, taobao_price, sku_Info, miaosha_begin_time, miaosha_end_time
from dbo.mia_xianshimiaosha
order by id DESC
'''