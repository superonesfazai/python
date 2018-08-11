# coding:utf-8

'''
@author = super_fazai
@File    : tm.py
@Time    : 2017/8/11 13:10
@connect : superonesfazai@gmail.com
'''

"""
天猫
"""

import re
import gc
import sys
from json import dumps
from time import sleep

from .reuse import (
    add_base_info_2_processed_data,
    compatible_api_goods_data,)
from .msg import (
    _error_data
)

sys.path.append('..')
from settings import (
    DEFAULT_USERNAME,
    TMALL_SLEEP_TIME,
)
from tmall_parse_2 import TmallParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from fzutils.cp_utils import _get_right_model_data

def _get_tmall_wait_to_save_data_goods_id_list(data, my_lg):
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
            is_tmall_url = re.compile(r'https://detail.tmall.com/item.htm.*?').findall(item)
            if is_tmall_url != []:  # 天猫常规商品
                tmp_tmall_url = re.compile(r'https://detail.tmall.com/item.htm.*?id=(\d+)&{0,20}.*?').findall(item)
                if tmp_tmall_url != []:
                    is_tmp_tmp_tmall_url = re.compile(r'https://detail.tmall.com/item.htm.*?&id=(\d+)&{0,20}.*?').findall(item)
                    if is_tmp_tmp_tmall_url != []:
                        goods_id = is_tmp_tmp_tmall_url[0]
                    else:
                        goods_id = tmp_tmall_url[0]
                else:
                    tmall_url = re.compile(r';').sub('', item)
                    goods_id = re.compile(r'https://detail.tmall.com/item.htm.*?id=(\d+)').findall(tmall_url)[0]
                tmp_goods_id = goods_id
                tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)
            else:
                is_tmall_supermarket = re.compile(r'https://chaoshi.detail.tmall.com/item.htm.*?').findall(item)
                if is_tmall_supermarket != []:  # 天猫超市
                    tmp_tmall_url = re.compile(r'https://chaoshi.detail.tmall.com/item.htm.*?id=(\d+)&.*?').findall(item)
                    if tmp_tmall_url != []:
                        goods_id = tmp_tmall_url[0]
                    else:
                        tmall_url = re.compile(r';').sub('', item)
                        goods_id = \
                        re.compile(r'https://chaoshi.detail.tmall.com/item.htm.*?id=(\d+)').findall(tmall_url)[0]
                    tmp_goods_id = goods_id
                    tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)
                else:
                    is_tmall_hk = re.compile(r'https://detail.tmall.hk/.*?item.htm.*?').findall(item)  # 因为中间可能有国家的地址 如https://detail.tmall.hk/hk/item.htm?
                    if is_tmall_hk != []:  # 天猫国际， 地址中有地域的也能正确解析, 嘿嘿 -_-!!!
                        tmp_tmall_url = re.compile(r'https://detail.tmall.hk/.*?item.htm.*?id=(\d+)&.*?').findall(item)
                        if tmp_tmall_url != []:
                            goods_id = tmp_tmall_url[0]
                        else:
                            tmall_url = re.compile(r';').sub('', item)
                            goods_id = re.compile(r'https://detail.tmall.hk/.*?item.htm.*?id=(\d+)').findall(tmall_url)[0]
                        # before_url = re.compile(r'https://detail.tmall.hk/.*?item.htm').findall(item)[0]
                        tmp_goods_id = goods_id
                        tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)
                    else:  # 非正确的天猫商品url
                        my_lg.info('天猫商品url错误, 非正规的url, 请参照格式(https://detail.tmall.com/item.htm)开头的...')
                        pass

    return tmp_wait_to_save_data_goods_id_list

def _get_db_tmall_insert_params(item):
    '''
    得到tmall待存储数据
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

def get_one_tm_data(**kwargs):
    '''
    抓取一个tm url的data
    :param kwargs:
    :return:
    '''
    username = kwargs.get('username', DEFAULT_USERNAME)
    wait_to_deal_with_url = kwargs.get('wait_to_deal_with_url', '')
    my_lg = kwargs.get('my_lg')

    login_tmall = TmallParse(logger=my_lg)
    goods_id = login_tmall.get_goods_id_from_url(wait_to_deal_with_url)  # 获取goods_id, 这里返回的是一个list
    if goods_id == []:  # 如果得不到goods_id, 则return error
        my_lg.info('获取到的goods_id为空!')
        try:
            del login_tmall  # 每次都回收一下
        except:
            pass
        gc.collect()

        return {'goods_id': ''}

    # 改进判断，根据传入数据判断是天猫，还是天猫超市，还是天猫国际
    #####################################################
    if goods_id[0] == 0:  # [0, '1111']
        wait_to_deal_with_url = 'https://detail.tmall.com/item.htm?id=' + goods_id[1]  # 构造成标准干净的天猫商品地址
    elif goods_id[0] == 1:  # [1, '1111']
        wait_to_deal_with_url = 'https://chaoshi.detail.tmall.com/item.htm?id=' + goods_id[1]
    elif goods_id[0] == 2:  # [2, '1111', 'https://xxxxx']
        wait_to_deal_with_url = str(goods_id[2]) + '?id=' + goods_id[1]

    tmp_result = login_tmall.get_goods_data(goods_id=goods_id)
    data = login_tmall.deal_with_data()  # 如果成功获取的话, 返回的是一个data的dict对象

    sleep(TMALL_SLEEP_TIME)  # 这个在服务器里面可以注释掉为.5s
    if data == {} or tmp_result == {}:
        my_lg.info('获取到的data为空!')
        try:
            del login_tmall
        except:
            pass
        gc.collect()

        return {'goods_id': goods_id[1], 'msg': 'data为空!'}

    wait_to_save_data = add_base_info_2_processed_data(
        data=data,
        spider_url=wait_to_deal_with_url,
        username=username,
        goods_id=goods_id[1]
    )
    try: del login_tmall
    except: pass

    return wait_to_save_data

def _get_tm_goods_id(goods_link):
    '''
    得到tm link的goods_id
    :param goods_link:
    :return:
    '''
    try:
        return re.compile('id=(\d+)').findall(goods_link)[0]
    except IndexError:
        return ''

def _deal_with_tm_goods(goods_link, my_lg):
    '''
    处理天猫商品
    :param goods_link:
    :return: json_str
    '''
    my_lg.info('进入天猫商品处理接口...')
    goods_id = _get_tm_goods_id(goods_link)
    if goods_id == '':
        msg = 'goods_id匹配失败!请检查url是否正确!'
        return _error_data(msg=msg)

    tm_url = 'https://detail.tmall.com/item.htm?id={0}'.format(goods_id)
    data = get_one_tm_data(wait_to_deal_with_url=tm_url)
    if data.get('msg', '') == 'data为空!':
        msg = '该goods_id:{0}, 抓取数据失败!'.format(goods_id)
        return _error_data(msg=msg)
    else:
        pass

    site_id = _from_tmall_type_get_site_id(type=data.get('type'))
    data = _get_right_model_data(data=data, site_id=site_id, logger=my_lg)
    my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
    my_lg.info('------>>>| 正在存储的数据为: ' + data.get('goods_id', ''))

    params = _get_db_tmall_insert_params(item=data)
    sql_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    is_insert_into = my_pipeline._insert_into_table_2(sql_str=sql_str, params=params, logger=my_lg)
    if is_insert_into:  # 如果返回值为True
        pass
    else:               # 不处理存储结果
        # msg = '存储该goods_id:{0}失败!'.format(goods_id)
        # return _error_data(msg=msg)
        pass

    return compatible_api_goods_data(data=data, my_lg=my_lg)

def _from_tmall_type_get_site_id(type):
    '''
    根据tmall的type得到site_id的值
    :param type:
    :return: bool or int
    '''
    # # 采集的来源地
    if type == 0:
        site_id = 3  # 采集来源地(天猫)
    elif type == 1:
        site_id = 4  # 采集来源地(天猫超市)
    elif type == 2:
        site_id = 6  # 采集来源地(天猫国际)
    else:
        return False

    return site_id