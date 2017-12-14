# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import re

class QuotesJsSpider(scrapy.Spider):
    name = 'quotes_js'

    def start_requests(self):
        yield SplashRequest(
            url='http://quotes.toscrape.com/js',
            callback=self.parse,
        )

    def parse(self, response):
        self.log('-' * 100)
        for i in range(0, len(response.css('div.quote span.text::text').extract())):
            item = {
                'text': response.css('div.quote span.text::text').extract()[i],
                'author': response.css('span small.author::text').extract(),
                'about_author': re.compile(r'(http://\w.*?.com)').findall(response.url)[0] +
                                response.css('div.quote span a::attr(href)').extract()[i],
                'tags': response.css('div.tags meta::attr(content)').extract()[i],
            }
            yield item
        self.log('-' * 100)