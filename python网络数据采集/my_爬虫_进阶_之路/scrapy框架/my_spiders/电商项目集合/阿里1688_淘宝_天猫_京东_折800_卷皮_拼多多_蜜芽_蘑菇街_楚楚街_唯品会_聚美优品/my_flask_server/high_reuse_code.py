# coding:utf-8

'''
@author = super_fazai
@File    : high_reuse_code.py
@Time    : 2018/8/2 09:57
@connect : superonesfazai@gmail.com
'''

from my_items import GoodsItem
from decimal import Decimal

from fzutils.time_utils import get_shanghai_time
from fzutils.common_utils import _print

__all__ = [
    '_get_right_model_data',            # 得到规范GoodsItem的model
]

def _get_right_model_data(data, site_id=None, logger=None):
    '''
    得到规范化的数据
    :param data:
    :return:
    '''
    data_list = data
    tmp = GoodsItem()
    tmp['goods_id'] = data_list['goods_id']     # 官方商品id
    tmp['main_goods_id'] = data_list.get('main_goods_id', '')

    if data_list.get('spider_url') is not None:
        tmp['goods_url'] = data_list['spider_url']  # 商品地址
    elif data_list.get('goods_url') is not None:
        tmp['goods_url'] = data_list['goods_url']  # 商品地址
    else:
        tmp['goods_url'] = ''       # 更新时, goods_url不传

    if data_list.get('username') is not None:
        tmp['username'] = data_list['username']     # 操作人员username
    else:
        tmp['username'] = '18698570079'

    now_time = get_shanghai_time()
    tmp['create_time'] = now_time               # 操作时间
    tmp['modify_time'] = now_time               # 修改时间

    if site_id is not None:
        # 采集的来源地
        tmp['site_id'] = site_id                # 采集来源地
    else:
        # my_lg.error('site_id赋值异常!请检查!出错地址:{0}'.format(tmp['goods_url']))
        _print(
            msg='site_id赋值异常!请检查!出错地址:{0}'.format(tmp['goods_url']),
            logger=logger,
            log_level=2
        )
        raise ValueError('site_id赋值异常!')

    if site_id == 2:
        tmp['shop_name'] = data_list['company_name']
    else:
        tmp['shop_name'] = data_list['shop_name']  # 公司名称

    tmp['title'] = data_list['title']  # 商品名称
    tmp['sub_title'] = data_list['sub_title'] if data_list.get('sub_title') is not None else '' # 商品子标题

    tmp['link_name'] = data_list['link_name'] if data_list.get('link_name') is not None else '' # 卖家姓名
    tmp['account'] = data_list['account'] if data_list.get('account') is not None else '' # 掌柜名称

    if data_list.get('all_sell_count') is not None:
        tmp['all_sell_count'] = str(data_list['all_sell_count'])  # 总销量
    elif data_list.get('sell_count') is not None:
        tmp['all_sell_count'] = str(data_list['sell_count'])        # 淘宝, 天猫月销量
    else:
        tmp['all_sell_count'] = ''

    # 设置最高价price， 最低价taobao_price
    try:
        tmp['price'] = data_list['price'] if isinstance(data_list['price'], Decimal) else Decimal(data_list['price']).__round__(2)
        tmp['taobao_price'] = data_list['taobao_price'] if isinstance(data_list['taobao_price'], Decimal) else Decimal(data_list['taobao_price']).__round__(2)
    except Exception as e:      # eg: 楚楚街秒杀券, 会有异常抛出
        raise e

    # 批发价
    tmp['price_info'] = data_list['price_info'] if data_list.get('price_info') is not None else []  # 价格信息

    if site_id == 2:
        detail_name_list = []
        for item in data_list['sku_props']:
            detail_name_list.append({
                'spec_name': item.get('prop'),
            })
        tmp['detail_name_list'] = detail_name_list
    else:
        tmp['detail_name_list'] = data_list.get('detail_name_list', [])  # 标签属性名称

    if site_id == 2:
        tmp['price_info_list'] = data_list.get('sku_map', [])
    else:
        tmp['price_info_list'] = data_list.get('price_info_list', [])  # 每个规格对应价格及其库存

    tmp['all_img_url'] = data_list.get('all_img_url')  # 所有示例图片地址

    if site_id == 2:
        tmp['p_info'] = data_list.get('property_info', [])
    else:
        tmp['p_info'] = data_list.get('p_info', [])  # 详细信息

    if site_id == 2:
        tmp['div_desc'] = data_list.get('detail_info', '')
    else:
        tmp['div_desc'] = data_list.get('div_desc', '')  # 下方div

    tmp['schedule'] = data_list.get('schedule') if data_list.get('schedule') is not None else []

    tmp['is_delete'] = data_list.get('is_delete') if data_list.get('is_delete') is not None else 0

    tmp['shelf_time'] = data_list.get('shelf_time', '')
    tmp['delete_time'] = data_list.get('delete_time', '')

    tmp['is_price_change'] = data_list.get('_is_price_change', 0)
    tmp['price_change_info'] = data_list.get('_price_change_info') if data_list.get('_price_change_info') is not None else []

    tmp['miaosha_time'] = data_list.get('miaosha_time', {})
    tmp['miaosha_begin_time'] = data_list.get('miaosha_begin_time', '')
    tmp['miaosha_end_time'] = data_list.get('miaosha_end_time', '')

    tmp['pintuan_time'] = data_list.get('pintuan_time', {})
    tmp['pintuan_begin_time'] = data_list.get('pintuan_begin_time', '')
    tmp['pintuan_end_time'] = data_list.get('pintuan_end_time', '')

    tmp['gender'] = data_list.get('gender', '')
    tmp['page'] = data_list.get('page', '')
    tmp['tab_id'] = data_list.get('tab_id', '')
    tmp['tab'] = data_list.get('tab', '')
    tmp['sort'] = data_list.get('sort', '')
    tmp['stock_info'] = data_list.get('stock_info', [])
    tmp['pid'] = data_list.get('pid', '')
    tmp['event_time'] = data_list.get('event_time', '')
    tmp['fcid'] = data_list.get('fcid', '')
    tmp['spider_time'] = data_list.get('spider_time', '')
    tmp['session_id'] = data_list.get('session_id', '')

    return tmp
