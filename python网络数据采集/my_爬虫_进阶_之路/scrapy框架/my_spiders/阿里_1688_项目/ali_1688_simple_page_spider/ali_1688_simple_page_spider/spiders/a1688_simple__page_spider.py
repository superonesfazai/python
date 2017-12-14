# -*- coding: utf-8 -*-
import scrapy
from ..settings import HEADERS
from ..items import Ali1688SimplePageSpiderItem

class A1688SimplePageSpiderSpider(scrapy.Spider):
    name = '1688_simple__page_spider'
    allowed_domains = ['1688.com']
    # start_urls = ['http://1688.com/']

    def __init__(self):
        super().__init__()
        self.headers = HEADERS


    def start_requests(self):
        # first_url = input('请输入要爬去的url的地址: ')
        first_url = 'https://detail.1688.com/offer/526362847506.html?spm=b26110380.sw1688.mof001.13.5rHmRl'
        yield scrapy.Request(url=first_url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        title = response.css('h1.d-title::text').extract_first().encode().decode()
        price = response.css('span.value.price-length-6::text').extract()
        trade_number = response.css('tr.amount span.value::text').extract()

        color = response.css('div.obj-content div.box-img img::attr("alt")').extract()
        color_img_url = response.css('div.obj-content div.box-img img::attr("src")').extract()

        print(title)
        print(price)
        print(trade_number)
        print(color)
        print(color_img_url)