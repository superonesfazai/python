# coding:utf-8

'''
@author = super_fazai
@File    : path_utils.py
@Time    : 2018/8/4 12:59
@connect : superonesfazai@gmail.com
'''

"""
提供处理路径的工具
"""

import os
from contextlib import contextmanager

__all__ = [
    'cd',                           # 进入到给定目录的上下文管理器
]

@contextmanager
def cd(path):
    '''
    进入到给定目录的上下文管理器
        用法: eg:
            with cd('/Users/afa'):
                print(True)
    :param path: 绝对路径
    :return:
    '''
    cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(cwd)
