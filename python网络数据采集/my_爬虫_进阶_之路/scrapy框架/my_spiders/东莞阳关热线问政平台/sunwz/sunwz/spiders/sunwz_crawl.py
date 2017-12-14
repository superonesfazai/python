# coding = utf-8

'''
@author = super_fazai
@File    : sunwz_crawl.py
@Time    : 2017/9/3 14:57
@connect : superonesfazai@gmail.com
'''

"""
CrawlSpider版本
"""

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import DongGuanItem
import time

class SunSpider(CrawlSpider):
    name = 'sun2'
    allowed_domains = ['wz.sun0769.com']
    start_urls = [
        'http://wz.sun0769.com/index.php/question/questionType?type=4&page=',
    ]

    # 每一页的匹配规则
    page_link = LinkExtractor(allow=('type=4'))
    # 每个帖子的匹配规则
    content_link = LinkExtractor(allow=r'/html/question/\d+/\d+.shtml')

    rules = [
        # 本案例为特殊情况, 需要调用deal_links方法处理每个页面里的链接
        Rule(page_link, process_links='deal_links', follow=True),
        Rule(content_link, callback='parse_item'),
    ]

    # 需要重新处理每个页面里的链接，将链接里的‘Type&type=4?page=xxx’替换为‘Type?type=4&page=xxx’（或者是Type&page=xxx?type=4’替换为‘Type?page=xxx&type=4’），否则无法发送这个链接
    def deal_links(self, links):
        for link in links:
            link.url = link.url.replace("?", "&").replace("Type&", "Type?")
            print(link.url)
        return links

    def parse_item(self, response):
        print(response.url)
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