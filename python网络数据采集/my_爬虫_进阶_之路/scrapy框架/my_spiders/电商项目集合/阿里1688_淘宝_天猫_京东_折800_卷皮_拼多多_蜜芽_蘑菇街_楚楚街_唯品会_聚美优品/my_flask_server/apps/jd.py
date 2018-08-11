# coding:utf-8

'''
@author = super_fazai
@File    : jd.py
@Time    : 2017/8/11 13:27
@connect : superonesfazai@gmail.com
'''

"""
京东
"""

import sys
import gc
import re
from json import dumps

from .reuse import (
    add_base_info_2_processed_data,
    compatible_api_goods_data,)
from .msg import _error_data

sys.path.append('..')
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from jd_parse import JdParse

from fzutils.cp_utils import _get_right_model_data

def _get_jd_wait_to_save_data_goods_id_list(data, my_lg):
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
            is_jd_url = re.compile(r'https://item.jd.com/.*?').findall(item)
            if is_jd_url != []:
                goods_id = re.compile(r'https://item.jd.com/(.*?).html.*?').findall(item)[0]
                tmp_goods_id = goods_id
                tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)
            else:
                is_jd_hk_url = re.compile(r'https://item.jd.hk/.*?').findall(item)
                if is_jd_hk_url != []:
                    goods_id = re.compile(r'https://item.jd.hk/(.*?).html.*?').findall(item)[0]
                    tmp_goods_id = goods_id
                    tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)
                else:
                    is_yiyao_jd_url = re.compile(r'https://item.yiyaojd.com/.*?').findall(item)
                    if is_yiyao_jd_url != []:
                        goods_id = re.compile(r'https://item.yiyaojd.com/(.*?).html.*?').findall(item)[0]
                        tmp_goods_id = goods_id
                        tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)
                    else:
                        my_lg.info('京东商品url错误, 非正规的url, 请参照格式(https://item.jd.com/)或者(https://item.jd.hk/)开头的...')
                        pass

    return tmp_wait_to_save_data_goods_id_list

def _get_db_jd_insert_params(item):
    '''
    得到db待插入数据
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

def get_one_jd_data(**kwargs):
    '''
    抓取jd url的data
    :param kwargs:
    :return:
    '''
    username = kwargs.get('username', '18698570079')
    wait_to_deal_with_url = kwargs.get('wait_to_deal_with_url', '')
    my_lg = kwargs.get('my_lg')

    jd = JdParse()
    goods_id = jd.get_goods_id_from_url(wait_to_deal_with_url)  # 获取goods_id, 这里返回的是一个list
    if goods_id == []:  # 如果得不到goods_id, 则return error
        my_lg.info('获取到的goods_id为空!')
        try:
            del jd  # 每次都回收一下
        except:
            pass
        gc.collect()

        return {'goods_id': ''}

    # 改进判断，根据传入数据判断是京东(京东超市属于其中)，还是京东全球购，还是京东大药房
    #####################################################
    if goods_id[0] == 0:  # [0, '1111']
        wait_to_deal_with_url = 'https://item.jd.com/' + goods_id[1] + '.html'  # 构造成标准干净的jd商品地址
    elif goods_id[0] == 1:  # [1, '1111']
        wait_to_deal_with_url = 'https://item.jd.hk/' + goods_id[1] + '.html'
    elif goods_id[0] == 2:  # [2, '1111', 'https://xxxxx']
        wait_to_deal_with_url = 'https://item.yiyaojd.com/' + goods_id[1] + '.html'

    tmp_result = jd.get_goods_data(goods_id=goods_id)
    data = jd.deal_with_data(goods_id=goods_id)  # 如果成功获取的话, 返回的是一个data的dict对象
    if data == {} or tmp_result == {}:
        my_lg.info('获取到的data为空!')
        try:
            del jd
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
    try: del jd
    except: pass

    return wait_to_save_data

def _get_jd_goods_id(goods_link):
    '''
    得到jd link的goods_id
    :param goods_link:
    :return:
    '''
    if re.compile('/(\d+).html').findall(goods_link) != []:
        return re.compile('/(\d+).html').findall(goods_link)[0]

    elif re.compile('wareId=(\d+)').findall(goods_link) != []:
        return re.compile('wareId=(\d+)').findall(goods_link)[0]

    else:
        return ''

def _deal_with_jd_goods(goods_link, my_lg):
    '''
    处理jd商品
    :param goods_link:
    :return:
    '''
    my_lg.info('进入京东商品处理接口...')
    goods_id = _get_jd_goods_id(goods_link)
    if goods_id == '':
        msg = 'goods_id匹配失败!请检查url是否正确!'
        return _error_data(msg=msg)

    jd_url = 'https://item.jd.com/{0}.html'.format(goods_id)
    data = get_one_jd_data(wait_to_deal_with_url=jd_url)
    if data.get('msg', '') == 'data为空!':
        msg = '该goods_id:{0}, 抓取数据失败!'.format(goods_id)
        return _error_data(msg=msg)

    else:
        pass

    site_id = _from_jd_type_get_site_id(type=data.get('jd_type'))
    data = _get_right_model_data(data=data, site_id=site_id, logger=my_lg)
    my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
    my_lg.info('------>>>| 正在存储的数据为: ' + data.get('goods_id', ''))

    params = _get_db_jd_insert_params(item=data)
    sql_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    is_insert_into = my_pipeline._insert_into_table(sql_str=sql_str, params=params)
    if is_insert_into:  # 如果返回值为True
        pass
    else:               # 不处理存储结果
        # msg = '存储该goods_id:{0}失败!'.format(goods_id)
        # return _error_data(msg=msg)
        pass

    return compatible_api_goods_data(data=data, my_lg=my_lg)

def _from_jd_type_get_site_id(type):
    '''
    根据jd的type得到site_id
    :param type:
    :return:
    '''
    # 采集的来源地
    if type == 7:
        site_id = 7  # 采集来源地(京东)
    elif type == 8:
        site_id = 8  # 采集来源地(京东超市)
    elif type == 9:
        site_id = 9  # 采集来源地(京东全球购)
    elif type == 10:
        site_id = 10  # 采集来源地(京东大药房)
    else:
        raise ValueError('jd的type传入非法!')

    return site_id
