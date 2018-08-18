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
fz_z8_insert_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, Schedule, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
fz_jp_insert_str = fz_z8_insert_str
fz_pd_insert_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, Schedule, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
fz_vi_insert_str = fz_pd_insert_str
fz_kl_insert_str = fz_pd_insert_str
fz_yx_insert_str = fz_pd_insert_str
fz_yp_insert_str = fz_pd_insert_str

"""
comment
"""
'''select'''
cm_select_str_1 = '''
select goods_id, SiteID as site_id 
from dbo.GoodsInfoAutoGet as a, dbo.all_goods_comment as b 
where a.GoodsID=b.goods_id and a.MainGoodsID is not null and a.IsDelete=0
order by b.id asc'''

cm_select_str_2 = '''
select GoodsID, SiteID 
from dbo.GoodsInfoAutoGet 
where MainGoodsID is not null and IsDelete=0 and GoodsID not in (select goods_id from dbo.all_goods_comment)
ORDER BY ID DESC'''
# 得到评论表中所有goods_id
cm_select_str_3 = 'select goods_id from dbo.all_goods_comment'
'''insert'''
# 评论插入
cm_insert_str_1 = 'insert into dbo.all_goods_comment(goods_id, create_time, modify_time, comment_info) values(%s, %s, %s, %s)'
'''update'''
# 评论更新
cm_update_str_1 = 'update dbo.all_goods_comment set modify_time=%s, comment_info=%s where goods_id=%s'

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

'''update'''
# 常规goods下架标记
al_update_str_1 = 'update dbo.GoodsInfoAutoGet set IsDelete=1 where GoodsID=%s'
# 常规goods更新
al_update_str_2 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, GoodsName=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, DetailInfo=%s, PropertyInfo=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, {0} {1} where GoodsID = %s'

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
'''insert'''
# 带MainGoodsID的插入
tb_insert_str_1 = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete, MainGoodsID) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# 不带MainGoodsID的插入
tb_insert_str_2 = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# 天天特价插入
tb_insert_str_3 = 'insert into dbo.taobao_tiantiantejia(goods_id, goods_url, create_time, modfiy_time, shop_name, account, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, month_sell_count, schedule, tejia_begin_time, tejia_end_time, block_id, tag_id, father_sort, child_sort, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

'''update'''
# 常规goods更新
tb_update_str_1 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, {0} {1} where GoodsID = %s'
# 天天特价更新
tb_update_str_2 = 'update dbo.taobao_tiantiantejia set modfiy_time = %s, shop_name=%s, account=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, month_sell_count=%s, is_delete=%s where goods_id=%s'

"""
天猫
"""
'''select'''
# 新表数据查询
tm_select_str_1 = 'select SiteID, GoodsID, IsDelete, MyShelfAndDownTime, Price, TaoBaoPrice from dbo.GoodsInfoAutoGet where (SiteID=3 or SiteID=4 or SiteID=6) order by ID desc'
# old表转新表数据查询
tm_select_str_2 = 'select GoodsOutUrl, goods_id from db_k85u.dbo.goodsinfo where OutGoodsType<=13 and onoffshelf=1 and not exists (select maingoodsid from gather.dbo.GoodsInfoAutoGet c where c.maingoodsid=goodsinfo.goods_id)'
'''insert'''
# 带MainGoodsID的插入
tm_insert_str_1 = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete, MainGoodsID) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# 不带MainGoodsID的插入
tm_insert_str_2 = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# 淘抢购插入
tm_insert_str_3 = 'insert into dbo.tao_qianggou_xianshimiaosha(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_info, all_image_url, property_info, detail_info, schedule, miaosha_time, miaosha_begin_time, miaosha_end_time, page, spider_time, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

'''update'''
# 常规goods更新
tm_update_str_1 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, {0} {1} where GoodsID = %s'
# 淘抢购更新
tm_update_str_2 = 'update dbo.tao_qianggou_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, schedule=%s where goods_id = %s'

"""
jd
"""
'''insert'''
# 带MainGoodsID的插入
jd_insert_str_1 = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete, MainGoodsID) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# 不带MainGoodsID的插入
jd_insert_str_2 = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

'''update'''
# 常规goods更新
jd_update_str_1 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, {0} {1} where GoodsID = %s'

"""
折800
"""
'''select'''
# 拼团db goods查询
z8_select_str_1 = 'select goods_id, is_delete from dbo.zhe_800_pintuan where site_id=17'
# 拼团更新待更新数据查询
z8_select_str_2 = '''
select goods_id, is_delete 
from dbo.zhe_800_pintuan 
where site_id=17 and GETDATE()-modfiy_time>2'''
'''insert'''
# 秒杀插入
z8_insert_str_1 = 'insert into dbo.zhe_800_xianshimiaosha(goods_id, goods_url, username, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, schedule, stock_info, miaosha_time, miaosha_begin_time, miaosha_end_time, session_id, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# 拼团插入
z8_insert_str_2 = 'insert into dbo.zhe_800_pintuan(goods_id, goods_url, username, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_info, all_image_url, all_sell_count, property_info, detail_info, schedule, miaosha_begin_time, miaosha_end_time, page, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
'''update'''
# 常规goods更新
z8_update_str_1 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s, {0} {1} where GoodsID = %s'
# 秒杀更新
z8_update_str_2 = 'update dbo.zhe_800_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, schedule=%s, stock_info=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s where goods_id = %s'
# 拼团更新
z8_update_str_3 = 'update dbo.zhe_800_pintuan set modfiy_time=%s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, all_sell_count=%s, property_info=%s, detail_info=%s, schedule=%s, is_delete=%s where goods_id = %s'
'''delete'''
# 拼团过期数据清空
z8_delete_str_1 = 'delete from dbo.zhe_800_pintuan where miaosha_end_time < GETDATE()-2'
# 拼团下架标记
z8_delete_str_2 = 'delete from dbo.zhe_800_pintuan where goods_id=%s'

"""
卷皮
"""
'''select'''
# db拼团数据查询
jp_select_str_1 = 'select goods_id, schedule, is_delete from dbo.juanpi_pintuan where site_id=18'
jp_select_str_2 = jp_select_str_1
'''insert'''
# 秒杀插入
jp_insert_str_1 = 'insert into dbo.juanpi_xianshimiaosha(goods_id, goods_url, username, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_info, all_image_url, property_info, detail_info, schedule, stock_info, miaosha_time, miaosha_begin_time, miaosha_end_time, tab_id, page, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# 拼团插入
jp_insert_str_2 = 'insert into dbo.juanpi_pintuan(goods_id, goods_url, username, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_info, all_image_url, all_sell_count, property_info, detail_info, schedule, miaosha_begin_time, miaosha_end_time, page, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
'''update'''
# 常规goods下架标记
jp_update_str_1 = 'update dbo.GoodsInfoAutoGet set IsDelete=1 where GoodsID=%s'
# 常规goods更新
jp_update_str_2 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s, {0} {1} where GoodsID = %s'
# 秒杀更新
jp_update_str_3 = 'update dbo.juanpi_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, schedule=%s, stock_info=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s where goods_id = %s'
# 拼团更新
jp_update_str_4 = 'update dbo.juanpi_pintuan set modfiy_time=%s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, schedule=%s, is_delete=%s where goods_id = %s'
'''delete'''
# 拼团下架清空
jp_delete_str_1 = 'delete from dbo.juanpi_pintuan where miaosha_end_time < GETDATE()-2'
# 拼团下架标记
jp_delete_str_2 = 'delete from dbo.juanpi_pintuan where goods_id=%s'

"""
聚美优品
"""
'''insert'''
# 秒杀插入
jm_insert_str_1 = 'insert into dbo.jumeiyoupin_xianshimiaosha(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, page, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# 拼团插入
jm_insert_str_2 = 'insert into dbo.jumeiyoupin_pintuan(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, all_sell_count, page, sort, tab, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

'''update'''
# 秒杀更新
jm_update_str_1 = 'update dbo.jumeiyoupin_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s where goods_id = %s'
# 拼团更新
jm_update_str_2 = 'update dbo.jumeiyoupin_pintuan set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s, all_sell_count=%s where goods_id = %s'
# 拼团更新2
jm_update_str_3 = 'update dbo.jumeiyoupin_pintuan set modfiy_time=%s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, all_sell_count=%s where goods_id = %s'

"""
楚楚街
"""
'''insert'''
# 秒杀插入
cc_insert_str_1 = 'insert into dbo.chuchujie_xianshimiaosha(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, gender, page, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

'''update'''
# 秒杀更新
cc_update_str_1 = 'update dbo.chuchujie_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s where goods_id = %s'

"""
网易考拉
"""
'''update'''
# 常规goods更新
kl_update_str_1 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, {0} {1} where GoodsID = %s'

"""
蜜芽
"""
'''select'''
# db拼团goods查询
mia_select_str_1 = 'select goods_id, miaosha_time, pid from dbo.mia_pintuan where site_id=21'
mia_select_str_2 = mia_select_str_1
'''insert'''
# 秒杀插入
mia_insert_str_1 = 'insert into dbo.mia_xianshimiaosha(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, pid, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
# 拼团插入
mia_insert_str_2 = 'insert into dbo.mia_pintuan(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, all_sell_count, pid, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
'''update'''
# 秒杀更新
mia_update_str_1 = 'update dbo.mia_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s where goods_id = %s'
# 拼团下架标记
mia_update_str_2 = 'update dbo.mia_pintuan set is_delete=1 where goods_id = %s'
# 拼团更新
mia_update_str_3 = 'update dbo.mia_pintuan set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s, all_sell_count=%s where goods_id = %s'
'''delete'''
# 拼团过期标记
mia_delete_str_1 = 'delete from dbo.mia_pintuan where goods_id=%s'
# 拼团过期清空
mia_delete_str_2 = 'delete from dbo.mia_pintuan where miaosha_end_time < GETDATE()-2'

"""
蘑菇街
"""
'''select'''
# db拼团goods查询
mg_select_str_1 = 'select goods_id, miaosha_time, fcid, page from dbo.mogujie_pintuan where site_id=23'
mg_select_str_2 = mg_select_str_1
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
'''delete'''
# 拼团下架标记
mg_delete_str_1 = 'delete from dbo.mogujie_pintuan where goods_id=%s'
# 拼团过期清空
mg_delete_str_2 = 'delete from dbo.mogujie_pintuan where miaosha_end_time < GETDATE()-2'

"""
拼多多
"""
'''insert'''
# 秒杀插入
pd_insert_str_1 = 'insert into dbo.pinduoduo_xianshimiaosha(goods_id, goods_url, username, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_info, all_image_url, property_info, detail_info, schedule, stock_info, miaosha_time, miaosha_begin_time, miaosha_end_time, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

'''update'''
# 常规goods更新
pd_update_str_1 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s, {0} {1} where GoodsID = %s'
# 秒杀更新
pd_update_str_2 = 'update dbo.pinduoduo_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, schedule=%s, stock_info=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s where goods_id = %s'

"""
唯品会
"""
'''update'''
vip_update_str_1 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s, {0} {1} where GoodsID = %s'

"""
网易严选
"""
'''update'''
# 常规goods更新
yx_update_str_1 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, {0} {1} where GoodsID = %s'

"""
小米有品
"""
'''update'''
# 常规goods更新
yp_update_str_1 = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, {0} {1} where GoodsID = %s'
