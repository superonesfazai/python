# coding:utf-8

'''
@author = super_fazai
@File    : thread_utils.py
@connect : superonesfazai@gmail.com
'''

"""
thread utils
"""

from functools import wraps

__all__ = [
    'thread_safe',      # 线程安全装饰器
]

def thread_safe(lock):
    """
    线程安全装饰器
    :param lock: 锁
    :return:
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)
        return wrapper

    return decorate