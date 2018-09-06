# coding:utf-8

'''
@author = super_fazai
@File    : base_spider.py
@connect : superonesfazai@gmail.com
'''

from settings import IP_POOL_TYPE

class BaseSpider(object):
    def __init__(self):
        super(BaseSpider, self).__init__()
        self.ip_pool_type = IP_POOL_TYPE

