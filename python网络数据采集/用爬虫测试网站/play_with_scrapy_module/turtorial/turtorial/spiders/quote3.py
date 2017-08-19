# coding = utf-8

'''
@author = super_fazai
@File    : quote3.py
@Time    : 2017/8/19 20:52
@connect : superonesfazai@gmail.com
'''

import scrapy

class AuthorSpider(scrapy.Spider):
    name = 'authors'
    start_url = [
        'http:://quotes.toscrape.com/',
    ]

    def parse(self, response):
        # author pages的links
        for href in response.css('span a::attr(href)').extract():
            yield response.follow(href, callback=self.parse_author)

        # 下一页的link
        for href in response.css('li.next a::attr(href)').extract():
            yield response.follow(href, callback=self.parse)

    # 该parse_author回调定义了一个辅助函数从css查询提取和清理数据, 并产生了Python字典与作者的数据
    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract()[0].strip()
        # 返回一个清理后的数据
        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }


"""
这个蜘蛛演示的另一个有趣的事情是，即使同一作者有许多引号，
我们也不用担心多次访问同一作者页面。
默认情况下，Scrapy会将重复的请求过滤出已访问的URL，
避免了由于编程错误导致服务器太多的问题。
这可以通过设置进行配置 DUPEFILTER_CLASS
"""