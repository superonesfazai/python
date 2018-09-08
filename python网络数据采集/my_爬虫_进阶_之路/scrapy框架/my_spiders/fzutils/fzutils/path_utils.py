# coding:utf-8

"""
提供处理路径的工具
"""

import os
from contextlib import contextmanager
from os.path import split, splitext

__all__ = [
    'cd',                                           # 进入到给定目录的上下文管理器
    'from_file_path_get_file_extension_name',       # 从文件路径得到该文件的扩展名
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

def from_file_path_get_file_extension_name(file_path) -> str:
    '''
    从文件路径得到该文件的扩展名
    :param file_path:
    :return:
    '''
    return splitext(split(file_path)[-1])[-1].replace('.', '')