# coding:utf-8

'''
@author = super_fazai
@File    : test_goods_info_change.py
@connect : superonesfazai@gmail.com
'''

from sys import path
path.append('..')

from pprint import pprint
from multiplex_code import (
    _get_spec_trans_record,
    _get_sku_price_trans_record,
    _get_stock_trans_record,)
# from fzutils.common_utils import json_2_dict
from fzutils.safe_utils import get_uuid3

def test1(old_sku_info, new_sku_info):
    """
    测试: 规格, 价格, 库存都变动的情况!
    :return:
    """
    is_spec_change = _get_spec_trans_record(
        old_sku_info=old_sku_info,
        new_sku_info=new_sku_info,
        is_spec_change=0,)[0]
    is_price_change, _, price_change_info = _get_sku_price_trans_record(
        old_sku_info=old_sku_info,
        new_sku_info=new_sku_info,
        is_price_change=0,
        db_price_change_info=[])
    is_stock_change, _, stock_change_info = _get_stock_trans_record(
        old_sku_info=old_sku_info,
        new_sku_info=new_sku_info,
        is_stock_change=0,
        db_stock_change_info=[])
    print('规格变动: {}\n价格变动: {}\n库存变动: {}'.format(is_spec_change, is_price_change, is_stock_change))
    pprint(price_change_info)
    pprint(stock_change_info)

    return

# old_sku_info = []
old_sku_info = [{
    'account_limit_buy_count': 5,
    'detail_price': '14.0',
    'img_url': 'https://img.alicdn.com/imgextra/i2/698722353/TB2_1E_pjoIL1JjSZFyXXbFBpXa_!!698722353.jpg',
    'is_on_sale': 1,
    'normal_price': '14.0',
    'pintuan_price': '',
    'rest_number': 9999,
    'spec_value': '粉色|100ml',
    'unique_id': get_uuid3('粉色|100ml'),
},]
# new_sku_info = []
new_sku_info = [
    {
        'account_limit_buy_count': 5,
        'detail_price': '13.0',
        'img_url': 'https://img.alicdn.com/imgextra/i2/698722353/TB2_1E_pjoIL1JjSZFyXXbFBpXa_!!698722353.jpg',
        'is_on_sale': 1,
        'normal_price': '13.5',
        'pintuan_price': '',
        'rest_number': 10,
        'spec_value': '粉色|100ml',
        'unique_id': get_uuid3('粉色|100ml'),
    },{
        'account_limit_buy_count': 5,
        'detail_price': '14.0',
        'img_url': 'https://img.alicdn.com/imgextra/i2/698722353/TB2_1E_pjoIL1JjSZFyXXbFBpXa_!!698722353.jpg',
        'is_on_sale': 1,
        'normal_price': '14.0',
        'pintuan_price': '',
        'rest_number': 1000,
        'spec_value': '黑色|100ml',
        'unique_id': get_uuid3('黑色|100ml'),
    },
]
test1(old_sku_info=old_sku_info, new_sku_info=new_sku_info)