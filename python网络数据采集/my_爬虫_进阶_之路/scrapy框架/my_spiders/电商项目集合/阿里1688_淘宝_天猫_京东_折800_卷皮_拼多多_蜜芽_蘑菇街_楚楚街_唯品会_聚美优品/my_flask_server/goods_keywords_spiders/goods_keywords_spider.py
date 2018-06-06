# coding:utf-8

'''
@author = super_fazai
@File    : goods_keywords_spider.py
@Time    : 2018/6/5 11:40
@connect : superonesfazai@gmail.com
'''
import sys
sys.path.append('..')

from my_requests import MyRequests
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from my_logging import set_logger
from my_utils import (
    daemon_init,
    get_shanghai_time,
)
from taobao_parse import TaoBaoLoginAndParse

from settings import (
    IS_BACKGROUND_RUNNING,
    MY_SPIDER_LOGS_PATH,
    HEADERS,
    TAOBAO_REAL_TIMES_SLEEP_TIME,
)

import gc
from logging import INFO, ERROR
from time import sleep
from json import (
    loads,
    JSONDecodeError,
)

from pprint import pprint
from random import randint
import re

class GoodsKeywordsSpider(object):
    def __init__(self):
        self._set_logger()
        self.msg = ''
        self._init_debugging_api()
        self.debugging_api = self._init_debugging_api()
        self._set_func_name_dict()
        self.my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
        # 插入数据到goods_id_and_keyword_middle_table表
        self.add_keyword_id_for_goods_id_sql_str = r'insert into dbo.goods_id_and_keyword_middle_table(goods_id, keyword_id) VALUES (%s, %s)'

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
            1: True,
            2: True,
            3: True,
            4: True,
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
            sql_str = r'select id, keyword from dbo.goods_keywords where is_delete=0'
            # 获取原先goods_db的所有已存在的goods_id
            sql_str_2 = r'select GoodsID from dbo.GoodsInfoAutoGet'

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

                for type, type_value in self.debugging_api.items():  # 遍历待抓取的电商分类
                    if type_value is False:
                        self.my_lg.info('api为False, 跳过!')
                        continue

                    for item in result:     # 遍历每个关键字
                        self.my_lg.info('正在处理id为{0}, 关键字为 {1} ...'.format(item[0], item[1]))
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
                        sleep(5)

    def _get_keywords_goods_id_list(self, type, keyword):
        '''
        获取goods_id_list
        :param type: 电商种类
        :param keyword:
        :return:
        '''
        if type == 1:
            goods_id_list = self._get_taobao_goods_keywords_goods_id_list(keyword=keyword)
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
            pass
        elif type == 3:
            pass
        elif type == 4:
            pass
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
            'user-agent': HEADERS[randint(0, len(HEADERS)-1)],
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

            data = self.json_str_2_dict(json_str=data)
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

        result = False      # 用于判断某个goods是否被插入的参数
        for item in goods_url_list:     # item为goods_url
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

    def _insert_into_goods_id_and_keyword_middle_table(self, **kwargs):
        '''
        数据插入goods_id_and_keyword_middle_table
        :param kwargs:
        :return:
        '''
        goods_id = kwargs['goods_id']
        keyword_id = kwargs['keyword_id']
        result = False

        '''先判断中间表goods_id_and_keyword_middle_table是否已新增该关键字的id'''
        sql_str = r'select keyword_id from dbo.goods_id_and_keyword_middle_table where goods_id=%s' % str(goods_id)
        try:
            _ = self.my_pipeline._select_table(sql_str=sql_str)
            _ = [i[0] for i in _]
        except Exception:
            self.my_lg.error('执行中间表goods_id_and_keyword_middle_table是否已新增该关键字的id的sql语句时出错, 跳过给商品加keyword_id')
            return result

        if keyword_id not in _:
            params = (
                goods_id,
                keyword_id,
            )
            self.my_lg.info('------>>>| 正在插入keyword_id为{0}, goods_id为{1}'.format(params[1], params[0]))
            result = self.my_pipeline._insert_into_table_2(sql_str=self.add_keyword_id_for_goods_id_sql_str, params=params, logger=self.my_lg)

        return result

    def json_str_2_dict(self, json_str):
        try:
            data = loads(json_str)
        except JSONDecodeError:
            self.my_lg.error('json转换字符串时出错, 请检查!')
            data = {}

        return data

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