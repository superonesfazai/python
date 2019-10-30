# coding:utf-8

'''
@author = super_fazai
@File    : driver_cookies_list_2_str.py
@connect : superonesfazai@gmail.com
'''

from fzutils.spider.async_always import *

# 目标cookie_list, 从chrome中拷贝而来
cookies = '''
'''
# pprint(json_2_dict(cookies))
cookies_str = driver_cookies_list_2_str(cookies_list=json_2_dict(cookies))
print(cookies_str)