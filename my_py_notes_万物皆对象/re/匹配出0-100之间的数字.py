# coding = utf-8

'''
@author = super_fazai
@File    : 匹配出0-100之间的数字.py
@Time    : 2017/8/18 16:13
@connect : superonesfazai@gmail.com
'''

import re

ret = re.match("[1-9]?\d","8")
ret.group()

ret = re.match("[1-9]?\d","78")
ret.group()

# 不正确的情况
ret = re.match("[1-9]?\d","08")
ret.group()

# 修正之后的
ret = re.match("[1-9]?\d$","08")
ret.group()

# 添加|
ret = re.match("[1-9]?\d$|100","8")
ret.group()

ret = re.match("[1-9]?\d$|100","78")
ret.group()

ret = re.match("[1-9]?\d$|100","08")
ret.group()

ret = re.match("[1-9]?\d$|100","100")
ret.group()