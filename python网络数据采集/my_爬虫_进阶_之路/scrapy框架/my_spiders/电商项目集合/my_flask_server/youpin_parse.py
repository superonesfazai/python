# coding:utf-8

'''
@author = super_fazai
@File    : youpin_parse.py
@Time    : 2018/8/13 09:53
@connect : superonesfazai@gmail.com
'''

"""
小米有品常规商品采集解析
"""

import gc
import re
from pprint import pprint
from logging import (
    INFO,
    ERROR,
)
from json import dumps

from settings import (
    MY_SPIDER_LOGS_PATH,
)

from fzutils.log_utils import set_logger
from fzutils.internet_utils import get_random_phone_ua
from fzutils.cp_utils import _get_right_model_data
from fzutils.spider.fz_requests import MyRequests
from fzutils.common_utils import (
    json_2_dict,
    wash_sensitive_info,)
from fzutils.time_utils import (
    get_shanghai_time,)

class YouPinParse(object):
    def __init__(self, logger=None):
        super(YouPinParse, self).__init__()
        self.result_data = {}
        self._set_logger(logger)
        self._set_headers()

    def _set_logger(self, logger):
        if logger is None:
            self.my_lg = set_logger(
                log_file_name=MY_SPIDER_LOGS_PATH + '/小米有品/_/' + str(get_shanghai_time())[0:10] + '.txt',
                console_log_level=INFO,
                file_log_level=ERROR
            )
        else:
            self.my_lg = logger

    def _set_headers(self):
        self.headers = {
            'Origin': 'https://home.mi.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': get_random_phone_ua(),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            # 'Referer': 'https://home.mi.com/detail?gid=101421',
            'DToken': '',
            'Connection': 'keep-alive',
        }

    def _get_target_data(self, **kwargs):
        '''
        获取目标需求数据
        :return:
        '''
        goods_id = kwargs.get('goods_id', '')

        if goods_id == '':
            self.my_lg.error('获取到的goods_id为空值!此处跳过!')
            return self._get_data_error_init()

        # 小米有品m站抓取
        base_url = 'https://home.mi.com/app/shop/pipe'
        # cookies = self._get_cookies()
        post_data = self._get_post_data(goods_id=goods_id)

        m_url = 'https://home.mi.com/detail?gid={0}'.format(goods_id)
        self.my_lg.info('------>>>| 正在抓取小米有品地址为: {0}'.format(m_url))

        write_info = '出错goods_id:{0}, 出错地址: {1}'.format(goods_id, m_url)

        body = MyRequests.get_url_body(method='post', url=base_url, headers=self.headers, cookies=None, data=post_data)
        # self.my_lg.info(str(body))
        if body == '':
            self.my_lg.error('获取到的body为空值!'+write_info)
            return self._get_data_error_init()

        _ = json_2_dict(json_str=body, logger=self.my_lg).get('result', {}).get('detail', {}).get('data', {})
        # pprint(_)
        if _ == {}:
            self.my_lg.error('获取到的data为空dict!'+write_info)
            return self._get_data_error_init()

        try:
            _ = self._wash_target_data(_)
        except Exception:
            self.my_lg.error('清洗数据时出错!'+write_info, exc_info=True)
            self._get_data_error_init()

        # pprint(_)
        data = {}
        try:
            data['title'] = self._wash_sensitive_info(self._get_title(data=_))
            data['sub_title'] = self._wash_sensitive_info(self._get_sub_title(data=_))
            data['shop_name'] = self._get_shop_name(data=_)
            data['all_img_url'] = self._get_all_img_url(data=_)
            data['p_info'] = self._get_p_info(data=_)       # 小米有品无p_info
            data['div_desc'] = self._get_div_desc(data=_)
            data['sell_time'] = {}      # 默认为空
            data['detail_name_list'] = self._get_detail_name_list(data=_.get('group', []))
            data['price_info_list'] = self._get_price_info_list(data=_.get('skuList', []))

        except Exception:
            self.my_lg.error('遇到错误:', exc_info=True)
            self.my_lg.error(write_info)
            return self._get_data_error_init()

        if data != {}:
            self.result_data = data
            return data
        else:
            self.my_lg.info('data为空值')
            return self._get_data_error_init()

    def _handle_target_data(self):
        '''
        处理 and 结构化目标数据
        :return:
        '''
        pass

    def _get_title(self, data):
        title = data.get('good').get('name', '')
        assert title != '', '获取到的name为空值!请检查!'

        return title

    def _get_sub_title(self, data):
        sub_title = data.get('good', {}).get('summary', '')

        return sub_title

    def _get_shop_name(self, data):
        shop_name = data.get('good', {}).get('brand', {}).get('name', '')

        return shop_name

    def _get_all_img_url(self, data):
        all_img_url = data.get('good', {}).get('album', [])
        assert all_img_url != [], '获取到的all_img_url为空list!'

        all_img_url = [{
            'img_url': item
        } for item in all_img_url]

        return all_img_url

    def _get_p_info(self, data):
        p_info = []

        return p_info

    def _get_div_desc(self, data):
        try:
            intros = data.get('good', {}).get('intros', [])[0]
        except IndexError:
            raise IndexError('获取intros获取异常!')

        tabs = intros.get('tabs', [])
        div_desc_url = ''
        for item in tabs:
            if item.get('title', '') == '产品介绍':
                div_desc_url = item.get('url', '')
                break

        if div_desc_url == '':
            raise ValueError('获取div_desc_url为空值!')

        body = MyRequests.get_url_body(url=div_desc_url, headers=self.headers)
        # self.my_lg.info(str(body))
        if body == '':
            raise ValueError('获取到的div_desc为空值!')

        # 处理data-lazy-src
        body = re.compile(r'<img src=').sub('<img data-lazy-src=', body)
        body = re.compile(r'data-lazy-src=').sub('src=', body)
        body = re.compile(r';opacity:0').sub('', body)  # 不替换否则不显示图片
        # print(body)

        div_desc = '<div>' + re.compile(r'<main .*?>.*</main>').findall(body)[0] + '</div>'
        # self.my_lg.info(str(div_desc))

        return div_desc

    def _get_detail_name_list(self, data):
        detail_name_list = []
        for item in data:
            if item.get('name') is None:
                return []
            else:
                detail_name_list.append({
                    'spec_name': item.get('name')
                })

        return detail_name_list

    def _get_price_info_list(self, data):
        pass

    def _wash_sensitive_info(self, target_str):
        '''
        清洗敏感信息
        :param target_str:
        :return:
        '''
        add_sensitive_str_list = [
            '小米有品',
        ]
        target_str = wash_sensitive_info(data=target_str, replace_str_list=[], add_sensitive_str_list=add_sensitive_str_list)

        return target_str

    def _wash_target_data(self, data):
        '''
        清洗数据
        :return:
        '''
        try:
            data['comment'] = {}
            data['service'] = []        # 发货售后
        except:
            pass

        tmp_activitys = data.get('good', {}).get('activitys', {})
        activitys = {}
        try:
            for key ,value in tmp_activitys.items():
                value = json_2_dict(value, logger=self.my_lg)
                activitys.update({
                    key: value,
                })
        except Exception as e:
            raise e

        data['good']['activitys'] = activitys

        return data

    def _get_post_data(self, **kwargs):
        goods_id = kwargs.get('goods_id', '')

        data_content = {
            'detail': {
                'model': 'Shopv2',
                'action': 'getDetail',
                'parameters': {
                    'gid': goods_id,
                }
            },
            'comment': {
                'model': 'Comment',
                'action': 'getList',
                'parameters': {
                    'goods_id': goods_id,
                    'orderby': '1',
                    'pageindex': '0',
                    'pagesize': 3,
                }
            },
            'activity': {
                'model': 'Activity',
                'action': 'getAct',
                'parameters': {
                    'gid': goods_id,
                }
            }
        }

        data = [
            ('data', dumps(data_content)),
        ]

        return data

    def _get_cookies(self):
        cookies = {
            '__utma': '127562001.1619662154.1533619468.1533619468.1533619468.1',
            '__utmz': '127562001.1533619468.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
            'youpindistinct_id': '16530eabfba59a-090b42a83ad5b4-34677908',
            'Hm_lvt_3d0145da4163eae34eb5e5c70dc07d97': '1534124030',
            'Hm_lpvt_3d0145da4163eae34eb5e5c70dc07d97': '1534124120',
            'youpin_sessionid': '16530ed9b60-0e4f922ba9d498-27ba',
            'mjclient': 'm',
        }

        return cookies

    def _get_data_error_init(self):
        self.result_data = {}
        return {}

    def _get_goods_id_from_url(self, yp_url):
        '''
        得到goods_id
        :param yp_url:
        :return:
        '''
        yp_url = yp_url.replace('http://', 'https://')
        is_yp_url = re.compile(r'https://youpin.mi.com/detail.*?').findall(yp_url)
        if is_yp_url != []:
            try:
                goods_id = re.compile(r'gid=(\d+)').findall(yp_url)[0]
            except IndexError:
                self.my_lg.error('获取goods_id时索引异常! 出错地址:{0}'.format(yp_url))
                return ''

            self.my_lg.info('------>>>| 得到的小米有品商品的goods_id为: {0}'.format(goods_id))
            return goods_id

        else:
            self.my_lg.info('小米有品商品url错误, 非正规的url, 请参照格式(https://youpin.mi.com/detail)开头的...')
            return ''

    def __del__(self):
        try:
            del self.my_lg
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    yp = YouPinParse()
    while True:
        kaola_url = input('请输入待爬取的严选商品地址: ')
        kaola_url.strip('\n').strip(';')
        goods_id = yp._get_goods_id_from_url(kaola_url)
        yp._get_target_data(goods_id=goods_id)
        yp = yp._handle_target_data()
        # pprint(data)