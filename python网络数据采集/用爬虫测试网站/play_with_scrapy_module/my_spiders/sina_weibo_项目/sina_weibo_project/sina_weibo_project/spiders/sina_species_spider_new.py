# -*- coding: utf-8 -*-
import scrapy
import requests
import json
from ..items import BoZhuUserItem
from scrapy.selector import Selector
import time
from random import randint

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
            'cookie': 'SINAGLOBAL=1920862274319.4636.1502628639473; httpsupgrade_ab=SSL; TC-Ugrow-G0=968b70b7bcdc28ac97c8130dd353b55e; login_sid_t=6c2521139641765552eaeffdc3bc61bb; TC-V5-G0=458f595f33516d1bf8aecf60d4acf0bf; _s_tentry=login.sina.com.cn; Apache=5561465425422.705.1506498709692; ULV=1506498709703:7:4:1:5561465425422.705.1506498709692:1506162530082; un=15661611306; TC-Page-G0=4c4b51307dd4a2e262171871fe64f295; YF-V5-G0=b2423472d8aef313d052f5591c93cb75; YF-Page-G0=b5853766541bcc934acef7f6116c26d1; cross_origin_proto=SSL; WBStorage=9fa115468b6c43a6|undefined; UOR=developer.51cto.com,widget.weibo.com,login.sina.com.cn; WBtopGlobal_register_version=1844f177002b1566; SCF=AluwsnVuuVb8f4iOGi5k7zRy-IBKAxmfDFs-_RbHERcHdUDJGWQpJm1Ui7yG47p9R92qkWR9fwNaJgW4Ttru2hw.; SUB=_2A250z_IADeRhGeNM41sX8ybLzjmIHXVXvWTIrDV8PUNbmtBeLXDwkW9b9vZp0F8LL4lEz4GUfwkSGT0kGA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFLov-n86vP3ShBTANACnLe5JpX5KzhUgL.Fo-E1h.ce0nNSK-2dJLoI7_0UPWLMLvJqPDyIBtt; SUHB=0S7CzD56B3SmUG; ALF=1538045387; SSOLoginState=1506509392'
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

        self.proxies = self.get_proxy_ip_from_ip_pool()

        self.index = 1
        self.pagebar = [0, 1, 2, 3, 4, '']

    def parse(self, response):
        if self.index > 17:
            print('-' * 100 + '爬取完成')
        else:
            for i in range(0, 16):    # 控制每个分类的循环
                bozhu = BoZhuUserItem()

                tmp_type = self.species[self.index][1]
                number = self.species[self.index][0]

                domain = '102803_ctg1_{}_-_ctg1_{}'.format(str(number), str(number))
                id = domain

                tmp_pagebar_index = 0
                tmp_pre_page_index = 1
                tmp_page_index = 1

                for count in range(0, 200):      # 又入坑(大多数热门页面30页后无法下拉)：弄清算法规律后，发现在不同的热门页面，下拉到一定的页数，就无法下拉获取数据，点背...
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
                        'http': self.proxies['http'][randint(0, 130)]
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
                            'http': self.proxies['http'][randint(0, 130)]
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


