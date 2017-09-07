# coding = utf-8

'''
@author = super_fazai
@File    : youyuan.py
@Time    : 2017/9/6 21:18
@connect : superonesfazai@gmail.com
'''

"""
运行程序：
    1. Master端打开 Redis： redis-server
    2. Slave端直接运行爬虫： scrapy crawl youyuan1
    3. 多个Slave端运行爬虫顺序没有限制
    
将项目修改成 RedisCrawlSpider 类的分布式爬虫，并尝试在多个Slave端运行
"""

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# 使用redis去重
from scrapy.dupefilters import RFPDupeFilter

from ..items import youyuanItem
import re

class YouYuanSpider(CrawlSpider):
    name = 'youyuan1'
    allowed_domains = ['youyuan.com']
    # 有缘网的列表页
    start_urls = ['http://www.youyuan.com/find/beijing/mm18-25/advance-0-0-0-0-0-0-0/p1/']

    # 搜索页面匹配规则，根据response提取链接
    list_page_lx = LinkExtractor(allow=(r'http://www.youyuan.com/find/.+'))

    # 北京、18~25岁、女性 的 搜索页面匹配规则，根据response提取链接
    page_lx = LinkExtractor(allow =(r'http://www.youyuan.com/find/beijing/mm18-25/advance-0-0-0-0-0-0-0/p\d+/'))

    # 个人主页 匹配规则，根据response提取链接
    profile_page_lx = LinkExtractor(allow=(r'http://www.youyuan.com/\d+-profile/'))

    rules = (
        # 匹配find页面，跟进链接，跳板
        Rule(list_page_lx, follow=True),

        # 匹配列表页成功，跟进链接，跳板
        Rule(page_lx, follow=True),

        # 匹配个人主页的链接，形成request保存到redis中等待调度，一旦有响应则调用parse_profile_page()回调函数处理，不做继续跟进
        Rule(profile_page_lx, callback='parse_profile_page', follow=False),
    )

    # 处理个人主页信息，得到我们要的数据
    def parse_profile_page(self, response):
        item = youyuanItem()
        item['header_url'] = self.get_header_url(response)
        item['username'] = self.get_username(response)
        item['monologue'] = self.get_monologue(response)
        item['pic_urls'] = self.get_pic_urls(response)
        item['age'] = self.get_age(response)
        item['source'] = 'youyuan'
        item['source_url'] = response.url

        #print "Processed profile %s" % response.url
        yield item


    # 提取头像地址
    def get_header_url(self, response):
        header = response.xpath('//dl[@class=\'personal_cen\']/dt/img/@src').extract()
        if len(header) > 0:
            header_url = header[0]
        else:
            header_url = ""
        return header_url.strip()

    # 提取用户名
    def get_username(self, response):
        usernames = response.xpath("//dl[@class=\'personal_cen\']/dd/div/strong/text()").extract()
        if len(usernames) > 0:
            username = usernames[0]
        else:
            username = "NULL"
        return username.strip()

    # 提取内心独白
    def get_monologue(self, response):
        monologues = response.xpath("//ul[@class=\'requre\']/li/p/text()").extract()
        if len(monologues) > 0:
            monologue = monologues[0]
        else:
            monologue = "NULL"
        return monologue.strip()

    # 提取相册图片地址
    def get_pic_urls(self, response):
        pic_urls = []
        data_url_full = response.xpath('//li[@class=\'smallPhoto\']/@data_url_full').extract()
        if len(data_url_full) <= 1:
            pic_urls.append("");
        else:
            for pic_url in data_url_full:
                pic_urls.append(pic_url)
        if len(pic_urls) <= 1:
            return "NULL"
        # 每个url用|分隔
        return '|'.join(pic_urls)

    # 提取年龄
    def get_age(self, response):
        age_urls = response.xpath("//dl[@class=\'personal_cen\']/dd/p[@class=\'local\']/text()").extract()
        if len(age_urls) > 0:
            age = age_urls[0]
        else:
            age = "0"
        age_words = re.split(' ', age)
        if len(age_words) <= 2:
            return "0"
        age = age_words[2][:-1]
        # 从age字符串开始匹配数字，失败返回None
        if re.compile(r'[0-9]').match(age):
            return age
        return "0"