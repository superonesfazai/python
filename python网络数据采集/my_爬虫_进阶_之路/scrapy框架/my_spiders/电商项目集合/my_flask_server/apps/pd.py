# coding:utf-8

'''
@author = super_fazai
@File    : pd.py
@Time    : 2018/8/11 13:44
@connect : superonesfazai@gmail.com
'''

"""
拼多多
"""

import re
from json import dumps

def _get_pinduoduo_wait_to_save_data_goods_id_list(data, my_lg):
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
            is_pinduoduo_url = re.compile(r'http://mobile.yangkeduo.com/goods.html.*?').findall(item)
            if is_pinduoduo_url != []:
                if re.compile(r'http://mobile.yangkeduo.com/goods.html\?.*?goods_id=(\d+).*?').findall(item) != []:
                    tmp_pinduoduo_url = \
                    re.compile(r'http://mobile.yangkeduo.com/goods.html\?.*?goods_id=(\d+).*?').findall(item)[0]
                    if tmp_pinduoduo_url != '':
                        goods_id = tmp_pinduoduo_url
                    else:  # 只是为了在pycharm里面测试，可以不加
                        pinduoduo_url = re.compile(r';').sub('', item)
                        goods_id = re.compile(r'http://mobile.yangkeduo.com/goods.html\?.*?goods_id=(\d+).*?').findall(pinduoduo_url)[0]
                    my_lg.info('------>>>| 得到的拼多多商品id为:{0}'.format(goods_id))
                    tmp_goods_id = goods_id
                    tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)
                else:
                    pass
            else:
                my_lg.info('拼多多商品url错误, 非正规的url, 请参照格式(http://mobile.yangkeduo.com/goods.html)开头的...')
                pass  # 不处理

    return tmp_wait_to_save_data_goods_id_list

def _get_db_pinduoduo_insert_params(item):
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
        dumps(item['schedule'], ensure_ascii=False),

        item['site_id'],
        item['is_delete'],
    )

    return params
