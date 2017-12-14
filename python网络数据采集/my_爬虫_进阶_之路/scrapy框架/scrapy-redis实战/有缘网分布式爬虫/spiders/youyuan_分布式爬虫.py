# coding = utf-8

'''
@author = super_fazai
@File    : youyuan_分布式爬虫.py
@Time    : 2017/9/6 21:24
@connect : superonesfazai@gmail.com
'''

from scrapy.linkextractors import LinkExtractor

# 1. 导入RedisCrawlSpider类，不使用CrawlSpider
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule

from scrapy.dupefilters import RFPDupeFilter
from ..items import youyuanItem
import re

"""
分布式爬虫执行方式：
    1. 在Master端启动redis-server：
        redis-server
    2. 在Slave端分别启动爬虫，不分先后：
        scrapy runspider youyuan.py
    3. 在Master端的redis-cli里push一个start_urls
        redis-cli> lpush youyuan:start_urls http://www.youyuan.com/find/beijing/mm18-25/advance-0-0-0-0-0-0-0/p1/
    4. 爬虫启动，查看redis数据库数据
"""

class YouYuanSpider(RedisCrawlSpider):
    name = 'youyuan'

# 3. 取消 allowed_domains() 和 start_urls
##### allowed_domains = ['youyuan.com']
##### start_urls = ['http://www.youyuan.com/find/beijing/mm18-25/advance-0-0-0-0-0-0-0/p1/']

# 4. 增加redis-key
    redis_key = 'youyuan:start_urls'

    list_page_lx = LinkExtractor(allow=(r'http://www.youyuan.com/find/.+'))
    page_lx = LinkExtractor(allow =(r'http://www.youyuan.com/find/beijing/mm18-25/advance-0-0-0-0-0-0-0/p\d+/'))
    profile_page_lx = LinkExtractor(allow=(r'http://www.youyuan.com/\d+-profile/'))

    rules = (
        Rule(list_page_lx, follow=True),
        Rule(page_lx, follow=True),
        Rule(profile_page_lx, callback='parse_profile_page', follow=False),
    )

# 5. 增加__init__()方法，动态获取allowed_domains()
    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(YouYuanSpider, self).__init__(*args, **kwargs)

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
            pic_urls.append("")
        else:
            for pic_url in data_url_full:
                pic_urls.append(pic_url)
        if len(pic_urls) <= 1:
            return "NULL"
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
        if re.compile(r'[0-9]').match(age):
            return age
        return "0"

'''
有缘网的数据爬回来了，但是放在Redis里没有处理。
之前我们配置文件里面没有定制自己的ITEM_PIPELINES，
而是使用了RedisPipeline，所以现在这些数据都被保存在redis的youyuan:items键中，
所以我们需要另外做处理。

在scrapy-youyuan目录下可以看到一个process_items.py文件，
这个文件就是scrapy-redis的example提供的从redis读取item进行处理的模版。

假设我们要把youyuan:items中保存的数据读出来写进MongoDB或者MySQL，
那么我们可以自己写一个process_youyuan_profile.py文件，然后保持后台运行就可以不停地将爬回来的数据入库了
'''