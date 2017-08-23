# -*- coding: utf-8 -*-
import scrapy
import re

class LoginspiderSpider(scrapy.Spider):
    name = 'loginspider'
    allowed_domains = ['toscrape.com']
    login_url = 'http://quotes.toscrape.com/login'
    start_urls = [login_url]

    def parse(self, response):
        token = response.css('input[name="csrf_token"]::attr(value)').extract()     # 此处为可变数据, 所以

        data = {
            'csrf_token': token,
            'username': 'abc',
            'password': 'abc',
        }

        yield scrapy.FormRequest(url=self.login_url, formdata=data, callback=self.parse_quotes)     # 提交表单的方式, 提交完就回调自定义parse_quotes()方法

    def parse_quotes(self, response):
        self.log('-' * 100)
        for i in range(0, len(response.css('div.quote span.text::text').extract())):
            item = {
                'text': response.css('div.quote span.text::text').extract()[i],
                'author': response.css('span small.author::text').extract(),
                'about_author': re.compile(r'(http://\w.*?.com)').findall(response.url)[0] +
                                response.css('div.quote span a::attr(href)').extract()[i],
                'tags': response.css('div.tags meta::attr(content)').extract()[i],
            }
            yield item
        self.log('-' * 100)