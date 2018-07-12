# coding:utf-8

'''
@author = super_fazai
@File    : ali_1688_comment_parse.py
@Time    : 2018/4/9 12:46
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from my_phantomjs import MyPhantomjs
from my_requests import MyRequests
from my_logging import set_logger
from my_utils import (
    get_shanghai_time,
    string_to_datetime,
    filter_invalid_comment_content,
)
from my_items import CommentItem
from settings import HEADERS, MY_SPIDER_LOGS_PATH

from random import randint
import gc, time
from time import sleep
from logging import INFO, ERROR
from scrapy.selector import Selector
import re, datetime, json
from pprint import pprint

class ALi1688CommentParse(object):
    '''
    阿里1688评论抓取解析类
    '''
    def __init__(self, logger=None):
        super().__init__()
        self.result_data = {}
        self.msg = ''
        self._set_headers()
        self._set_logger(logger)
        self.my_phantomjs = MyPhantomjs()
        # 可动态执行的代码
        self._exec_code = '''
        self.driver.find_element_by_css_selector('div.tab-item.filter:nth-child(2)').click() 
        _text = str(self.driver.find_element_by_css_selector('div.tab-item.filter:nth-child(2)').text)
        print(_text)
        # if _text == '四五星(0)':
        assert _text != '四五星(0)', 'my assert error!'    # 通过断言来跳过执行下面的代码
        sleep(2.5)
        # 向下滚动10000像素
        js = 'document.body.scrollTop=10000'
        self.driver.execute_script(js)  # 每划一次，就刷6条
        sleep(4)
        '''
        self._page_sleep_time = 1.2

    def _get_comment_data(self, goods_id):
        if goods_id == '':
            self.result_data = {}
            return {}
        self.my_lg.info('------>>>| 待处理的goods_id为: %s' % str(goods_id))

        # 原先采用phantomjs, 改用pc端抓包到的接口(speed slow, give up)
        tmp_url = 'https://m.1688.com/page/offerRemark.htm?offerId=' + str(goods_id)
        body = self.my_phantomjs.use_phantomjs_to_get_url_body(url=tmp_url, exec_code=self._exec_code)
        # self.my_lg.info(str(body))

        if body == '':
            self.result_data = {}
            self.my_lg.error('该地址的body为空值, 出错地址: ' + tmp_url)
            return {}

        _html_comment_list = list(Selector(text=body).css('div.remark-item').extract())
        if _html_comment_list != []:
            _comment_list = []
            for index, item in enumerate(_html_comment_list):
                if index > 25:  # 就取前25条评论信息
                    break

                buyer_name = str(Selector(text=item).css('span.member::text').extract_first())
                quantify = str(Selector(text=item).css('span.amount::text').extract_first())
                try:
                    quantify = int(re.compile(r'\d+').findall(quantify)[0])
                except IndexError:
                    self.my_lg.error('获取quantify时索引异常! 出错地址: ' + tmp_url)
                    self.result_data = {}
                    return {}

                comment_date = str(Selector(text=item).css('div.date span::text').extract_first())
                comment_date = self._get_comment_date(comment_date)     # str '2017-01-25 17:06:00'
                tmp_sku_info = str(Selector(text=item).css('div.date::text').extract_first())

                _comment_content = self._wash_comment(str(Selector(text=item).css('div.bd::text').extract_first()))
                if not filter_invalid_comment_content(_comment_content):
                    continue

                comment = [{
                    'comment': _comment_content,
                    'comment_date': comment_date,                                               # 评论创建日期
                    'sku_info': re.compile(r'<span.*?</span>').sub('', tmp_sku_info),           # 购买的商品规格
                    'img_url_list': [],
                    'star_level': randint(3, 5),                                                # 几星好评
                    'video': '',
                }]

                _ = {
                    'buyer_name': buyer_name,           # 买家昵称
                    'comment': comment,                 # 评论内容
                    'quantify': quantify,               # 购买数量
                    'head_img': '',                     # 用户头像
                    'append_comment': {},               # 追评
                }
                _comment_list.append(_)

            _t = datetime.datetime.now()

            _r = CommentItem()
            _r['goods_id'] = str(goods_id)
            _r['create_time'] = _t
            _r['modify_time'] = _t
            _r['_comment_list'] = _comment_list
            self.result_data = _r
            # pprint(self.result_data)
            return self.result_data
        else:
            self.my_lg.error('该商品的comment为空list! 出错地址: ' + tmp_url)
            self.result_data = {}
            return {}

        # 下面是模拟手机端好评接口
        # _comment_list = []
        # for page_num in range(1, 4):
        #     tmp_url = 'https://m.1688.com/page/offerRemark.htm'
        #     _params = self._set_params(goods_id=goods_id, page_num=page_num)
        #
        #     body = MyRequests.get_url_body(url=tmp_url, headers=self.headers, params=_params)
        #
        #     _url = self._set_url(url=tmp_url, params=_params)
        #     # print(_url)
        #     # self.my_lg.info(str(body))
        #     if body == '':
        #         self.result_data = {}
        #         self.my_lg.error('该地址的body为空值, 出错goods_id: ' + goods_id)
        #         return {}
        #
        #     data = self.json_str_2_dict(json_str=body).get('data', {}).get('model', [])
        #     pprint(data)
        #     try:
        #         for item in data:
        #             buyer_name = item.get('member', '')
        #             comment = [{
        #                 'comment': i.get('remarkContent', ''),
        #                 'comment_date': string_to_datetime(i.get('remarkTime', '')),    # 评论日期
        #                 'star_level': i.get('starLevel', 5),
        #                 'sku_info': '',                                                 # 购买的商品规格(pc端1688商品没有规格)
        #                 'img_url_list': [],
        #             } for i in item.get('rateItem', [])]
        #             quantify = item.get('quantity', 1)                                  # 购买数量
        #
        #             _ = {
        #                 'buyer_name': buyer_name,           # 买家昵称
        #                 'comment': comment,                 # 评论内容
        #                 'quantify': quantify                # 购买数量
        #             }
        #             _comment_list.append(_)
        #
        #     except Exception as e:
        #         self.result_data = {}
        #         self.my_lg.error('出错商品goods_id: ' + goods_id)
        #         self.my_lg.exception(e)
        #         return {}
        #     sleep(self._page_sleep_time)
        #
        # pprint(_comment_list)
        # self.result_data = {
        #     'goods_id': str(goods_id),
        #     'modify_time': datetime.datetime.now(),
        #     '_comment_list': _comment_list,
        # }
        # pprint(self.result_data)
        # return self.result_data

    def _wash_comment(self, comment:str):
        '''
        清洗comment
        :param comment:
        :return:
        '''
        comment = re.compile('阿里巴巴').sub('', comment)
        comment = re.compile('1688|合作|阿里').sub('', comment)

        return comment

    def _set_headers(self):
        self.headers = {
            # 下面的ali-ss为必要字段
            'cookie': 'ali-ss=eyJ1c2VySWQiOm51bGwsImxvZ2luSWQiOm51bGwsInNpZCI6bnVsbCwiZWNvZGUiOm51bGwsIm1lbWJlcklkIjpudWxsLCJzZWNyZXQiOiI5WmZucV96VDl6NDhTOTg4WkNsaFpxSEwiLCJfZXhwaXJlIjoxNTI0MTE5MzI3NDQ5LCJfbWF4QWdlIjo4NjQwMDAwMH0=; ',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': HEADERS[randint(0, len(HEADERS) - 1)],
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'referer': 'https://m.1688.com/page/offerRemark.htm?offerId=42735065607',
            'x-requested-with': 'XMLHttpRequest',
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

    def _set_params(self, goods_id, page_num:int):
        '''
        设置params
        :param goods_id:
        :param page_num:
        :return:
        '''
        data = json.dumps({
            'data': {
                'offerId': goods_id,
                # 'receiveUserId': 2318703732,
                'starLevel': 7,
                'itemId': int(goods_id),
                'bizType': 'trade',
                'page': page_num,
                'pageSize': 5,
            }
        })

        params = (
            ('_csrf', 'xMrEnTz7-VByOlidz0AzkXFg_ifMZBv6bCA0'),
            ('__wing_navigate_type', 'view'),
            ('__wing_navigate_url', 'detail:modules/offerRemarkList/view'),
            # ('__wing_navigate_options', '{"data":{"offerId":"42735065607","receiveUserId":2318703732,"starLevel":7,"itemId":42735065607,"bizType":"trade","page":1,"pageSize":5}}'),
            ('__wing_navigate_options', data),
            ('_', str(time.time().__round__()) + str(randint(100, 999))),
        )

        return params

    def json_str_2_dict(self, json_str):
        '''
        json字符串转dict
        :param json_str:
        :return:
        '''
        try:
            data = json.loads(json_str)
        except:
            self.my_lg.error('json.loads转换json_str时出错!请检查!')
            data = {}

        return data

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
            del self.my_phantomjs
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



