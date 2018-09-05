# coding:utf-8

"""
pickle 对象utils
"""

from pickle import loads
from ..common_utils import _print

__all__ = [
    'deserializate_pickle_object',                  # 反序列化pickle对象
    'serialize_obj_item_2_dict',                    # 将序列化对象的子对象强转为dict类型
]

def deserializate_pickle_object(pickle_object, logger=None, default_res=None):
    '''
    反序列化pickle对象(python对象)
    :param pickle_object:
    :param default_res: 出错默认返回值
    :return:
    '''
    _ = {} if default_res is None else default_res
    try:
        _ = loads(pickle_object)
    except Exception as e:
        _print(msg='反序列化pickle对象出错!', logger=logger, log_level=2, exception=e)

    return _

def serialize_obj_item_2_dict(target) -> list:
    '''
    将序列化对象的子对象强转为dict类型
    :param target:
    :return:
    '''
    return [dict(item) for item in target]