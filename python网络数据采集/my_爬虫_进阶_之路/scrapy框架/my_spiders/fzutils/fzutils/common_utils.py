# coding:utf-8

'''
@author = super_fazai
@File    : common_utils.py
@Time    : 2018/7/13 18:19
@connect : superonesfazai@gmail.com
'''

__all__ = [
    '_json_str_to_dict',                                        # json转dict
    '_green',                                                   # 将字体变成绿色
    'delete_list_null_str',                                     # 删除list中的空str
    'list_duplicate_remove',                                    # list去重

    # json_str转dict时报错处理方案
    'deal_with_JSONDecodeError_about_value_invalid_escape',     # 错误如: ValueError: Invalid \escape: line 1 column 35442 (char 35441)
]

def _json_str_to_dict(json_str):
    '''
    json字符串转dict
    :param json_str:
    :return:
    '''
    from json import (
        loads,
        JSONDecodeError,)

    try:
        _ = loads(json_str)
    except JSONDecodeError as e:
        print(e)
        return {}

    return _

def _green(string):
    '''
    将字体转变为绿色
    :param string:
    :return:
    '''
    return '\033[32m{}\033[0m'.format(string)

def delete_list_null_str(_list):
    '''
    删除list中的所有空str
    :param _list:
    :return:
    '''
    while '' in _list:
        _list.remove('')

    return _list

def list_duplicate_remove(_list:list):
    '''
    list去重
    :param _list:
    :return:
    '''
    b = []
    [b.append(i) for i in _list if not i in b]

    return b

def deal_with_JSONDecodeError_about_value_invalid_escape(json_str):
    '''
    ValueError: Invalid \escape: line 1 column 35442 (char 35441)
    问题在于编码中是\xa0之类的，当遇到有些 不用转义的\http之类的，则会出现以上错误。
    :param json_str:
    :return: 正常的str类型的json字符串
    '''
    import re

    return re.compile(r'\\(?![/u"])').sub(r"\\\\", json_str)
