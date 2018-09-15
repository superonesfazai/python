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
    from urllib.parse import unquote

    string = string.replace('+', ' ')

    return unquote(string=string, encoding=encoding, errors=errors)

