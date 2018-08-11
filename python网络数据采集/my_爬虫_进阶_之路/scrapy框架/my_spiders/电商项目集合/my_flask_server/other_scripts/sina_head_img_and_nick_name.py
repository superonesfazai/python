# coding:utf-8

'''
@author = super_fazai
@File    : sina_head_img_and_nick_name.py
@Time    : 2018/1/10 10:03
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

import scrapy
import requests
import json
from scrapy.selector import Selector
from time import sleep
from settings import SINA_COOKIES, IS_BACKGROUND_RUNNING
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from random import randint
import gc
import re

from fzutils.time_utils import (
    get_shanghai_time,
)
from fzutils.linux_utils import daemon_init
from fzutils.internet_utils import get_random_pc_ua
from fzutils.ip_pools import MyIpPools

class SinaSpeciesSpiderNewSpider():
    def __init__(self):
        super(SinaSpeciesSpiderNewSpider, self).__init__()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'd.weibo.com',
            'User-Agent': get_random_pc_ua(),
            'cookie': SINA_COOKIES,
        }

        self.species = {
            1: [4288, '明星'],
            2: [6388, '财经'],
            3: [6288, '国际'],
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
            20: [5988, '科普'],
            21: [2488, '电视剧'],
            22: [5288, '音乐'],
            23: [4788, '运动健身'],
            24: [2188, '健康'],
            25: [6488, '瘦身'],
            26: [6588, '养生'],
            27: [6788, '历史'],
            28: [2288, '美女模特'],
            29: [4988, '美图'],
            30: [4388, '搞笑'],
            31: [6988, '辟谣'],
            32: [7088, '正能量'],
            33: [5788, '政务'],
            34: [4888, '游戏'],
            35: [2588, '旅游'],
            36: [3188, '育儿'],
            37: [5888, '家居'],
            38: [1688, '星座'],
            39: [4588, '读书'],
            40: [7188, '三农'],
            41: [5488, '艺术'],
            42: [1588, '美妆'],
            43: [2388, '动漫'],
            44: [5688, '宗教'],
            45: [2788, '萌宠'],
            46: [1788, '婚庆'],
            47: [8788, '舞蹈'],
            48: [8189, '收藏'],
        }

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

    def parse(self):
        while True:
            if self.index > 48:
                print('-' * 100 + '一次大循环爬取完成')
                print()
                print('-' * 100 + '即将重新开始爬取....')
                ip_object = MyIpPools()
                self.proxies = ip_object.get_proxy_ip_from_ip_pool()     # 获取新的代理pool
                self.index = 1

            else:
                sleep(5)
                tmp_number = randint(1, 8)      # 随机一个数，来获取随机爬取范围

                my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                tmp_index = 1
                for i in range(0, 49):    # 控制每个分类的循环
                    bozhu = {}

                    if self.index == 49:
                        break

                    tmp_type = self.species[self.index][1]
                    number = self.species[self.index][0]

                    domain = '102803_ctg1_{}_-_ctg1_{}'.format(str(number), str(number))
                    id = domain

                    tmp_pagebar_index = 0
                    tmp_pre_page_index = 1
                    tmp_page_index = 1

                    for count in self.page_range[tmp_number]:      # 又入坑(大多数热门页面30页后无法下拉)：弄清算法规律后，发现在不同的热门页面，下拉到一定的页数，就无法下拉获取数据，点背...
                        if tmp_index % 50 == 0:  # 每50次重连一次，避免单次长连无响应报错
                            print('正在重置，并与数据库建立新连接中...')
                            my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                            print('与数据库的新连接成功建立...')

                        if my_pipeline.is_connect_success:
                            print('============| 正在采集第%d页的内容 ...... |' % (count+1,))
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
                            __rnd = str(15064) + str(randint(1, 9)) + str(randint(1, 9)) + str(randint(1, 9)) + str(randint(1, 9)) + str(randint(1, 9)) + str(randint(1, 9)) + str(randint(1, 9)) + str(randint(1, 9))
                            # __rnd = str(1506471533330)
                            if (count) % 6 == 0:        # 分析出来count为6的倍数则pre_page加1
                                tmp_pre_page_index += 1
                            pre_page = str(tmp_pre_page_index)

                            if (count + 1) % 6 == 0:    # 分析出来count+1为6的倍数则page加1
                                tmp_page_index += 1
                            page = str(tmp_page_index)

                            url = 'https://d.weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&from=faxian_hot&mod=fenlei&tab=home&pl_name=Pl_Core_NewMixFeed__3&feed_type=1&domain={}&pagebar={}&current_page={}&id={}&script_uri={}&domain_op={}&__rnd={}&pre_page={}&page={}' \
                                .format(domain, pagebar, current_page, id, script_uri, domain_op, __rnd, pre_page, page)
                            print(url)
                            sleep(2)       # 设置等待时间避免微博进行网页重定向

                            # 发现规律，每爬取多少页面时，会将页面重定向，并且很久不响应，所以间隔性休眠
                            # if count == 50 or count == 100 or count == 150 or count == 200 or count == 250:
                            #     print('============| >>>>>> 爬虫正在休眠中 ...... <<<<<<')
                            #     time.sleep(100)

                            tmp_html = self.get_url_body(url=url)

                            if len(tmp_html) <= 100000:
                                print('==========| 此时返回的content["data"]为空值, 爬虫进入短暂休眠 ....... |')
                                print('==========| 请稍后，即将开始继续爬取------>>>>>')
                                sleep(2)
                                tmp_html = self.get_url_body(url=url)
                                # print(tmp_html)

                            for item in Selector(text=tmp_html).css('div.face a').extract():
                                tmp_nick_name = Selector(text=item).css('img::attr("title")').extract_first()
                                tmp_head_img_url = 'https:' + Selector(text=item).css('img::attr("src")').extract_first()

                                bozhu['nick_name'] = self.wash_nick_name(nick_name=tmp_nick_name)
                                bozhu['sina_type'] = tmp_type
                                bozhu['head_img_url'] = tmp_head_img_url

                                print('---->> ', [tmp_nick_name, tmp_type, tmp_head_img_url])

                                # yield bozhu
                                my_pipeline.insert_into_sina_weibo_table(item=bozhu)
                                gc.collect()

                            print('============| 采集第%d页的内容 完毕 |' % (count + 1,))
                            tmp_pagebar_index += 1  # 累加1

                        else:
                            print('数据库连接失败!')
                            pass
                        tmp_index += 1
                    self.index += 1     # 更换索引地址

    def get_url_body(self, url):
        '''
        根据url获取到需求的data数据
        :param url: str
        :return: str
        '''
        # 设置代理ip
        ip_object = MyIpPools()
        self.proxies = ip_object.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]

        tmp_proxies = {
            'http': self.proxy,
        }
        print('------>>>>>>| 正在使用代理 %s 进行爬取 ...... |<<<<<<------' % tmp_proxies['http'])

        try:
            content = requests.get(url, headers=self.headers, proxies=tmp_proxies, timeout=12).json()  # 用requests自带就很友好，还能避免错误
        except:
            content = {}

        return content.get('data', '')

    def wash_nick_name(self, nick_name):
        '''
        清洗nick_name
        :param nick_name:
        :return: 过滤后的nick_name
        '''
        # 清洗
        nick_name = re.compile(r'的微博').sub('', nick_name)
        nick_name = re.compile(r'微博').sub('', nick_name)
        nick_name = re.compile(r'新浪').sub('', nick_name)
        nick_name = re.compile(r'官博').sub('', nick_name)

        return nick_name

def main_2():
    tmp = SinaSpeciesSpiderNewSpider()
    tmp.parse()

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')  # 在调用daemon_init函数前是可以使用print到标准输出的，调用之后就要用把提示信息通过stdout发送到日志系统中了
    daemon_init()  # 调用之后，你的程序已经成为了一个守护进程，可以执行自己的程序入口了
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    # time.sleep(10)  # daemon化自己的程序之后，sleep 10秒，模拟阻塞
    main_2()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        main_2()