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
from fzutils.time_utils import get_shanghai_time

def test1(old_sku_info, new_sku_info):
    """
    测试: 规格, 价格, 库存都变动的情况!
    :return:
    """
    is_spec_change = _get_spec_trans_record(
        old_sku_info=old_sku_info,
        new_sku_info=new_sku_info,
        is_spec_change=0,
        old_spec_trans_time=get_shanghai_time())[0]
    is_price_change, _, price_change_info = _get_sku_price_trans_record(
        old_sku_info=old_sku_info,
        new_sku_info=new_sku_info,
        is_price_change=0,
        db_price_change_info=[],
        old_price_trans_time=get_shanghai_time())
    is_stock_change, _, stock_change_info = _get_stock_trans_record(
        old_sku_info=old_sku_info,
        new_sku_info=new_sku_info,
        is_stock_change=0,
        db_stock_change_info=[],
        old_stock_trans_time=get_shanghai_time())
    print('规格变动: {}\n价格变动: {}\n库存变动: {}'.format(is_spec_change, is_price_change, is_stock_change))
    print('-->> 价格变动情况:')
    pprint(price_change_info)
    print('-->> 库存变动情况:')
    pprint(stock_change_info)

    return

# old_sku_info = []
# old_sku_info = [{
#     'account_limit_buy_count': 5,
#     'detail_price': '14.0',
#     'img_url': 'https://img.alicdn.com/imgextra/i2/698722353/TB2_1E_pjoIL1JjSZFyXXbFBpXa_!!698722353.jpg',
#     'is_on_sale': 1,
#     'normal_price': '14.0',
#     'pintuan_price': '',
#     'rest_number': 9999,
#     'spec_value': '粉色|100ml',
#     'unique_id': get_uuid3('粉色|100ml'),
# },]

# new_sku_info = []
# new_sku_info = [
#     {
#         'account_limit_buy_count': 5,
#         'detail_price': '13.0',
#         'img_url': 'https://img.alicdn.com/imgextra/i2/698722353/TB2_1E_pjoIL1JjSZFyXXbFBpXa_!!698722353.jpg',
#         'is_on_sale': 1,
#         'normal_price': '13.5',
#         'pintuan_price': '',
#         'rest_number': 10,
#         'spec_value': '粉色|100ml',
#         'unique_id': get_uuid3('粉色|100ml'),
#     },{
#         'account_limit_buy_count': 5,
#         'detail_price': '14.0',
#         'img_url': 'https://img.alicdn.com/imgextra/i2/698722353/TB2_1E_pjoIL1JjSZFyXXbFBpXa_!!698722353.jpg',
#         'is_on_sale': 1,
#         'normal_price': '14.0',
#         'pintuan_price': '',
#         'rest_number': 1000,
#         'spec_value': '黑色|100ml',
#         'unique_id': get_uuid3('黑色|100ml'),
#     },
# ]

# old_sku_info = [{'account_limit_buy_count': 5,
#   'detail_price': '79.0',
#   'img_url': '',
#   'is_on_sale': 1,
#   'normal_price': '158.0',
#   'pintuan_price': '',
#   'rest_number': 1965,
#   'spec_value': '【经典紫】双心巧克力款',
#   'unique_id': '3b1b524d-efe3-32b4-ad95-bfc4c31b9707'},
#  {'account_limit_buy_count': 5,
#   'detail_price': '79.0',
#   'img_url': '',
#   'is_on_sale': 1,
#   'normal_price': '158.0',
#   'pintuan_price': '',
#   'rest_number': 328,
#   'spec_value': '【小幸运】双心巧克力款',
#   'unique_id': 'b39f5068-af59-35bd-a2f3-7b493492d409'},
#  {'account_limit_buy_count': 5,
#   'detail_price': '79.0',
#   'img_url': '',
#   'is_on_sale': 1,
#   'normal_price': '158.0',
#   'pintuan_price': '',
#   'rest_number': 314,
#   'spec_value': '【小幸运】单心星空棒棒糖',
#   'unique_id': 'c064626c-84b2-3418-967c-1d493b2feb9f'},
#  {'account_limit_buy_count': 5,
#   'detail_price': '79.0',
#   'img_url': '',
#   'is_on_sale': 1,
#   'normal_price': '158.0',
#   'pintuan_price': '',
#   'rest_number': 438,
#   'spec_value': '【思念款】双心巧克力款',
#   'unique_id': 'ba752ab6-c32a-322d-b400-aa37bc134b1b'},
#  {'account_limit_buy_count': 5,
#   'detail_price': '79.0',
#   'img_url': '',
#   'is_on_sale': 1,
#   'normal_price': '158.0',
#   'pintuan_price': '',
#   'rest_number': 446,
#   'spec_value': '【思念款】单心星空棒棒糖',
#   'unique_id': '49692114-f318-3076-bda0-323dcdc2c3d3'}]
# new_sku_info = [{'account_limit_buy_count': 5,
#   'detail_price': '79.0',
#   'img_url': '',
#   'is_on_sale': 1,
#   'normal_price': '158.0',
#   'pintuan_price': '',
#   'rest_number': 1965,
#   'spec_value': '【经典紫】双心巧克力款',
#   'unique_id': '3b1b524d-efe3-32b4-ad95-bfc4c31b9707'},
#  {'account_limit_buy_count': 5,
#   'detail_price': '79.0',
#   'img_url': '',
#   'is_on_sale': 1,
#   'normal_price': '158.0',
#   'pintuan_price': '',
#   'rest_number': 328,
#   'spec_value': '【小幸运】双心巧克力款',
#   'unique_id': 'b39f5068-af59-35bd-a2f3-7b493492d409'},
#  {'account_limit_buy_count': 5,
#   'detail_price': '79.0',
#   'img_url': '',
#   'is_on_sale': 1,
#   'normal_price': '158.0',
#   'pintuan_price': '',
#   'rest_number': 314,
#   'spec_value': '【小幸运】单心星空棒棒糖',
#   'unique_id': 'c064626c-84b2-3418-967c-1d493b2feb9f'},
#  {'account_limit_buy_count': 5,
#   'detail_price': '79.0',
#   'img_url': '',
#   'is_on_sale': 1,
#   'normal_price': '158.0',
#   'pintuan_price': '',
#   'rest_number': 438,
#   'spec_value': '【思念款】双心巧克力款',
#   'unique_id': 'ba752ab6-c32a-322d-b400-aa37bc134b1b'},
#  {'account_limit_buy_count': 5,
#   'detail_price': '79.0',
#   'img_url': '',
#   'is_on_sale': 1,
#   'normal_price': '158.0',
#   'pintuan_price': '',
#   'rest_number': 446,
#   'spec_value': '【思念款】单心星空棒棒糖',
#   'unique_id': '49692114-f318-3076-bda0-323dcdc2c3d3'}]

old_sku_info = [
    {
        "unique_id":"fe3c900d-dacb-3329-aa42-ab5880d15c36",
        "spec_value":"10斤|80mm（含）-85mm(不含)",
        "detail_price":"37.59",
        "normal_price":"124.95",
        "pintuan_price":"",
        "img_url":"",
        "rest_number":74851,
        "account_limit_buy_count":5,
        "is_on_sale":1
    },
    {
        "unique_id":"9aab9ba4-f479-3f00-a948-7e5174c56a21",
        "spec_value":"10斤|75mm（含）-80mm(不含)",
        "detail_price":"31.29",
        "normal_price":"124.95",
        "pintuan_price":"",
        "img_url":"",
        "rest_number":20938,
        "account_limit_buy_count":5,
        "is_on_sale":1
    }
]
new_sku_info = [
    {
        "unique_id":"fe3c900d-dacb-3329-aa42-ab5880d15c36",
        "spec_value":"10斤|80mm（含）-85mm(不含)",
        "detail_price":"90.09",
        "normal_price":"124.95",
        "pintuan_price":"",
        "img_url":"",
        "rest_number":74851,
        "account_limit_buy_count":5,
        "is_on_sale":1
    },
    {
        "unique_id":"9aab9ba4-f479-3f00-a948-7e5174c56a21",
        "spec_value":"10斤|75mm（含）-80mm(不含)",
        "detail_price":"83.79",
        "normal_price":"124.95",
        "pintuan_price":"",
        "img_url":"",
        "rest_number":20938,
        "account_limit_buy_count":5,
        "is_on_sale":1
    }
]
test1(old_sku_info=old_sku_info, new_sku_info=new_sku_info)