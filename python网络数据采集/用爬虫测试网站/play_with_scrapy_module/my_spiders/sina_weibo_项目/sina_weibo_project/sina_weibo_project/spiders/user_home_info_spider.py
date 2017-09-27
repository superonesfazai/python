# -*- coding: utf-8 -*-
import scrapy


class UserHomeInfoSpiderSpider(scrapy.Spider):
    name = 'user_home_info_spider'
    allowed_domains = ['weibo.com']
    start_urls = ['http://weibo.com/']

    def parse(self, response):
        pass
