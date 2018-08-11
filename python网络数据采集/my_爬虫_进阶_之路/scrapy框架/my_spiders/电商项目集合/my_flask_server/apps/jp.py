# coding:utf-8

'''
@author = super_fazai
@File    : jp.py
@Time    : 2017/8/11 13:41
@connect : superonesfazai@gmail.com
'''

"""
卷皮
"""

import re
from json import dumps

def _get_juanpi_wait_to_save_data_goods_id_list(data, my_lg):
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
            is_juanpi_url = re.compile(r'http://shop.juanpi.com/deal/.*?').findall(item)
            if is_juanpi_url != []:
                if re.compile(r'http://shop.juanpi.com/deal/(\d+).*?').findall(item) != []:
                    tmp_juanpi_url = re.compile(r'http://shop.juanpi.com/deal/(\d+).*?').findall(item)[0]
                    if tmp_juanpi_url != '':
                        goods_id = tmp_juanpi_url
                    else:  # 只是为了在pycharm运行时不调到chrome，其实else完全可以不要的
                        juanpi_url = re.compile(r';').sub('', item)
                        goods_id = re.compile(r'http://shop.juanpi.com/deal/(\d+).*?').findall(juanpi_url)[0]
                    my_lg.info('------>>>| 得到的卷皮商品的地址为:{0}'.format(goods_id))
                    tmp_goods_id = goods_id
                    tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)

            else:
                my_lg.info('卷皮商品url错误, 非正规的url, 请参照格式(http://shop.juanpi.com/deal/)开头的...')
                pass  # 不处理

    return tmp_wait_to_save_data_goods_id_list

def _get_db_juanpi_insert_params(item):
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
        dumps(item['schedule'], ensure_ascii=False),

        item['site_id'],
        item['is_delete'],
    )

    return params
