# coding:utf-8

'''
@author = super_fazai
@File    : al.py
@Time    : 2017/8/11 11:57
@connect : superonesfazai@gmail.com
'''

"""
1688
"""

import sys

import re
from json import dumps
import gc

from .reuse import add_base_info_2_processed_data
sys.path.append('..')
from ali_1688_parse import ALi1688LoginAndParse

def _get_ali_wait_to_save_data_goods_id_list(data):
    '''
    得到待存取的goods_id的list
    :param data:
    :return:
    '''
    wait_to_save_data_url_list = data

    tmp_wait_to_save_data_goods_id_list = []
    for item in wait_to_save_data_url_list:
        if item == '':  # 除去传过来是空值
            pass
        else:
            tmp_goods_id = re.compile(r'.*?/offer/(.*?).html.*?').findall(item)[0]
            tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)

    return tmp_wait_to_save_data_goods_id_list

def _get_db_ali_insert_params(item):
    '''
    得到阿里待插入的数据
    :param item:
    :return: tuple
    '''
    params = (
        item['goods_id'],
        item['goods_url'],
        item['username'],
        item['create_time'],
        item['modify_time'],
        item['shop_name'],
        item['title'],
        item['link_name'],
        item['price'],
        item['taobao_price'],
        dumps(item['price_info'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
        dumps(item['detail_name_list'], ensure_ascii=False),
        dumps(item['price_info_list'], ensure_ascii=False),
        dumps(item['all_img_url'], ensure_ascii=False),
        item['div_desc'],  # 存入到DetailInfo
        dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo

        item['site_id'],
        item['is_delete'],
    )

    return params

def get_one_1688_data(**kwargs):
    '''
    抓取一个1688 url 的data
    :param kwargs:
    :return:
    '''
    username = kwargs.get('username', '18698570079')
    wait_to_deal_with_url = kwargs.get('wait_to_deal_with_url', '')
    my_lg = kwargs.get('my_lg')

    login_ali = ALi1688LoginAndParse()
    goods_id = login_ali.get_goods_id_from_url(wait_to_deal_with_url)  # 获取goods_id
    if goods_id == '':  # 如果得不到goods_id, 则return error
        my_lg.info('获取到的goods_id为空!')
        try:del login_ali  # 每次都回收一下
        except:pass
        gc.collect()

        return {'goods_id': ''}             # 错误1: goods_id为空值

    tmp_result = login_ali.get_ali_1688_data(goods_id=goods_id)
    data = login_ali.deal_with_data()  # 如果成功获取的话, 返回的是一个data的dict对象
    if data == {} or tmp_result == {}:
        my_lg.info('获取到的data为空!')
        try:del login_ali
        except:pass
        gc.collect()

        return {'goods_id': goods_id, 'msg': 'data为空!'}     # 错误2: 抓取失败

    wait_to_save_data = add_base_info_2_processed_data(
        data=data,
        spider_url=wait_to_deal_with_url,
        username=username,
        goods_id=goods_id
    )
    try: del login_ali
    except: pass

    return wait_to_save_data