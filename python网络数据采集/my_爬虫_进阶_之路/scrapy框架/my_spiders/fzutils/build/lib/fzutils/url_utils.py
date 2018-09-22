# coding:utf-8

'''
@author = super_fazai
@File    : url_utils.py
@Time    : 2016/7/28 11:59
@connect : superonesfazai@gmail.com
'''

"""
url parser
"""

from urllib.parse import unquote

__all__ = [
    'unquote_plus',         # url解码
]

def unquote_plus(string, encoding='utf-8', errors='replace'):
    '''
    url解码
        eg: unquote_plus('%7e/abc+def') -> '~/abc def'
    :param string:
    :param encoding:
    :param errors:
    :return:
    '''
    string = string.replace('+', ' ')

    return unquote(string=string, encoding=encoding, errors=errors)

