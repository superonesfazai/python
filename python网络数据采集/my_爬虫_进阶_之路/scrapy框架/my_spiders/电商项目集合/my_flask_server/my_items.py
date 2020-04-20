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
    price_change_info = Field()     # 纯规格价格变动记录下的信息
    main_goods_id = Field()         # 公司商品id
    parent_dir = Field()            # parent_dir
    sku_info_trans_time = Field()   # 规格信息变换记录时间点
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
    block_id = Field()              # 未知
    father_sort = Field()           # 未知
    child_sort = Field()            # 未知
    is_spec_change = Field()        # 纯规格变动标记
    spec_trans_time = Field()       # 纯规格变动时间点
    is_stock_change = Field()       # 纯库存变化标记
    stock_trans_time = Field()      # 纯库存变动时间点
    stock_change_info = Field()     # 纯库存变动记录的信息
    is_sku_name_change = Field()    # sku_name是否变动
    sku_name_change_time = Field()  # sku_name变动记录下的时间点

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
    comment_num = Field()           # 评论数 int
    short_name = Field()            # 爬取来源缩写

class CompanyItem(Item):
    """企业 or 商铺对象"""
    province_id = Field()           # 省份id
    city_id = Field()               # city id
    unique_id = Field()             # 企业唯一的id
    company_url = Field()           # 企业信息的url
    company_link = Field()          # 企业的官网网址
    company_status = Field()        # 企业状态
    company_name = Field()          # 企业名称
    legal_person = Field()          # 法人
    phone = Field()                 # 电话
    email_address = Field()         # 企业邮箱
    address = Field()               # 企业地址
    brief_introduction = Field()    # company简介
    business_range = Field()        # 经营范围
    founding_time = Field()         # 成立时间
    create_time = Field()           # 记录创建时间点
    site_id = Field()               # 采集源
    employees_num = Field()         # 员工人数
    type_code = Field()             # 公司 or 商品分类的code
    lng = Field()                   # 经度
    lat = Field()                   # 纬度

class ZWMBusinessSettlementRecordItem(Item):
    """
    zwm 商户结算记录
    """
    unique_id = Field()             # 用于区别每条交易记录, 唯一
    create_time = Field()           # 该记录存储时间点
    shop_name = Field()             # 商户名称
    shop_id = Field()               # 商户编号
    agent_name = Field()            # 代理商名称
    top_agent_name = Field()        # 顶级代理商名称
    date_settle_type = Field()      # 结算类型
    trans_amount = Field()          # 交易金额
    service_charge = Field()        # 手续费
    accounting_amount = Field()     # 入账金额
    trans_date = Field()            # 交易日期
    trans_status = Field()          # 交易状态
    settle_type = Field()           # 结算类型
    settle_date = Field()           # 结算日期

class ZWMBusinessManageRecordItem(Item):
    """
    zwm 商户及门店记录
    """
    unique_id = Field()                     # 用于区别每条交易记录, 唯一, 用后台自身的id, item.get('id', '')
    create_time = Field()                   # 该记录存储时间点
    modify_time = Field()                   # 该记录更新时间点, 因为人工会改动
    agent_name = Field()                    # 代理商名称
    top_agent_name = Field()                # 顶级代理商名称
    shop_type = Field()                     # 商户类型
    is_high_quality_shop = Field()          # 是否为高质量商户, 0 否 1是
    shop_id = Field()                       # 商户编号
    shop_chat_name = Field()                # 商户注册名称
    phone_num = Field()                     # 手机号
    shop_chant_num = Field()                # 门店数量
    sale = Field()                          # 销售
    is_real_time = Field()                  # 是否开通实时到账, 0 否 1是
    approve_date = Field()                  # 审核通过日期
    rate = Field()                          # 费率
    account_type = Field()                  # 账户性质
    apply_time = Field()                    # 申请时间
    process_context = Field()               # 受理描述
    is_non_contact = Field()                # 是否开通非接, 0 否 1是
    approval_status = Field()               # 审核状态, 审核通过0, 待审核1, 退回2
    approval_status_change_time = Field()   # 审核状态变动记录时间点

class AskQuestionsResultItem(Item):
    """
    搜题结果item
    """
    question_desc = Field()
    answer = Field()