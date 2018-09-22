# coding:utf-8

'''
@author = super_fazai
@File    : str_utils.py
@Time    : 2016/8/4 13:15
@connect : superonesfazai@gmail.com
'''

"""
字符处理utils
"""

__all__ = [
    'char_is_alphabet',             # 判断单个字符是否是英文字母
    'char_is_chinese',              # 判断单个字符是否是汉字
    'char_is_number',               # 判断单个字符是否是数字
    'char_is_other',                # 判断单个字符是否非汉字，数字和英文字符
    'str_2_unicode',                # str 转 unicode
]

def char_is_alphabet(uchar):
    '''
    判断单个字符是否是英文字母
    :param uchar: 单个字符
    :return: bool
    '''
    if (u'\u0041' <= str(uchar) <= u'\u005a') or (u'\u0061' <= str(uchar) <= u'\u007a'):
        return True
    else:
        return False

def char_is_chinese(uchar):
    '''
    判断单个字符是否是汉字
    :param uchar: 单个字符
    :return: bool
    '''
    if u'\u4e00' <= str(uchar) <= u'\u9fa5':
        return True
    else:
        return False

def char_is_number(uchar):
    '''
    判断单个字符是否是数字
    :param uchar: 单个字符
    :return: bool
    '''
    if u'\u0030' <= str(uchar) <= u'\u0039':
        return True
    else:
        return False

def char_is_other(uchar):
    '''
    判断单个字符是否非汉字，数字和英文字符
    :param uchar:
    :return:
    '''
    uchar = str(uchar)
    if not (char_is_chinese(uchar) or char_is_number(uchar) or char_is_alphabet(uchar)):
        return True
    else:
        return False

def str_2_unicode(target:str):
    '''
    str 转 unicode
    :param target:
    :return:
    '''
    return target.encode('unicode_escape').decode('utf-8')