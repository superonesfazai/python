# coding:utf-8

'''
@author = super_fazai
@File    : z8.py
@Time    : 2017/8/11 13:36
@connect : superonesfazai@gmail.com
'''

"""
折800
"""

import re
from json import dumps

def _get_zhe_800_wait_to_save_data_goods_id_list(data, my_lg):
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
            is_zhe_800_url = re.compile(r'https://shop.zhe800.com/products/.*?').findall(item)
            if is_zhe_800_url != []:
                if re.compile(r'https://shop.zhe800.com/products/(.*?)\?.*?').findall(item) != []:
                    tmp_zhe_800_url = re.compile(r'https://shop.zhe800.com/products/(.*?)\?.*?').findall(item)[0]
                    if tmp_zhe_800_url != '':
                        goods_id = tmp_zhe_800_url
                    else:
                        zhe_800_url = re.compile(r';').sub('', item)
                        goods_id = re.compile(r'https://shop.zhe800.com/products/(.*?)\?.*?').findall(zhe_800_url)[0]
                else:  # 处理从数据库中取出的数据
                    zhe_800_url = re.compile(r';').sub('', item)
                    goods_id = re.compile(r'https://shop.zhe800.com/products/(.*)').findall(zhe_800_url)[0]
                tmp_goods_id = goods_id
                tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)

            else:
                is_miao_sha_url = re.compile(r'https://miao.zhe800.com/products/.*?').findall(item)
                if is_miao_sha_url != []:  # 先不处理这种链接的情况
                    if re.compile(r'https://miao.zhe800.com/products/(.*?)\?.*?').findall(item) != []:
                        tmp_zhe_800_url = re.compile(r'https://miao.zhe800.com/products/(.*?)\?.*?').findall(item)[0]
                        if tmp_zhe_800_url != '':
                            goods_id = tmp_zhe_800_url
                        else:
                            zhe_800_url = re.compile(r';').sub('', item)
                            goods_id = re.compile(r'https://miao.zhe800.com/products/(.*?)\?.*?').findall(zhe_800_url)[0]

                    else:  # 处理从数据库中取出的数据
                        zhe_800_url = re.compile(r';').sub('', item)
                        goods_id = re.compile(r'https://miao.zhe800.com/products/(.*)').findall(zhe_800_url)[0]
                    pass  # 不处理
                else:
                    my_lg.info('折800商品url错误, 非正规的url, 请参照格式(https://shop.zhe800.com/products/)开头的...')
                    pass  # 不处理

    return tmp_wait_to_save_data_goods_id_list

def _get_db_zhe_800_insert_params(item):
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
        dumps(item['schedule'], ensure_ascii=False),

        item['site_id'],
        item['is_delete'],
    )

    return params
