# coding = utf-8

'''
@author = super_fazai
@File    : quotes_spider.py
@Time    : 2017/8/19 16:45
@connect : superonesfazai@gmail.com
'''

"""
先转到项目的顶级目录并运行：
    scrapy crawl quotes

学习使用scrapy提取数据的最佳方式是尝试使用：scrapy shell [url]
    >>> response.css('title')
    [<Selector xpath='descendant-or-self::title' data='<title>Quotes to Scrape</title>'>]
    >>> response.css('title::text').extract()
    ['Quotes to Scrape']
    >>> # extract() -> a list
    >>> response.css('title::text').extract()[0]
    'Quotes to Scrape'
    >>> response.css('title::text').extract_first()
    'Quotes to Scrape'
    >>> # extract_first() 当没有找到与选择匹配的元素时, 能避免IndexError并返回None
除了extract()和 extract_first()方法之外，
还可以re()使用正则表达式提取该方法：
    >>> response.css('title::text').re(r'Quotes.*')
    ['Quotes to Scrape']
    >>> response.css('title::text').re(r'Q\w+')
    ['Quotes']
    >>> response.css('title::text').re(r'(\w+) to (\w+)')
    ['Quotes', 'Scrape']
"""

import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'      # 识别爬虫, 它在项目中必须是唯一的, 即唯一用来识别和标识这个爬虫
    # 除了重写start_requests()方法, 还可以将其直接作为类的默认属性start_urls,
    # 即start_requests方法的快捷方式
    # 它也会被默认完成类似start_requests()的功能
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    # # 必须返回一个可迭代的请求(你可以返回一个请求list或写一个生成器函数)
    # # spider将开始爬取, 随后的请求将从这些这些初始请求连续生成
    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)
    #

    # 一个将被调用来为处理每个下载请求的响应方法
    # 该parse()方法通常解析响应, 将爬取的数据提取为实例
    # 并且还可以查找新的url以从中创建新的请求(Request)
    def parse(self, response):  # response是一个TextResponse保存页面内容的实例
        page = response.url.split('/')[-2]
        file_name = 'quotes-%s.html' % page
        with open(file_name, 'wb') as f:
            f.write(response.body)
        self.log('Save file %s' % file_name)

