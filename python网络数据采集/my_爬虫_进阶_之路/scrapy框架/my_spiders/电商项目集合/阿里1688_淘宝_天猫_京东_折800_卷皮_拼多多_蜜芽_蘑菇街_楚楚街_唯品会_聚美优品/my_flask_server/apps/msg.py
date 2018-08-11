# coding:utf-8

'''
@author = super_fazai
@File    : msg.py
@Time    : 2017/8/11 11:16
@connect : superonesfazai@gmail.com
'''

"""
错误处理/成功处理
"""
import sys
sys.path.append('..')

from json import dumps
from sql_lang.cp_sql import error_insert_sql_str
from fzutils.time_utils import (
    datetime_to_timestamp,
    get_shanghai_time,)

def _success_data(**kwargs):
    '''
    获取数据成功!
    :param kwargs:
    :return:
    '''
    return dumps({
        'reason': 'success',
        'msg': kwargs.get('msg') if kwargs is not None else '成功!',
        'data': kwargs.get('data', {}),
        'error_code': '0008',
    }, ensure_ascii=False).encode().decode()

def _error_data(**kwargs):
    '''
    获取数据成功!
    :param kwargs:
    :return:
    '''
    return dumps({
        'reason': 'error',
        'msg': kwargs.get('msg') if kwargs is not None else '失败!',
        'data': {},
        'error_code': '0009',
    }, ensure_ascii=False).encode().decode()

def _null_goods_link():
    # 空goods_link
    return dumps({
        'reason': 'error',
        'msg': 'goods_link为空值!',
        'data': '',
        'error_code': '0001',
    })

def _invalid_goods_link():
    # 无效goods_link
    return dumps({
        'reason': 'error',
        'msg': '无效的goods_link, 请检查!',
        'data': '',
        'error_code': '0002',
    })

def _null_goods_id():
    # 空goods_id
    return dumps({
        'reason': 'error',
        'msg': '获取到的goods_id为空str, 无效的goods_link, 请检查!',
        'data': '',
        'error_code': '0003',
    })

def _null_goods_data():
    # 获取到的goods_data为{}
    return dumps({
        'reason': 'error',
        'msg': '获取到的goods_data为空dict!',
        'data': '',
        'error_code': '0004',
    })

def _insert_into_db_result(**kwargs):
    '''
    抓取后数据储存处理结果, msg显示
    :param pipeline:
    :param is_inserted_and_goods_id_list: a list eg: [('db插入结果类型bool', '对应goods_id'), ...]
    :return:
    '''
    def execute_sql_error():
        '''
        执行sql语句错误返回的东西
        :return:
        '''
        if _ is None or _ == []:        # 查询失败处理!
            msg = r'执行搜索对应商品语句时出错! 可能已被入录! 请在公司后台对应查询!<br/><br/>'
            for _u in goods_id_list:
                msg += r'官方GoodsID: {0}<br/>'.format(_u)

            return dumps({
                'reason': 'error',
                'msg': msg,
                'data': '',
                'error_code': '0005',
            })
        else:
            return None

    def judge_create_time_is_old(now_time, create_time):
        '''
        判断商品创建时间是否超过8小时
        :param now_time: datetime
        :param create_time: datetime
        :return: bool
        '''
        if int(datetime_to_timestamp(now_time) - datetime_to_timestamp(create_time)) < 28800:    # 小于8小时
            return True
        else:
            return False

    pipeline = kwargs.get('pipeline')
    is_inserted_and_goods_id_list = kwargs.get('is_inserted_and_goods_id_list', [])

    msg = ''

    # 原先是只查没有被插入的, 现在都查, because 重复插入也返回True
    # goods_id_list = [item[1] for item in is_inserted_and_goods_id_list if not item[0]]
    goods_id_list = [item[1] for item in is_inserted_and_goods_id_list]

    _e = error_insert_sql_str
    _e += ' or GoodsID=%s ' * (len(goods_id_list)-1)
    _ = pipeline._select_table(sql_str=_e, params=tuple(goods_id_list))
    execute_sql_result = execute_sql_error()
    if execute_sql_result is not None:
        return execute_sql_result

    for _i in is_inserted_and_goods_id_list:
        goods_id = _i[1]
        for _r in _:
            if goods_id == _r[2]:
                if _i[0] and judge_create_time_is_old(now_time=get_shanghai_time(), create_time=_r[1]):
                    msg += r'新采集的商品[GoodsID={0}]已存入db中!<br/><br/>'.format(goods_id)
                else:
                    if goods_id == _r[2]:
                        tmp_msg = r'这个商品原先已被存入db中! 相关信息如下:<br/>操作人员: {0}<br/>创建时间: {1}<br/>官方GoodsID: {2}<br/>商品名称: {3}<br/>转换时间: {4}<br/>优秀商品ID: {5}<br/><br/>'.format(
                            _r[0], str(_r[1]), _r[2], _r[3], str(_r[4]) if _r[4] is not None else '未转换', _r[5] if _r[5] is not None else '未转换',
                        )
                        msg += tmp_msg
            else:
                pass

    return dumps({
        'reason': 'success',
        'msg': msg,
        'data': '',
        'error_code': '0006',
    })

def _error_msg(msg):
    '''
    错误的msg, json返回
    :param msg:
    :return:
    '''
    return dumps({
        'reason': 'error',
        'msg': str(msg),
        'data': '',
        'error_code': '0007',
    })
