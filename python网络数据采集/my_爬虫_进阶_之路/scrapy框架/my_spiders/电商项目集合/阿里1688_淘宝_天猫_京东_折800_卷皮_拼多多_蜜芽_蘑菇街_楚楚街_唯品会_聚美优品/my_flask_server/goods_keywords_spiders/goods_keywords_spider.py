# coding:utf-8

'''
@author = super_fazai
@File    : goods_keywords_spider.py
@Time    : 2018/6/5 11:40
@connect : superonesfazai@gmail.com
'''
import sys
sys.path.append('..')

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from taobao_parse import TaoBaoLoginAndParse
from ali_1688_parse import ALi1688LoginAndParse
from tmall_parse_2 import TmallParse
from jd_parse import JdParse

from settings import (
    IS_BACKGROUND_RUNNING,
    MY_SPIDER_LOGS_PATH,
    TAOBAO_REAL_TIMES_SLEEP_TIME,
)

import gc
from logging import INFO, ERROR
from time import sleep

from pprint import pprint
import re
from scrapy.selector import Selector

from fzutils.log_utils import set_logger
from fzutils.common_utils import deal_with_JSONDecodeError_about_value_invalid_escape
from fzutils.time_utils import (
    get_shanghai_time,
)
from fzutils.linux_utils import daemon_init
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests
from fzutils.common_utils import json_2_dict
from fzutils.data.excel_utils import read_info_from_excel_file

class GoodsKeywordsSpider(object):
    def __init__(self):
        self._set_logger()
        self.msg = ''
        self._init_debugging_api()
        self.debugging_api = self._init_debugging_api()
        self._set_func_name_dict()
        self.my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
        # 插入数据到goods_id_and_keyword_middle_table表
        self.add_keyword_id_for_goods_id_sql_str = 'insert into dbo.goods_id_and_keyword_middle_table(goods_id, keyword_id) VALUES (%s, %s)'

    def _set_logger(self):
        self.my_lg = set_logger(
            log_file_name=MY_SPIDER_LOGS_PATH + '/goods_keywords/_/' + str(get_shanghai_time())[0:10] + '.txt',
            console_log_level=INFO,
            file_log_level=ERROR
        )

    def _init_debugging_api(self):
        '''
        用于设置待抓取的商品的site_id
        :return: dict
        '''
        return {
            1: True,   # 淘宝
            2: True,   # 阿里1688
            3: True,   # 天猫
            4: True,   # 京东
        }

    def _set_func_name_dict(self):
        self.func_name_dict = {
            'taobao': 'self._taobao_keywords_spider(goods_id_list={0}, keyword_id={1})',
            'ali': 'self._ali_keywords_spider(goods_id_list={0}, keyword_id={1})',
            'tmall': 'self._tmall_keywords_spider(goods_id_list={0}, keyword_id={1})',
            'jd': 'self._jd_keywords_spider(goods_id_list={0}, keyword_id={1})'
        }

    def _just_run(self):
        while True:
            # 获取keywords
            sql_str = 'select id, keyword from dbo.goods_keywords where is_delete=0'
            # 获取原先goods_db的所有已存在的goods_id
            sql_str_2 = 'select GoodsID from dbo.GoodsInfoAutoGet'

            try:
                result = list(self.my_pipeline._select_table(sql_str=sql_str))
                self.my_lg.info('正在获取db中已存在的goods_id...')
                result_2 = list(self.my_pipeline._select_table(sql_str=sql_str_2))
                self.my_lg.info('db中已存在的goods_id获取成功!')

            except TypeError:
                self.my_lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')
                result = None
                result_2 = None

            if result is not None and result_2 is not None:
                self.my_lg.info('------>>> 下面是数据库返回的所有符合条件的goods_id <<<------')
                self.my_lg.info(str(result))
                self.my_lg.info('--------------------------------------------------------')

                self.my_lg.info('即将开始实时更新数据, 请耐心等待...'.center(100, '#'))
                self.add_goods_index = 0           # 用于定位增加商品的个数
                self.db_existed_goods_id_list = [item[0] for item in result_2]
                # 即时释放资源
                try: del result_2
                except: pass
                gc.collect()

                for item in result:     # 每个关键字在True的接口都抓完, 再进行下一次
                    self.my_lg.info('正在处理id为{0}, 关键字为 {1} ...'.format(item[0], item[1]))
                    for type, type_value in self.debugging_api.items():  # 遍历待抓取的电商分类
                        if type_value is False:
                            self.my_lg.info('api为False, 跳过!')
                            continue

                        if self.add_goods_index % 20 == 0:
                            self.my_lg.info('my_pipeline客户端重连中...')
                            try: del self.my_pipeline
                            except: pass
                            self.my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                            self.my_lg.info('my_pipeline客户端重连完毕!')

                        goods_id_list = self._get_keywords_goods_id_list(type=type, keyword=item)
                        self.my_lg.info('关键字为{0}, 获取到的goods_id_list 如下: {1}'.format(item[1], str(goods_id_list)))
                        '''处理goods_id_list'''
                        self._deal_with_goods_id_list(
                            type=type,
                            goods_id_list=goods_id_list,
                            keyword_id=item[0]
                        )
                        sleep(3)

    def _get_keywords_goods_id_list(self, type, keyword):
        '''
        获取goods_id_list
        :param type: 电商种类
        :param keyword:
        :return:
        '''
        if type == 1:
            self.my_lg.info('下面是淘宝的关键字采集...')
            goods_id_list = self._get_taobao_goods_keywords_goods_id_list(keyword=keyword)
        elif type == 2:
            self.my_lg.info('下面是阿里1688的关键字采集...')
            goods_id_list = self._get_1688_goods_keywords_goods_id_list(keyword=keyword)
        elif type == 3:
            self.my_lg.info('下面是天猫的关键字采集...')
            goods_id_list = self._get_tmall_goods_keywords_goods_id_list(keyword=keyword)
        elif type == 4:
            self.my_lg.info('下面是京东的关键字采集...')
            goods_id_list = self._get_jd_goods_keywords_goods_id_list(keyword=keyword)

        else:
            goods_id_list = []

        return goods_id_list

    def _deal_with_goods_id_list(self, **kwargs):
        '''
        分类执行代码
        :param kwargs:
        :return:
        '''
        type = kwargs.get('type', '')
        goods_id_list = kwargs.get('goods_id_list', [])
        keyword_id = kwargs.get('keyword_id', '')

        if type == 1:
            self._taobao_keywords_spider(goods_id_list=goods_id_list, keyword_id=keyword_id)
        elif type == 2:
            self._1688_keywords_spider(goods_id_list=goods_id_list, keyword_id=keyword_id)
        elif type == 3:
            self._tmall_keywords_spider(goods_id_list=goods_id_list, keyword_id=keyword_id)
        elif type == 4:
            self._jd_keywords_spider(goods_id_list=goods_id_list, keyword_id=keyword_id)
        else:
            pass

        return None

    def _get_taobao_goods_keywords_goods_id_list(self, keyword):
        '''
        获取该keywords的商品的goods_id_list
        :param keyword: (id, keyword)
        :return: a list
        '''
        headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_pc_ua(),
            'accept': '*/*',
            # 'referer': 'https://s.taobao.com/search?q=%E8%BF%9E%E8%A1%A3%E8%A3%99%E5%A4%8F&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306',
            'authority': 's.taobao.com',
            # 'cookie': 't=70c4fb481898a67a66d437321f7b5cdf; cna=nbRZExTgqWsCAXPCa6QA5B86; l=AkFBuFEM2rj4GbU8Mjl3KsFo0YZa/7Vg; thw=cn; tracknick=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; _cc_=UIHiLt3xSw%3D%3D; tg=0; enc=OFbfiyN19GGi1GicxsjVmrZoFzlt9plbuviK5OuthXYfocqTD%2BL079G%2BIt4OMg6ZrbV4veSg5SQEpzuMUgLe0w%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; miid=763730917900964122; mt=ci%3D-1_1; linezing_session=i72FGC0gr3GTls7K7lswxen2_1527664168714VAPN_1; cookie2=1cf9585e0c6d98c72c64beac41a68107; v=0; _tb_token_=5ee03e566b165; uc1=cookie14=UoTeOZOVOtrsVw%3D%3D; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; _m_h5_tk=14984d833a4647c13d4207c86d0dbd97_1528036508423; _m_h5_tk_enc=a8709d79a833625dc5c42b778ee7f1ee; JSESSIONID=F57610F0B34140EDC9F242BEA0F4800A; isg=BLm5VsJ0xr4M-pvu-R_LcQkeyCNTbqwVe7qvs9vvJODVYtj0JBZ5Sd704WaUEkWw',
        }

        # 获取到的为淘宝关键字搜索按销量排名
        params = (
            ('data-key', 'sort'),
            ('data-value', 'sale-desc'),
            ('ajax', 'true'),
            # ('_ksTS', '1528171408340_395'),
            ('callback', 'jsonp396'),
            ('q', keyword[1]),
            ('imgfile', ''),
            ('commend', 'all'),
            ('ssid', 's5-e'),
            ('search_type', 'item'),
            ('sourceId', 'tb.index'),
            # ('spm', 'a21bo.2017.201856-taobao-item.1'),
            ('ie', 'utf8'),
            # ('initiative_id', 'tbindexz_20170306'),
        )

        s_url = 'https://s.taobao.com/search'
        body = MyRequests.get_url_body(url=s_url, headers=headers, params=params)
        if body == '':
            return []
        else:
            try:
                data = re.compile('\((.*)\)').findall(body)[0]
            except IndexError:
                self.my_lg.error('re获取淘宝data时出错, 出错关键字为{0}'.format(keyword[1]))
                return []

            data = json_2_dict(json_str=data, logger=self.my_lg)
            if data == {}:
                self.my_lg.error('获取到的淘宝搜索data为空dict! 出错关键字为{0}'.format(keyword[1]))
                return []
            else:
                goods_id_list = data.get('mainInfo', {}).get('traceInfo', {}).get('traceData', {}).get('allNids', [])
                if goods_id_list is None or goods_id_list == []:
                    self.my_lg.error('获取淘宝搜索goods_id_list为空list! 出错关键字{0}'.format(keyword[1]))
                    return []
                else:
                    return goods_id_list

    def _get_1688_goods_keywords_goods_id_list(self, keyword):
        '''
        根据keyword获取1688销量靠前的商品信息
        :param keyword:
        :return: a list eg: ['11111', ...]
        '''
        '''方案1: 从m.1688.com搜索页面进行抓取, 只取第一页的销量排名靠前的商品'''
        headers = {
            'authority': 'm.1688.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_pc_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'cookie': 'cna=nbRZExTgqWsCAXPCa6QA5B86; ali_ab=113.215.180.118.1523857816418.4; lid=%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA; _csrf_token=1528708263870; JSESSIONID=9L783sX92-8iXZBHLCgK4fJiFKG9-W66WeuQ-BRgo4; hng=CN%7Czh-CN%7CCNY%7C156; t=70c4fb481898a67a66d437321f7b5cdf; _tb_token_=5ee03e566b165; __cn_logon__=false; h_keys="aa#2018%u5973%u88c5t%u6064"; alicnweb=homeIdttS%3D38414563432175544705031886000168094537%7Ctouch_tb_at%3D1528767881872%7ChomeIdttSAction%3Dtrue; ctoken=YnzGSFi23yEECqVO988Gzealot; _m_h5_tk=1cdad4dba1f1502fb29f57b3f73f5610_1528770803659; _m_h5_tk_enc=64259ec4fe4c33bc4555166994ed7b4d; __cn_logon__.sig=i6UL1cVhdIpbPPA_02yGiEyKMeZR2hBfnaoYK1CcrF4; ali_apache_id=11.182.158.193.1528768195886.327406.1; XSRF-TOKEN=b84fcec8-8bdf-41a5-a5c1-f8d6bfc9f83e; _tmp_ck_0=IlQ2M6x9F5xTkEpGRay66FVl%2BBaIEY076xELE8UtaLcz%2BgR%2FJ2UZOfDeKILA7R2VgXEJ7VYCkEQjS1RcUCwfL%2Br8ZFi0vwyVwyNpQsD2QG0HaihwedkkF9Cp9Ww0Jr%2BZF4la9CTe0AY8d1E1lDF91tD7lMAKIGVSne3V95CfI8VzpiWJ415B1IA0cc9J6IpYzn0mT1xLYnXcBAkDq0gop74NaynWIxw%2BLqmnXr%2BYU2bkOyMxZOBVY9B%2Bb0FU82h3TC9HCM8dGLnK2kxlgR%2B5lyT%2BCCFhhIX%2FioEMtA0TvDpXvRSUKoDTQG%2FCeJiKfy3LxMXmcTs5TBuWkh31F8nDCpLf6%2FlYOGkqeV1WLJeYXVe3SBvZC2O2JcYBQaKHcesETe%2FwTJL1fyc%3D; ad_prefer="2018/06/12 10:18:21"; webp=1; isg=BJWVxP7WYsuzzEf8vnJ3nRJEpJdFFdP4_0ZTRxc4b4wzbrxg3ONSdf5sPHJY2WFc; ali-ss=eyJ1c2VySWQiOm51bGwsImxvZ2luSWQiOm51bGwsInNpZCI6bnVsbCwiZWNvZGUiOm51bGwsIm1lbWJlcklkIjpudWxsLCJzZWNyZXQiOiJ5V3I0UVJGelVSVGp4dWs4aUxPWGl4dDIiLCJfZXhwaXJlIjoxNTI4ODU3MDE5ODMzLCJfbWF4QWdlIjo4NjQwMDAwMH0=; ali-ss.sig=z0qrG8Cj9BhDL_CLwTzgBGcdjSOXtp6YLxgDdTQRcWE',
        }

        params = (
            ('sortType', 'booked'),
            ('filtId', ''),
            ('keywords', keyword[1]),
            ('descendOrder', 'true'),
        )

        url = 'https://m.1688.com/offer_search/-6161.html'
        body = MyRequests.get_url_body(url=url, headers=headers, params=params)
        # self.my_lg.info(str(body))
        if body == '':
            return []
        else:
            try:
                goods_id_list = Selector(text=body).css('div.list_group-item::attr("data-offer-id")').extract()
                # pprint(goods_id_list)
            except Exception as e:
                self.my_lg.exception(e)
                self.my_lg.error('获取1688搜索goods_id_list为空list! 出错关键字{0}'.format(keyword[1]))
                goods_id_list = []

        return goods_id_list

    def _get_tmall_goods_keywords_goods_id_list(self, keyword):
        '''
        根据keyword获取tmall销量靠前的商品
        :param keyword:
        :return: list eg: ['//detail.tmall.com/item.htm?id=566978017832&skuId=3606684772412', ...] 不是返回goods_id
        '''
        '''方案: tmall m站的搜索'''   # 搜索: 偶尔不稳定但是还是能用
        headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_pc_ua(),
            'accept': '*/*',
            # 'referer': 'https://list.tmall.com/search_product.htm?q=%B0%A2%B5%CF%B4%EF%CB%B9&type=p&spm=a220m.6910245.a2227oh.d100&from=mallfp..m_1_suggest&sort=d',
            'authority': 'list.tmall.com',
            # 'cookie': 'cna=nbRZExTgqWsCAXPCa6QA5B86; _med=dw:1280&dh:800&pw:2560&ph:1600&ist:0; cq=ccp%3D1; hng=CN%7Czh-CN%7CCNY%7C156; lid=%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA; enc=zIc9Cy5z0iS95tACxeX82fUsJdrekjC6%2BomP3kNKji1Z9RKwOt%2Fysyyewwf8twcytUGt2yT9AlAh5ASUlds05g%3D%3D; t=70c4fb481898a67a66d437321f7b5cdf; tracknick=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; _tb_token_=5ee03e566b165; cookie2=1cf9585e0c6d98c72c64beac41a68107; tt=tmall-main; pnm_cku822=098%23E1hvHpvUvbpvUvCkvvvvvjiPPFcvsjYnn2dvljEUPmP9sj1HPFsWtj3EP25ptj3PiQhvCvvvpZptvpvhvvCvpvhCvvOv9hCvvvmtvpvIvvCvxQvvvUgvvhVXvvvCxvvvBZZvvUhpvvChiQvv9Opvvho5vvmC3UyCvvOCvhEC0nkivpvUvvCCEppK6NOEvpCWvKXQwCzE%2BFuTRogRD76fdigqb64B9C97%2Bul1B5c6%2Bu0OVC61D70O58TJOymQD40OeutYon29V3Q7%2B3%2Busj7J%2Bu0OaokQD40OeutYLpGCvvpvvPMM; res=scroll%3A990*6982-client%3A472*680-offset%3A472*6982-screen%3A1280*800; _m_h5_tk=69794695b8eeb690d3ef037f6780d514_1529036786907; _m_h5_tk_enc=3e31314740c37d1fb14a26989cdac03c; isg=BN_f5lvy-LULYv0VwEkGMp59bjVjxpc1-mcB0nEsew7VAP6CeRTDNl2Gx5Z-nAte',
        }

        params = {
            'page_size': '20',
            'page_no': '1',
            'q': str(keyword[1]),
            'type': 'p',
            'spm': 'a220m.6910245.a2227oh.d100',
            'from': 'mallfp..m_1_suggest',
            'sort': 'd',
        }

        s_url = 'https://list.tmall.com/m/search_items.htm'
        body = MyRequests.get_url_body(url=s_url, headers=headers, params=params)
        # self.my_lg.info(str(body))
        if body == '':
            return []
        else:
            data = json_2_dict(json_str=body, logger=self.my_lg)
            if data == {}:
                self.my_lg.error('获取到的天猫搜索data为空dict! 出错关键字为{0}'.format(keyword[1]))
                return []
            else:
                _ = data.get('item', [])
                if _ is None or _ == []:
                    self.my_lg.error('获取天猫搜索goods_id_list为空list! 出错关键字{0}'.format(keyword[1]))
                    return []
                try:
                    goods_id_list = [str(item.get('url', '')) for item in _]
                except Exception as e:
                    self.my_lg.exception(e)
                    self.my_lg.error('获取天猫搜索goods_id_list为空list! 出错关键字{0}'.format(keyword[1]))
                    return []

                return goods_id_list

    def _get_jd_goods_keywords_goods_id_list(self, keyword):
        '''
        根据keyword获取京东销量靠前的商品
        :param keyword:
        :return: [] or ['xxxx', ....]
        '''
        # 方案1: jd m站的搜索(基于搜索接口)
        headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_pc_ua(),
            'accept': '*/*',
            # 'referer': 'https://so.m.jd.com/ware/search.action?keyword=b&area_ids=1,72,2819&sort_type=sort_totalsales15_desc&qp_disable=no&fdesc=%E5%8C%97%E4%BA%AC&t1=1529934870416',
            'authority': 'so.m.jd.com',
            # 'cookie': '3AB9D23F7A4B3C9B=SL4YPRE3Y4C627UCHFP4ROHI54TTYYJKLFSVROZQ57T7K3OUUKSYIVFUJKQHBAUPRANZOTPLCVC2TICTSJG6WEMUII; mba_muid=1523868445027-16c30fbc5f8c54c429; abtest=20180416164812814_35; visitkey=41587293677961039; shshshfpa=9e159581-c64f-e9f4-ad0c-8b6ced0d9f28-1525907842; shshshfpb=1a725fe3148b84c839f009c93fc261f2218f59c61e7f4e6c05af381826; retina=1; webp=1; TrackerID=GGwYSka4RvH3lm0ZwLoO2_qdMpBwRG39BvyBvQaJfzyN5cmdGt4lEMSqqJS-sbDqj4nAUX2HU4sVDGA8vl169D37w4EqceYcH6ysXv46kMVfvVdAPmSMV9LceeO3Cc6Z; whwswswws=; __jdc=122270672; subAbTest=20180604104024339_59; mobilev=html5; m_uuid_new=05C2D24B7D8FFDA8D4243A929A5C6234; intlIpLbsCountrySite=jd; mhome=1; cid=9; M_Identification=3721cafc2442fba2_42b6f64bb933019fdb27c9e124cfd67f; M_Identification_abtest=20180604104040270_32361722; M_Identification=3721cafc2442fba2_42b6f64bb933019fdb27c9e124cfd67f; so_eggsCount=1; warehistory="4764260,10658784927,"; wq_logid=1528080290.1936376147; __jdu=15238681432201722645210; __jda=122270672.15238681432201722645210.1523868143.1528255502.1529934182.18; __jdv=122270672|direct|-|none|-|1529934182053; cn=0; user-key=ecfc3673-cc54-43e2-96bd-fb7a7e700c32; ipLoc-djd=1-72-2799-0; shshshfp=a3b9323dfc6a675230170e6a43efcb81; USER_FLAG_CHECK=d9f73823a80c0305366f70a3b99b9ecb; sid=57ea016fe0ab4b04271e00f01d94d3b9; intlIpLbsCountryIp=60.177.32.78; autoOpenApp_downCloseDate_auto=1529934572240_21600000; wxa_level=1; PPRD_P=UUID.15238681432201722645210; sc_width=1280; wq_area=15_1213_0%7C3; __jdb=122270672.10.15238681432201722645210|18.1529934182; mba_sid=15299345705167145512031951538.7; __wga=1529934993217.1529934585585.1528080039013.1526716673573.6.3; shshshsID=7f3d94fa215b4e53b467f0d5e0563e9c_9_1529934993592',
        }

        params = (
            ('keyword', keyword[1]),
            ('datatype', '1'),
            ('callback', 'jdSearchResultBkCbA'),
            ('page', '1'),
            ('pagesize', '10'),
            ('ext_attr', 'no'),
            ('brand_col', 'no'),
            ('price_col', 'no'),
            ('color_col', 'no'),
            ('size_col', 'no'),
            ('ext_attr_sort', 'no'),
            ('merge_sku', 'yes'),
            ('multi_suppliers', 'yes'),
            ('area_ids', '1,72,2819'),
            ('sort_type', 'sort_totalsales15_desc'),
            ('qp_disable', 'no'),
            ('fdesc', '\u5317\u4EAC'),
            # ('t1', '1529934992189'),
        )

        s_url = 'https://so.m.jd.com/ware/search._m2wq_list'
        body = MyRequests.get_url_body(url=s_url, headers=headers, params=params)
        # self.my_lg.info(str(body))
        if body == '':
            return []
        else:
            try:
                data = re.compile('jdSearchResultBkCbA\((.*)\)').findall(body)[0]
            except IndexError:
                self.my_lg.error('获取jd的关键字数据时, IndexError! 出错关键字为{0}'.format((keyword[1])))
                return []

            '''问题在于编码中是\xa0之类的，当遇到有些 不用转义的\http之类的，则会出现以上错误。'''
            data = deal_with_JSONDecodeError_about_value_invalid_escape(json_str=data)
            data = json_2_dict(json_str=data, logger=self.my_lg)
            if data == {}:
                self.my_lg.error('获取到的天猫搜索data为空dict! 出错关键字为{0}'.format(keyword[1]))
                return []
            else:
                # 注意拿到的数据如果是京东拼购则跳过
                # pprint(data)
                data = data.get('data', {}).get('searchm', {}).get('Paragraph', [])
                # pingou中字段'bp'不为空即为拼购商品，抓取时不抓取拼购商品, 即'pingou_price': item.get('pinGou', {}).get('bp', '') == ''
                if data is not None and data != []:
                    goods_id_list = [item.get('wareid', '') for item in data if item.get('pinGou', {}).get('bp', '') == '']

                    return goods_id_list

                else:
                    self.my_lg.error('获取到的data为空list, 请检查!')
                    return []

    def _taobao_keywords_spider(self, **kwargs):
        '''
        抓取goods_id_list的数据，并存储
        :param kwargs:
        :return:
        '''
        goods_id_list = kwargs.get('goods_id_list')
        keyword_id = kwargs.get('keyword_id')
        goods_url_list = ['https://item.taobao.com/item.htm?id=' + item for item in goods_id_list]

        self.my_lg.info('即将开始抓取该关键字的goods, 请耐心等待...')

        for item in goods_url_list:     # item为goods_url
            result = False  # 用于判断某个goods是否被插入的参数
            try:
                goods_id = re.compile(r'id=(\d+)').findall(item)[0]
            except IndexError:
                self.my_lg.error('re获取goods_id时出错, 请检查!')
                continue

            if goods_id in self.db_existed_goods_id_list:
                self.my_lg.info('该goods_id[{0}]已存在于db中!'.format(goods_id))
                result = True   # 原先存在的情况
                pass

            else:
                taobao = TaoBaoLoginAndParse(logger=self.my_lg)
                if self.add_goods_index % 20 == 0:  # 每50次重连一次，避免单次长连无响应报错
                    self.my_lg.info('正在重置，并与数据库建立新连接中...')
                    self.my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                    self.my_lg.info('与数据库的新连接成功建立...')

                if self.my_pipeline.is_connect_success:
                    goods_id = taobao.get_goods_id_from_url(item)
                    if goods_id == '':
                        self.my_lg.error('@@@ 原商品的地址为: {0}'.format(item))
                        continue

                    else:
                        self.my_lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (goods_id, str(self.add_goods_index)))
                        tt = taobao.get_goods_data(goods_id)
                        data = taobao.deal_with_data(goods_id=goods_id)
                        if data != {}:
                            data['goods_id'] = goods_id
                            data['goods_url'] = 'https://item.taobao.com/item.htm?id=' + str(goods_id)
                            data['username'] = '18698570079'
                            data['main_goods_id'] = None

                            # print('------>>>| 爬取到的数据为: ', data)
                            result = taobao.old_taobao_goods_insert_into_new_table(data, pipeline=self.my_pipeline)
                        else:
                            pass

                else:  # 表示返回的data值为空值
                    self.my_lg.info('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                self.add_goods_index += 1
                gc.collect()
                sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)
            if result:      # 仅处理goods_id被插入或者原先已存在于db中
                self._insert_into_goods_id_and_keyword_middle_table(goods_id=goods_id, keyword_id=keyword_id)
            else:
                pass

        self.my_lg.info('该关键字的商品已经抓取完毕!')

        return True

    def _1688_keywords_spider(self, **kwargs):
        '''
        1688对应关键字的商品信息抓取存储
        :param kwargs:
        :return:
        '''
        goods_id_list = kwargs.get('goods_id_list')
        keyword_id = kwargs.get('keyword_id')
        goods_url_list = ['https://detail.1688.com/offer/{0}.html'.format(item) for item in goods_id_list]

        self.my_lg.info('即将开始抓取该关键字的goods, 请耐心等待...')

        for item in goods_url_list:
            result = False  # 每次重置
            try:
                goods_id = re.compile('offer/(.*?).html').findall(item)[0]
            except IndexError:
                self.my_lg.error('re获取goods_id时出错, 请检查!')
                continue
            if goods_id in self.db_existed_goods_id_list:
                self.my_lg.info('该goods_id[{0}]已存在于db中!'.format(goods_id))
                result = True   # 原先存在的情况
                pass
            else:
                ali_1688 = ALi1688LoginAndParse()
                if self.add_goods_index % 20 == 0:  # 每50次重连一次，避免单次长连无响应报错
                    self.my_lg.info('正在重置，并与数据库建立新连接中...')
                    self.my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                    self.my_lg.info('与数据库的新连接成功建立...')

                if self.my_pipeline.is_connect_success:
                    goods_id = ali_1688.get_goods_id_from_url(item)
                    if goods_id == '':
                        self.my_lg.error('@@@ 原商品的地址为: {0}'.format(item))
                        continue
                    else:
                        self.my_lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (goods_id, str(self.add_goods_index)))
                        tt = ali_1688.get_ali_1688_data(goods_id)
                        if tt.get('is_delete') == 1 and tt.get('before') is False:    # 处理已下架的但是还是要插入的
                            # 下架的商品就pass
                            continue

                        data = ali_1688.deal_with_data()
                        if data != {}:
                            data['goods_id'] = goods_id
                            data['goods_url'] = 'https://detail.1688.com/offer/' + goods_id + '.html'
                            data['username'] = '18698570079'
                            data['main_goods_id'] = None

                            result = ali_1688.old_ali_1688_goods_insert_into_new_table(data=data, pipeline=self.my_pipeline)
                        else:
                            pass

                else:  # 表示返回的data值为空值
                    self.my_lg.info('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                self.add_goods_index += 1
                try: del ali_1688
                except: pass
                gc.collect()
                sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)
            if result:      # 仅处理goods_id被插入或者原先已存在于db中
                self._insert_into_goods_id_and_keyword_middle_table(goods_id=goods_id, keyword_id=keyword_id)
            else:
                pass

        self.my_lg.info('该关键字的商品已经抓取完毕!')

        return True

    def _tmall_keywords_spider(self, **kwargs):
        '''
        tmall对应关键字采集
        :param kwargs:
        :return:
        '''
        goods_id_list = kwargs.get('goods_id_list')
        keyword_id = kwargs.get('keyword_id')
        goods_url_list = ['https:' + re.compile('&skuId=.*').sub('', item) for item in goods_id_list]

        self.my_lg.info('即将开始抓取该关键字的goods, 请耐心等待...')

        for item in goods_url_list:     # item为goods_url
            result = False  # 用于判断某个goods是否被插入的参数
            try:
                goods_id = re.compile(r'id=(\d+)').findall(item)[0]
            except IndexError:
                self.my_lg.error('re获取goods_id时出错, 请检查!')
                continue

            if goods_id in self.db_existed_goods_id_list:
                self.my_lg.info('该goods_id[{0}]已存在于db中!'.format(goods_id))
                result = True   # 原先存在的情况
                pass
            else:
                tmall = TmallParse(logger=self.my_lg)
                if self.add_goods_index % 20 == 0:  # 每20次重连一次，避免单次长连无响应报错
                    self.my_lg.info('正在重置，并与数据库建立新连接中...')
                    self.my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                    self.my_lg.info('与数据库的新连接成功建立...')

                if self.my_pipeline.is_connect_success:
                    goods_id = tmall.get_goods_id_from_url(item)
                    if goods_id == []:
                        self.my_lg.error('@@@ 原商品的地址为: {0}'.format(item))
                        continue
                    else:
                        self.my_lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (goods_id[1], str(self.add_goods_index)))
                        tt = tmall.get_goods_data(goods_id)
                        data = tmall.deal_with_data()
                        goods_id = goods_id[1]
                        if data != {}:
                            data['goods_id'] = goods_id
                            data['username'] = '18698570079'
                            data['main_goods_id'] = None
                            data['goods_url'] = tmall._from_tmall_type_get_tmall_url(type=data['type'], goods_id=goods_id)
                            if data['goods_url'] == '':
                                self.my_lg.error('该goods_url为空值! 此处跳过!')
                                continue

                            result = tmall.old_tmall_goods_insert_into_new_table(data, pipeline=self.my_pipeline)
                        else:
                            pass

                else:
                    self.my_lg.info('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                self.add_goods_index += 1
                gc.collect()
                sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)
            if result:      # 仅处理goods_id被插入或者原先已存在于db中
                self._insert_into_goods_id_and_keyword_middle_table(goods_id=goods_id, keyword_id=keyword_id)
            else:
                pass

        self.my_lg.info('该关键字的商品已经抓取完毕!')

        return True

    def _jd_keywords_spider(self, **kwargs):
        '''
        jd对应关键字采集
        :param kwargs:
        :return:
        '''
        goods_id_list = kwargs.get('goods_id_list')
        keyword_id = kwargs.get('keyword_id')
        '''初始地址可以直接用这个[https://item.jd.com/xxxxx.html]因为jd会给你重定向到正确地址, 存也可以存这个地址'''
        # 所以这边jd就不分类存，一律存为常规商品site_id = 7
        goods_url_list = ['https://item.jd.com/{0}.html'.format(str(item)) for item in goods_id_list]

        self.my_lg.info('即将开始抓取该关键字的goods, 请耐心等待...')

        for item in goods_url_list:     # item为goods_url
            result = False  # 用于判断某个goods是否被插入db的参数
            try:
                goods_id = re.compile('\/(\d+)\.html').findall(item)[0]
            except IndexError:
                self.my_lg.error('re获取goods_id时出错, 请检查!')
                continue

            if goods_id in self.db_existed_goods_id_list:
                self.my_lg.info('该goods_id[{0}]已存在于db中!'.format(goods_id))
                result = True   # 原先存在的情况
                pass
            else:
                jd = JdParse()
                if self.add_goods_index % 20 == 0:  # 每20次重连一次，避免单次长连无响应报错
                    self.my_lg.info('正在重置，并与数据库建立新连接中...')
                    self.my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                    self.my_lg.info('与数据库的新连接成功建立...')

                if self.my_pipeline.is_connect_success:
                    goods_id = jd.get_goods_id_from_url(item)
                    if goods_id == []:
                        self.my_lg.error('@@@ 原商品的地址为: {0}'.format(item))
                        continue
                    else:
                        self.my_lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (goods_id[1], str(self.add_goods_index)))
                        tt = jd.get_goods_data(goods_id)
                        data = jd.deal_with_data(goods_id)
                        goods_id = goods_id[1]
                        if data != {}:
                            data['goods_id'] = goods_id
                            data['username'] = '18698570079'
                            data['main_goods_id'] = None
                            data['goods_url'] = item

                            result = jd.old_jd_goods_insert_into_new_table(data, self.my_pipeline)
                        else:
                            pass
                else:
                    self.my_lg.info('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                self.add_goods_index += 1
                sleep(1)
                try:
                    del jd
                except: pass
                gc.collect()

            if result:      # 仅处理goods_id被插入或者原先已存在于db中
                self._insert_into_goods_id_and_keyword_middle_table(goods_id=goods_id, keyword_id=keyword_id)
            else:
                pass

        self.my_lg.info('该关键字的商品已经抓取完毕!')

        return True

    def _insert_into_goods_id_and_keyword_middle_table(self, **kwargs):
        '''
        数据插入goods_id_and_keyword_middle_table
        :param kwargs:
        :return:
        '''
        goods_id = str(kwargs['goods_id'])
        keyword_id = int(kwargs['keyword_id'])
        # self.my_lg.info(goods_id)
        # self.my_lg.info(keyword_id)
        result = False

        '''先判断中间表goods_id_and_keyword_middle_table是否已新增该关键字的id'''
        # 注意非完整sql语句不用r'', 而直接''
        sql_str = 'select keyword_id from dbo.goods_id_and_keyword_middle_table where goods_id=%s'
        try:
            _ = self.my_pipeline._select_table(sql_str=sql_str, params=(goods_id,))
            _ = [i[0] for i in _]
            # pprint(_)
        except Exception:
            self.my_lg.error('执行中间表goods_id_and_keyword_middle_table是否已新增该关键字的id的sql语句时出错, 跳过给商品加keyword_id')
            return result

        if keyword_id not in _:
            params = (
                goods_id,
                keyword_id,)
            self.my_lg.info('------>>>| 正在插入keyword_id为{0}, goods_id为{1}'.format(params[1], params[0]))
            result = self.my_pipeline._insert_into_table_2(sql_str=self.add_keyword_id_for_goods_id_sql_str, params=params, logger=self.my_lg)

        return result

    def _add_keyword_2_db_from_excel_file(self):
        '''
        从excel插入新关键字到db
        :return:
        '''
        excel_file_path = '/Users/afa/Desktop/2018-07-18-淘宝phone-top20万.xlsx'
        self.my_lg.info('正在读取{0}, 请耐心等待...'.format(excel_file_path))
        try:
            excel_result = read_info_from_excel_file(excel_file_path=excel_file_path)
        except Exception:
            self.my_lg.error('遇到错误:', exc_info=True)
            return False

        self.my_lg.info('读取完毕!!')
        self.my_lg.info('正在读取db中原先的keyword...')
        s_sql_str = 'select keyword from dbo.goods_keywords where is_delete=0'
        db_keywords = self.my_pipeline._select_table(sql_str=s_sql_str)
        db_keywords = [i[0] for i in db_keywords]
        self.my_lg.info('db keywords 读取完毕!')

        sql_str = 'insert into dbo.goods_keywords(keyword, is_delete) values (%s, %s)'
        for item in excel_result:
            keyword = item.get('关键词', None)
            if not keyword:
                continue

            if keyword in db_keywords:
                self.my_lg.info('该关键字{0}已经存在于db中...'.format(keyword))
                continue

            self.my_lg.info('------>>>| 正在存储关键字 {0}'.format(keyword))
            self.my_pipeline._insert_into_table_2(sql_str=sql_str, params=(str(keyword), 0), logger=self.my_lg)

        self.my_lg.info('全部写入完毕!')

        return True

    def __del__(self):
        try:
            del self.my_lg
            del self.msg
            del self.my_pipeline
        except:
            pass
        try:
            del self.db_existed_goods_id_list
        except:
            pass
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        _tmp = GoodsKeywordsSpider()
        # _tmp._add_keyword_2_db_from_excel_file()
        _tmp._just_run()
        # try:
        #     del _tmp
        # except:
        #     pass
        gc.collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))
        sleep(60*5)

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')  # 在调用daemon_init函数前是可以使用print到标准输出的，调用之后就要用把提示信息通过stdout发送到日志系统中了
    daemon_init()  # 调用之后，你的程序已经成为了一个守护进程，可以执行自己的程序入口了
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    # time.sleep(10)  # daemon化自己的程序之后，sleep 10秒，模拟阻塞
    just_fuck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        just_fuck_run()