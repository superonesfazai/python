# coding:utf-8

'''
@author = super_fazai
@File    : binary_utils.py
@connect : superonesfazai@gmail.com
'''

"""
进制转换 utils
"""

from binascii import (
    a2b_hex,
    b2a_hex,)

__all__ = [
    'int_to_8_digit_sixteen_digit_num',         # 整数转换为8位十六进制数
    'hex_2_str',                                # 16进制转文本
    'str_2_hex',                                # 文本转16进制
]

def int_to_8_digit_sixteen_digit_num(i:int) -> str:
    '''
    整数转换为8位十六进制数
    :param i:
    :return:
    '''
    hexrep = format(i,'08x')
    thing = ""
    for i in [3, 2, 1, 0]:
        thing += hexrep[2*i:2*i+2]

    return thing

def hex_2_str(target) -> bytes:
    '''
    16进制转文本
    :param target: 16进制字符串
    :return:
    '''
    return a2b_hex(target)

def str_2_hex(target) -> bytes:
    '''
    文本转16进制
    :param target:
    :return:
    '''
    return b2a_hex(target)