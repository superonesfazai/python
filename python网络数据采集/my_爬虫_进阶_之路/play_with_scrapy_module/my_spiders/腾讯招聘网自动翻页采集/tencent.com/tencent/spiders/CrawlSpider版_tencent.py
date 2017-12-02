# coding = utf-8

'''
@author = super_fazai
@File    : CrawlSpider版_tencent.py
@Time    : 2017/9/2 16:52
@connect : superonesfazai@gmail.com
'''

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import TencentItem

class TencentSpider(CrawlSpider):
    name = "crawlspider_tencent"
    allowed_domains = ["hr.tencent.com"]
    start_urls = [
        "http://hr.tencent.com/position.php?&start=0#a",
    ]

    page_lx = LinkExtractor(allow=("start=\d+"))

    rules = [
        Rule(page_lx, callback = "parseContent", follow = True),
    ]

    def parseContent(self, response):
        for each in response.xpath('//*[@class="even"]'):
            name = each.xpath('./td[1]/a/text()').extract()[0]
            detailLink = each.xpath('./td[1]/a/@href').extract()[0]
            positionInfo = each.xpath('./td[2]/text()').extract()[0]

            peopleNumber = each.xpath('./td[3]/text()').extract()[0]
            workLocation = each.xpath('./td[4]/text()').extract()[0]
            publishTime = each.xpath('./td[5]/text()').extract()[0]
            #print name, detailLink, catalog,recruitNumber,workLocation,publishTime

            item = TencentItem()
            item['name']=name
            item['detailLink']=detailLink
            item['positionInfo']=positionInfo
            item['peopleNumber']=peopleNumber
            item['workLocation']=workLocation
            item['publishTime']=publishTime

            yield item

    # parse() 方法不需要写
    # def parse(self, response):
    #     pass