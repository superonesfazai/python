# coding:utf-8

'''
@author = super_fazai
@File    : my_items.py
@Time    : 2017/10/19 22:17
@connect : superonesfazai@gmail.com
'''

from scrapy.item import Item
from scrapy import Field    # 只能通过x['aa']或者x.get('aa')访问, x.aa无法访问

# ORM 数据库关系对象映射

class GoodsItem(Item):              # Item属性固定，无法外在添加属性(不同于dict)
    goods_id = Field()              # 商品id
    create_time = Field()           # 创建时间点
    modify_time = Field()           # 更改时间点
    goods_url = Field()             # 商品地址
    shop_name = Field()             # 店铺名称
    title = Field()                 # 商品名称
    sub_title = Field()             # 子标题
    link_name = Field()             # 卖家姓名
    account = Field()               # 掌柜名称
    price = Field()                 # 商品最高价
    taobao_price = Field()          # 商品最低价
    price_info = Field()            # 进货价信息
    detail_name_list = Field()      # 标签属性名称
    price_info_list = Field()       # 每个规格对应的价格及其库存
    all_sell_count = Field()        # 商品总销量或者月销量
    all_img_url = Field()           # 所有示例图片
    p_info = Field()                # 商品属性
    div_desc = Field()              # div_desc描述
    is_delete = Field()             # 是否下架
    schedule = Field()              # 官方上下架时间
    my_shelf_and_down_time = Field()# 我的上下架时间
    delete_time = Field()           # 用来记录下架时间点
    is_price_change = Field()       # 记录最高价和最低价是否改变
    price_change_info = Field()     # 最高价最低价价格改变信息
