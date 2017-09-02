# coding = utf-8

'''
@author = super_fazai
@File    : 发送POST请求_demo.py
@Time    : 2017/9/2 17:21
@connect : superonesfazai@gmail.com
'''

"""
* 可以使用 yield scrapy.FormRequest(url, formdata, callback)方法发送POST请求。

* 如果希望程序执行一开始就发送POST请求，可以重写Spider类的start_requests(self) 方法，并且不再调用start_urls里的url
"""

import scrapy

class mySpider(scrapy.Spider):
    # start_urls = ["http://www.example.com/"]

    def start_requests(self):
        url = 'http://www.renren.com/PLogin.do'

        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url = url,
            formdata = {"email" : "mr_mao_hacker@163.com", "password" : "axxxxxxxe"},
            callback = self.parse_page
        )
    def parse_page(self, response):
        # do something
        pass