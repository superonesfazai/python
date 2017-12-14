# -*- coding: utf-8 -*-
import scrapy
import re

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        self.log('-' * 100)
        for i in range(0, len(response.css('div.quote span.text::text').extract())):
            item =  {
                'text': response.css('div.quote span.text::text').extract()[i],
                'author': response.css('span small.author::text').extract(),
                'about_author': re.compile(r'(http://\w.*?.com)').findall(response.url)[0] + response.css('div.quote span a::attr(href)').extract()[i],
                'tags': response.css('div.tags meta::attr(content)').extract()[i],
            }
            yield item

        next_page = response.css('li.next a::attr(href)').extract()[0]
        # next_page = response.url + response.css('li.next a::attr(href)').extract()[0]
        # 上面的等于这句 # next_page = response.urljoin(next_page)

        if next_page:
            # yield scrapy.Request(next_page, callback=self.parse)      # 其中的next_page为绝对路径
            # 与scrapy.Request不同, response.follow直接支持相关URL-无需调用urljoin.
            yield response.follow(next_page, callback=self.parse)       # 其中的next_page为相对路径
        self.log('-' * 100)

