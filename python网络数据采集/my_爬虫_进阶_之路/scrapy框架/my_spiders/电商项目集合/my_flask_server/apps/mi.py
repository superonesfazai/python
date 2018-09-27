# coding:utf-8

'''
@author = super_fazai
@File    : mi.py
@connect : superonesfazai@gmail.com
'''

"""
mia
"""

import re
import gc
from json import dumps
import sys

from .reuse import (
    add_base_info_2_processed_data,
)

sys.path.append('..')
from settings import DEFAULT_USERNAME
from mia_parse import MiaParse

def _get_mia_wait_to_save_data_goods_id_list(data, my_lg):
    '''
    获取mia待存取的goods_id的list
    :param data:
    :param my_lg:
    :return:
    '''
    wait_to_save_data_url_list = data

    tmp_wait_to_save_data_goods_id_list = []
    for item in wait_to_save_data_url_list:
        if item == '':  # 除去传过来是空值
            pass
        else:
            is_mia_irl = re.compile(r'mia.com/item|miyabaobei.hk/item').findall(item)
            if is_mia_irl != []:
                try:
                    goods_id = re.compile(r'item-(\d+).html.*?').findall(item)[0]
                    assert goods_id != '', 'goods_id为空值!'
                except (IndexError, AssertionError):
                    continue
                my_lg.info('------>>>| 得到的蜜芽商品的goods_id为: {}'.format(goods_id))
                tmp_wait_to_save_data_goods_id_list.append(goods_id)

            else:
                my_lg.info('蜜芽商品url错误, 非正规的url, 请参照格式(https://www.mia.com/item-)开头的...')
                pass

    return tmp_wait_to_save_data_goods_id_list

def _get_db_mia_insert_params(item):
    params = (
        item['goods_id'],
        item['goods_url'],
        item['username'],
        item['create_time'],
        item['modify_time'],
        item['shop_name'],
        item['account'],
        item['title'],
        item['sub_title'],
        item['link_name'],
        item['price'],
        item['taobao_price'],
        dumps(item['price_info'], ensure_ascii=False),
        dumps(item['detail_name_list'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
        dumps(item['price_info_list'], ensure_ascii=False),
        dumps(item['all_img_url'], ensure_ascii=False),
        dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
        item['div_desc'],  # 存入到DetailInfo
        item['all_sell_count'],
        dumps(item['schedule'], ensure_ascii=False),
        item['parent_dir'],

        item['site_id'],
        item['is_delete'],
    )

    return params

def get_one_mia_data(**kwargs):
    '''
    抓取一个mia地址的数据
    :param kwargs: 
    :return: 
    '''
    username = kwargs.get('username', DEFAULT_USERNAME)
    wait_to_deal_with_url = kwargs.get('wait_to_deal_with_url', '')
    my_lg = kwargs.get('my_lg')

    mi = MiaParse()
    goods_id = mi.get_goods_id_from_url(wait_to_deal_with_url)  # 获取goods_id, 这里返回的是一个list
    if goods_id == '':  # 如果得不到goods_id, 则return error
        my_lg.info('获取到的goods_id为空!')
        try:
            del mi  # 每次都回收一下
        except Exception:
            pass
        gc.collect()
        return {'goods_id': ''}  # 错误1: goods_id为空值

    tmp_result = mi.get_goods_data(goods_id=goods_id)
    data = mi.deal_with_data()  # 如果成功获取的话, 返回的是一个data的dict对象
    if data == {} or tmp_result == {}:
        my_lg.error('获取到的data为空!出错地址: {0}'.format(wait_to_deal_with_url))
        try:
            del mi
        except:
            pass
        gc.collect()
        return {'goods_id': goods_id, 'msg': 'data为空!'}  # 错误2: 抓取失败

    wait_to_deal_with_url = 'https://www.mia.com/item-{}.html'.format(goods_id)
    wait_to_save_data = add_base_info_2_processed_data(
        data=data,
        spider_url=wait_to_deal_with_url,
        username=username,
        goods_id=goods_id
    )
    try:
        del mi
    except:
        pass

    return wait_to_save_data