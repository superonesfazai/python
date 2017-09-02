# -*- coding: utf-8 -*-
import scrapy
from ..items import TencentItem
import re

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = [
        'http://hr.tencent.com/position.php?&start=0#a',
    ]

    def parse(self, response):
        for each in response.xpath('//*[@class="even"]'):
            item = TencentItem()
            name = each.xpath('./td[1]/a/text()').extract()[0]
            detailLink = each.xpath('./td[1]/a/@href').extract()[0]
            positionInfo = each.xpath('./td[2]/text()').extract()[0]
            peopleNumber = each.xpath('./td[3]/text()').extract()[0]
            workLocation = each.xpath('./td[4]/text()').extract()[0]
            publishTime = each.xpath('./td[5]/text()').extract()[0]

            print(name)
            print(detailLink)
            print(positionInfo)
            print(peopleNumber)
            print(workLocation)
            print(publishTime)

            item['name'] = name
            item['detail_link'] = detailLink
            item['position_info'] = positionInfo
            item['people_number'] = peopleNumber
            item['work_location'] = workLocation
            item['publish_time'] = publishTime

            curpage = re.search(r'(\d+)', response.url).group(1)
            page = int(curpage) + 10
            url = re.sub(r'\d+', str(page), response.url)

            # 发送新的url请求加入待爬队列, 并调用回调函数self.parse
            yield scrapy.Request(url, callback=self.parse)

            # 将获取的数据交给pipeline
            yield item

