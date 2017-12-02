# coding = utf-8

'''
@author = super_fazai
@File    : items.py
@Time    : 2017/9/1 21:00
@connect : superonesfazai@gmail.com
'''

import scrapy

class TencentItem(scrapy.Item):
    name = scrapy.Field()
    detail_link = scrapy.Field()
    position_info = scrapy.Field()
    people_number = scrapy.Field()
    work_location = scrapy.Field()
    publish_time = scrapy.Field()

