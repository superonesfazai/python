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
select top 20 ID, UserName, GoodsUrl, CreateTime, MainGoodsID, IsPriceChange, ModfiyTime
from dbo.GoodsInfoAutoGet 
where GETDATE()-CreateTime < 1
order by ID desc;
'''

# 查询某个goods的信息变动
sql_str_3 = '''
select MainGoodsID, GoodsID, SiteID, SKUInfo, PriceChangeInfo, IsPriceChange, sku_info_trans_time, is_spec_change, spec_trans_time, is_stock_change, stock_change_info, stock_trans_time
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

# 查看db大小
sql_str_17 = '''
exec sp_helpdb gather 
'''

# 查看db每张表的行数
sql_str_22 = '''
SELECT a.name, b.rows
FROM sysobjects AS a 
INNER JOIN sysindexes AS b ON a.id = b.id
WHERE (a.type = 'u') 
AND (b.indid IN (0, 1))
ORDER BY b.rows DESC
'''

# 查看点半每张表大小
sql_str_23 = '''
SELECT 
    t.NAME AS TableName,
    s.Name AS SchemaName,
    p.rows AS RowCounts,
    SUM(a.total_pages) * 8 AS TotalSpaceKB, 
    CAST(ROUND(((SUM(a.total_pages) * 8) / 1024.00), 2) AS NUMERIC(36, 2)) AS TotalSpaceMB,
    SUM(a.used_pages) * 8 AS UsedSpaceKB, 
    CAST(ROUND(((SUM(a.used_pages) * 8) / 1024.00), 2) AS NUMERIC(36, 2)) AS UsedSpaceMB, 
    (SUM(a.total_pages) - SUM(a.used_pages)) * 8 AS UnusedSpaceKB,
    CAST(ROUND(((SUM(a.total_pages) - SUM(a.used_pages)) * 8) / 1024.00, 2) AS NUMERIC(36, 2)) AS UnusedSpaceMB
FROM 
    sys.tables t
INNER JOIN      
    sys.indexes i ON t.OBJECT_ID = i.object_id
INNER JOIN 
    sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id
INNER JOIN 
    sys.allocation_units a ON p.partition_id = a.container_id
LEFT OUTER JOIN 
    sys.schemas s ON t.schema_id = s.schema_id
WHERE 
    t.NAME NOT LIKE 'dt%' 
    AND t.is_ms_shipped = 0
    AND i.OBJECT_ID > 255 
GROUP BY 
    t.Name, s.Name, p.Rows
ORDER BY t.Name
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

'''
company
'''
sql_str_7 = '''
select unique_id as ID, company_link as '官网地址', company_name as '公司 or 工厂 or 部门名', legal_person as '法人', phone as '电话', email_address as '邮件', address as '地址', brief_introduction as '简介', business_range as '经营范围', founding_time as '成立时间', employees_num as '员工数'
-- select count(unique_id)
from dbo.company_info 
where site_id=2 
and city_id in (select code from dbo.Region where c_name='上海市')
'''
sql_str_8 = '''
use Gather;
select 
-- a.province_id as '省份id', 
-- a.city_id as '城市id', 
a.company_name as '公司or部门名',
a.legal_person as '法人',
a.phone as '手机',
a.email_address as '邮件',
a.address as '地址',
a.brief_introduction as '简介',
a.business_range as '经营范围',
a.employees_num as '员工人数',
a.company_link as '公司or部门官网地址', 
b.c_name as '城市名'
-- select count(id)
from dbo.company_info as a, dbo.Region as b
-- from dbo.company_info
where site_id=2 
and (phone != '[]' or email_address != '[]')
and a.city_id = b.code
order by id desc;
'''
sql_str_9 = '''
select 
-- a.province_id as '省份id', 
-- a.city_id as '城市id', 
a.company_name as '供应商or厂商名称',
a.legal_person as '法人',
a.phone as '手机',
-- a.email_address as '邮件',
a.address as '地址',
a.brief_introduction as '简介',
a.business_range as '经营范围',
a.founding_time as '成立时间',
-- a.employees_num as '员工人数',
-- a.company_link as '公司or部门官网地址', 
b.c_name as '城市名'
-- select count(id)
from dbo.company_info as a, dbo.Region as b
-- from dbo.company_info
where site_id=5
and phone != '[]'
and a.city_id = b.code
-- order by id desc;
'''
sql_str_10 = '''
select unique_id as ID,  company_name as '供应商or厂商名称', legal_person as '法人', phone as '电话', address as '地址', brief_introduction as '简介', business_range as '经营范围', founding_time as '成立时间'
-- select count(unique_id)
from dbo.company_info 
where site_id=5
and phone != '[]'
and city_id in (select code from dbo.Region where c_name='天津市')
'''
# 义乌购
sql_str_11 = '''
select
a.unique_id as 'id',
a.company_name as '商铺 or 批发商名称',
a.phone as '手机',
a.email_address as '邮件',
a.brief_introduction as '简介',
a.business_range as '经营范围',
a.address as '地址',
b.c_name as '城市名'
-- select count(id)
from dbo.company_info as a, dbo.Region as b
-- from dbo.company_info
where site_id=8
and (phone != '[]' or email_address != '[]')
and a.city_id = b.code
-- order by id desc;
'''

"""
查看某site_id常规商品的更新状况
"""
sql_str_12 = '''
select count(ID)
-- select top 100 GoodsID, shelf_time, IsDelete, ModfiyTime
from dbo.GoodsInfoAutoGet
where MainGoodsID is not null 
-- and IsDelete=0
-- and (SiteID=3 or SiteID=4 or SiteID=6)
and GETDATE()-ModfiyTime > 0.5
and SiteID=2
-- order by shelf_time asc
'''

"""
同步数据
"""
sql_str_13 = '''
-- update dbo.GoodsInfoAutoGet 
-- set is_spec_change = 1,
-- spec_trans_time = GETDATE()
-- where MainGoodsID is not NUll and IsDelete=0

-- update dbo.GoodsInfoAutoGet 
-- set IsPriceChange = 1,
-- PriceChangeInfo=SKUInfo,
-- sku_info_trans_time = GETDATE()
-- where MainGoodsID is not NUll and IsDelete=0

-- update dbo.GoodsInfoAutoGet 
-- set is_stock_change = 1,
-- stock_change_info=SKUInfo,
-- stock_trans_time = GETDATE()
-- where MainGoodsID is not NUll and IsDelete=0
'''

# 批量更改下架状态但是delete_time<shelf_time的商品(原因后台无法更新上架变下架)
sql_str_18 = '''
update dbo.GoodsInfoAutoGet set delete_time=GETDATE()
-- select top 10 MainGoodsID, SiteID, shelf_time, delete_time, IsDelete
-- select count(MainGoodsID)
-- from dbo.GoodsInfoAutoGet
where 
IsDelete=1
and MainGoodsID is not NUll
and shelf_time>delete_time
'''
# 批量更改上架状态但是delete_time>shelf_time的商品(原因后台无法更新下架变上架)
sql_str_19 = '''
update dbo.GoodsInfoAutoGet set shelf_time=GETDATE()
-- select top 10 MainGoodsID, SiteID, shelf_time, delete_time, IsDelete
-- select count(MainGoodsID)
-- from dbo.GoodsInfoAutoGet
where 
IsDelete=0
and MainGoodsID is not NUll
and shelf_time<delete_time
'''

# 批量更改原先下架但是delete_time为空的商品(原因后台无法由上架变下架)
sql_str_20 = '''
update dbo.GoodsInfoAutoGet set delete_time=GETDATE()
where MainGoodsID is not null
and IsDelete=1
and delete_time is null
'''

"""
comment
"""
# 查看指定site_id的comment info
sql_str_14 = '''
select top 500 *
from dbo.goods_comment_new as a, dbo.GoodsInfoAutoGet as b
where a.goods_id =b.GoodsID 
-- and goods_id='6120129'
and (b.SiteID=7 or b.SiteID=8 or b.SiteID=9 or b.SiteID=10)
-- and (b.SiteID=3 or b.SiteID=4 or b.SiteID=6)
-- and b.SiteID=1
'''
# 查看还有多少个goods_id 未被同步到goods_comment_new表中
sql_str_15 = '''
select count(GoodsID)
from dbo.GoodsInfoAutoGet
where MainGoodsID is not null
and IsDelete=0
and GoodsID not in (
select DISTINCT goods_id
from dbo.goods_comment_new
GROUP BY goods_id)
'''
# 查看现有goods comment 更新情况
sql_str_16 = '''
select top 10 GoodsId, CreateTime, comment_modify_time
from dbo.GoodsInfoAutoGet
where MainGoodsID is not null
and IsDelete=0
and GoodsID in (
select DISTINCT goods_id
from dbo.goods_comment_new
GROUP BY goods_id)
ORDER BY comment_modify_time desc
'''

"""
异常数据处理
"""
# 删除下架又上架但是状态还是下架的异常数据
sql_str_24 = '''
update dbo.GoodsInfoAutoGet
set ModfiyTime=GETDATE(), delete_time=GETDATE()
-- select count(*)
-- from dbo.GoodsInfoAutoGet
where MainGoodsID is not null
and IsDelete=1
and shelf_time > delete_time
'''

# 批量下架敏感词商品(注意: 批量执行只会显示最后一次update的结果)
sql_str_25 = '''
DECLARE @ss VARCHAR(100)
set @ss = '%创可贴%'

-- select top 10 *
UPDATE dbo.chuchujie_xianshimiaosha set is_delete=1, modfiy_time=GETDATE()
from dbo.chuchujie_xianshimiaosha
where goods_name like @ss

-- select top 10 *
UPDATE dbo.juanpi_pintuan set is_delete=1, modfiy_time=GETDATE()
from dbo.juanpi_pintuan
where goods_name like @ss

-- select top 10 *
UPDATE dbo.juanpi_xianshimiaosha set is_delete=1, modfiy_time=GETDATE()
from dbo.juanpi_xianshimiaosha
where goods_name like @ss

-- select top 10 *
UPDATE dbo.jumeiyoupin_pintuan set is_delete=1, modfiy_time=GETDATE()
from dbo.jumeiyoupin_pintuan
where goods_name like @ss

-- select top 10 *
UPDATE dbo.jumeiyoupin_xianshimiaosha set is_delete=1, modfiy_time=GETDATE()
from dbo.jumeiyoupin_xianshimiaosha
where goods_name like @ss

-- select top 10 *
UPDATE dbo.mia_pintuan set is_delete=1, modfiy_time=GETDATE()
from dbo.mia_pintuan
where goods_name like @ss

-- select top 10 *
UPDATE dbo.mia_xianshimiaosha set is_delete=1, modfiy_time=GETDATE()
from dbo.mia_xianshimiaosha
where goods_name like @ss

-- select top 10 *
UPDATE dbo.mogujie_pintuan set is_delete=1, modfiy_time=GETDATE()
from dbo.mogujie_pintuan
where goods_name like @ss

-- select top 10 *
UPDATE dbo.mogujie_xianshimiaosha set is_delete=1, modfiy_time=GETDATE()
from dbo.mogujie_xianshimiaosha
where goods_name like @ss

-- select top 10 *
UPDATE dbo.pinduoduo_xianshimiaosha set is_delete=1, modfiy_time=GETDATE()
from dbo.pinduoduo_xianshimiaosha
where goods_name like @ss

-- select top 10 *
UPDATE dbo.tao_qianggou_xianshimiaosha set is_delete=1, modfiy_time=GETDATE()
from dbo.tao_qianggou_xianshimiaosha
where goods_name like @ss

-- select top 10 *
UPDATE dbo.taobao_tiantiantejia set is_delete=1, modfiy_time=GETDATE()
from dbo.taobao_tiantiantejia
where goods_name like @ss

-- -- select top 10 *
UPDATE dbo.zhe_800_pintuan set is_delete=1, modfiy_time=GETDATE()
from dbo.zhe_800_pintuan
where goods_name like @ss

-- select top 10 *
UPDATE dbo.zhe_800_xianshimiaosha set is_delete=1, modfiy_time=GETDATE()
from dbo.zhe_800_xianshimiaosha
where goods_name like @ss

-- select top 10 *
UPDATE dbo.GoodsInfoAutoGet set IsDelete=1, ModfiyTime=GETDATE(), delete_time=GETDATE()
from dbo.GoodsInfoAutoGet
where GoodsName like @ss
'''

# 批量删除关键字中间表中不在GoodsInfoAutoGet中的数据
sql_str_26 = '''
-- select count(id)
-- select top 10 id, goods_id
delete 
from dbo.goods_id_and_keyword_middle_table
where goods_id not in (
select GoodsID
from dbo.GoodsInfoAutoGet)
'''