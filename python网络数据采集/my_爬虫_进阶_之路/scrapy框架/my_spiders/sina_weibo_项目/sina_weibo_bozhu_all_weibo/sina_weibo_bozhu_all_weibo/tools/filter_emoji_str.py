# coding:utf-8

'''
@author = super_fazai
@File    : filter_emoji_str.py
@Time    : 2017/10/1 18:17
@connect : superonesfazai@gmail.com
'''
import re

def filter_emoji_str(content):
    '''
    过滤四个字节以上的表情字符
    :param content:
    :return:
    '''
    try:
        # python UCS-4 build的处理方式
        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        # python UCS-2 build的处理方式
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')

    resovle_value = highpoints.sub(u'', content)

    return resovle_value

# a = '你好aaaa7878$🌶'
# resovle_str = filter_emoji_str(a)
# print(resovle_str)
