# coding:utf-8

'''
@author = super_fazai
@File    : zhe_800_comment_parse.py
@Time    : 2018/5/4 10:27
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from my_items import CommentItem
from settings import MY_SPIDER_LOGS_PATH

from random import randint
from time import sleep
import gc
from logging import INFO, ERROR
import re, datetime, json
from pprint import pprint

from fzutils.log_utils import set_logger
from fzutils.time_utils import (
    get_shanghai_time,
)
from fzutils.cp_utils import filter_invalid_comment_content
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests
from fzutils.common_utils import json_2_dict

class Zhe800CommentParse(object):
    def __init__(self, logger=None):
        super().__init__()
        self.result_data = {}
        self.msg = ''
        self._set_logger(logger=logger)
        self._set_headers()
        self.page_size = '20'  # 固定值
        self.comment_page_switch_sleep_time = 1.5  # 评论下一页sleep time

    def _set_logger(self, logger):
        '''
        设置logger
        :param logger:
        :return:
        '''
        if logger is None:
            self.my_lg = set_logger(
                log_file_name=MY_SPIDER_LOGS_PATH + '/折800/comment/' + str(get_shanghai_time())[0:10] + '.txt',
                console_log_level=INFO,
                file_log_level=ERROR
            )
        else:
            self.my_lg = logger

    def _set_headers(self):
        '''
        设置headers
        :return: dict
        '''
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_pc_ua(),
            'accept': 'application/json, text/plain, */*',
            'referer': 'https://th5.m.zhe800.com/h5/comment/list?zid=ze180424214500488079&dealId=39890410&tagId=',
            # 'cookie': 'gr_user_id=84b21fed-0302-46e0-a01a-f8f3d4cb223e; session_id=439012875.1524042625; user_id=; utm_csr_first=direct; utm_csr=direct; utm_ccn=notset_c0; utm_cmd=; utm_ctr=; utm_cct=; utm_etr=tao.home; firstTime=2018-04-20; __utmz=148564220.1524192137.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); qd_user=96713570.1524192142912; frequency=1%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0; lastTime=2018-04-28; unix_time=1524881786; ju_version=0; __utma=148564220.212449404.1524192137.1524208015.1524881786.3; __utmc=148564220; cart_mark=1%7C0%7C0%7Cnil%7C0; user_type=0; user_role=4; student=0; dialog_time=2; downloadGuide_config=%257B%25220direct%2522%253A%257B%2522open%2522%253A2%257D%252C%25221002direct%2522%253A%257B%2522open%2522%253A1%257D%257D; f_jk_r=https://m.zhe800.com/mz/list/wireless3982; source=; platform=; version=; channelId=; deviceId=; userId=; cType=; cId=; dealId=; f_jk=6628971525400935425TfActXWw; f_jk_t=1525400935426; f_jk_e_t=1527992935; jk=6628971525400935425TfActXWw; wris_session_id=1145460586.1525400937; visit=18',
        }

    def _get_comment_data(self, goods_id):
        if goods_id == '':
            self.result_data = {}
            return {}
        _tmp_comment_list = []
        self.my_lg.info('------>>>| 待抓取的goods_id: %s' % goods_id)

        '''
        下面是抓取m.zhe800.com的数据地址
        '''
        for current_page_num in range(1, 4):    # 起始页为1
            self.my_lg.info('------>>>| 正在抓取第%s页评论...' % str(current_page_num))
            tmp_url = 'https://th5.m.zhe800.com/app/detail/comment/list'
            _params = self._set_params(current_page_num=current_page_num, goods_id=goods_id)

            self.headers.update({
                'referer': 'https://th5.m.zhe800.com/h5/comment/list?zid={0}&dealId=39890410&tagId='.format(str(goods_id))
            })
            body = MyRequests.get_url_body(url=tmp_url, headers=self.headers, params=_params, encoding='utf-8')
            # self.my_lg.info(str(body))

            data = json_2_dict(json_str=body, logger=self.my_lg)
            # pprint(data)

            if data.get('comments') is not None:
                _tmp_comment_list += data.get('comments')

            # print(type(data.get('hasNext')))    # <class 'bool'>
            if not data.get('hasNext', False):     # 先判断是否下页还有评论信息
                break

            if data.get('comments') is None and data.get('hasNext') is None:    # 默认为空，如果下页没有的话，但是上面已经进行下页判断，此处加这个用于异常退出
                self.my_lg.error('获取到的data为None, 出错goods_id: ' + goods_id)
                self.result_data = {}
                return {}

            sleep(self.comment_page_switch_sleep_time)

        # self.my_lg.info(str(len(_tmp_comment_list)))
        try:
            _comment_list = self._get_comment_list(_tmp_comment_list=_tmp_comment_list)
        except Exception as e:
            self.my_lg.error('出错goods_id: ' + goods_id)
            self.my_lg.exception(e)
            self.result_data = {}
            return {}

        _t = datetime.datetime.now()

        _r = CommentItem()
        _r['goods_id'] = str(goods_id)
        _r['create_time'] = _t
        _r['modify_time'] = _t
        _r['_comment_list'] = _comment_list
        self.result_data = _r
        # pprint(self.result_data)

        return self.result_data

    def _get_comment_list(self, _tmp_comment_list):
        '''
        获取规范化的comment结果集
        :param _tmp_comment_list:
        :return:
        '''
        _comment_list = []
        for item in _tmp_comment_list:
            comment_date = item.get('createTime', '')
            assert comment_date != '', '得到的comment_date为空str!请检查!'
            comment_date = self._get_comment_date(comment_date)

            buyer_name = item.get('nickname', '')
            assert buyer_name != '', '得到的用户昵称为空值!请检查!'

            _comment_content = item.get('content', '')
            assert _comment_content != '', '得到的评论内容为空str!请检查!'
            _comment_content = self._wash_comment(comment=_comment_content)

            sku_info = item.get('skuDesc', '')
            # self.my_lg.info(sku_info)
            # 存在规格为空的
            # assert sku_info != '', '得到的sku_info为空str!请检查!'
            sku_info = self._wash_sku_info(sku_info)

            # 第一次评论照片
            img_url_list = item.get('firstEvidences', [])
            # self.my_lg.info(img_url_list)
            if img_url_list is None:
                img_url_list = []
            else:
                img_url_list = [{
                    'img_url': _i.get('big', '')
                } for _i in img_url_list]

            '''追评'''
            append_comment = {}
            if item.get('appendTime', '') == '':    # 追评时间为空即表示无追评
                pass
            else:
                _tmp_append_comment_content = item.get('append', '')
                # 追评的图片
                _append_comment_img_list = [{'img_url': img.get('big', '')} for img in item.get('appendEvidences')] if item.get('appendEvidences') is not None else []
                # self.my_lg.info(_append_comment_img_list)

                append_comment = {
                    'comment_date': item.get('appendTime', ''),
                    'comment': self._wash_comment(_tmp_append_comment_content),
                    'img_url_list': _append_comment_img_list,
                }

            # 购买数量, 随机
            quantify = randint(1, 2)

            # 用户头像, 默认留空
            head_img = ''

            # 评论星级
            star_level = int(item.get('levelStar', 5))

            if not filter_invalid_comment_content(_comment_content):
                continue

            comment = [{
                'comment': _comment_content,
                'comment_date': comment_date,
                'sku_info': sku_info,
                'img_url_list': img_url_list,
                'star_level': star_level,
                'video': '',
            }]

            _ = {
                'buyer_name': buyer_name,  # 买家昵称
                'comment': comment,  # 评论内容
                'quantify': quantify,  # 购买数量
                'head_img': head_img,  # 头像
                'append_comment': append_comment,  # 追评
            }

            _comment_list.append(_)

        return _comment_list

    def _wash_comment(self, comment):
        '''
        清洗评论
        :param sku_info:
        :return:
        '''
        comment = re.compile('折800|zhe800|ZHE800').sub('', comment)

        return comment

    def _get_comment_date(self, comment_date:str):
        '''
        得到规范化的时间信息
        :param comment_date:
        :return: str 格式: 2017-05-26 09:00:00
        '''
        comment_date = comment_date.replace('.', '-')

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

        return comment_date + ' ' + _hour + ':' + _min + ':' + _s

    def _wash_sku_info(self, sku_info):
        sku_info = sku_info.replace('&nbsp;', ' ').replace('&nbsp', ' ')
        sku_info = re.compile('zhe800|折800|ZHE800').sub('', sku_info)

        return sku_info

    def _set_params(self, current_page_num, goods_id):
        '''
        设置params
        :param current_page_num:
        :param goods_id:
        :return:
        '''
        params = (
            ('productId', str(goods_id)),
            ('tagId', ''),
            ('page', str(current_page_num)),
            ('perPage', self.page_size),
        )

        return params

    def __del__(self):
        try:
            del self.my_lg
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    taobao = Zhe800CommentParse()
    while True:
        goods_id = input('请输入要爬取的商品goods_id(以英文分号结束): ')
        goods_id = goods_id.strip('\n').strip(';')
        taobao._get_comment_data(goods_id=goods_id)

        gc.collect()