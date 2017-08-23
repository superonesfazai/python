# -*- coding: utf-8 -*-
import scrapy
import json


"""
爬取可滚动的页面(即滚动刷新下一页的那种页面)
"""

class ScollQuotesSpider(scrapy.Spider):
    name = 'scoll_quotes'
    allowed_domains = ['toscrape.com']
    api_url = 'http://quotes.toscrape.com/api/quotes?page={}'
    start_urls = [api_url.format(1)]

    def parse(self, response):
        data = json.loads(response.text)

        # 通过data.keys()查看其属性
        for quote in data['quotes']:
            yield {
                'author_name': quote['author']['name'],
                'text': quote['text'],
                'tags': quote['tags']
            }
        if data['has_next']:
            next_page = data['page'] + 1
            yield scrapy.Request(url=self.api_url.format(next_page), callback=self.parse)
