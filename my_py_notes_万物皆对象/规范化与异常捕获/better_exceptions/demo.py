# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

import better_exceptions

better_exceptions.MAX_LENGTH = None
# 手动激活挂钩, 不激活也生效
# better_exceptions.hook()

request = "test test test"
a, b, c, d = request.split()
