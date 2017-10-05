# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaWeiboHomeInfoSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class HomeInfoItem(scrapy.Item):
    nick_name = scrapy.Field()
    care_number = scrapy.Field()
    fans_number = scrapy.Field()
    weibo_number = scrapy.Field()
    verify_type = scrapy.Field()
    sina_level = scrapy.Field()
    verify_desc = scrapy.Field()
    personal_deal_info_url = scrapy.Field()


