# -*- coding: utf-8 -*-

'''
@author = super_fazai
@File    : get_1000000_微信公众号.py
@Time    : 2017/9/24 10:25
@connect : superonesfazai@gmail.com
'''

import scrapy
import urllib.parse, urllib.request
from ..items import Get1000000Item
import re
import random

from .always_used_chinese_character import always_used_chinese_character

class GongzonghaoSpider(scrapy.Spider):
    name = 'gongzonghao'
    allowed_domains = ['weixin.sogou.com']
    page_index = 1
    base_url = 'http://weixin.sogou.com/weixin?type=1&s_from=input&ie=utf8&_sug_=y&_sug_type_=&w=01019900&sut=433918&sst0=1506220275057&lkt=0%2C0%2C0&query='

    def start_requests(self):
        query = chr(random.randint(97, 122))
        # 改规则，改为从常用的2054个汉字中随机取一个汉字
        # query = always_used_chinese_character[random.randint(1, len(always_used_chinese_character))]
        first_url = 'http://weixin.sogou.com/weixin?type=1&s_from=input&ie=utf8&_sug_=y&_sug_type_=&w=01019900&sut=433918&sst0=1506220275057&lkt=0%2C0%2C0&query={}'.format(urllib.parse.quote(query))
        yield scrapy.Request(first_url, callback=self.parse)

    def parse(self, response):
        self.log('===========================| 正在爬取第%s页的内容 |' % self.page_index)

        number_item = Get1000000Item()
        tmp = []
        for item in response.css('ul.news-list2 li div.gzh-box2 p.info label').extract():
            a = re.compile(r'<label name="em_weixinhao">(.*?)</label>').findall(item)[0]
            # print(a)
            tmp.append(a)
        print(tmp)
        number_item['em_weixinhao'] = tmp
        # self.log('===========================| tmp |', tmp)
        yield number_item

        next_page = response.css('.news-box .p-fy a#sogou_next::attr(href)').extract_first()  # extract_first()能避免索引越界而报错，更具健壮性
        if next_page is not None:
            next_page = r'http://weixin.sogou.com/weixin' + next_page

            self.page_index += 1
            self.log('===========================| 下一页的url = |' + next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            self.log('===========================| 刚获取的下一页面为None |')

            # tmp_number = random.randint(97, 122)    # 在a到z中随机一个字母
            # query = chr(tmp_number)
            # 改规则，改为从常用的2054个汉字中随机取一个汉字
            query = always_used_chinese_character[random.randint(1, len(always_used_chinese_character))]
            print(query)
            next_page = self.base_url + urllib.parse.quote(query)
            yield scrapy.Request(next_page, callback=self.parse)      # # 通过这样能解决 no more duplicates will be shown (see DUPEFILTER_DEBUG to show all duplicates)
        # yield number_item
