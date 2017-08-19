# coding = utf-8

'''
@author = super_fazai
@File    : quotes2.py
@Time    : 2017/8/19 19:28
@connect : superonesfazai@gmail.com
'''

"""
如果你运行这个爬虫，它会在日志中输出提取的数据

你也可以输出为其它可读格式:
    eg(以JSON序列化). scrapy crawl quotes -o quotes2.json
    eg(以jsonline序列化). scrapy crawl quotes -o quotes2.jl
"""

import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes2"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract()[0],
                'author': quote.css('span small.author::text').extract()[0],
                'tags': quote.css('div.tags meta.keywords::attr(content)').extract()[0],
            }
        # 查找下一页, (相当于创建了一个循环,跟随到所有到下一页的链接，直到它找不到一个方便的抓取博客，论坛和其他站点分页)
        next_page = response.css('ul.pager li.next a::attr(href)').extract()[0]
        if next_page is not None:
            # next_page = response.urljoin(next_page)     # 构建完整的url
            # yield scrapy.Request(next_page, callback=self.parse)    # 再次请求新的页面

            # 上面2句的创建一个request请求等价于下面的这句
            # 与scrapy.Request不同, response.follow直接支持相关URL-无需调用urljoin.
            # 请注意,response.follow只返回一个Request实例, 你仍然必须提供此请求
            yield response.follow(next_page, callback=self.parse)

        # 上面也可以直接写成如下
        # for a in response.css('ul.pager li.next a::attr(href)').extract():
        #     yield response.follow(a, callback=self.parse)
'''
你在这里看到的是Scrapy的以下链接机制：
    当您以回调方式生成请求时，Scrapy将安排该请求发送，
    并注册一个回调方法，以在该请求完成时执行
    
使用它，你可以根据您定义的规则构建复杂的跟踪链接，
并根据访问页面提取不同类型的数据
'''

"""
该jsonline格式是有用的，因为它的流状，你可以很容易地新记录追加到它。
当运行两次时，它没有相同的JSON问题。另外，由于每条记录都是单独的行，
所以您可以处理大文件，而无需将内存中的所有内容都放在一起，
还有JQ等工具可以帮助您在命令行中执行此操作
"""

