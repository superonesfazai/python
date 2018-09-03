# coding:utf-8

'''
@author = super_fazai
@File    : items.py
@connect : superonesfazai@gmail.com
'''

from scrapy.item import Item
from scrapy import Field

class ProxyItem(Item):
    ip = Field()
    port = Field()
    ip_type = Field()           # ip代理类型('http'/'https')
    anonymity = Field()         # 匿名度(0:透明, 1:高匿)
    score = Field()             # 代理分数
    last_check_time = Field()   # 最后验证时间
