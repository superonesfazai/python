# coding = utf-8

'''
@author = super_fazai
@File    : sunwz.py
@Time    : 2017/9/2 21:37
@connect : superonesfazai@gmail.com
'''

"""
Spider 版本
"""

import scrapy
from ..items import DongGuanItem
from scrapy.spiders import Spider

class SunSpider(Spider):
    name = 'sun1'
    allowed_domains = ['wz.sun0769.com']
    url = 'http://wz.sun0769.com/index.php/question/questionType?type=4&page='
    offset = 0
    start_urls = [
        url + str(offset),
    ]

    def parse(self, response):
        # 取出每个页面里帖子链接list
        links = response.css('tr > td > a.news14::attr(href)').extract()
        # 迭代发送每个帖子的请求, 调用parse_item方法处理
        for link in links:
            yield scrapy.Request(link, callback=self.parse_item)
        # 设置页码终止条件，并且每次发送新的页面请求调用parse方法处理
        if self.offset <= 71130:
            self.offset += 30
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

    def parse_item(self, response):
        item = DongGuanItem()
        # 标题
        item['title'] = response.xpath('//div[contains(@class, "pagecenter p3")]//strong/text()').extract()[0]
        # 编号
        item['number'] = item['title'].split(' ')[-1].split(":")[-1]
        # 文字内容，默认先取出有图片情况下的文字内容列表
        content = response.xpath('//div[@class="contentext"]/text()').extract()
        # 如果没有内容，则取出没有图片情况下的文字内容列表
        if len(content) == 0:
            content = response.xpath('//div[@class="c1 text14_2"]/text()').extract()
            # content为列表，通过join方法拼接为字符串，并去除首尾空格
            item['content'] = "".join(content).strip()
        else:
            item['content'] = "".join(content).strip()

        # 链接
        item['url'] = response.url

        yield item