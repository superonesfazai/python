# coding:utf-8

'''
@author = super_fazai
@File    : tb.py
@Time    : 2017/8/11 12:50
@connect : superonesfazai@gmail.com
'''

"""
淘宝
"""

import sys
import re
from json import dumps
from time import sleep
import gc

from .reuse import (
    add_base_info_2_processed_data,
    compatible_api_goods_data,)
from .msg import _error_data

sys.path.append('..')
from settings import TAOBAO_SLEEP_TIME
from taobao_parse import TaoBaoLoginAndParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from fzutils.cp_utils import _get_right_model_data

def _get_taobao_wait_to_save_data_goods_id_list(data, my_lg):
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
            is_taobao_url = re.compile(r'https://item.taobao.com/item.htm.*?').findall(item)
            if is_taobao_url != []:
                if re.compile(r'https://item.taobao.com/item.htm.*?id=(\d+)&{0,20}.*?').findall(item) != []:
                    tmp_taobao_url = re.compile(r'https://item.taobao.com/item.htm.*?id=(\d+)&{0,20}.*?').findall(item)[0]
                    # my_lg.info(tmp_taobao_url)
                    if tmp_taobao_url != []:
                        goods_id = tmp_taobao_url
                    else:
                        item = re.compile(r';').sub('', item)
                        goods_id = re.compile(r'https://item.taobao.com/item.htm.*?id=(\d+)').findall(item)[0]
                else:  # 处理存数据库中取出的如: https://item.taobao.com/item.htm?id=560164926470
                    # my_lg.info('9999')
                    item = re.compile(r';').sub('', item)
                    goods_id = re.compile(r'https://item.taobao.com/item.htm\?id=(\d+)&{0,20}.*?').findall(item)[0]
                    # my_lg.info('------>>>| 得到的淘宝商品id为:' + goods_id)
                tmp_goods_id = goods_id
                tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)
            else:
                my_lg.info('淘宝商品url错误, 非正规的url, 请参照格式(https://item.taobao.com/item.htm)开头的...')

    return tmp_wait_to_save_data_goods_id_list

def _get_db_taobao_insert_params(item):
    '''
    得到db待插入的数据
    :param item:
    :return:
    '''
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

        item['site_id'],
        item['is_delete'],
    )

    return params

def get_one_tb_data(**kwargs):
    '''
    抓取一个tb url的data
    :return: a dict
    '''
    username = kwargs.get('username', '18698570079')
    tb_url = kwargs.get('tb_url', '')
    my_lg = kwargs.get('my_lg')

    login_taobao = TaoBaoLoginAndParse(logger=my_lg)
    goods_id = login_taobao.get_goods_id_from_url(tb_url)  # 获取goods_id
    if goods_id == '':
        my_lg.info('获取到的goods_id为空!')
        try: del login_taobao  # 每次都回收一下
        except: pass
        gc.collect()

        return {'goods_id': ''}                                    # 错误1: goods_id为空!

    wait_to_deal_with_url = 'https://item.taobao.com/item.htm?id={0}'.format(goods_id)  # 构造成标准干净的淘宝商品地址
    tmp_result = login_taobao.get_goods_data(goods_id=goods_id)
    data = login_taobao.deal_with_data(goods_id=goods_id)  # 如果成功获取的话, 返回的是一个data的dict对象

    sleep(TAOBAO_SLEEP_TIME)  # 这个在服务器里面可以注释掉为.5s
    if data == {} or tmp_result == {}:
        my_lg.info('获取到的data为空!')
        try:del login_taobao
        except:pass
        gc.collect()

        return {'goods_id': goods_id, 'msg': 'data为空!'}           # 错误2: 抓取data为空!

    wait_to_save_data = add_base_info_2_processed_data(
        data=data,
        spider_url=wait_to_deal_with_url,
        username=username,
        goods_id=goods_id
    )
    try: del login_taobao
    except: pass

    return wait_to_save_data

def _get_tb_goods_id(goods_link):
    '''
    获取m站或者pc站的goods_id
    :param goods_link:
    :return:
    '''
    try:
        return re.compile(r'id=(\d+)').findall(goods_link)[0]
    except IndexError:
        return ''

def _deal_with_tb_goods(goods_link, my_lg):
    '''
    处理淘宝商品
    :param goods_link:
    :return: json_str
    '''
    my_lg.info('进入淘宝商品处理接口...')
    goods_id = _get_tb_goods_id(goods_link)
    if goods_id == '':
        msg = 'goods_id匹配失败!请检查url是否正确!'
        return _error_data(msg=msg)

    tb_url = 'https://item.taobao.com/item.htm?id=' + goods_id  # 构造成标准干净的淘宝商品地址
    data = get_one_tb_data(tb_url=tb_url)
    my_lg.info(str(data))
    if data.get('msg', '') == 'data为空!':
        msg = '该goods_id:{0}, 抓取数据失败!'.format(goods_id)
        return _error_data(msg=msg)

    else:
        pass

    data = _get_right_model_data(data=data, site_id=1, logger=my_lg)
    my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
    my_lg.info('------>>>| 正在存储的数据为: ' + data.get('goods_id', ''))

    params = _get_db_taobao_insert_params(item=data)
    sql_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    is_insert_into = my_pipeline._insert_into_table_2(sql_str=sql_str, params=params, logger=my_lg)
    if is_insert_into:  # 如果返回值为True
        pass
    else:   # 不处理存储结果!
        # msg = '存储该goods_id:{0}失败!'.format(goods_id)
        # return _error_data(msg=msg)
        pass

    return compatible_api_goods_data(data=data, my_lg=my_lg)
