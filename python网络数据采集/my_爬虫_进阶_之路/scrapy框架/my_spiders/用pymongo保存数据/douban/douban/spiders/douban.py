# coding = utf-8

'''
@author = super_fazai
@File    : douban.py
@Time    : 2017/9/5 19:22
@connect : superonesfazai@gmail.com
'''

import scrapy
from ..items import DouBanSpiderItem

class DouBanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = [
        'movie.douban.com',
    ]
    start = 0
    url = 'https://movie.douban.com/top250?start='
    end = '&filter='
    start_urls = [url + str(start) + end]

    def parse(self, response):
        item = DouBanSpiderItem()
        movies = response.xpath('//div[@class="info"]')

        for each in movies:
            title = each.xpath('div[@class="hd"]/a/span[@class="title"]/text()').extract()
            content = each.xpath('div[@class="bd"]/p/text()').extract()
            score = each.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()
            info = each.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()

            item['title'] = title[0]
            # 以;作为分隔，将content列表里所有元素合并成一个新的字符串
            item['content'] = ';'.join(content)
            item['score'] = score[0]
            item['info'] = info[0]
            # 提交item

            yield item

        if self.start <= 225:
            self.start += 25
            yield scrapy.Request(self.url + str(self.start) + self.end, callback=self.parse)