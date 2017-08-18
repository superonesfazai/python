# coding = utf-8

'''
@author = super_fazai
@File    : re_search_test.py
@Time    : 2017/8/18 16:26
@connect : superonesfazai@gmail.com
'''

import re

res = re.search(r'\d+', '阅读次数为 9999')
print(res.group(0))