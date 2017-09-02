# coding = utf-8

'''
@author = super_fazai
@File    : zhihu_spider.py
@Time    : 2017/9/2 17:35
@connect : superonesfazai@gmail.com
'''

"""
已失效, 新版验证码为倒立文字
"""

from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy import Request, FormRequest
from ..items import ZhihuItem

class ZhihuSipder(CrawlSpider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = [
        "http://www.zhihu.com"
    ]

    rules = (
        Rule(LinkExtractor(allow = ('/question/\d+#.*?', )), callback = 'parse_page', follow = True),
        Rule(LinkExtractor(allow = ('/question/\d+', )), callback = 'parse_page', follow = True),
    )

    headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
    "Connection": "keep-alive",
    "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Referer": "http://www.zhihu.com/",
    }

    # 重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数
    def start_requests(self):
        return [
            Request("https://www.zhihu.com/login", meta = {'cookiejar': 1}, callback = self.post_login)
        ]

    def post_login(self, response):
        print('Preparing login')
        # 下面这句话用于抓取请求网页后返回网页中的_xsrf字段的文字, 用于成功提交表单
        xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        print(xsrf)
        # FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        # 登陆成功后, 会调用after_login回调函数
        return [FormRequest.from_response(response,   # "http://www.zhihu.com/login",
                            meta = {'cookiejar' : response.meta['cookiejar']},
                            headers = self.headers,  # 注意此处的headers
                            formdata = {
                            '_xsrf': xsrf,
                            'email': '1095511864@qq.com',
                            'password': '123456'
                            },
                            callback = self.after_login,
                            dont_filter = True
                            )]

    def after_login(self, response) :
        for url in self.start_urls :
            yield self.make_requests_from_url(url)

    def parse_page(self, response):
        problem = Selector(response)
        item = ZhihuItem()
        item['url'] = response.url
        item['name'] = problem.xpath('//span[@class="name"]/text()').extract()
        print(item['name'])
        item['title'] = problem.xpath('//h2[@class="zm-item-title zm-editable-content"]/text()').extract()
        item['description'] = problem.xpath('//div[@class="zm-editable-content"]/text()').extract()
        item['answer']= problem.xpath('//div[@class=" zm-editable-content clearfix"]/text()').extract()
        return item