# -*- coding: utf-8 -*-
import scrapy
import requests
import json
from ..items import BoZhuUserItem
from scrapy.selector import Selector
import time
from random import randint
from ..settings import COOKIES

class SinaSpeciesSpiderNewSpider(scrapy.Spider):
    name = 'sina_species_spider_new'
    # allowed_domains = ['d.weibo.com/']
    start_urls = ['http://d.weibo.com/']
    # start_urls = ['http://www.baidu.com']

    def __init__(self):
        super(SinaSpeciesSpiderNewSpider, self).__init__()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'd.weibo.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'cookie': COOKIES
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
            18: [2688, '美食'],
            19: [3288, '电影'],
        }

        self.proxies = self.get_proxy_ip_from_ip_pool()

        self.index = 1
        self.pagebar = [0, 1, 2, 3, 4, '']

        self.page_range = {
            1: range(0, 31),
            2: range(31, 61),
            3: range(61, 91),
            4: range(91, 121),
            5: range(121, 151),
            6: range(151, 181),
            7: range(181, 211),
            8: range(211, 241),
            9: range(241, 271),
            10: range(271, 301),
            # 11: range(301, 331),
            # 12: range(331, 361),
            # 13: range(361, 391),
            # 14: range(391, 421),
            # 15: range(421, 451),
            # 16: range(451, 481),
            # 17: range(481, 511),
            # 18: range(511, 541),
            # 19: range(541, 571),
            # 20: range(571, 601),
            # 21: range(601, 631),
            # 22: range(631, 661),
            # 23: range(661, 691),
            # 24: range(691, 721),
            # 25: range(721, 751),
            # 26: range(751, 781),
            # 27: range(781, 811),
            # 28: range(811, 841),
            # 29: range(871, 901),
            # 30: range(901, 931),
            # 31: range(961, 991),
            # 32: range(991, 1021),
        }

    def parse(self, response):
        while True:
            if self.index > 19:
                print('-' * 100 + '一次大循环爬取完成')
                print()
                print('-' * 100 + '即将重新开始爬取....')
                self.proxies = self.get_proxy_ip_from_ip_pool()     # 获取新的代理pool
                self.index = 1

            else:
                time.sleep(10)
                tmp_number = randint(1, 8)      # 随机一个数，来获取随机爬取范围
                for i in range(0, 19):    # 控制每个分类的循环
                    bozhu = BoZhuUserItem()

                    tmp_type = self.species[self.index][1]
                    number = self.species[self.index][0]

                    domain = '102803_ctg1_{}_-_ctg1_{}'.format(str(number), str(number))
                    id = domain

                    tmp_pagebar_index = 0
                    tmp_pre_page_index = 1
                    tmp_page_index = 1

                    for count in self.page_range[tmp_number]:      # 又入坑(大多数热门页面30页后无法下拉)：弄清算法规律后，发现在不同的热门页面，下拉到一定的页数，就无法下拉获取数据，点背...
                        self.log('============| 正在采集第%d页的内容 ...... |' % (count+1,))
                        # 分析pagebar
                        #                    5            11           17
                        # pagebar: 0 1 2 3 4 无 0 1 2 3 4 无 0 1 2 3 4 无....
                        if tmp_pagebar_index > 5:   # 控制其始终小于5
                            tmp_pagebar_index = 0
                        pagebar = str(self.pagebar[tmp_pagebar_index])

                        current_page = str(count + 1)
                        script_uri = r'/102803_ctg1_{}_-_ctg1_{}'.format(str(number), str(number))
                        domain_op = domain
                        # 1506471533330
                        __rnd = str(15064) + str(range(1, 10)) + str(range(1, 10)) + str(range(1, 10)) + str(range(1, 10)) + str(range(1, 10)) + str(range(1, 10)) + str(range(1, 10)) + str(range(1, 10))
                        # __rnd = str(1506471533330)
                        if (count) % 6 == 0:        # 分析出来count为6的倍数则pre_page加1
                            tmp_pre_page_index += 1
                        pre_page = str(tmp_pre_page_index)

                        if (count + 1) % 6 == 0:    # 分析出来count+1为6的倍数则page加1
                            tmp_page_index += 1
                        page = str(tmp_page_index)

                        url = 'https://d.weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&from=faxian_hot&mod=fenlei&tab=home&pl_name=Pl_Core_NewMixFeed__3&feed_type=1&domain={}&pagebar={}&current_page={}&id={}&script_uri={}&domain_op={}&__rnd={}&pre_page={}&page={}' \
                            .format(domain, pagebar, current_page, id, script_uri, domain_op, __rnd, pre_page, page)

                        time.sleep(2)       # 设置等待时间便面微博进行网页重定向

                        # 发现规律，每爬取多少页面时，会将页面重定向，并且很久不响应，所以间隔性休眠
                        # if count == 50 or count == 100 or count == 150 or count == 200 or count == 250:
                        #     print('============| >>>>>> 爬虫正在休眠中 ...... <<<<<<')
                        #     time.sleep(100)

                        tmp_proxies = {
                            'http': self.proxies['http'][randint(1, 70)]
                        }

                        print('------>>>>>>| 正在使用代理 %s 进行爬取 ...... |<<<<<<------' % tmp_proxies['http'])

                        content = requests.get(url, headers=self.headers, proxies=tmp_proxies).json()    # 用requests自带就很友好，还能避免错误

                        # content = json.loads(response.text)  # json返回的数据进行转码为dict格式, 顺带识别里面的文字
                        # print(content['data'])

                        tmp_html = content['data']

                        if len(tmp_html) <= 100000:
                            print('==========| 此时返回的content["data"]为空值, 爬虫进入短暂休眠 ....... |')
                            print('==========| 请稍后，即将开始继续爬取------>>>>>')
                            time.sleep(2)

                            tmp_proxies = {
                                'http': self.proxies['http'][randint(1, 70)]
                            }

                            print('------>>>>>>| 正在使用代理 %s 进行爬取 ...... |<<<<<<------' % tmp_proxies['http'])

                            content = requests.get(url, headers=self.headers, proxies=tmp_proxies).json()

                            time.sleep(1)
                            tmp_html = content['data']

                        for item in Selector(text=tmp_html).css('.WB_detail .WB_info').extract():
                            tmp_nick_name = Selector(text=item).css('a::attr("nick-name")').extract_first()
                            tmp_nick_name_url = Selector(text=item).css('a::attr("href")').extract_first()

                            bozhu['nick_name'] = tmp_nick_name
                            bozhu['sina_type'] = tmp_type
                            bozhu['nick_name_url'] = tmp_nick_name_url

                            print('---->> ', [tmp_nick_name, tmp_type, tmp_nick_name_url])

                            yield bozhu

                        self.log('============| 采集第%d页的内容 完毕 |' % (count + 1,))

                        tmp_pagebar_index += 1  # 累加1

                    self.index += 1     # 更换索引地址

    def get_proxy_ip_from_ip_pool(self):
        base_url = 'http://127.0.0.1:8000'
        result = requests.get(base_url).json()

        result_ip_list = {}
        result_ip_list['http'] = []
        for item in result:
            tmp_url = 'http://' + str(item[0]) + ':' + str(item[1])
            result_ip_list['http'].append(tmp_url)
        # pprint(result_ip_list)

        return result_ip_list


