# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import DouyuSpiderItem

class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['http://capi.douyucdn.cn']

    offset = 0
    url = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset='
    start_urls = [
        url + str(offset),
    ]

    def parse(self, response):
        # 返回从json中获取的data段数据集合
        data = json.loads(response.text)['data']

        for each in data:
            item = DouyuSpiderItem()
            item['name'] = each['nickname']
            item['images_urls'] = each['vertical_src']

            yield item

        self.offset += 20
        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

