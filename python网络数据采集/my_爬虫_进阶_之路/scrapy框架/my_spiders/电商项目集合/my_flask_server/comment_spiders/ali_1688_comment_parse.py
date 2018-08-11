# coding:utf-8

'''
@author = super_fazai
@File    : ali_1688_comment_parse.py
@Time    : 2018/4/9 12:46
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from my_items import CommentItem
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from settings import (
    MY_SPIDER_LOGS_PATH,
    PHANTOMJS_DRIVER_PATH,)

from random import (
    randint,
    choice,
)

import gc
from time import sleep
from logging import INFO, ERROR
from scrapy.selector import Selector
import re, datetime, json
from pprint import pprint
from demjson import decode

from fzutils.log_utils import set_logger
from fzutils.time_utils import (
    get_shanghai_time,
    string_to_datetime,
)
from fzutils.cp_utils import filter_invalid_comment_content
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests
from fzutils.spider.fz_phantomjs import MyPhantomjs
from fzutils.common_utils import json_2_dict

class ALi1688CommentParse(object):
    '''
    阿里1688评论抓取解析类
    '''
    def __init__(self, logger=None):
        super(ALi1688CommentParse, self).__init__()
        self.result_data = {}
        self.msg = ''
        self._set_headers()
        self._set_logger(logger)
        # self.my_phantomjs = MyPhantomjs(executable_path=PHANTOMJS_DRIVER_PATH)
        # 可动态执行的代码
        self._exec_code = '''
        _text = str(self.driver.find_element_by_css_selector('div.tab-item.filter:nth-child(2)').text)
        print(_text)
        assert _text != '四五星(0)', 'my assert error!'    # 通过断言来跳过执行下面的代码

        # 单个element老是定位不到, 就用elements
        # self.driver.find_element_by_css_selector('div.tab-item.filter:nth-child(2)').click() 
        self.driver.find_elements_by_css_selector('div.tab-item')[1].click()
        # if _text == '四五星(0)':
        sleep(3)
        
        # 向下滚动10000像素
        js = 'document.body.scrollTop=10000'
        self.driver.execute_script(js)  # 每划一次，就刷6条
        sleep(4)
        '''
        self._page_sleep_time = 2

    def _get_comment_data(self, goods_id):
        if goods_id == '':
            self.result_data = {}
            return {}
        self.my_lg.info('------>>>| 待处理的goods_id为: %s' % str(goods_id))

        # # 原先采用phantomjs, 改用手机端抓html(speed slow, give up)
        # tmp_url = 'https://m.1688.com/page/offerRemark.htm?offerId=' + str(goods_id)
        # body = self.my_phantomjs.use_phantomjs_to_get_url_body(url=tmp_url, exec_code=self._exec_code)
        # # self.my_lg.info(str(body))
        #
        # if body == '':
        #     self.result_data = {}
        #     self.my_lg.error('该地址的body为空值, 出错地址: ' + tmp_url)
        #     return {}
        #
        # _html_comment_list = list(Selector(text=body).css('div.remark-item').extract())
        # if _html_comment_list != []:
        #     _comment_list = []
        #     for index, item in enumerate(_html_comment_list):
        #         if index > 25:  # 就取前25条评论信息
        #             break
        #
        #         buyer_name = str(Selector(text=item).css('span.member::text').extract_first())
        #         quantify = str(Selector(text=item).css('span.amount::text').extract_first())
        #         try:
        #             quantify = int(re.compile(r'\d+').findall(quantify)[0])
        #         except IndexError:
        #             self.my_lg.error('获取quantify时索引异常! 出错地址: ' + tmp_url)
        #             self.result_data = {}
        #             return {}
        #
        #         comment_date = str(Selector(text=item).css('div.date span::text').extract_first())
        #         comment_date = self._get_comment_date(comment_date)     # str '2017-01-25 17:06:00'
        #         tmp_sku_info = str(Selector(text=item).css('div.date::text').extract_first())
        #
        #         _comment_content = self._wash_comment(str(Selector(text=item).css('div.bd::text').extract_first()))
        #         if not filter_invalid_comment_content(_comment_content):
        #             continue
        #
        #         comment = [{
        #             'comment': _comment_content,
        #             'comment_date': comment_date,                                               # 评论创建日期
        #             'sku_info': re.compile(r'<span.*?</span>').sub('', tmp_sku_info),           # 购买的商品规格
        #             'img_url_list': [],
        #             'star_level': randint(3, 5),                                                # 几星好评
        #             'video': '',
        #         }]
        #
        #         _ = {
        #             'buyer_name': buyer_name,           # 买家昵称
        #             'comment': comment,                 # 评论内容
        #             'quantify': quantify,               # 购买数量
        #             'head_img': '',                     # 用户头像
        #             'append_comment': {},               # 追评
        #         }
        #         _comment_list.append(_)
        #
        #     _t = datetime.datetime.now()
        #
        #     _r = CommentItem()
        #     _r['goods_id'] = str(goods_id)
        #     _r['create_time'] = _t
        #     _r['modify_time'] = _t
        #     _r['_comment_list'] = _comment_list
        #     self.result_data = _r
        #     # pprint(self.result_data)
        #     return self.result_data
        # else:
        #     self.my_lg.error('该商品的comment为空list! 出错地址: ' + tmp_url)
        #     self.result_data = {}
        #     return {}

        '''下面是模拟pc端好评接口'''
        member_id = self._get_this_goods_member_id(goods_id=goods_id)
        self.my_lg.info('------>>>| 获取到的member_id: {0}'.format(member_id))
        if member_id == '':
            self.my_lg.error('获取到的member_id为空值!请检查!')
            self.result_data = {}
            return {}

        # 这里从db获取该商品原先的规格值
        sku_info = self._get_sku_info_from_db(goods_id)
        # self.my_lg.info('sku_info: {0}'.format(sku_info))
        if sku_info == []:
            self.result_data = {}
            return {}

        _comment_list = []
        for page_num in range(1, 4):
            self.my_lg.info('------>>>| 正在抓取第{0}页...'.format(page_num))
            params = self._set_params(goods_id=goods_id, member_id=member_id, page_num=page_num)
            url = 'https://rate.1688.com/remark/offerDetail/rates.json'
            tmp_headers = self.headers
            tmp_headers.update({
                'referer': 'https://detail.1688.com/offer/{0}.html'.format(str(goods_id))
            })
            # 原先用MyRequests老是404，改用phantomjsy也还是老是404
            body = MyRequests.get_url_body(url=url, headers=tmp_headers, params=params)
            # self.my_lg.info(str(body))

            # 用phantomjs
            # url = self._set_url(url=url, params=params)
            # self.my_lg.info(url)
            # body = self.my_phantomjs.use_phantomjs_to_get_url_body(url)
            # try:
            #     body = re.compile('<pre.*?>(.*)</pre>').findall(body)[0]
            # except IndexError:
            #     self.my_lg.error('获取body时索引异常!')
            #     self.result_data = {}
            #     return {}

            if body == '':
                self.result_data = {}
                self.my_lg.error('该地址的body为空值, 出错goods_id: {0}'.format(goods_id))
                return {}

            data = json_2_dict(json_str=body, logger=self.my_lg)
            if data.get('url') is not None:
                self.my_lg.info('------>>>| 被重定向到404页面, 休眠{0}s中...'.format(self._page_sleep_time))
                sleep(self._page_sleep_time)
                break

            # self.my_lg.info(str(body))
            data = data.get('data', {}).get('rates', [])
            # pprint(data)
            if data == []:
                # sleep(self._page_sleep_time)
                break

            try:
                for item in data:
                    buyer_name = item.get('member', '')
                    comment = []
                    for i in item.get('rateItem', []):
                        _comment_content = self._wash_comment(i.get('remarkContent', ''))
                        if not filter_invalid_comment_content(_comment_content):
                            continue

                        comment.append({
                            'comment': _comment_content,
                            'comment_date': str(i.get('remarkTime', '')),    # 评论日期
                            'sku_info': choice(sku_info),  # 购买的商品规格(pc端1688商品没有规格)
                            'star_level': i.get('starLevel', 5),
                            'img_url_list': [],
                            'video': '',
                        })
                    quantify = item.get('quantity', 1)                                  # 购买数量
                    if comment == []:   # 为空不录入
                        continue

                    _ = {
                        'buyer_name': buyer_name,           # 买家昵称
                        'comment': comment,                 # 评论内容
                        'quantify': quantify,               # 购买数量
                        'head_img': '',                     # 用户头像
                        'append_comment': {},               # 追评
                    }
                    _comment_list.append(_)

            except Exception:
                self.result_data = {}
                self.my_lg.error('出错商品goods_id: {0}'.format(goods_id), exc_info=True)
                return {}

            sleep(self._page_sleep_time)

        if _comment_list != []:
            # pprint(_comment_list)
            _t = datetime.datetime.now()

            _r = CommentItem()
            _r['goods_id'] = str(goods_id)
            _r['create_time'] = _t
            _r['modify_time'] = _t
            _r['_comment_list'] = _comment_list
            self.result_data = _r

            return self.result_data
        else:
            self.my_lg.error('出错goods_id: {0}'.format(goods_id))
            self.result_data = {}
            return {}

    def _get_sku_info_from_db(self, goods_id):
        '''
        从db中得到sku_info
        :param goods_id:
        :return:
        '''
        _ = SqlServerMyPageInfoSaveItemPipeline()
        sql_str = 'select SKUInfo from dbo.GoodsInfoAutoGet where GoodsID=%s'
        # sku_info = self.json_2_dict(_._select_table(sql_str=sql_str, params=(str(goods_id),)))
        try:
            _r = _._select_table(sql_str=sql_str, params=(str(goods_id),))[0][0]
            # print(_r)
            sku_info = decode(_r)
        except Exception:
            self.my_lg.error('demjson.decode数据时遇到错误!', exc_info=True)
            return []

        if sku_info == []:
            return ['']
        else:
            return list(set([item.get('spec_type', '').replace('|', ';') for item in sku_info]))

    def _get_this_goods_member_id(self, goods_id):
        '''
        获取member_id
        :param goods_id:
        :return: '' or str
        '''
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_pc_ua(),
            # 'X-DevTools-Emulate-Network-Conditions-Client-Id': '5C1ED6AF76F4F84D961F136EAA06C40F',
        }

        params = (
            ('offerId', str(goods_id)),
        )

        url = 'https://m.1688.com/page/offerRemark.htm'
        body = MyRequests.get_url_body(url=url, headers=headers, params=params)
        # self.my_lg.info(str(body))
        if body == '':
            self.my_lg.error('获取到的body为空值!此处跳过!')
            return ''

        try:
            member_id = re.compile(r'"memberId":"(.*?)",').findall(body)[0]
        except IndexError:
            self.my_lg.error('获取member_id时索引异常!请检查!')
            return ''

        return member_id

    def _wash_comment(self, comment:str):
        '''
        清洗comment
        :param comment:
        :return:
        '''
        comment = re.compile('1688|合作|阿里|阿里巴巴').sub('', comment)
        comment = re.compile('\r|\n|\t').sub(' ', comment)

        return comment

    def _set_headers(self):
        # self.headers = {
        #     # 下面的ali-ss为必要字段
        #     'cookie': 'ali-ss=eyJ1c2VySWQiOm51bGwsImxvZ2luSWQiOm51bGwsInNpZCI6bnVsbCwiZWNvZGUiOm51bGwsIm1lbWJlcklkIjpudWxsLCJzZWNyZXQiOiI5WmZucV96VDl6NDhTOTg4WkNsaFpxSEwiLCJfZXhwaXJlIjoxNTI0MTE5MzI3NDQ5LCJfbWF4QWdlIjo4NjQwMDAwMH0=; ',
        #     'accept-language': 'zh-CN,zh;q=0.9',
        #     'user-agent': get_random_pc_ua(),
        #     'accept': 'application/json, text/javascript, */*; q=0.01',
        #     'referer': 'https://m.1688.com/page/offerRemark.htm?offerId=42735065607',
        #     'x-requested-with': 'XMLHttpRequest',
        # }
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_pc_ua(),
            'accept': '*/*',
            # 'referer': 'https://detail.1688.com/offer/44412151595.html?spm=a2604.8117111.ji00a0ac.3.2e8e3ea73bvZT4',
            'authority': 'rate.1688.com',
            # 其中的ali-ss为必须参数
            'cookie': 'ali-ss=eyJ1c2VySWQiOm51bGwsImxvZ2luSWQiOm51bGwsInNpZCI6bnVsbCwiZWNvZGUiOm51bGwsIm1lbWJlcklkIjpudWxsLCJzZWNyZXQiOiJFOF9XcF9NMWV5QWRKWHBVb1lLTlhaZk8iLCJfZXhwaXJlIjoxNTMxNTM0MTMwODMzLCJfbWF4QWdlIjo4NjQwMDAwMH0=; ali-ss.sig=573tlT1Aed2ggvlhClMHb8sZatbgVlRrIxljURSRZys; JSESSIONID=9L78RXlv1-k80a7jb9VDbOxXoH4H-OW2AexQ-jQ3d; cookie2=10d7bba23bbc61948af48e1dd2611282; t=1bdcbe0b678123e1755897be375b453f; _tb_token_=77fe63e3066b3; _tmp_ck_0=3Oo5x6beKeA77mSeFyI8GT8FHF5re5voELqxVsc%2FfpE4tqj%2B88wXi1tm1CBqsrie3iytT%2FtexS2f1gz4cNHi2Eu4hv7YjQ3LERzyqyHdFPQhvo0xY7gXNGXM9%2FZ1vj7kgF%2FDvB6r3ddV6BnQSr5Z6yrZIruC7DPdfJO0g23ShfLkoDeSB6j7j5l9OOSrQ0hXXsClBhhps89CzdCYLvmRWeOqmbTf1LoCMhMayyk116UUrhNQqpgoaurnG6C1XKdmm1QpNwyCdPzmJxb2%2FhafYOVC8Zmqu9DtlO48topX3Pg9HVynFVMDXBBTq6GYgoVx5rwkN6JkXezXK9RU9OIu3o9TtslpsNTXIwD1NkXOb4mUmH1PDBJ3yvST9GePCQeaxovWab0bwzQ%3D;',
        }

    def _set_logger(self, logger):
        if logger is None:
            self.my_lg = set_logger(
                log_file_name=MY_SPIDER_LOGS_PATH + '/阿里1688/comment/' + str(get_shanghai_time())[0:10] + '.txt',
                console_log_level=INFO,
                file_log_level=ERROR
            )
        else:
            self.my_lg = logger

    def _set_url(self, url, params):
        '''
        得到待抓取的api接口地址
        :param url:
        :param params:
        :return: str
        '''
        _ = [item[0] + '=' + str(item[1]) for item in params]

        return url + '?' + '&'.join(_)

    def _set_params(self, goods_id, member_id, page_num:int):
        '''
        设置params
        :param goods_id:
        :param member_id:
        :param page_num:
        :return:
        '''
        # t = str(int(time.time())) + str(randint(100, 999))
        params = (
            ('_input_charset', 'GBK'),
            ('offerId', str(goods_id)),
            ('page', str(page_num)),
            ('pageSize', '15'),
            ('starLevel', '7'),
            ('orderBy', 'date'),
            ('semanticId', ''),
            ('showStat', '0'),
            ('content', '1'),
            # ('t', t),
            ('memberId', str(member_id)),
            # ('callback', 'jQuery17205914468174705312_1531451658317'),
        )

        return params

    def _get_comment_date(self, comment_date):
        '''
        得到datetime类型的时间
        :param comment_date: eg: 2017-12-04
        :return: datetime
        '''
        _ = str(randint(0, 23))
        if len(_) == 1:
            _hour = '0' + _
        else:
            _hour = _

        _ = str(randint(0, 59))
        if len(_) == 1:
            _min = '0' + _
        else:
            _min = _

        _ = str(randint(0, 59))
        if len(_) == 1:
            _s = '0' + _
        else:
            _s = _

        comment_date = comment_date + ' ' + _hour + ':' + _min + ':' + _s

        return comment_date

    def __del__(self):
        try:
            # del self.my_phantomjs
            del self.my_lg
            del self.msg
        except:
            pass
        gc.collect()


if __name__ == '__main__':
    ali_1688 = ALi1688CommentParse()
    while True:
        goods_id = input('请输入要爬取的商品goods_id(以英文分号结束): ')
        goods_id = goods_id.strip('\n').strip(';')
        ali_1688._get_comment_data(goods_id=goods_id)

        gc.collect()



