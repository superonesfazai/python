# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class WikiSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 我们需要定义一个 Article 类
class Article(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    '''
    Scrapy的每个Item(条目)对象表示网站上的一个页面
    当然, 你可以根据需要定义不同的条目(比如url, content, header,image
    等), 但是现在我只演示收集每页的title字段(field)
    '''
    title = Field()
