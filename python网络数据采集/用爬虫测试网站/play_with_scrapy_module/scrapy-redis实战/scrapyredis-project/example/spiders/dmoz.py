from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

"""
这个爬虫继承的是CrawlSpider，它是用来说明Redis的持续性，
当我们第一次运行dmoz爬虫，然后Ctrl + C停掉之后，
再运行dmoz爬虫，之前的爬取记录是保留在Redis里的

分析起来，其实这就是一个 scrapy-redis 版 CrawlSpider 类，
需要设置Rule规则，以及callback不能写parse()方法

执行方式：scrapy crawl dmoz
"""

class DmozSpider(CrawlSpider):
    """Follow categories and extract links."""
    name = 'dmoz'
    allowed_domains = ['dmoz.org']
    start_urls = ['http://www.dmoz.org/']

    rules = [
        Rule(LinkExtractor(
            restrict_css=('.top-cat', '.sub-cat', '.cat-item')
        ), callback='parse_directory', follow=True),
    ]

    def parse_directory(self, response):
        for div in response.css('.title-and-desc'):
            yield {
                'name': div.css('.site-title::text').extract_first(),
                'description': div.css('.site-descr::text').extract_first().strip(),
                'link': div.css('a::attr(href)').extract_first(),
            }
