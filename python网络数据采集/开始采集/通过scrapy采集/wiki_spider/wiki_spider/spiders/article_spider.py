#coding: utf-8

# from scrapy.selector import Selector
# from scrapy import Spider
#
# from wiki_spider.items import Article
#
# class articleSpider(Spider):
#     name =  'article'       #决定爬虫调用的名字
#     allowed_domains = ['en.wikipedia.org']
#     start_urls = ['http://en.wikipedia.org/wiki/Main_Page',
#                   'http://en.wikipedia.org/wiki/Python_%28programming_language%29']
#     def parse(self, response):
#         item = Article()
#         title = response.xpath('//h1/text()')[0].extract()
#         print('Title is:' + title)
#         item['title'] = title
#         return item
#
# # 你可以在wiki_spider主目录中调用如下命令运行爬虫articleSpider:
# #    $ scrapy crawl article
# # 这行命令会用条目名称 article来调用爬虫(不是类名,也不是文件名,而是由ArticleSpider 的 name = "article" 决定的)

from scrapy.contrib.spiders import CrawlSpider, Rule
from wikiSpider.items import Article
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class articleSpider(CrawlSpider):
    name="article"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["http://en.wikipedia.org/wiki/Python_\
                    %28programming_language%29"]
    rules = [Rule(SgmlLinkExtractor(allow=('(/wiki/)((?!:).)*$'),),
                                    callback="parse_item", follow=True)]
    def parse_item(self, response):
        item = Article()
        title = response.xpath('//h1/text()')[0].extract()
        print("Title is: "+title)
        item['title'] = title
        return item

# 虽然这个爬虫和前面那个爬虫的启动命令一样
# 但是如果你不用 Ctrl+C 中止程序,它是不会停止的(很长时间也不会停止)
'''
Scrapy 用 Item 对象决定要从它浏览的页面中提取哪些信息。Scrapy 支持用不同的输出格
式来保存这些信息,比如 CSV、JSON 或 XML 文件格式,对应命令如下所示:
    $ scrapy crawl article -o articles.csv -t csv
    $ scrapy crawl article -o articles.json -t json
    $ scrapy crawl article -o articles.xml -t xml
当然,你也可以自定义 Item 对象,把结果写入你需要的一个文件或数据库中,只要在爬虫
的 parse 部分增加相应的代码即可
'''

'''
Scrapy 是处理网络数据采集相关问题的利器。它可以自动收集所有 URL,然后和指定的规
则进行比较;确保所有的 URL 是唯一的;根据需求对相关的 URL 进行标准化;以及到更
深层的页面中递归查找
'''