# coding = utf-8

'''
@author = super_fazai
@File    : quote_toscrape_com_demo.py
@Time    : 2017/8/19 15:41
@connect : superonesfazai@gmail.com
'''

import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/tag/humor/'
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract[0],
                'author': quote.xpath('span/small').extract[0],
            }

        next_page = response.css('li.next a::attr("href")').extract[0]
        if next_page is not None:
            yield response.follow(next_page, self.parse)

"""
测试方式:
    scrapy runspider quote_toscrape_com_demo.py -o quote.json
"""