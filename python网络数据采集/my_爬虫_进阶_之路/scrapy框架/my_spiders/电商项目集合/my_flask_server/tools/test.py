# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/10/11 14:24
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from fzutils.spider.fz_requests import MyRequests
from fzutils.internet_utils import get_random_pc_ua

print(get_uuid3('yiuxiu').replace('-', ''))
print(get_uuid3('yiuxiu6688').replace('-', ''))

