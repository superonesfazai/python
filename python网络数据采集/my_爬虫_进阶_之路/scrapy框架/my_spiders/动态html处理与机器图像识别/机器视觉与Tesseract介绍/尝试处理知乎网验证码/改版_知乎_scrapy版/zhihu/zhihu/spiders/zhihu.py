# coding = utf-8

'''
@author = super_fazai
@File    : zhihu.py
@Time    : 2017/9/5 15:51
@connect : superonesfazai@gmail.com
'''

import scrapy
from selenium import webdriver
import time
from scrapy import cmdline
from scrapy.selector import Selector
from pprint import pprint

class ZhiHuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    start_urls = [
        'https://www.zhihu.com/#signin',
    ]

    def __init__(self):
        super().__init__()
        self.driver = webdriver.Chrome('/Users/afa/myFiles/tools/chromedriver')
        self.start_url = 'https://www.zhihu.com/#signin'

    def driver_run(self):
        self.driver.get(self.start_url)
        self.driver.find_element_by_class_name('signin-switch-password').click()
        time.sleep(1)
        self.driver.save_screenshot('密码login.png')
        # 发送邮箱, 账号
        self.driver.find_element_by_name('account').send_keys('superonesfazai@gmail.com')
        self.driver.find_element_by_name('password').send_keys('lrf123456')
        self.driver.save_screenshot('密码login2.png')

        time.sleep(8)
        self.driver.find_element_by_class_name('sign-button').click()

        time.sleep(4)
        self.driver.save_screenshot('成功登录.png')

        return self.driver

    def parse(self, response=None):
        response = Selector(text=self.driver.page_source, type='html')
        # print(response)
        title = response.xpath('h2.ContentItem-title div a::text').extract()
        content = response.css('div.RichContent-inner span.RichText.CopyrightRichText-richText::text').extract()
        urls = []
        for url in response.css('h2.ContentItem-title div a::attr(href)').extract():
            tmp_url = 'https://www.zhihu.com' + url
            urls.append(tmp_url)

        pprint(title)
        pprint(content)
        pprint(urls)


if __name__ == "__main__":
    tmp = ZhiHuSpider()
    tmp.driver_run()
    # cmdline.execute('scrapy crawl zhihu'.split())
    tmp.parse()

