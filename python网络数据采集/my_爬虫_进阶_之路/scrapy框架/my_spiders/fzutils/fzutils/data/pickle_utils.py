# coding:utf-8

"""
pickle 对象utils
"""

from pickle import loads
from ..common_utils import _print

__all__ = [
    'deserializate_pickle_object',                  # 反序列化pickle对象
]

def deserializate_pickle_object(pickle_object, logger=None):
    '''
    反序列化pickle对象(python对象)
    :param pickle_object:
    :return:
    '''
    _ = {}
    try:
        _ = loads(pickle_object)
    except Exception as e:
        _print(msg='反序列化pickle对象出错!', logger=logger, log_level=2, exception=e)

    return _