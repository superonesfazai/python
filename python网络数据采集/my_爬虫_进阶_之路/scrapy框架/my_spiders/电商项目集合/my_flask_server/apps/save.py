# coding:utf-8

'''
@author = super_fazai
@File    : save.py
@Time    : 2017/6/11 14:01
@connect : superonesfazai@gmail.com
'''

"""
save data相关
"""

from .al import (
    _get_ali_wait_to_save_data_goods_id_list,
    _get_db_ali_insert_params,)
from .tb import (
    _get_taobao_wait_to_save_data_goods_id_list,
    _get_db_taobao_insert_params,)
from .tm import (
    _get_tmall_wait_to_save_data_goods_id_list,
    _get_db_tmall_insert_params,)
from .jd import (
    _get_jd_wait_to_save_data_goods_id_list,
    _get_db_jd_insert_params,)
from .z8 import (
    _get_zhe_800_wait_to_save_data_goods_id_list,
    _get_db_zhe_800_insert_params,)
from .jp import (
    _get_juanpi_wait_to_save_data_goods_id_list,
    _get_db_juanpi_insert_params,)
from .pd import (
    _get_pinduoduo_wait_to_save_data_goods_id_list,
    _get_db_pinduoduo_insert_params,)
from .vp import (
    _get_vip_wait_to_save_data_goods_id_list,
    _get_db_vip_insert_params,)
from .kl import (
    _get_kaola_wait_to_save_data_goods_id_list,
    _get_db_kaola_insert_params,)
from .yx import (
    _get_yanxuan_wait_to_save_data_goods_id_list,
    _get_db_yanxuan_insert_params,)
from .yp import (
    _get_youpin_wait_to_save_data_goods_id_list,
    _get_db_youpin_insert_params,)
from .jd import _from_jd_type_get_site_id
from .tm import _from_tmall_type_get_site_id

from fzutils.cp_utils import _get_right_model_data

def get_who_wait_to_save_data_goods_id_list(**kwargs):
    '''
    对应得到wait_to_save_data_goods_id_list
    :param kwargs:
    :return: a list
    '''
    type = kwargs.get('type')
    data = kwargs.get('wait_to_save_data_url_list')
    my_lg = kwargs.get('my_lg')

    if type == 'ali':
        return _get_ali_wait_to_save_data_goods_id_list(data=data)

    elif type == 'taobao':
        return _get_taobao_wait_to_save_data_goods_id_list(data=data, my_lg=my_lg)

    elif type == 'tmall':
        return _get_tmall_wait_to_save_data_goods_id_list(data=data, my_lg=my_lg)

    elif type == 'jd':
        return _get_jd_wait_to_save_data_goods_id_list(data=data, my_lg=my_lg)

    elif type == 'zhe_800':
        return _get_zhe_800_wait_to_save_data_goods_id_list(data=data, my_lg=my_lg)

    elif type == 'juanpi':
        return _get_juanpi_wait_to_save_data_goods_id_list(data=data, my_lg=my_lg)

    elif type == 'pinduoduo':
        return _get_pinduoduo_wait_to_save_data_goods_id_list(data=data, my_lg=my_lg)

    elif type == 'vip':
        return _get_vip_wait_to_save_data_goods_id_list(data=data, my_lg=my_lg)

    elif type == 'kaola':
        return _get_kaola_wait_to_save_data_goods_id_list(data=data, my_lg=my_lg)

    elif type == 'yanxuan':
        return _get_yanxuan_wait_to_save_data_goods_id_list(data=data, my_lg=my_lg)

    elif type == 'youpin':
        return _get_youpin_wait_to_save_data_goods_id_list(data=data, my_lg=my_lg)

    else:
        return []

def get_who_right_data(**kwargs):
    '''
    对应得到right_data
    :param kwargs:
    :return:
    '''
    type = kwargs.get('type')
    data = kwargs.get('data_list')
    my_lg = kwargs.get('my_lg')

    if type == 'ali':
        return _get_right_model_data(data=data, site_id=2, logger=my_lg)

    elif type == 'taobao':
        return _get_right_model_data(data=data, site_id=1, logger=my_lg)

    elif type == 'tmall':
        site_id = _from_tmall_type_get_site_id(type=data.get('type'))
        return _get_right_model_data(data=data, site_id=site_id, logger=my_lg)

    elif type == 'jd':
        site_id = _from_jd_type_get_site_id(type=data.get('jd_type'))
        return _get_right_model_data(data=data, site_id=site_id, logger=my_lg)

    elif type == 'zhe_800':
        return _get_right_model_data(data=data, site_id=11, logger=my_lg)

    elif type == 'juanpi':
        return _get_right_model_data(data=data, site_id=12, logger=my_lg)

    elif type == 'pinduoduo':
        return _get_right_model_data(data=data, site_id=13, logger=my_lg)

    elif type == 'vip':
        return _get_right_model_data(data=data, site_id=25, logger=my_lg)

    elif type == 'kaola':
        return _get_right_model_data(data=data, site_id=29, logger=my_lg)

    elif type == 'yanxuan':
        return _get_right_model_data(data=data, site_id=30, logger=my_lg)

    elif type == 'youpin':
        return _get_right_model_data(data=data, site_id=31, logger=my_lg)

    else:
        return {}

def get_db_who_insert_params(type, item):
    '''
    返回用哪个get_db_who_insert_params处理数据
    :param type:
    :return: params
    '''
    if type == 'ali':
        params = _get_db_ali_insert_params(item=item)

    elif type == 'taobao':
        params = _get_db_taobao_insert_params(item=item)

    elif type == 'tmall':
        params = _get_db_tmall_insert_params(item=item)

    elif type == 'jd':
        params = _get_db_jd_insert_params(item=item)

    elif type == 'zhe_800':
        params = _get_db_zhe_800_insert_params(item=item)

    elif type == 'juanpi':
        params = _get_db_juanpi_insert_params(item=item)

    elif type == 'pinduoduo':
        params = _get_db_pinduoduo_insert_params(item=item)

    elif type == 'vip':
        params = _get_db_vip_insert_params(item=item)

    elif type == 'kaola':
        params = _get_db_kaola_insert_params(item=item)

    elif type == 'yanxuan':
        params = _get_db_yanxuan_insert_params(item=item)

    elif type == 'youpin':
        params = _get_db_youpin_insert_params(item=item)

    else:
        params = {}

    return params