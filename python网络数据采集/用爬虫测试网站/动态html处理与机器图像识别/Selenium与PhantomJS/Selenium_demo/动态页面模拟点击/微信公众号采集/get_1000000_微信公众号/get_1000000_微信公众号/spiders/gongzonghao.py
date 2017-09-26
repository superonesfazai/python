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
    base_url = 'http://weixin.sogou.com/weixin?type=1&s_from=input&ie=utf8&_sug_=y&w=01019900&query='
    # http://weixin.sogou.com/weixin?type=1&s_from=input&ie=utf8&_sug_=y&w=01019900&query=

    def start_requests(self):
        query = chr(random.randint(97, 122))
        # 改规则，改为从常用的2054个汉字中随机取一个汉字
        # query = always_used_chinese_character[random.randint(1, len(always_used_chinese_character))]
        self.log('===========================| 关键字为(%s) |' % str(query))
        first_url = \
            'http://weixin.sogou.com/weixin?type=1&s_from=input&ie=utf8&_sug_=y&w=01019900&query={}'\
                .format(query)      # urllib.parse.quote(query)
        yield scrapy.Request(first_url, callback=self.parse)

    def parse(self, response):
        self.log('===========================| 正在使用user-agent为%s' % response)
        self.log('===========================| 正在爬取第(%s)页的内容 |' % self.page_index)

        number_item = Get1000000Item()
        tmp = []
        for item in response.css('ul.news-list2 li div.gzh-box2 p.info label').extract():
            a = re.compile(r'<label name="em_weixinhao">(.*?)</label>').findall(item)[0]
            print(a)
            tmp.append(a)
        print(tmp)
        number_item['em_weixinhao'] = tmp
        yield number_item

        next_page = response.css('.news-box .p-fy a#sogou_next::attr(href)').extract_first()  # extract_first()能避免索引越界而报错，更具健壮性
        if next_page is not None:
            next_page = r'http://weixin.sogou.com/weixin' + next_page

            self.page_index += 1
            self.log('===========================| 下一页的url = |' + next_page)
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)
        else:
            self.log('===========================| 刚获取的下一页面为None |')

            # query = chr(random.randint(97, 122))  # 在a到z中随机一个字母
            # 改规则，改为从常用的2054个汉字中随机取一个汉字
            try:
                # query = always_used_chinese_character[random.randint(1, len(always_used_chinese_character))]
                query = random.randint(0, 1000)
            except IndexError as e:
                self.log('===========================| query索引异常 |')
                query = chr(random.randint(97, 122))
            self.log('===========================| 关键字为(%s) |' % str(query))
            next_page = self.base_url + query   # urllib.parse.quote(query)

            self.log('===========================| 下一页的url = |' + next_page)

            # scrapy会对request的URL去重(RFPDupeFilter)，加上dont_filter则告诉它这个URL不参与去重
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)      # 通过这样能解决 no more duplicates will be shown (see DUPEFILTER_DEBUG to show all duplicates)
        # yield number_item
