# -*- coding: utf-8 -*-
import scrapy
from urllib import parse

class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['https://baike.baidu.com/']

    def parse(self, response):
        total_divide = {}
        # renwu = response.xpath('//h2/a[@href="/renwu"]/text()').extract()[0]
        # 得到总分类字典
        for i in range(0, 10):
            tmp_key = response.css('div#commonCategories dl dt h2 a::attr(href)').extract()[i].lstrip('/')
            tmp_value = response.css('div#commonCategories dl dt h2 a::text').extract()[i]
            total_divide[tmp_key] = tmp_value
        # print(total_divide)
        # post_url = response.css('div#commonCategories dl dd div a::attr(href)').extract()
        # 链接的绝对路径
        tmp_abs_urls = ['/'+k for k in total_divide.keys()]
        # print(tmp_abs_urls)
        # 分类的完整路径
        divide_urls = []
        # 得到分类完整路径
        for i in range(0, 10):
            tmp_url = response.url + tmp_abs_urls[i]
            divide_urls.append(tmp_url)
        print(divide_urls)
