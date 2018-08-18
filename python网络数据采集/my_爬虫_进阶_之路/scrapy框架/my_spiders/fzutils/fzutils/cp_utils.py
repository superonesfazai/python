# coding:utf-8

'''
@author = super_fazai
@File    : cp_utils.py
@Time    : 2018/7/13 18:05
@connect : superonesfazai@gmail.com
'''

# cp的utils

import json
import asyncio

from .common_utils import _print
from .time_utils import string_to_datetime

__all__ = [
    '_get_price_change_info',                               # cp用来记录价格改变信息
    'get_shelf_time_and_delete_time',                       # cp得到shelf_time和delete_time
    'get_miaosha_begin_time_and_miaosha_end_time',          # cp返回秒杀开始和结束时间
    'filter_invalid_comment_content',                       # cp过滤无效comment

    # 淘宝签名相关
    'calculate_right_sign',                                 # 获取淘宝sign
    'get_taobao_sign_and_body',                             # 得到淘宝带签名sign的接口数据

    # get model data
    '_get_right_model_data',                                # 得到规范化GoodsItem model的数据
]

def get_shelf_time_and_delete_time(tmp_data, is_delete, shelf_time, delete_time):
    '''
    公司得到my_shelf_and_down_time和delete_time
    :param tmp_data:
    :param is_delete:
    :param shelf_time: datetime or ''
    :param delete_time: datetime or ''
    :return: delete_time datetime or '', shelf_time datetime or ''
    '''
    from .time_utils import get_shanghai_time

    tmp_shelf_time = shelf_time if shelf_time is not None else ''
    tmp_down_time = delete_time if delete_time is not None else ''
    _ = str(get_shanghai_time())

    # 设置最后刷新的商品状态上下架时间
    # 1. is_delete由0->1 为下架时间点 delete_time
    # 2. is_delete由1->0 为上架时间点 shelf_time
    if tmp_data['is_delete'] != is_delete:  # 表示状态改变
        if is_delete == 1 and tmp_data['is_delete'] == 0:
            # is_delete由1->0 表示商品状态下架变为上架，记录上架时间点
            shelf_time = _
            delete_time = tmp_down_time
        else:
            # is_delete由0->1 表示商品状态上架变为下架，记录下架时间点
            shelf_time = tmp_shelf_time
            delete_time = _

    else:  # 表示状态不变
        # print('商品状态不变!')
        if tmp_data['is_delete'] == 0:  # 原先还是上架状态的
            if tmp_shelf_time == '':
                if tmp_down_time == '':
                    shelf_time = _
                    delete_time = ''
                else:
                   shelf_time = _
                   delete_time = tmp_down_time
            else:
                if tmp_down_time == '':
                    shelf_time = tmp_shelf_time
                    delete_time = ''
                else:
                    shelf_time = tmp_shelf_time
                    delete_time = tmp_down_time

        else:                           # 原先还是下架状态的
            if tmp_shelf_time == '':
                if tmp_down_time == '':
                    shelf_time = ''
                    delete_time = _
                else:
                    shelf_time = ''
                    delete_time = tmp_down_time
            else:
                if tmp_down_time == '':
                    shelf_time = tmp_shelf_time
                    delete_time = _
                else:
                    shelf_time = tmp_shelf_time
                    delete_time = tmp_down_time

    return (shelf_time, delete_time)

def _get_price_change_info(old_price, old_taobao_price, new_price, new_taobao_price):
    '''
    公司用来记录价格改变信息
    :param old_price: 原始最高价 type Decimal
    :param old_taobao_price: 原始最低价 type Decimal
    :param new_price: 新的最高价
    :param new_taobao_price: 新的最低价
    :return: _is_price_change 0 or 1 | _
    '''
    # print(old_price)
    # print(type(old_price))
    # print(new_price)
    # print(type(new_price))
    _is_price_change = 0
    if float(old_price) != float(new_price) or float(old_taobao_price) != float(new_taobao_price):
        _is_price_change = 1

    _ = {
        'old_price': str(old_price),
        'old_taobao_price': str(old_taobao_price),
        'new_price': str(new_price),
        'new_taobao_price': str(new_taobao_price),
    }

    return _is_price_change, _

async def calculate_right_sign(_m_h5_tk: str, data: json):
    '''
    根据给的json对象 data 和 _m_h5_tk计算出正确的sign
    :param _m_h5_tk:
    :param data:
    :return: sign 类型str, t 类型str
    '''
    import execjs
    import time
    from random import randint
    from .safe_utils import md5_encrypt

    # with open('../static/js/get_h_func.js', 'r') as f:  # 打开js源文件
    #     js = f.read()
    #
    # js_parser = execjs.compile(js)                      # 编译js得到python解析对象
    t = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位

    # 构造参数e
    appKey = '12574478'
    # e = 'undefine' + '&' + t + '&' + appKey + '&' + '{"optStr":"{\"displayCount\":4,\"topItemIds\":[]}","bizCode":"tejia_003","currentPage":"1","pageSize":"4"}'
    e = _m_h5_tk + '&' + t + '&' + appKey + '&' + data

    # sign = js_parser.call('h', e)
    sign = md5_encrypt(e)

    return sign, t

async def get_taobao_sign_and_body(base_url, headers:dict, params:dict, data:json, timeout=13, _m_h5_tk='undefine', session=None, logger=None):
    '''
    得到淘宝带签名sign接口数据
    :param base_url:
    :param headers:
    :param params:
    :param data:
    :param timeout:
    :param _m_h5_tk:
    :param session:
    :return: (_m_h5_tk, session, body)
    '''
    import re
    import requests
    from .ip_pools import MyIpPools

    sign, t = await calculate_right_sign(data=data, _m_h5_tk=_m_h5_tk)
    headers['Host'] = re.compile(r'://(.*?)/').findall(base_url)[0]
    params.update({  # 添加下面几个query string
        't': t,
        'sign': sign,
        'data': data,
    })

    # 设置代理ip
    ip_object = MyIpPools()
    proxy = ip_object._get_random_proxy_ip()    # 失败返回False

    tmp_proxies = {
        'http': proxy,
    }

    if session is None:
        session = requests.session()
    else:
        session = session
    try:
        response = session.get(url=base_url, headers=headers, params=params, proxies=tmp_proxies, timeout=timeout)
        _m_h5_tk = response.cookies.get('_m_h5_tk', '')
        _m_h5_tk = _m_h5_tk.split('_')[0]
        # print(s.cookies.items())
        # print(_m_h5_tk)

        body = response.content.decode('utf-8')
        # print(body)

    except Exception as e:
        logger.exception(e)
        _m_h5_tk = ''
        body = ''

    return (_m_h5_tk, session, body)

def get_miaosha_begin_time_and_miaosha_end_time(miaosha_time):
    '''
    返回秒杀开始和结束时间
    :param miaosha_time: 里面的miaosha_begin_time的类型为字符串类型
    :return: tuple  miaosha_begin_time, miaosha_end_time
    '''
    miaosha_begin_time = miaosha_time.get('miaosha_begin_time')
    miaosha_end_time = miaosha_time.get('miaosha_end_time')

    if miaosha_begin_time is None or miaosha_end_time is None:
        miaosha_begin_time = miaosha_time.get('begin_time')
        miaosha_end_time = miaosha_time.get('end_time')

    # 将字符串转换为datetime类型
    miaosha_begin_time = string_to_datetime(miaosha_begin_time)
    miaosha_end_time = string_to_datetime(miaosha_end_time)

    return miaosha_begin_time, miaosha_end_time

def filter_invalid_comment_content(_comment_content):
    '''
    过滤无效评论(复用code)
    :param _comment_content:
    :return: bool
    '''
    import re

    filter_str = '''
    此用户没有填写|评价方未及时做出评价|系统默认好评!|
    假的|坏的|差的|差评|退货|不想要|无良商家|再也不买|
    我也是服了|垃圾|破东西|打电话骂人|骚扰|狗屁东西|
    sb|SB|MB|mb|质量太差
    '''.replace(' ', '').replace('\n', '')
    if re.compile(filter_str).findall(_comment_content) != []\
            or _comment_content.__len__() <= 3:
        return False
    else:
        return True

def _get_right_model_data(data, site_id=None, logger=None):
    '''
    得到规范化GoodsItem model的数据
    :param data:
    :return:
    '''
    from .time_utils import get_shanghai_time
    from .items import GoodsItem
    from .common_utils import _print
    from decimal import Decimal

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