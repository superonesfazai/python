# coding:utf-8

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
