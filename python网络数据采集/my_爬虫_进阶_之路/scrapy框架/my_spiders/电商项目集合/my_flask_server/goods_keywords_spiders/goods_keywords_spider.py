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
    IP_POOL_TYPE,
)

from gc import collect
from time import sleep

from pprint import pprint
import re
from scrapy.selector import Selector

from sql_str_controller import (
    kw_insert_str_1,
    kw_select_str_1,
    kw_select_str_2,
    kw_select_str_3,
    kw_select_str_4,
    kw_insert_str_2,
)
from multiplex_code import _block_get_new_db_conn

from fzutils.common_utils import deal_with_JSONDecodeError_about_value_invalid_escape
from fzutils.linux_utils import daemon_init
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import Requests
from fzutils.common_utils import json_2_dict
from fzutils.data.excel_utils import read_info_from_excel_file
from fzutils.spider.crawler import Crawler

class GoodsKeywordsSpider(Crawler):
    def __init__(self):
        super(GoodsKeywordsSpider, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            logger=None,
            log_save_path=MY_SPIDER_LOGS_PATH + '/goods_keywords/_/',
        )
        self.msg = ''
        self._init_debugging_api()
        self.debugging_api = self._init_debugging_api()
        self._set_func_name_dict()
        self.my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
        # 插入数据到goods_id_and_keyword_middle_table表
        self.add_keyword_id_for_goods_id_sql_str = kw_insert_str_1

    def _init_debugging_api(self):
        '''
        用于设置crawl的关键字热销商品的site_id
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
            # 获取原先goods_db的所有已存在的goods_id
            try:
                result = list(self.my_pipeline._select_table(sql_str=kw_select_str_1))
                self.lg.info('正在获取db中已存在的goods_id...')
                result_2 = list(self.my_pipeline._select_table(sql_str=kw_select_str_2))
                self.lg.info('db中已存在的goods_id获取成功!')

            except TypeError:
                self.lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')
                result = None
                result_2 = None

            if result is not None and result_2 is not None:
                self.lg.info('------>>> 下面是数据库返回的所有符合条件的goods_id <<<------')
                self.lg.info(str(result))
                self.lg.info('--------------------------------------------------------')

                self.lg.info('即将开始实时更新数据, 请耐心等待...'.center(100, '#'))
                self.add_goods_index = 0           # 用于定位增加商品的个数
                self.db_existed_goods_id_list = [item[0] for item in result_2]
                # 即时释放资源
                try: del result_2
                except: pass
                collect()

                for item in result:     # 每个关键字在True的接口都抓完, 再进行下一次
                    self.lg.info('正在处理id为{0}, 关键字为 {1} ...'.format(item[0], item[1]))
                    for type, type_value in self.debugging_api.items():  # 遍历待抓取的电商分类
                        if type_value is False:
                            self.lg.info('api为False, 跳过!')
                            continue

                        self.my_pipeline = _block_get_new_db_conn(
                            db_obj=self.my_pipeline,
                            index=self.add_goods_index,
                            logger=self.lg,
                            remainder=20,)

                        goods_id_list = self._get_keywords_goods_id_list(type=type, keyword=item)
                        self.lg.info('关键字为{0}, 获取到的goods_id_list 如下: {1}'.format(item[1], str(goods_id_list)))
                        '''处理goods_id_list'''
                        self._deal_with_goods_id_list(
                            type=type,
                            goods_id_list=goods_id_list,
                            keyword_id=item[0])
                        sleep(3)

    def _get_keywords_goods_id_list(self, type, keyword):
        '''
        获取goods_id_list
        :param type: 电商种类
        :param keyword:
        :return:
        '''
        if type == 1:
            self.lg.info('下面是淘宝的关键字采集...')
            goods_id_list = self._get_taobao_goods_keywords_goods_id_list(keyword=keyword)
        elif type == 2:
            self.lg.info('下面是阿里1688的关键字采集...')
            goods_id_list = self._get_1688_goods_keywords_goods_id_list(keyword=keyword)
        elif type == 3:
            self.lg.info('下面是天猫的关键字采集...')
            goods_id_list = self._get_tmall_goods_keywords_goods_id_list(keyword=keyword)
        elif type == 4:
            self.lg.info('下面是京东的关键字采集...')
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
        body = Requests.get_url_body(url=s_url, headers=headers, params=params, ip_pool_type=self.ip_pool_type)
        if body == '':
            return []
        else:
            try:
                data = re.compile('\((.*)\)').findall(body)[0]
            except IndexError:
                self.lg.error('re获取淘宝data时出错, 出错关键字为{0}'.format(keyword[1]))
                return []

            data = json_2_dict(json_str=data, logger=self.lg)
            if data == {}:
                self.lg.error('获取到的淘宝搜索data为空dict! 出错关键字为{0}'.format(keyword[1]))
                return []
            else:
                goods_id_list = data.get('mainInfo', {}).get('traceInfo', {}).get('traceData', {}).get('allNids', [])
                if goods_id_list is None or goods_id_list == []:
                    self.lg.error('获取淘宝搜索goods_id_list为空list! 出错关键字{0}'.format(keyword[1]))
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
        }
        params = (
            ('sortType', 'booked'),
            ('filtId', ''),
            ('keywords', keyword[1]),
            ('descendOrder', 'true'),
        )
        url = 'https://m.1688.com/offer_search/-6161.html'
        body = Requests.get_url_body(url=url, headers=headers, params=params, ip_pool_type=self.ip_pool_type)
        # self.lg.info(str(body))
        if body == '':
            return []
        else:
            try:
                goods_id_list = Selector(text=body).css('div.list_group-item::attr("data-offer-id")').extract()
                # pprint(goods_id_list)
            except Exception as e:
                self.lg.exception(e)
                self.lg.error('获取1688搜索goods_id_list为空list! 出错关键字{0}'.format(keyword[1]))
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
        body = Requests.get_url_body(url=s_url, headers=headers, params=params, ip_pool_type=self.ip_pool_type)
        # self.lg.info(str(body))
        if body == '':
            return []
        else:
            data = json_2_dict(json_str=body, logger=self.lg)
            if data == {}:
                self.lg.error('获取到的天猫搜索data为空dict! 出错关键字为{0}'.format(keyword[1]))
                return []
            else:
                _ = data.get('item', [])
                if _ is None or _ == []:
                    self.lg.error('获取天猫搜索goods_id_list为空list! 出错关键字{0}'.format(keyword[1]))
                    return []
                try:
                    goods_id_list = [str(item.get('url', '')) for item in _]
                except Exception as e:
                    self.lg.exception(e)
                    self.lg.error('获取天猫搜索goods_id_list为空list! 出错关键字{0}'.format(keyword[1]))
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
        body = Requests.get_url_body(url=s_url, headers=headers, params=params, ip_pool_type=self.ip_pool_type)
        # self.lg.info(str(body))
        if body == '':
            return []
        else:
            try:
                data = re.compile('jdSearchResultBkCbA\((.*)\)').findall(body)[0]
            except IndexError:
                self.lg.error('获取jd的关键字数据时, IndexError! 出错关键字为{0}'.format((keyword[1])))
                return []

            '''问题在于编码中是\xa0之类的，当遇到有些 不用转义的\http之类的，则会出现以上错误。'''
            data = deal_with_JSONDecodeError_about_value_invalid_escape(json_str=data)
            data = json_2_dict(json_str=data, logger=self.lg)
            if data == {}:
                self.lg.error('获取到的天猫搜索data为空dict! 出错关键字为{0}'.format(keyword[1]))
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
                    self.lg.error('获取到的data为空list, 请检查!')
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

        self.lg.info('即将开始抓取该关键字的goods, 请耐心等待...')

        for item in goods_url_list:     # item为goods_url
            result = False  # 用于判断某个goods是否被插入的参数
            try:
                goods_id = re.compile(r'id=(\d+)').findall(item)[0]
            except IndexError:
                self.lg.error('re获取goods_id时出错, 请检查!')
                continue

            if goods_id in self.db_existed_goods_id_list:
                self.lg.info('该goods_id[{0}]已存在于db中!'.format(goods_id))
                result = True   # 原先存在的情况
                pass

            else:
                taobao = TaoBaoLoginAndParse(logger=self.lg)
                if self.add_goods_index % 20 == 0:  # 每50次重连一次，避免单次长连无响应报错
                    self.lg.info('正在重置，并与数据库建立新连接中...')
                    self.my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                    self.lg.info('与数据库的新连接成功建立...')

                if self.my_pipeline.is_connect_success:
                    goods_id = taobao.get_goods_id_from_url(item)
                    if goods_id == '':
                        self.lg.error('@@@ 原商品的地址为: {0}'.format(item))
                        continue

                    else:
                        self.lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (goods_id, str(self.add_goods_index)))
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
                    self.lg.info('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                self.add_goods_index += 1
                collect()
                sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)
            if result:      # 仅处理goods_id被插入或者原先已存在于db中
                self._insert_into_goods_id_and_keyword_middle_table(goods_id=goods_id, keyword_id=keyword_id)
            else:
                pass

        self.lg.info('该关键字的商品已经抓取完毕!')

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

        self.lg.info('即将开始抓取该关键字的goods, 请耐心等待...')

        for item in goods_url_list:
            result = False  # 每次重置
            try:
                goods_id = re.compile('offer/(.*?).html').findall(item)[0]
            except IndexError:
                self.lg.error('re获取goods_id时出错, 请检查!')
                continue
            if goods_id in self.db_existed_goods_id_list:
                self.lg.info('该goods_id[{0}]已存在于db中!'.format(goods_id))
                result = True   # 原先存在的情况
                pass
            else:
                ali_1688 = ALi1688LoginAndParse(logger=self.lg)
                if self.add_goods_index % 20 == 0:  # 每50次重连一次，避免单次长连无响应报错
                    self.lg.info('正在重置，并与数据库建立新连接中...')
                    self.my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                    self.lg.info('与数据库的新连接成功建立...')

                if self.my_pipeline.is_connect_success:
                    goods_id = ali_1688.get_goods_id_from_url(item)
                    if goods_id == '':
                        self.lg.error('@@@ 原商品的地址为: {0}'.format(item))
                        continue
                    else:
                        self.lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (goods_id, str(self.add_goods_index)))
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
                    self.lg.info('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                self.add_goods_index += 1
                try: del ali_1688
                except: pass
                collect()
                sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)
            if result:      # 仅处理goods_id被插入或者原先已存在于db中
                self._insert_into_goods_id_and_keyword_middle_table(goods_id=goods_id, keyword_id=keyword_id)
            else:
                pass

        self.lg.info('该关键字的商品已经抓取完毕!')

        return True

    def _tmall_keywords_spider(self, **kwargs):
        """
        tmall对应关键字采集
        :param kwargs:
        :return:
        """
        goods_id_list = kwargs.get('goods_id_list')
        keyword_id = kwargs.get('keyword_id')
        goods_url_list = ['https:' + re.compile('&skuId=.*').sub('', item) for item in goods_id_list]

        self.lg.info('即将开始抓取该关键字的goods, 请耐心等待...')

        for item in goods_url_list:     # item为goods_url
            result = False  # 用于判断某个goods是否被插入的参数
            try:
                goods_id = re.compile(r'id=(\d+)').findall(item)[0]
            except IndexError:
                self.lg.error('re获取goods_id时出错, 请检查!')
                continue

            if goods_id in self.db_existed_goods_id_list:
                self.lg.info('该goods_id[{0}]已存在于db中!'.format(goods_id))
                result = True   # 原先存在的情况
                pass
            else:
                tmall = TmallParse(logger=self.lg)
                if self.add_goods_index % 20 == 0:  # 每20次重连一次，避免单次长连无响应报错
                    self.lg.info('正在重置，并与数据库建立新连接中...')
                    self.my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                    self.lg.info('与数据库的新连接成功建立...')

                if self.my_pipeline.is_connect_success:
                    goods_id = tmall.get_goods_id_from_url(item)
                    if goods_id == []:
                        self.lg.error('@@@ 原商品的地址为: {0}'.format(item))
                        continue
                    else:
                        self.lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (goods_id[1], str(self.add_goods_index)))
                        tt = tmall.get_goods_data(goods_id)
                        data = tmall.deal_with_data()
                        goods_id = goods_id[1]
                        if data != {}:
                            data['goods_id'] = goods_id
                            data['username'] = '18698570079'
                            data['main_goods_id'] = None
                            data['goods_url'] = tmall._from_tmall_type_get_tmall_url(type=data['type'], goods_id=goods_id)
                            if data['goods_url'] == '':
                                self.lg.error('该goods_url为空值! 此处跳过!')
                                continue

                            result = tmall.old_tmall_goods_insert_into_new_table(data, pipeline=self.my_pipeline)
                        else:
                            pass

                else:
                    self.lg.info('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                self.add_goods_index += 1
                collect()
                sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)
            if result:      # 仅处理goods_id被插入或者原先已存在于db中
                self._insert_into_goods_id_and_keyword_middle_table(goods_id=goods_id, keyword_id=keyword_id)
            else:
                pass

        self.lg.info('该关键字的商品已经抓取完毕!')

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

        self.lg.info('即将开始抓取该关键字的goods, 请耐心等待...')

        for item in goods_url_list:     # item为goods_url
            result = False  # 用于判断某个goods是否被插入db的参数
            try:
                goods_id = re.compile('\/(\d+)\.html').findall(item)[0]
            except IndexError:
                self.lg.error('re获取goods_id时出错, 请检查!')
                continue

            if goods_id in self.db_existed_goods_id_list:
                self.lg.info('该goods_id[{0}]已存在于db中!'.format(goods_id))
                result = True   # 原先存在的情况
                pass
            else:
                jd = JdParse(logger=self.lg)
                if self.add_goods_index % 20 == 0:  # 每20次重连一次，避免单次长连无响应报错
                    self.lg.info('正在重置，并与数据库建立新连接中...')
                    self.my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                    self.lg.info('与数据库的新连接成功建立...')

                if self.my_pipeline.is_connect_success:
                    goods_id = jd.get_goods_id_from_url(item)
                    if goods_id == []:
                        self.lg.error('@@@ 原商品的地址为: {0}'.format(item))
                        continue
                    else:
                        self.lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (goods_id[1], str(self.add_goods_index)))
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
                    self.lg.info('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                self.add_goods_index += 1
                sleep(1)
                try:
                    del jd
                except: pass
                collect()

            if result:      # 仅处理goods_id被插入或者原先已存在于db中
                self._insert_into_goods_id_and_keyword_middle_table(goods_id=goods_id, keyword_id=keyword_id)
            else:
                pass

        self.lg.info('该关键字的商品已经抓取完毕!')

        return True

    def _insert_into_goods_id_and_keyword_middle_table(self, **kwargs):
        '''
        数据插入goods_id_and_keyword_middle_table
        :param kwargs:
        :return:
        '''
        goods_id = str(kwargs['goods_id'])
        keyword_id = int(kwargs['keyword_id'])
        # self.lg.info(goods_id)
        # self.lg.info(keyword_id)
        result = False

        '''先判断中间表goods_id_and_keyword_middle_table是否已新增该关键字的id'''
        # 注意非完整sql语句不用r'', 而直接''
        try:
            _ = self.my_pipeline._select_table(sql_str=kw_select_str_3, params=(goods_id,))
            _ = [i[0] for i in _]
            # pprint(_)
        except Exception:
            self.lg.error('执行中间表goods_id_and_keyword_middle_table是否已新增该关键字的id的sql语句时出错, 跳过给商品加keyword_id')
            return result

        if keyword_id not in _:
            params = (
                goods_id,
                keyword_id,)
            self.lg.info('------>>>| 正在插入keyword_id为{0}, goods_id为{1}'.format(params[1], params[0]))
            result = self.my_pipeline._insert_into_table_2(sql_str=self.add_keyword_id_for_goods_id_sql_str, params=params, logger=self.lg)

        return result

    def _add_keyword_2_db_from_excel_file(self):
        '''
        从excel插入新关键字到db
        :return:
        '''
        excel_file_path = '/Users/afa/Desktop/2018-07-18-淘宝phone-top20万.xlsx'
        self.lg.info('正在读取{0}, 请耐心等待...'.format(excel_file_path))
        try:
            excel_result = read_info_from_excel_file(excel_file_path=excel_file_path)
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)
            return False

        self.lg.info('读取完毕!!')
        self.lg.info('正在读取db中原先的keyword...')
        db_keywords = self.my_pipeline._select_table(sql_str=kw_select_str_4)
        db_keywords = [i[0] for i in db_keywords]
        self.lg.info('db keywords 读取完毕!')

        for item in excel_result:
            keyword = item.get('关键词', None)
            if not keyword:
                continue

            if keyword in db_keywords:
                self.lg.info('该关键字{0}已经存在于db中...'.format(keyword))
                continue

            self.lg.info('------>>>| 正在存储关键字 {0}'.format(keyword))
            self.my_pipeline._insert_into_table_2(sql_str=kw_insert_str_2, params=(str(keyword), 0), logger=self.lg)

        self.lg.info('全部写入完毕!')

        return True

    def __del__(self):
        try:
            del self.lg
            del self.msg
            del self.my_pipeline
        except:
            pass
        try:
            del self.db_existed_goods_id_list
        except:
            pass
        collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        _tmp = GoodsKeywordsSpider()
        # _tmp._add_keyword_2_db_from_excel_file()
        _tmp._just_run()
        collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))
        sleep(60*5)

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')
    daemon_init()
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    just_fuck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        just_fuck_run()