# coding:utf-8

'''
@author = super_fazai
@File    : sql_str_controller.py
@Time    : 2017/8/17 16:46
@connect : superonesfazai@gmail.com
'''

"""
sql str controller
"""

"""
flask_server
"""
fz_al_insert_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, GoodsName, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, DetailInfo, PropertyInfo, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
fz_tb_insert_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
fz_tm_insert_str = fz_tb_insert_str
fz_jd_insert_str = fz_tb_insert_str
fz_z8_insert_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, Schedule, SiteID, IsDelete, parent_dir) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
fz_jp_insert_str = fz_z8_insert_str
fz_pd_insert_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, Schedule, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
fz_vi_insert_str = fz_pd_insert_str
fz_kl_insert_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, Schedule, SiteID, IsDelete, parent_dir) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
fz_yx_insert_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, Schedule, SiteID, IsDelete, parent_dir) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
fz_yp_insert_str = fz_pd_insert_str
fz_mi_insert_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, Schedule, parent_dir, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

"""
comment
"""
'''select'''
cm_select_str_1 = '''
select top 888 GoodsID, SiteID 
from dbo.GoodsInfoAutoGet
where MainGoodsID is not null
and IsDelete=0
and GoodsID in (
select DISTINCT goods_id
from dbo.goods_comment_new
GROUP BY goods_id)
ORDER BY comment_modify_time asc
'''
cm_select_str_2 = '''
select GoodsID, SiteID 
from dbo.GoodsInfoAutoGet 
where MainGoodsID is not null and IsDelete=0 and GoodsID not in (select DISTINCT goods_id from dbo.goods_comment_new)
ORDER BY CreateTime DESC
'''
# 得到评论表中所有goods_id
cm_select_str_3 = 'select DISTINCT goods_id from dbo.goods_comment_new'
'''insert'''
# 评论插入
# 老版本对应all_goods_comment 表
cm_insert_str_1 = 'insert into dbo.all_goods_comment(goods_id, create_time, modify_time, comment_info) values(%s, %s, %s, %s)'
# 新版
cm_insert_str_2 = 'insert into dbo.goods_comment_new(goods_id, create_time, buyer_name, head_img_url, sku_info, purchase_quantify, comment_content, comment_date, img_url_list, video_url, star_level, append_comment_content, append_comment_date, append_comment_img_url_list) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
'''update'''
# 评论更新
cm_update_str_1 = 'update dbo.all_goods_comment set modify_time=%s, comment_info=%s where goods_id=%s'
# comment更新时间点记录
cm_update_str_2 = 'update dbo.GoodsInfoAutoGet set comment_modify_time=%s where GoodsID=%s'

"""
关键字spider
"""
'''select'''
# 获取keywords
kw_select_str_1 = 'select id, keyword from dbo.goods_keywords where is_delete=0'
kw_select_str_2 = 'select GoodsID from dbo.GoodsInfoAutoGet'
# 中间表goods_id_and_keyword_middle_table是否已新增该关键字的id
kw_select_str_3 = 'select keyword_id from dbo.goods_id_and_keyword_middle_table where goods_id=%s'
# db中原先的keyword
kw_select_str_4 = 'select keyword from dbo.goods_keywords where is_delete=0'
'''insert'''
# 中间表插入
kw_insert_str_1 = 'insert into dbo.goods_id_and_keyword_middle_table(goods_id, keyword_id) VALUES (%s, %s)'
# 关键字插入
kw_insert_str_2 = 'insert into dbo.goods_keywords(keyword, is_delete) values (%s, %s)'

"""
head_img spider
"""
'''select'''
# 获取所有nick_name
hi_select_str_1 = 'select nick_name from dbo.sina_weibo'

"""
1688
"""
'''select'''
# 查看某个goods_id是否存在
al_select_str_1 = 'select GoodsID from dbo.GoodsInfoAutoGet where SiteID=2 and GoodsID=%s'
# 得到sku_info
al_select_str_2 = 'select SKUInfo from dbo.GoodsInfoAutoGet where GoodsID=%s'
# 新表数据查询
al_select_str_3 = 'select GoodsID, IsDelete, MyShelfAndDownTime, Price, TaoBaoPrice from dbo.GoodsInfoAutoGet where SiteID=2 order by ID desc'
# old表转新表数据查询
al_select_str_4 = 'select GoodsOutUrl, goods_id from db_k85u.dbo.goodsinfo where OutGoodsType<=13 and onoffshelf=1 and not exists (select maingoodsid from gather.dbo.GoodsInfoAutoGet c where c.maingoodsid=goodsinfo.goods_id)'
# goods_id是否已存在于db
al_select_str_5 = al_select_str_1
# 常规goods待更新数据获取(用asc, 使未被更新的优先更新)
# and IsDelete=0
al_select_str_6 = '''
select top 1200 SiteID, GoodsID, IsDelete, Price, TaoBaoPrice, shelf_time, delete_time, SKUInfo, IsPriceChange, is_spec_change, PriceChangeInfo, is_stock_change, stock_change_info, sku_info_trans_time, spec_trans_time, stock_trans_time
from dbo.GoodsInfoAutoGet 
where SiteID=2 
and MainGoodsID is not null 
and IsDelete=0
order by ModfiyTime asc
'''

'''update'''
# 常规goods下架标记
al_update_str_1 = 'update dbo.GoodsInfoAutoGet set IsDelete=1, ModfiyTime=%s where GoodsID=%s'
# 常规goods更新
al_update_str_2 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, GoodsName=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, DetailInfo=%s, PropertyInfo=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, sku_info_trans_time=%s, is_spec_change=%s, spec_trans_time=%s, is_stock_change=%s, stock_trans_time=%s, stock_change_info=%s, {0} {1} where GoodsID = %s'

'''insert'''
# 带MainGoodsID的插入
al_insert_str_1 = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, GoodsName, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, DetailInfo, PropertyInfo, SiteID, IsDelete, MainGoodsID) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# 不带MainGoodsID的插入
al_insert_str_2 = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, GoodsName, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, DetailInfo, PropertyInfo, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

"""
淘宝
"""
'''select'''
# 新表数据查询
tb_select_str_1 = 'select GoodsID, IsDelete, MyShelfAndDownTime from dbo.GoodsInfoAutoGet where SiteID=1'
# old表转新表数据查询
tb_select_str_2 = 'select GoodsOutUrl, goods_id from db_k85u.dbo.goodsinfo where OutGoodsType<=13 and onoffshelf=1 and not exists (select maingoodsid from gather.dbo.GoodsInfoAutoGet c where c.maingoodsid=goodsinfo.goods_id)'
# 常规goods实时更新
# and IsDelete=0 下架的也进行监控, 测试发现: 只是部分会无数据, 总体IsDelete=1的也可以的
tb_select_str_3 = '''
select top 1000 SiteID, GoodsID, IsDelete, Price, TaoBaoPrice, shelf_time, delete_time, SKUInfo, IsPriceChange, is_spec_change, PriceChangeInfo, is_stock_change, stock_change_info, sku_info_trans_time, spec_trans_time, stock_trans_time 
from dbo.GoodsInfoAutoGet 
where SiteID=1 
and MainGoodsID is not null
-- and MainGoodsID=157097
-- and GoodsID='561349437472'
order by ModfiyTime asc
'''
# 淘抢购实时更新
tb_select_str_4 = 'select goods_id, miaosha_time, goods_url, page, spider_time from dbo.tao_qianggou_xianshimiaosha where site_id=28'
tb_select_str_5 = tb_select_str_4
# 天天特价秒杀
tb_select_str_6 = 'select goods_id, is_delete, tejia_end_time, block_id, tag_id from dbo.taobao_tiantiantejia where site_id=19'
# 天天特价实时更新
# and GETDATE()-modfiy_time > 2
tb_select_str_7 = '''
select goods_id, is_delete, tejia_end_time, block_id, tag_id 
from dbo.taobao_tiantiantejia 
where site_id=19 
and is_delete=0 
and MainGoodsID is not null
'''
'''insert'''
# 带MainGoodsID的插入
tb_insert_str_1 = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete, MainGoodsID) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# 不带MainGoodsID的插入
tb_insert_str_2 = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# 天天特价插入
tb_insert_str_3 = 'insert into dbo.taobao_tiantiantejia(goods_id, goods_url, create_time, modfiy_time, shop_name, account, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, month_sell_count, schedule, tejia_begin_time, tejia_end_time, block_id, tag_id, father_sort, child_sort, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
'''update'''
# 常规goods更新
tb_update_str_1 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, sku_info_trans_time=%s, is_spec_change=%s, spec_trans_time=%s, is_stock_change=%s, stock_trans_time=%s, stock_change_info=%s, {0} {1} where GoodsID = %s'
# 天天特价更新
tb_update_str_2 = 'update dbo.taobao_tiantiantejia set modfiy_time = %s, shop_name=%s, account=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, month_sell_count=%s, is_delete=%s where goods_id=%s'
# 常规goods下架标记
tb_update_str_3 = 'update dbo.GoodsInfoAutoGet set IsDelete=1, ModfiyTime=%s  where GoodsID=%s'
# 秒杀逻辑删
tb_update_str_4 = 'update dbo.tao_qianggou_xianshimiaosha set is_delete=1, modfiy_time=%s where goods_id=%s'
# 天天特价下架标记
tb_update_str_5 = 'update dbo.taobao_tiantiantejia set is_delete=1, modfiy_time=%s where goods_id=%s'
'''delete'''
# 淘抢购下架删除
tb_delete_str_1 = 'delete from dbo.tao_qianggou_xianshimiaosha where goods_id=%s'
# 天天特价过期清空
tb_delete_str_2 = 'delete from dbo.taobao_tiantiantejia where tejia_end_time < GETDATE()-2'

"""
天猫
"""
'''select'''
# 新表数据查询
tm_select_str_1 = 'select SiteID, GoodsID, IsDelete, MyShelfAndDownTime, Price, TaoBaoPrice from dbo.GoodsInfoAutoGet where (SiteID=3 or SiteID=4 or SiteID=6) order by ID desc'
# old表转新表数据查询
tm_select_str_2 = 'select GoodsOutUrl, goods_id from db_k85u.dbo.goodsinfo where OutGoodsType<=13 and onoffshelf=1 and not exists (select maingoodsid from gather.dbo.GoodsInfoAutoGet c where c.maingoodsid=goodsinfo.goods_id)'
# 常规goods实时更新(下架的也更新)
# and IsDelete=0 下架的也进行监控, 测试发现: 只是部分会无数据, 总体IsDelete=1的也可以的
# and MainGoodsID=134804
tm_select_str_3 = '''
select top 1000 SiteID, GoodsID, IsDelete, Price, TaoBaoPrice, shelf_time, delete_time, SKUInfo, IsPriceChange, is_spec_change, PriceChangeInfo, is_stock_change, stock_change_info, sku_info_trans_time, spec_trans_time, stock_trans_time 
from dbo.GoodsInfoAutoGet 
where MainGoodsID is not null 
and (SiteID=3 or SiteID=4 or SiteID=6) 
-- and GoodsID='45095189863'
-- and MainGoodsID=32055
order by ModfiyTime asc
'''
'''insert'''
# 带MainGoodsID的插入
tm_insert_str_1 = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete, MainGoodsID) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# 不带MainGoodsID的插入
tm_insert_str_2 = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# 淘抢购插入
tm_insert_str_3 = 'insert into dbo.tao_qianggou_xianshimiaosha(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_info, all_image_url, property_info, detail_info, schedule, miaosha_time, miaosha_begin_time, miaosha_end_time, page, spider_time, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

'''update'''
# 常规goods更新
tm_update_str_1 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, sku_info_trans_time=%s, is_spec_change=%s, spec_trans_time=%s, is_stock_change=%s, stock_trans_time=%s, stock_change_info=%s, {0} {1} where GoodsID = %s'
# 淘抢购更新
tm_update_str_2 = 'update dbo.tao_qianggou_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, schedule=%s where goods_id = %s'
tm_update_str_3 = 'update dbo.GoodsInfoAutoGet set IsDelete=1, ModfiyTime=%s where GoodsID=%s'

"""
jd
"""
'''select'''
# 常规goods实时更新数据获取
jd_select_str_1 = '''
select top 1000 SiteID, GoodsID, IsDelete, Price, TaoBaoPrice, shelf_time, delete_time, SKUInfo, IsPriceChange, is_spec_change, PriceChangeInfo, is_stock_change, stock_change_info, sku_info_trans_time, spec_trans_time, stock_trans_time
from dbo.GoodsInfoAutoGet 
where (SiteID=7 or SiteID=8 or SiteID=9 or SiteID=10) 
and MainGoodsID is not null
order by ModfiyTime asc
'''
'''insert'''
# 带MainGoodsID的插入
jd_insert_str_1 = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete, MainGoodsID) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# 不带MainGoodsID的插入
jd_insert_str_2 = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

'''update'''
# 常规goods更新
jd_update_str_1 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, sku_info_trans_time=%s, is_spec_change=%s, spec_trans_time=%s, is_stock_change=%s, stock_trans_time=%s, stock_change_info=%s, {0} {1} where GoodsID = %s'
jd_update_str_2 = 'update dbo.GoodsInfoAutoGet set IsDelete=1, ModfiyTime=%s where GoodsID=%s'

"""
折800
"""
'''select'''
# 拼团db goods查询
z8_select_str_1 = 'select goods_id, is_delete from dbo.zhe_800_pintuan where site_id=17'
# 拼团更新待更新数据查询
z8_select_str_2 = '''
select top 1000 goods_id, is_delete 
from dbo.zhe_800_pintuan 
where site_id=17
order by modfiy_time asc
'''
# 常规goods实时更新
z8_select_str_3 = '''
select top 500 SiteID, GoodsID, IsDelete, Price, TaoBaoPrice, shelf_time, delete_time, SKUInfo, IsPriceChange, is_spec_change, PriceChangeInfo, is_stock_change, stock_change_info, sku_info_trans_time, spec_trans_time, stock_trans_time
from dbo.GoodsInfoAutoGet 
where SiteID=11 
and MainGoodsID is not null
-- and IsDelete=0
-- and GoodsID='ze171216155155183345'
-- and MainGoodsID=37526
order by ModfiyTime asc
'''
# 秒杀实时更新
z8_select_str_4 = '''
select goods_id, miaosha_time, session_id 
from dbo.zhe_800_xianshimiaosha 
where site_id=14 and is_delete = 0
'''
# 包括下架的也要被拿到
z8_select_str_5 = '''
select goods_id, miaosha_time, session_id 
from dbo.zhe_800_xianshimiaosha 
where site_id=14
'''
'''insert'''
# 秒杀插入
z8_insert_str_1 = 'insert into dbo.zhe_800_xianshimiaosha(goods_id, goods_url, username, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, schedule, stock_info, miaosha_time, miaosha_begin_time, miaosha_end_time, session_id, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# 拼团插入
z8_insert_str_2 = 'insert into dbo.zhe_800_pintuan(goods_id, goods_url, username, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_info, all_image_url, all_sell_count, property_info, detail_info, schedule, miaosha_begin_time, miaosha_end_time, page, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
'''update'''
# 常规goods更新
z8_update_str_1 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s, parent_dir=%s, sku_info_trans_time=%s, is_spec_change=%s, spec_trans_time=%s, is_stock_change=%s, stock_trans_time=%s, stock_change_info=%s, {0} {1} where GoodsID = %s'
# 秒杀更新
z8_update_str_2 = 'update dbo.zhe_800_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, schedule=%s, stock_info=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s, parent_dir=%s where goods_id = %s'
# 拼团更新
z8_update_str_3 = 'update dbo.zhe_800_pintuan set modfiy_time=%s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, all_sell_count=%s, property_info=%s, detail_info=%s, schedule=%s, is_delete=%s, parent_dir=%s where goods_id = %s'
# 拼团下架标记
z8_update_str_4 = 'update dbo.zhe_800_pintuan set is_delete=1, modfiy_time=%s where goods_id=%s'
z8_update_str_5 = 'update dbo.GoodsInfoAutoGet set IsDelete=1, ModfiyTime=%s where GoodsID=%s'
# 秒杀逻辑下架标记
z8_update_str_6 = 'update dbo.zhe_800_xianshimiaosha set is_delete=1, modify_time=%s where goods_id=%s'

'''delete'''
# 拼团过期数据清空
z8_delete_str_1 = 'delete from dbo.zhe_800_pintuan where miaosha_end_time < GETDATE()-2'
# 拼团下架标记
z8_delete_str_2 = 'delete from dbo.zhe_800_pintuan where goods_id=%s'
# 秒杀过期清空
z8_delete_str_4 = 'delete from dbo.zhe_800_xianshimiaosha where miaosha_end_time < GETDATE()-2'

"""
卷皮
"""
'''select'''
# db拼团数据查询
jp_select_str_1 = 'select goods_id, schedule, is_delete from dbo.juanpi_pintuan where site_id=18'
jp_select_str_2 = jp_select_str_1
# 常规goods实时更新数据获取
jp_select_str_3 = '''
select SiteID, GoodsID, IsDelete, Price, TaoBaoPrice, shelf_time, delete_time, SKUInfo, IsPriceChange, is_spec_change, PriceChangeInfo, is_stock_change, stock_change_info, sku_info_trans_time, spec_trans_time, stock_trans_time
from dbo.GoodsInfoAutoGet 
where SiteID=12 
and MainGoodsID is not null
-- and IsDelete=0
order by ModfiyTime asc
'''
# 秒杀实时更新
jp_select_str_4 = '''
select goods_id, miaosha_time, tab_id, page 
from dbo.juanpi_xianshimiaosha 
where site_id=15
order by id asc
'''
jp_select_str_5 = jp_select_str_4
'''insert'''
# 秒杀插入
jp_insert_str_1 = 'insert into dbo.juanpi_xianshimiaosha(goods_id, goods_url, username, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_info, all_image_url, property_info, detail_info, schedule, stock_info, miaosha_time, miaosha_begin_time, miaosha_end_time, tab_id, page, site_id, is_delete, parent_dir) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# 拼团插入
jp_insert_str_2 = 'insert into dbo.juanpi_pintuan(goods_id, goods_url, username, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_info, all_image_url, all_sell_count, property_info, detail_info, schedule, miaosha_begin_time, miaosha_end_time, page, site_id, parent_dir, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
'''update'''
# 常规goods下架标记
jp_update_str_1 = 'update dbo.GoodsInfoAutoGet set IsDelete=1 where GoodsID=%s'
# 常规goods更新
jp_update_str_2 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s, sku_info_trans_time=%s, parent_dir=%s, is_spec_change=%s, spec_trans_time=%s, is_stock_change=%s, stock_trans_time=%s, stock_change_info=%s, {0} {1} where GoodsID = %s'
# 秒杀更新
jp_update_str_3 = 'update dbo.juanpi_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, schedule=%s, stock_info=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s, parent_dir=%s where goods_id = %s'
# 拼团更新
jp_update_str_4 = 'update dbo.juanpi_pintuan set modfiy_time=%s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, schedule=%s, is_delete=%s, parent_dir=%s where goods_id = %s'
# 拼团下架标记
jp_update_str_5 = 'update dbo.juanpi_pintuan set is_delete=1 where goods_id = %s'
# 秒杀下架标记
jp_update_str_6 = 'update dbo.juanpi_xianshimiaosha set is_delete=1, modfiy_time=%s where goods_id=%s'
# 拼团下架标记
jp_update_str_7 = 'update dbo.juanpi_pintuan set is_delete=1, modfiy_time=%s  where goods_id = %s'
'''delete'''
# 拼团下架清空
jp_delete_str_1 = 'delete from dbo.juanpi_pintuan where miaosha_end_time < GETDATE()-2'
# 拼团下架删除
jp_delete_str_2 = 'delete from dbo.juanpi_pintuan where goods_id=%s'
# 秒杀下架删除
jp_delete_str_3 = 'delete from dbo.juanpi_xianshimiaosha where goods_id=%s'
# 秒杀过期清空
jp_delete_str_4 = 'delete from dbo.juanpi_xianshimiaosha where miaosha_end_time < GETDATE()-2'

"""
聚美优品
"""
'''select'''
# 秒杀实时更新
jm_select_str_1 = 'select goods_id, miaosha_time, page, goods_url from dbo.jumeiyoupin_xianshimiaosha where site_id=26'
jm_select_str_2 = jm_select_str_1
jm_select_str_3 = 'select goods_id, miaosha_time, tab, page, goods_url from dbo.jumeiyoupin_pintuan where site_id=27'
'''insert'''
# 秒杀插入
jm_insert_str_1 = 'insert into dbo.jumeiyoupin_xianshimiaosha(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, page, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# 拼团插入
jm_insert_str_2 = 'insert into dbo.jumeiyoupin_pintuan(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, all_sell_count, page, sort, tab, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
'''update'''
# 秒杀更新
jm_update_str_1 = 'update dbo.jumeiyoupin_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s where goods_id = %s'
# 拼团更新
jm_update_str_2 = 'update dbo.jumeiyoupin_pintuan set modfiy_time=%s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s, all_sell_count=%s where goods_id = %s'
# 拼团更新2
jm_update_str_3 = 'update dbo.jumeiyoupin_pintuan set modfiy_time=%s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, all_sell_count=%s where goods_id=%s'
# 秒杀下架标记
jm_update_str_4 = 'update dbo.jumeiyoupin_xianshimiaosha set is_delete=1, modfiy_time=%s where goods_id=%s'
# 拼团下架标记
jm_update_str_5 = 'update dbo.jumeiyoupin_pintuan set is_delete=1, modfiy_time=%s where goods_id=%s'
# 拼团下架标记
'''delete'''
# 秒杀下架删除
jm_delete_str_1 = 'delete from dbo.jumeiyoupin_xianshimiaosha where goods_id=%s'
# 秒杀过期清空
jm_delete_str_2 = 'delete from dbo.jumeiyoupin_xianshimiaosha where miaosha_end_time < GETDATE()-2'
# 拼团过期清空
jm_delete_str_3 = 'delete from dbo.jumeiyoupin_pintuan where miaosha_end_time < GETDATE()-2'

"""
楚楚街
"""
'''select'''
# 秒杀实时更新
cc_select_str_1 = 'select goods_id, miaosha_time, gender, page, goods_url from dbo.chuchujie_xianshimiaosha where site_id=24'
cc_select_str_2 = cc_select_str_1
'''insert'''
# 秒杀插入
cc_insert_str_1 = 'insert into dbo.chuchujie_xianshimiaosha(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, gender, page, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
'''update'''
# 秒杀更新
cc_update_str_1 = 'update dbo.chuchujie_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s where goods_id = %s'
cc_update_str_2 = 'update dbo.chuchujie_xianshimiaosha set is_delete=1, modfiy_time=%s where goods_id=%s'
'''delete'''
# 秒杀下架删除
cc_delete_str_1 = 'delete from dbo.chuchujie_xianshimiaosha where goods_id=%s'
# 秒杀过期清空
cc_delete_str_2 = 'delete from dbo.chuchujie_xianshimiaosha where miaosha_end_time < GETDATE()-2'

"""
网易考拉
"""
'''select'''
# 常规goods实时更新数据获取
kl_select_str_1 = '''
select top 500 SiteID, GoodsID, IsDelete, Price, TaoBaoPrice, shelf_time, delete_time, SKUInfo, IsPriceChange, is_spec_change, PriceChangeInfo, is_stock_change, stock_change_info, sku_info_trans_time, spec_trans_time, stock_trans_time
from dbo.GoodsInfoAutoGet 
where SiteID=29 
and MainGoodsID is not null
-- and GETDATE()-ModfiyTime>0.3 
order by ModfiyTime asc'''
'''update'''
# 常规goods更新
kl_update_str_1 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, sku_info_trans_time=%s, is_spec_change=%s, spec_trans_time=%s, is_stock_change=%s, stock_trans_time=%s, stock_change_info=%s, parent_dir=%s, {0} {1} where GoodsID = %s'
# 常规goods下架标记
kl_update_str_2 = 'update dbo.GoodsInfoAutoGet set IsDelete=1 where GoodsID=%s'
kl_update_str_3 = 'update dbo.GoodsInfoAutoGet set IsDelete=1, ModfiyTime=%s  where GoodsID=%s'

"""
蜜芽
"""
'''select'''
# db拼团goods查询
mia_select_str_1 = 'select goods_id, miaosha_time, pid from dbo.mia_pintuan where site_id=21'
# db拼团更新
# and is_delete=0 下架的也进行检查更新(避免上下架状态改变)!!
mia_select_str_2 = '''
select top 1500 goods_id, miaosha_time, pid 
from dbo.mia_pintuan 
where site_id=21 and is_delete=0
order by modfiy_time asc
'''
# 秒杀实时更新
mia_select_str_3 = 'select goods_id, miaosha_time, pid from dbo.mia_xianshimiaosha where site_id=20'
mia_select_str_4 = mia_select_str_3
# 常规goods实时更新
mia_select_str_5 = '''
select SiteID, GoodsID, IsDelete, Price, TaoBaoPrice, shelf_time, delete_time, SKUInfo, IsPriceChange, is_spec_change, PriceChangeInfo, is_stock_change, stock_change_info, sku_info_trans_time, spec_trans_time, stock_trans_time
from dbo.GoodsInfoAutoGet 
where SiteID=32 and GETDATE()-ModfiyTime>0.2 and MainGoodsID is not null
order by ModfiyTime asc'''
'''insert'''
# 秒杀插入
mia_insert_str_1 = 'insert into dbo.mia_xianshimiaosha(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, pid, site_id, is_delete, parent_dir) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# 拼团插入
mia_insert_str_2 = 'insert into dbo.mia_pintuan(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, all_sell_count, pid, site_id, is_delete, parent_dir) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
'''update'''
# 秒杀更新
mia_update_str_1 = 'update dbo.mia_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s, parent_dir=%s where goods_id = %s'
# 拼团下架标记
mia_update_str_2 = 'update dbo.mia_pintuan set is_delete=1 where goods_id = %s'
# 拼团更新
mia_update_str_3 = 'update dbo.mia_pintuan set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s, all_sell_count=%s, parent_dir=%s where goods_id=%s'
# 常规商品实时更新
mia_update_str_4 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, sku_info_trans_time=%s, parent_dir=%s, is_spec_change=%s, spec_trans_time=%s, is_stock_change=%s, stock_trans_time=%s, stock_change_info=%s, {0} {1} where GoodsID=%s'
# 常规商品下架标记
mia_update_str_5 = 'update dbo.GoodsInfoAutoGet set IsDelete=1 where GoodsID=%s'
# 秒杀逻辑删
mia_update_str_6 = 'update dbo.mia_xianshimiaosha set is_delete=1, modfiy_time=%s where goods_id=%s'
mia_update_str_7 = 'update dbo.mia_pintuan set is_delete=1, modfiy_time=%s where goods_id = %s'
'''delete'''
# 拼团过期标记
mia_delete_str_1 = 'delete from dbo.mia_pintuan where goods_id=%s'
# 拼团过期清空
mia_delete_str_2 = 'delete from dbo.mia_pintuan where miaosha_end_time < GETDATE()-2'
# 秒杀下架删除
mia_delete_str_3 = 'delete from dbo.mia_xianshimiaosha where goods_id=%s'
# 秒杀过期清空
mia_delete_str_4 = 'delete from dbo.mia_xianshimiaosha where miaosha_end_time < GETDATE()-2'

"""
蘑菇街
"""
'''select'''
# db拼团goods查询
mg_select_str_1 = 'select goods_id, miaosha_time, fcid, page from dbo.mogujie_pintuan where site_id=23'
mg_select_str_2 = mg_select_str_1
# 秒杀实时更新
mg_select_str_3 = '''
select goods_id, miaosha_time, event_time, goods_url 
from dbo.mogujie_xianshimiaosha 
where site_id=22 and is_delete = 0'''
mg_select_str_4 = '''
select goods_id, miaosha_time, event_time, goods_url 
from dbo.mogujie_xianshimiaosha 
where site_id=22'''
'''insert'''
# 秒杀插入
mg_insert_str_1 = 'insert into dbo.mogujie_xianshimiaosha(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, event_time, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# 拼团插入
mg_insert_str_2 = 'insert into dbo.mogujie_pintuan(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, all_sell_count, fcid, page, sort, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
'''update'''
# 秒杀下架标记
mg_update_str_1 = 'update dbo.mogujie_xianshimiaosha set is_delete=1 where goods_id = %s'
# 秒杀更新
mg_update_str_2 = 'update dbo.mogujie_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s where goods_id = %s'
# 拼团更新
mg_update_str_3 = 'update dbo.mogujie_pintuan set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s, all_sell_count=%s where goods_id = %s'
# 拼团更新2
mg_update_str_4 = 'update dbo.mogujie_pintuan set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s where goods_id = %s'
# 拼团下架标记
mg_update_str_5 = 'update dbo.mogujie_pintuan set is_delete=1, modfiy_time = %s where goods_id=%s'
'''delete'''
# 拼团下架标记
mg_delete_str_1 = 'delete from dbo.mogujie_pintuan where goods_id=%s'
# 拼团过期清空
mg_delete_str_2 = 'delete from dbo.mogujie_pintuan where miaosha_end_time < GETDATE()-2'
# 秒杀下架删除
mg_delete_str_3 = 'delete from dbo.mogujie_xianshimiaosha where goods_id=%s'
# 秒杀过期清空
mg_delete_str_4 = 'delete from dbo.mogujie_xianshimiaosha where miaosha_end_time < GETDATE()-2'

"""
拼多多
"""
'''select'''
# 常规goods实时更新
pd_select_str_1 = '''
select GoodsID, IsDelete, Price, TaoBaoPrice, shelf_time, delete_time, SKUInfo, IsPriceChange, is_spec_change, PriceChangeInfo, is_stock_change, stock_change_info, sku_info_trans_time, spec_trans_time, stock_trans_time 
from dbo.GoodsInfoAutoGet 
where SiteID=13 and MainGoodsID is not null'''
# 秒杀实时更新
pd_select_str_2 = 'select goods_id, miaosha_time from dbo.pinduoduo_xianshimiaosha where site_id=16'
pd_select_str_3 = pd_select_str_2
'''insert'''
# 秒杀插入
pd_insert_str_1 = 'insert into dbo.pinduoduo_xianshimiaosha(goods_id, goods_url, username, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_info, all_image_url, property_info, detail_info, schedule, stock_info, miaosha_time, miaosha_begin_time, miaosha_end_time, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
'''update'''
# 常规goods更新
pd_update_str_1 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s, sku_info_trans_time=%s, is_spec_change=%s, spec_trans_time=%s, is_stock_change=%s, stock_trans_time=%s, stock_change_info=%s, {0} {1} where GoodsID = %s'
# 秒杀更新
pd_update_str_2 = 'update dbo.pinduoduo_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, schedule=%s, stock_info=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s where goods_id = %s'
'''delete'''
# 秒杀下架删除
pd_delete_str_1 = 'delete from dbo.pinduoduo_xianshimiaosha where goods_id=%s'

"""
唯品会
"""
'''select'''
vip_select_str_1 = '''
select GoodsID, IsDelete, Price, TaoBaoPrice, shelf_time, delete_time, SKUInfo, IsPriceChange, is_spec_change, PriceChangeInfo, is_stock_change, stock_change_info, sku_info_trans_time, spec_trans_time, stock_trans_time 
from dbo.GoodsInfoAutoGet 
where SiteID=25
'''
'''update'''
vip_update_str_1 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s, sku_info_trans_time=%s, is_spec_change=%s, spec_trans_time=%s, is_stock_change=%s, stock_trans_time=%s, stock_change_info=%s, {0} {1} where GoodsID = %s'

"""
网易严选
"""
'''select'''
# 常规goods实时更新
# and GETDATE()-ModfiyTime>0.3 and MainGoodsID is not null
yx_select_str_1 = '''
select SiteID, GoodsID, IsDelete, Price, TaoBaoPrice, shelf_time, delete_time, SKUInfo, IsPriceChange, is_spec_change, PriceChangeInfo, is_stock_change, stock_change_info, sku_info_trans_time, spec_trans_time, stock_trans_time
from dbo.GoodsInfoAutoGet 
where SiteID=30 
order by ModfiyTime asc
'''
'''update'''
# 常规goods更新
yx_update_str_1 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, sku_info_trans_time=%s, is_spec_change=%s, spec_trans_time=%s, is_stock_change=%s, stock_trans_time=%s, stock_change_info=%s, parent_dir=%s, {0} {1} where GoodsID = %s'
# 常规goods下架标记
yx_update_str_2 = 'update dbo.GoodsInfoAutoGet set IsDelete=1 where GoodsID=%s'

"""
小米有品
"""
'''select'''
# 常规goods实时更新
yp_select_str_1 = '''
select SiteID, GoodsID, IsDelete, Price, TaoBaoPrice, shelf_time, delete_time, SKUInfo, IsPriceChange, is_spec_change, PriceChangeInfo, is_stock_change, stock_change_info, sku_info_trans_time, spec_trans_time, stock_trans_time 
from dbo.GoodsInfoAutoGet 
where SiteID=31 and GETDATE()-ModfiyTime>0.3 and MainGoodsID is not null
order by ID asc'''
'''update'''
# 常规goods更新
yp_update_str_1 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, sku_info_trans_time=%s, is_spec_change=%s, spec_trans_time=%s, is_stock_change=%s, stock_trans_time=%s, stock_change_info=%s, {0} {1} where GoodsID = %s'
yp_update_str_2 = 'update dbo.GoodsInfoAutoGet set IsDelete=1 where GoodsID=%s'

"""
工商信息
"""
'''select'''
gs_select_str_1 = '''select unique_id from dbo.company_info where site_id=%s'''
'''insert'''
gs_insert_str_1 = '''insert into dbo.company_info(province_id, city_id, unique_id, company_url, company_link, company_name, legal_person, phone, email_address, address, brief_introduction, business_range, founding_time, create_time, site_id, employees_num, type_code, lng, lat) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

"""
zwm
"""
'''select'''
zwm_select_str_1 = '''select unique_id from dbo.zwm_buss_settle_records'''
zwm_select_str_2 = '''select unique_id, approval_status, approval_status_change_time from dbo.zwm_buss_manage_records'''
'''insert'''
zwm_insert_str_1 = 'insert into dbo.zwm_buss_settle_records(unique_id, create_time, shop_name, shop_id, agent_name, top_agent_name, date_settle_type, trans_amount, service_charge, accounting_amount, trans_date, trans_status, settle_type, settle_date) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
zwm_insert_str_2 = 'insert into dbo.zwm_buss_manage_records(unique_id, create_time, modify_time, agent_name, top_agent_name, shop_type, is_high_quality_shop, shop_id, shop_chat_name, phone_num, shop_chant_num, sale, is_real_time, approve_date, rate, account_type, apply_time, process_context, is_non_contact, approval_status, approval_status_change_time) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
'''update'''
zwm_update_str_1 = 'update dbo.zwm_buss_manage_records set modify_time=%s, agent_name=%s, top_agent_name=%s, shop_type=%s, is_high_quality_shop=%s, shop_id=%s, shop_chat_name=%s, phone_num=%s, shop_chant_num=%s, sale=%s, is_real_time=%s, approve_date=%s, rate=%s, account_type=%s, apply_time=%s, process_context=%s, is_non_contact=%s, approval_status=%s, approval_status_change_time=%s where unique_id=%s'
