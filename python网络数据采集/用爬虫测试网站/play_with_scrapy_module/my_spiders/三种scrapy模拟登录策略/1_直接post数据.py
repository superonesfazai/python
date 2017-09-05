# coding = utf-8

'''
@author = super_fazai
@File    : 1_直接post数据.py
@Time    : 2017/9/5 20:07
@connect : superonesfazai@gmail.com
'''

import scrapy

class RenRen1Spider(scrapy.Spider):
    name = 'renren1'
    allowed_domains = [
        'renren.com'
    ]

    def start_requests(self):
        url = 'http://www.renren.com/PLogin.do'
        # FormRequest是scrapy发送post请求的方法
        yield scrapy.FormRequest(
            url = url,
            formdata = {
                'email': 'mr_mao_hacker@163.com',
                'password': 'axxxxxxxe',
            },
            callback=self.parse_page,
        )

    def parse_page(self, response):
        with open('mao2.html', 'w') as file_name:
            file_name.write(response.body)
