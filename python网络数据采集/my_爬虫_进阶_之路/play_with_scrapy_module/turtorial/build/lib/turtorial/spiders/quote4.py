# coding = utf-8

'''
@author = super_fazai
@File    : quote4.py
@Time    : 2017/8/19 21:40
@connect : superonesfazai@gmail.com
'''

"""
使用crawl论证
    您可以通过-a 在运行它们时使用该选项为您的蜘蛛提供命令行参数
    scrapy crawl quotes4 -o quotes-humor.json -a tag=humor
"""

import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes4"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag    # 添加子标签为绝对url
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

'''
如果您将tag=humor参数传递给此蜘蛛，
您会注意到它只会访问humor标记中的URL ，
例如 http://quotes.toscrape.com/tag/humor
'''