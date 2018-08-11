# coding:utf-8

'''
@author = super_fazai
@File    : reuse.py
@Time    : 2017/8/11 11:24
@connect : superonesfazai@gmail.com
'''

# high reuse(高复用code)

from .msg import _success_data

def add_base_info_2_processed_data(**kwargs):
    '''
    给采集后的data增加基础信息
    :param kwargs:
    :return:
    '''
    data = kwargs.get('data')
    spider_url = kwargs.get('spider_url')
    username = kwargs.get('username')
    goods_id = str(kwargs.get('goods_id'))

    wait_to_save_data = data
    wait_to_save_data['spider_url'] = spider_url
    wait_to_save_data['username'] = username
    wait_to_save_data['goods_id'] = goods_id

    return wait_to_save_data

def is_login(**kwargs):
    '''
    判断是否合法登录
    :param kwargs:
    :return: bool
    '''
    request = kwargs.get('request')

    if request.cookies.get('username') is not None \
            and request.cookies.get('passwd') is not None:   # request.cookies -> return a dict
        return True
    else:
        return False

def compatible_api_goods_data(data, my_lg):
    '''
    兼容处理data, 规范返回数据
    :param data:
    :return: json_str
    '''
    from decimal import Decimal
    from datetime import datetime

    # 返回给APP时, 避免json.dumps转换失败... TODO
    _data = data
    for key, value in _data.items():
        if isinstance(value, Decimal):
            data.update({key: float(value)})
        elif isinstance(value, datetime):
            data.update({key: str(value)})
        else:
            pass
    # pprint(data)

    _ = {
        'goods_id': data.get('goods_id'),
        'title': data.get('title', ''),
        'price': str(data.get('taobao_price')),         # 最低价
        'sell_count': data.get('sell_count') if not data.get('sell_count') else data.get('all_sell_count'),
        'img_url': data.get('all_img_url'),             # 商品示例图, eg: [{'img_url': xxx}, ...]
        'spider_url': data.get('spider_url') if not data.get('spider_url') else data.get('goods_url'),
        'sku_name': data.get('detail_name_list', []),   # 规格名, eg: 颜色，尺码 [{'spec_name': '颜色'}, ...]
        'sku_info': data.get('price_info_list', []),    # 详细规格, eg: [{"spec_value": "10片", "detail_price": "79", "rest_number": "3394"}, ...]
    }

    my_lg.info('此次请求接口返回数据: {0}'.format(str(_)))
    msg = '抓取数据成功!'

    return _success_data(msg=msg, data=_)
