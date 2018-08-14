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
    get_shanghai_time,
    datetime_to_timestamp,
    string_to_datetime,)

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
            data['price_info_list'] = self._get_price_info_list(data=_)
            data['price'], data['taobao_price'] = self._get_price_and_taobao_price(
                price_info_list=data['price_info_list']
            )
            if data['price'] == 0 or data['taobao_price'] == 0:     # 售罄商品处理
                data['is_delete'] = 1
            else:
                data['is_delete'] = self._get_is_delete(price_info_list=data['price_info_list'], data=data, other=_)


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
        data = self.result_data
        if data != {}:
            # 店铺名称
            shop_name = data['shop_name']
            # 掌柜
            account = ''
            # 商品名称
            title = data['title']
            # 子标题
            sub_title = data['sub_title']

            # 商品标签属性名称
            detail_name_list = data['detail_name_list']

            # 要存储的每个标签对应规格的价格及其库存
            price_info_list = data['price_info_list']

            # 所有示例图片地址
            all_img_url = data['all_img_url']

            # 详细信息标签名对应属性
            p_info = data['p_info']
            # pprint(p_info)

            # div_desc
            div_desc = data['div_desc']

            is_delete = data['is_delete']

            # 上下架时间
            if data.get('sell_time', {}) != {}:
                schedule = [{
                    'begin_time': data.get('sell_time', {}).get('begin_time', ''),
                    'end_time': data.get('sell_time', {}).get('end_time', ''),
                }]
            else:
                schedule = []

            # 销售总量
            all_sell_count = ''

            # 商品价格和淘宝价
            price, taobao_price = data['price'], data['taobao_price']

            result = {
                'shop_name': shop_name,                 # 店铺名称
                'account': account,                     # 掌柜
                'title': title,                         # 商品名称
                'sub_title': sub_title,                 # 子标题
                'price': price,                         # 商品价格
                'taobao_price': taobao_price,           # 淘宝价
                # 'goods_stock': goods_stock,               # 商品库存
                'detail_name_list': detail_name_list,   # 商品标签属性名称
                # 'detail_value_list': detail_value_list,   # 商品标签属性对应的值
                'price_info_list': price_info_list,     # 要存储的每个标签对应规格的价格及其库存
                'all_img_url': all_img_url,             # 所有示例图片地址
                'p_info': p_info,                       # 详细信息标签名对应属性
                'div_desc': div_desc,                   # div_desc
                'schedule': schedule,                   # 商品特价销售时间段
                'all_sell_count': all_sell_count,       # 销售总量
                'is_delete': is_delete                  # 是否下架
            }
            # pprint(result)
            # print(result)
            # wait_to_send_data = {
            #     'reason': 'success',
            #     'data': result,
            #     'code': 1
            # }
            # json_data = json.dumps(wait_to_send_data, ensure_ascii=False)
            # print(json_data)
            self.result_data = {}
            return result

        else:
            self.my_lg.error('待处理的data为空的dict, 该商品可能已经转移或者下架')

            return self._get_data_error_init()

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
        # pprint(tabs)
        div_desc_url = ''
        title_list = [
            '功能详情',
            '产品介绍',
            '概述',
            '商品详情',
        ]
        for item in tabs:
            if item.get('title', '') in title_list:
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

        try:
            main_body = re.compile(r'<main .*?>(.*)</main>').findall(body)[0]
        except IndexError:
            main_body = re.compile(r'<body>(.*?)<script src=').findall(body)[0]

        div_desc = '<div>' + main_body + '</div>'
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
        origin_group = data.get('group', [])
        origin_props = data.get('props', [])
        tag_prop = data.get('tag_prop', [])

        # had_size = False
        # group = []
        # size_name_list = ['尺寸', '尺寸大小']
        # for item in origin_group:
        #     children = []
        #     # self.my_lg.info(str(item))
        #     if item.get('name', '') in size_name_list:  # 单独处理属性有尺寸的
        #         had_size = True
        #     for i in item.get('tags', []):
        #         children.append(i.get('name'))
        #     group.append(children)
        # pprint(group)     # group eg: [['藏青色', '黑色'], ['165/88A', '170/92A', '175/96A']]

        group = []
        for item in origin_group:
            children = []
            # self.my_lg.info(str(item))
            for i in item.get('tags', []):
                children.append({
                    'tid': i.get('tid'),
                    'name': i.get('name'),
                })
            group.append(children)
        # pprint(group)

        price_info_list = []
        # pprint(origin_props)
        for item in origin_props:   # TODO 小米有品pc官网显示商品有bug, 会出现规格显示, 实际提示无法购买(不友好), m站直接显示已告罄
            if not item.get('onsale'):  # True or False
                continue
            '''获取spec_value'''
            # 方案1: 自己找规律拼接成spec_value, 错误较多
            # name = item.get('name', '')
            # # self.my_lg.info(name)
            # spec_value_list = []
            # for i in group:
            #     for spec_value in i:    # spec_value eg: '黑色'
            #         if spec_value in name:
            #             spec_value_list.append(spec_value)
            #         else:
            #             if had_size:        # 单独处理属性中有尺寸的
            #                 try:
            #                     size_num = re.compile('\d+.{0,1}\d+').findall(name)[0]
            #                     # self.my_lg.info(str(size_num))
            #                 except IndexError:
            #                     continue
            #                 if size_num in spec_value:
            #                     spec_value_list.append(spec_value)
            #                 else:
            #                     pass
            #             else:
            #                 pass
            # # self.my_lg.info(str(spec_value_list))

            # 方案2: 根据官方查找属性方式
            pid = item.get('pid', '')
            tid_list = list(set([i.get('tid', '') for i in tag_prop if i.get('pid') == pid]))

            spec_value_list = []
            for i in group:
                for k in i:
                    if k.get('tid', '') in tid_list:
                        spec_value_list.append(k.get('name', ''))
            spec_value = ''
            if spec_value_list != []:
                spec_value = '|'.join(spec_value_list)

            img_url = item.get('img', '')
            detail_price = str(float(item.get('price', ''))/100)
            normal_price = str(float(item.get('market_price', ''))/100)
            account_limit_buy_count = int(item.get('buy_limit', 5))
            rest_number = int(item.get('inventory', '0'))
            if rest_number == 0:
                continue

            price_info_list.append({
                'spec_value': spec_value,
                'img_url': img_url,
                'detail_price': detail_price,
                'normal_price': normal_price,
                'account_limit_buy_count': account_limit_buy_count,
                'rest_number': rest_number,
            })

        return price_info_list

    def _get_price_and_taobao_price(self, price_info_list):
        # pprint(price_info_list)
        if price_info_list == []:   # 售罄商品处理
            return 0, 0

        try:
            tmp_price_list = sorted([round(float(item.get('detail_price', '')), 2) for item in price_info_list])
            price = tmp_price_list[-1]  # 商品价格
            taobao_price = tmp_price_list[0]  # 淘宝价
        except IndexError:
            raise IndexError('获取price, taobao_price时索引异常!请检查!')

        return price, taobao_price

    def _get_is_delete(self, price_info_list, data, other):
        is_delete = 0
        all_rest_number = 0
        if price_info_list != []:
            for item in price_info_list:
                all_rest_number += item.get('rest_number', 0)
            if all_rest_number == 0:
                is_delete = 1
        else:
            is_delete = 1

        # 当官方下架时间< 当前时间戳 则商品已下架 is_delete = 1
        if data['sell_time'] != {}:
            end_time = datetime_to_timestamp(string_to_datetime(data.get('sell_time', {}).get('end_time', '')))
            if end_time < datetime_to_timestamp(get_shanghai_time()):
                self.my_lg.info('该商品已经过期下架...! 进行逻辑删除 is_delete=1')
                is_delete = 1
            # print(is_delete)

        if not other.get('good', {}).get('onsale'):  # True or False
            is_delete = 1

        return is_delete

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

    def _get_data_error_init(self):
        self.result_data = {}
        return {}

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
        data = yp._handle_target_data()
        pprint(data)