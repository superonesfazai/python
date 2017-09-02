# coding = utf-8

'''
@author = super_fazai
@File    : 模拟登陆_demo.py
@Time    : 2017/9/2 17:24
@connect : superonesfazai@gmail.com
'''

"""
使用FormRequest.from_response()方法模拟用户登录
    通常网站通过 <input type="hidden"> 实现对某些表单字段(如数据或是登录界面中的认证令牌等)
    的预填充。使用Scrapy抓取网页时，如果想要预填充或重写像用户名、用户密码这些表单字段， 
    可以使用 FormRequest.from_response() 方法实现。下面是使用这种方法的爬虫例子:
"""

import scrapy
from scrapy import log

class LoginSpider(scrapy.Spider):
    name = 'example.com'
    start_urls = ['http://www.example.com/users/login.php']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'john', 'password': 'secret'},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.log("Login failed", level=log.ERROR)
            return

        # continue scraping with authenticated session...