# coding:utf-8

'''
@author = super_fazai
@File    : test_bd_map_shop_info.py
@connect : superonesfazai@gmail.com
'''

"""
测试bd or gd map shop_info
"""

from json import dumps
from pprint import pprint
from fzutils.common_utils import json_2_dict
from fzutils.ip_pools import tri_ip_pool
from fzutils.data.list_utils import list_remove_repeat_dict_plus
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import Requests
from fzutils.free_api_utils import (
    get_bd_map_shop_info_list_by_keyword_and_area_name,
    get_gd_map_shop_info_list_by_keyword_and_area_name,)

def get_bd_shop_info():
    ak = get_ak()
    # ak = ''

    # 百度api 关键字搜索信息
    tmp_shop_list = get_bd_map_shop_info_list_by_keyword_and_area_name(
        ak=ak,
        keyword='官方',
        area_name='杭州',
        page_num=2,
        ip_pool_type=tri_ip_pool,
        timeout=15,
        num_retries=8,)
    # pprint(tmp_shop_list)

    shop_info_list = []
    for item in tmp_shop_list:
        try:
            phone = item.get('telephone', '')
            assert phone != '', 'phone不为空str!'
            phone = [{
                'phone': item.replace('(', '').replace(')', ''),
            } for item in phone.split(',')]
            address = item.get('address', '')
            assert address != '', 'address不为空str'
            company_name = item.get('name', '')
            assert company_name != '', 'company_name不为空str!'
            city_name = item.get('city', '')
            assert city_name != '', 'city_name != ""'
            province_name = item.get('province', '')
            assert province_name != '', 'province_name != ""'
            company_id = item.get('uid', '')
            assert company_id != '', 'company_id != ""'
            lat = item.get('location', {}).get('lat', 0.)
            lng = item.get('location', {}).get('lng', 0.)
            assert lat != 0. or lng != 0., 'lat or lng异常!'
        except AssertionError:
            continue

        shop_info_list.append({
            'company_id': company_id,
            'company_name': company_name,
            'address': address,
            'city_name': city_name,
            'province_name': province_name,
            'phone': phone,
            'lat': lat,
            'lng': lng,
        })

    shop_info_list = list_remove_repeat_dict_plus(
        target=shop_info_list,
        repeat_key='company_id',)
    pprint(shop_info_list)

def get_gd_shop_info():
    gd_key = get_gd_key()
    # gd_key = ''
    tmp_shop_info_data = get_gd_map_shop_info_list_by_keyword_and_area_name(
        gd_key=gd_key,
        keyword='鞋子',
        area_name='北京',
        page_num=1,
        ip_pool_type=tri_ip_pool,
        num_retries=8,
        timeout=15,)

    shop_info_list = []
    for item in tmp_shop_info_data:
        try:
            company_id = item.get('id', '')
            assert company_id != '', 'company_id != ""'
            company_name = item.get('name', '')
            assert company_name != '', 'company_name != ""'
            address = item.get('address', '')
            assert address != '', "address != ''"
            city_name = item.get('cityname', '')
            assert city_name != '', 'city_name != ""'
            province_name = item.get('pname', '')
            assert province_name != '', 'province_name != ""'
            phone = item.get('tel', '').replace(';', ',')
            assert phone != '', 'phone != ""'
            location = item.get('location', '')
            assert location != '', 'localtion != ""'
            # 经度
            lng = float(location.split(',')[0])
            # 纬度
            lat = float(location.split(',')[1])
        except (AssertionError, Exception):
            continue

        shop_info_list.append({
            'company_id': company_id,
            'company_name': company_name,
            'address': address,
            'city_name': city_name,
            'province_name': province_name,
            'phone': phone,
            'lat': lat,
            'lng': lng,
        })
    pprint(shop_info_list)

def get_ak() -> str:
    bd_api_json = ''
    with open('/Users/afa/myFiles/pwd/baidu_map_pwd.json', 'r') as f:
        for line in f:
            bd_api_json += line.replace('\n', '').replace('  ', '')
        # print(bd_api_json)
        ak = json_2_dict(json_str=bd_api_json) \
            .get('fz_map_info', {}) \
            .get('ak', '')
    assert ak != '', 'ak不为空str!'

    return ak

def get_gd_key() -> str:
    gd_api_json = ''
    gd_map_pwd_file_path = '/Users/afa/myFiles/pwd/gaode_map_pwd.json'
    with open(gd_map_pwd_file_path, 'r') as f:
        for line in f:
            gd_api_json += line.replace('\n', '').replace('  ', '')
        # self.lg.info(gd_api_json)
        gd_key_list = json_2_dict(
            json_str=gd_api_json, ) \
            .get('fz_map_info', [])
    pprint(gd_key_list)
    assert gd_key_list != [], 'gd_key_list不为空list!'
    gd_key_list = [item.get('key', '') for item in gd_key_list]
    gd_key = gd_key_list[1]
    assert gd_key != '', 'gd_key不为空str!'

    return gd_key

get_gd_shop_info()
