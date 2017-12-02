# -*- coding: utf-8 -*-
import scrapy
from pprint import pprint

class BukeSpider(scrapy.Spider):
    name = 'buke'
    allowed_domains = ['65hs.com']
    # start_urls = ['http://65hs.com/']

    def start_requests(self):
        bash_url = 'http://www.65hs.com/buke/index/index.jsp'

        header = {
            'host': 'www.65hs.com',
            'proxy-connection': 'keep-alive',
            'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.2.2; zh-cn; HTC S720t Build/JDQ39E) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 MicroMessenger/6.5.7.1041 NetType/WIFI Language/zh_CN',
            'accept-language': 'zh-CN, en-US',
            'accept-charset': 'utf-8, iso-8859-1, utf-16, *;q=0.7',
            'x-requested-with': 'com.tencent.mm',
            'content-length': 0
        }

        cookies = {
            'JSESSIONID': '985E44F56F3932BB81E71CA8622784AA',
            'openid': 'oUoc2swunJ8L28J-lO0K2q1m5Ulc'
        }

        first_request = scrapy.Request(bash_url, headers=header, cookies=cookies, callback=self.parse)
        yield first_request

    def parse(self, response):
        html = response.css('body').extract()[0]
        pprint(html)
