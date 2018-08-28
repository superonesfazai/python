# coding:utf-8

from scrapy.item import Item
from scrapy import Field    # 只能通过x['aa']或者x.get('aa')访问, x.aa无法访问, 除非重写__getattribute__()
from pprint import pformat
from collections import MutableMapping
import six
from scrapy.utils.trackref import object_ref

__all__ = [
    'DictItem',                 # 可被a.b访问属性的DictItem类
]

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

class BaseItem(object_ref):
    """Base class for all scraped items."""
    pass

class DictItem(MutableMapping, BaseItem):
    fields = {}

    def __init__(self, *args, **kwargs):
        self._values = {}
        if args or kwargs:  # avoid creating dict for most common case
            for k, v in six.iteritems(dict(*args, **kwargs)):
                self[k] = v

    def __getitem__(self, key):
        return self._values[key]

    def __setitem__(self, key, value):
        if key in self.fields:
            self._values[key] = value
        else:
            raise KeyError("%s does not support field: %s" %
                (self.__class__.__name__, key))

    def __delitem__(self, key):
        del self._values[key]

    def __getattr__(self, name):
        if name in self.fields:
            raise AttributeError("Use item[%r] to get field value" % name)
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            raise AttributeError("Use item[%r] = %r to set field value" %
                (name, value))
        super(DictItem, self).__setattr__(name, value)

    def __len__(self):
        return len(self._values)

    def __iter__(self):
        return iter(self._values)

    __hash__ = BaseItem.__hash__

    def keys(self):
        return self._values.keys()

    def __repr__(self):
        return pformat(dict(self))

    def copy(self):
        return self.__class__(self)

