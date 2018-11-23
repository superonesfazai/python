# coding:utf-8

'''
@author = super_fazai
@File    : items.py
@connect : superonesfazai@gmail.com
'''

from scrapy.item import Field, Item

class ProxyItem(Item):
    ip = Field()
    port = Field()
    score = Field()             # 分值
    agency_agreement = Field()  # 代理协议: http/https
    check_time = Field()        # 上次检测记录时间点

