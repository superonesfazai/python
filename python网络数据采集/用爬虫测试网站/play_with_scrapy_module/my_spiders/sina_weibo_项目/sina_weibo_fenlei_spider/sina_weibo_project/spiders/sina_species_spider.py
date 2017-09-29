# -*- coding: utf-8 -*-


"""
需求:
    每个类别先获取2000个不重复ID。我想在如下类别里获取。
    国际(6288)；财经(6388)；明星(4288)；体育(1388)；
    设计(5388)；时尚(4488)；法律(7388)；社会(4188)；
    科技(2088)；数码(5088)；股市(1288)；综艺(4688)；
    汽车(5188)；军事(6688)；情感(1988)；校园(1488)；
    房产(5588)
"""


import scrapy
from selenium import webdriver
import time
from pprint import pprint
from scrapy.selector import Selector

from ..items import BoZhuUserItem
from os import system

class SinaSpeciesSpiderSpider(scrapy.Spider):
    name = 'sina_species_spider'
    # allowed_domains = ['d.weibo.com/']
    # start_urls = ['http://d.weibo.com//']
    def __init__(self):
        # super().__init__()
        scrapy.Spider.__init__(self)
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'd.weibo.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        }

        self.cookies = {
            'ALF': '1537948304',
            'Apache': '7249798919057.913.1506162529527',
            'SCF': 'AluwsnVuuVb8f4iOGi5k7zRy-IBKAxmfDFs-_RbHERcHHeIBBuFjx2PMZUS-wHdbD5YPOfD8LUX8NcsbcXPp3rM.',
            'SINAGLOBAL': '1920862274319.4636.1502628639473',
            'SSOLoginState': '1506412304',
            'SUB': '_2A250zndBDeRhGeNM41sX8ybLzjmIHXVXuu-JrDV8PUNbmtBeLWXnkW8U8mBbCeUC6dQVP77W1IQLHBNsbg..',
            'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WFLov-n86vP3ShBTANACnLe5JpX5K2hUgL.Fo-E1h.ce0nNSK-2dJLoI7_0UPWLMLvJqPDyIBtt',
            'SUHB': '08J7I6GiMwQzNU',
            'TC-Ugrow-G0': 'e66b2e50a7e7f417f6cc12eec600f517',
            'TC-V5-G0': 'f88ad6a0154aa03e3d2a393c93b76575',
            'ULV': '1506162530082:6:3:3:7249798919057.913.1506162529527:1505873317470',
            'UOR': 'developer.51cto.com,widget.weibo.com,login.sina.com.cn',
            'WBStorage': '9fa115468b6c43a6|undefined',
            'YF-Page-G0': 'f27a36a453e657c2f4af998bd4de9419',
            'YF-Ugrow-G0': '57484c7c1ded49566c905773d5d00f82',
            'YF-V5-G0': '02157a7d11e4c84ad719358d1520e5d4',
            '_s_tentry': 'cuiqingcai.com',
            'cross_origin_proto': 'SSL',
            'httpsupgrade_ab': 'SSL',
            'login_sid_t': '2a41e3628a877dcd52fb5a9091b93e77',
            'un': '15661611306',
            'wvr': '6'
        }

        self.species = {
            1: [6288, '国际'],
            2: [6388, '财经'],
            3: [4288, '明星'],
            4: [1388, '体育'],
            5: [5388, '设计'],
            6: [4488, '时尚'],
            7: [7388, '法律'],
            8: [4188, '社会'],
            9: [2088, '科技'],
            10: [5088, '数码'],
            11: [1288, '股市'],
            12: [4688, '综艺'],
            13: [5188, '汽车'],
            14: [6688, '军事'],
            15: [1988, '情感'],
            16: [1488, '校园'],
            17: [5588, '房产'],
        }

        self.index = 1

    # def __del__(self):
    #     self.driver.close()

    def start_requests(self):
        number = self.species[1][0]
        tmp_url = 'https://d.weibo.com/102803_ctg1_' + str(number) + '_-_ctg1_' + str(number) + '?from=faxian_hot&mod=fenlei#'
        print('============| 此时的分类链接为: %s |' % tmp_url)
        yield scrapy.Request(tmp_url, headers=self.header, cookies=self.cookies, callback=self.parse, dont_filter=True) # 不过滤地址

    def parse(self, response):
        if self.index >17:
            print('-' * 100 + '爬取完成')

        bozhu = BoZhuUserItem()
        tmp_type = self.species[1][1]
        for item in response.css('.WB_detail .WB_info').extract():
            bozhu = {}
            tmp_nick_name = Selector(text=item).css('a::attr("nick-name")').extract_first()
            tmp_nick_name_url = Selector(text=item).css('a::attr("href")').extract_first()

            bozhu['nick_name'] = tmp_nick_name
            bozhu['sina_type'] = tmp_type
            bozhu['nick_name_url'] = tmp_nick_name_url
            print('---->> ', [tmp_nick_name, tmp_type, tmp_nick_name_url])
            yield bozhu

        # number = self.species[self.index + 1][0]    # 更换索引地址
        # new_url = 'https://d.weibo.com/102803_ctg1_' + str(number) + '_-_ctg1_' + str(number) + '?from=faxian_hot&mod=fenlei#'
        #
        # yield scrapy.Request(new_url, headers=self.header, cookies=self.cookies)
