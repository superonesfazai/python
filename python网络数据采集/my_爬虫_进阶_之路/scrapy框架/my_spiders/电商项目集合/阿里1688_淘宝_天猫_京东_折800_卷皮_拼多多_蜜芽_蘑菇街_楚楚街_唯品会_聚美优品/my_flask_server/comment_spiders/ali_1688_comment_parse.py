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
# from my_requests import MyRequests
from my_logging import set_logger
from my_utils import get_shanghai_time, string_to_datetime
from settings import HEADERS, MY_SPIDER_LOGS_PATH

from random import randint
import gc
from logging import INFO, ERROR
from scrapy.selector import Selector
import re, datetime, json
from pprint import pprint

class ALi1688CommentParse(object):
    def __init__(self, logger=None):
        super().__init__()
        self.result_data = {}
        self.msg = ''
        if logger is None:
            self.my_lg = set_logger(
                log_file_name=MY_SPIDER_LOGS_PATH + '/阿里1688/comment/' + str(get_shanghai_time())[0:10] + '.txt',
                console_log_level=INFO,
                file_log_level=ERROR
            )
        else:
            self.my_lg = logger
        self.my_phantomjs = MyPhantomjs()
        # 可动态执行的代码
        self._exec_code = '''
        self.driver.find_element_by_css_selector('div.tab-item.filter:nth-child(2)').click() 
        sleep(1.5)
        # 向下滚动10000像素
        js = 'document.body.scrollTop=10000'
        self.driver.execute_script(js)
        sleep(3)
        '''
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': HEADERS[randint(0, len(HEADERS)-1)],
            'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'referer': 'https://detail.1688.com/offer/45579899125.html',
        }
        self.page_size = '30'

    def _get_comment_data(self, goods_id):
        if goods_id == '':
            self.result_data = {}
            return {}

        '''
        原先采用phantomjs, 改用pc端抓包到的接口
        '''
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
                comment_date = self._get_comment_date(comment_date)
                tmp_sku_info = str(Selector(text=item).css('div.date::text').extract_first())
                comment = [{
                    'comment': str(Selector(text=item).css('div.bd::text').extract_first()),
                    'comment_date': comment_date,                                               # 评论创建日期
                    'sku_info': re.compile(r'<span.*?</span>').sub('', tmp_sku_info),           # 购买的商品规格
                    'img_url_list': [],
                    'star_level': randint(3, 5),                                                # 几星好评
                }]

                _ = {
                    'buyer_name': buyer_name,           # 买家昵称
                    'comment': comment,                 # 评论内容
                    'quantify': quantify                # 购买数量
                }
                _comment_list.append(_)

            self.result_data = {
                'goods_id': str(goods_id),
                'modify_time': datetime.datetime.now(),
                '_comment_list': _comment_list,
            }
            pprint(self.result_data)
            return self.result_data
        else:
            self.my_lg.error('该商品的comment为空list! 出错地址: ' + tmp_url)
            self.result_data = {}
            return {}

        # 下面是模拟pc端接口的
        # tmp_url = 'https://rate.1688.com/remark/offerDetail/rates.json'
        # _params = self._set_params(goods_id=goods_id)
        #
        # # 常规requests获取不到数据改用phantomjs
        # # body = MyRequests.get_url_body(url=tmp_url, headers=self.headers, params=_params)
        #
        # _url = self._set_url(url=tmp_url, params=_params)
        # print(_url)
        # body = self.my_phantomjs.use_phantomjs_to_get_url_body(url=_url)
        # self.my_lg.info(str(body))
        # if body == '':
        #     self.result_data = {}
        #     self.my_lg.error('该地址的body为空值, 出错goods_id: ' + goods_id)
        #     return {}
        # try:
        #     body = re.compile('<pre.*?>(.*)</pre>').findall(body)[0]
        # except IndexError:
        #     self.result_data = {}
        #     self.my_lg.error('re筛选body为空[], 出错goods_id: ' + goods_id)
        #     return {}
        #
        # data = self.json_str_2_dict(json_str=body).get('data', {}).get('rates', [])
        # # pprint(data)
        # _comment_list = []
        # try:
        #     for item in data:
        #         buyer_name = item.get('member', '')
        #         comment = [{
        #             'comment': i.get('remarkContent', ''),
        #             'comment_date': string_to_datetime(i.get('remarkTime', '')),    # 评论日期
        #             'star_level': i.get('starLevel', 5),
        #             'sku_info': '',                                                 # 购买的商品规格(pc端1688商品没有规格)
        #             'img_url_list': [],
        #         } for i in item.get('rateItem', [])]
        #         quantify = item.get('quantity', 1)                                  # 购买数量
        #
        #         _ = {
        #             'buyer_name': buyer_name,           # 买家昵称
        #             'comment': comment,                 # 评论内容
        #             'quantify': quantify                # 购买数量
        #         }
        #         _comment_list.append(_)
        #
        # except Exception as e:
        #     self.result_data = {}
        #     self.my_lg.error('出错商品goods_id: ' + goods_id)
        #     self.my_lg.exception(e)
        #     return {}
        #
        # self.result_data = {
        #     'goods_id': str(goods_id),
        #     'modify_time': datetime.datetime.now(),
        #     '_comment_list': _comment_list,
        # }
        # pprint(self.result_data)
        # return self.result_data

    def _set_url(self, url, params):
        '''
        得到待抓取的api接口地址
        :param url:
        :param params:
        :return: str
        '''
        _ = [item[0] + '=' + str(item[1]) for item in params]

        return url + '?' + '&'.join(_)

    def _set_params(self, goods_id):
        '''
        设置params
        :param goods_id:
        :return:
        '''
        params = (
            ('_input_charset', 'GBK'),
            ('offerId', goods_id),
            ('page', '1'),
            ('pageSize', self.page_size),   # 一个页面返回的comment数量
            ('starLevel', '7'),
            ('orderBy', 'date'),
            # ('semanticId', ''),
            ('showStat', '0'),
            ('content', '1'),
            # ('t', '1523264528741'),
            ('memberId', 'zhangchenghao2009'),
            # ('callback', 'jQuery1720041881430222992844_1523264353082'),
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

        return string_to_datetime(comment_date)

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
        goods_id = ali_1688._get_comment_data(goods_id=goods_id)

        gc.collect()



