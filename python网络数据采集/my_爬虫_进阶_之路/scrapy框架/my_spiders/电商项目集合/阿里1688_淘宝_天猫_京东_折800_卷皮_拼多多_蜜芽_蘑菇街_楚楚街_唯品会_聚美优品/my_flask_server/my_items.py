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
    """
    商品关系对象
    """
    goods_id = Field()              # 商品id
    create_time = Field()           # 创建时间点
    modify_time = Field()           # 更改时间点
    username = Field()              # 平台操作人员的手机号
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
    site_id = Field()               # site_id
    schedule = Field()              # 官方商品上下架时间
    my_shelf_and_down_time = Field()# 我的上下架时间
    miaosha_time = Field()          # 秒杀时间段
    miaosha_begin_time = Field()    # 秒杀开始时间点
    miaosha_end_time = Field()      # 秒杀结束时间点
    pintuan_time = Field()          # 拼团时间段
    pintuan_begin_time = Field()    # 拼团开始时间点
    pintuan_end_time = Field()      # 拼团结束时间点
    shelf_time = Field()            # 用来记录1->0的上架时间点
    delete_time = Field()           # 用来记录0->1的下架时间点
    is_price_change = Field()       # 记录最高价和最低价是否改变
    price_change_info = Field()     # 最高价最低价价格改变信息
    main_goods_id = Field()         # 公司商品id
    gender = Field()                # 商品适用性别
    page = Field()                  # 商品所在page的number
    tab_id = Field()                # 商品所在分类tab_id
    tab = Field()                   # tab
    sort = Field()                  # 分类名
    stock_info = Field()            # 商品在售库存, 秒杀里的
    pid = Field()                   # 未知
    event_time = Field()            # 未知
    fcid = Field()                  # 未知
    spider_time = Field()           # 未知
    session_id = Field()            # 未知

class CommentItem(Item):
    """
    评论关系对象
    """
    goods_id = Field()              # 商品id
    create_time = Field()           # 创建时间点
    modify_time = Field()           # 更改时间点
    _comment_list = Field()         # comment_info

class WellRecommendArticle(Item):
    """
    荐好文章关系对象
    """
    nick_name = Field()             # 推荐人昵称
    head_url = Field()              # 推荐人头像
    profile = Field()               # 推荐人简介或个性签名
    share_id = Field()              # 分享的文章的id
    title = Field()                 # 文章title
    comment_content = Field()       # 达人的评论，可用于荐好首页的文字信息
    share_img_url_list = Field()    # 达人分享的商品图片
    goods_id_list = Field()         # 该文章对应的所有商品的id
    div_body = Field()              # 文章详细介绍的div_body
    gather_url = Field()            # 文章采集地址
    create_time = Field()           # 文章录入的创建时间
    site_id = Field()               # 采集的位置类型int
    goods_url_list = Field()        # 该文章待抓取的商品地址
    tags = Field()                  # 用于存微淘的tags信息
    share_goods_base_info = Field() # goods_id对应goods_url
    video_url = Field()             # article的视频url
    likes = Field()                 # 点赞数 int
    collects = Field()              # 收藏数 int
