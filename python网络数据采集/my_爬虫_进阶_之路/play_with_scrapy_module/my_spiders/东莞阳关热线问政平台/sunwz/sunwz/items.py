# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SunwzItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DongGuanItem(scrapy.Item):
    title = scrapy.Field()      # 帖子标题
    number = scrapy.Field()     # 帖子编号
    content = scrapy.Field()    # 帖子的文字内容
    url = scrapy.Field()        # 帖子的url