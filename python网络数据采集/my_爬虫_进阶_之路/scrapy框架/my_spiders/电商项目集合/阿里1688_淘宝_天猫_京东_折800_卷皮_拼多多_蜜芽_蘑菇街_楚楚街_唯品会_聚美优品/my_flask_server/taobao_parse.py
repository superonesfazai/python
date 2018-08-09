# coding:utf-8

'''
@author = super_fazai
@File    : taobao_parse.py
@Time    : 2017/10/25 07:40
@connect : superonesfazai@gmail.com
'''

"""
可爬取淘宝, 全球购, 天天特价
"""

import time
from random import randint
import json
import re
from pprint import pprint
from decimal import Decimal
from json import dumps
import asyncio
from time import sleep
import datetime
import gc
# import pycurl
# from io import StringIO
# import traceback
# from io import BytesIO

from settings import MY_SPIDER_LOGS_PATH
from settings import (
    PHANTOMJS_DRIVER_PATH,
    CHROME_DRIVER_PATH,
)
import pytz
from logging import INFO, ERROR
from json import JSONDecodeError
from urllib.parse import urlencode

from fzutils.cp_utils import _get_right_model_data
from fzutils.log_utils import set_logger
from fzutils.time_utils import get_shanghai_time
from fzutils.internet_utils import tuple_or_list_params_2_dict_params
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests
from fzutils.common_utils import json_2_dict

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

# chrome驱动地址
my_chrome_driver_path = CHROME_DRIVER_PATH

class TaoBaoLoginAndParse(object):
    def __init__(self, logger=None):
        self._set_headers()
        self.result_data = {}
        self._set_logger(logger)
        self.msg = ''

    def _set_headers(self):
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_pc_ua(),
            'accept': '*/*',
            # 'referer': 'https://h5.m.taobao.com/awp/core/detail.htm?id=560666972076',
            # 'authority': 'h5api.m.taobao.com',
            # 'cookie': 'v=0; cookie2=1e478415a5583e8e0f5ec1598fe22224; t=1bdcbe0b678123e1755897be375b453f; _tb_token_=8f81eeeb31d0; cna=UOK9Ey4N1hYCAXHXtRx8QV37; thw=cn; mt=ci%3D-1_0; enc=b5TkGZ7%2F21TQIJJszNV9Lh6NcqQo2HsiX8RUxdH1xWxdk1bDmUu4bwcp%2FdmRjjjgULSKAfJQPasgu2nWMNNlnw%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; _m_h5_tk=19d41e6c7d8fda1949de6878565815aa_1530352039810; _m_h5_tk_enc=f2fdd16bbc1f39ce53446f1cbc8a9118; isg=BCQkk16MI6DwJFftGmJ7sz3H9STWFUpaNIkeKj5FM-9R6cWzZM0Kt3oArUFxMYB_',
        }

    def _set_logger(self, logger):
        if logger is None:
            self.my_lg = set_logger(
                log_file_name=MY_SPIDER_LOGS_PATH + '/淘宝/_/' + str(get_shanghai_time())[0:10] + '.txt',
                console_log_level=INFO,
                file_log_level=ERROR
            )
        else:
            self.my_lg = logger

    def get_goods_data(self, goods_id):
        '''
        模拟构造得到data的url
        :param goods_id:
        :return: data   类型dict
        '''
        self.msg = '------>>>| 对应的手机端地址为: ' + 'https://h5.m.taobao.com/awp/core/detail.htm?id=' + str(goods_id)
        self.my_lg.info(self.msg)

        # 获取主接口的body
        last_url = self._get_last_url(goods_id=goods_id)
        data = MyRequests.get_url_body(url=last_url, headers=self.headers, params=None, timeout=14)
        if data == '':
            self.my_lg.error('出错goods_id: {0}'.format((goods_id)))
            self.result_data = {}
            return {}

        try:
            data = re.compile(r'mtopjsonp1\((.*)\)').findall(data)[0]  # 贪婪匹配匹配所有
            # self.my_lg.info(str(data))
        except IndexError:
            self.my_lg.error('data为空! 出错goods_id: {0}'.format(goods_id))
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            return {}

        data = json_2_dict(json_str=data, logger=self.my_lg)
        if data == {}:
            self.my_lg.error('出错goods_id: {0}'.format(str(goods_id)))
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            return {}
        # pprint(data)

        if data.get('data', {}).get('trade', {}).get('redirectUrl', '') != '' \
                and data.get('data', {}).get('seller', {}).get('evaluates') is None:
            '''
            ## 表示该商品已经下架, 原地址被重定向到新页面
            '''
            self.my_lg.info('@@@@@@ 该商品已经下架...')
            tmp_data_s = self.init_pull_off_shelves_goods()
            self.result_data = {}
            return tmp_data_s

        # 处理商品被转移或者下架导致页面不存在的商品
        if data.get('data').get('seller', {}).get('evaluates') is None:
            self.my_lg.info('data为空, 地址被重定向, 该商品可能已经被转移或下架')
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            return {}

        data['data']['rate'] = ''           # 这是宝贝评价
        data['data']['resource'] = ''       # 买家询问别人
        data['data']['vertical'] = ''       # 也是问和回答
        data['data']['seller']['evaluates'] = ''  # 宝贝描述, 卖家服务, 物流服务的评价值...
        result_data = data['data']

        # 处理result_data['apiStack'][0]['value']
        # self.my_lg.info(result_data.get('apiStack', [])[0].get('value', ''))
        result_data_apiStack_value = result_data.get('apiStack', [])[0].get('value', {})

        # 将处理后的result_data['apiStack'][0]['value']重新赋值给result_data['apiStack'][0]['value']
        result_data['apiStack'][0]['value'] = self._wash_result_data_apiStack_value(
            goods_id=goods_id,
            result_data_apiStack_value=result_data_apiStack_value
        )

        # 处理mockData
        mock_data = result_data['mockData']
        mock_data = json_2_dict(json_str=mock_data, logger=self.my_lg)
        if mock_data == {}:
            self.my_lg.error('出错goods_id: {0}'.format(goods_id))
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            return {}
        mock_data['feature'] = ''
        # pprint(mock_data)
        result_data['mockData'] = mock_data

        # self.my_lg.info(str(result_data.get('apiStack', [])[0]))   # 可能会有{'name': 'esi', 'value': ''}的情况
        if result_data.get('apiStack', [])[0].get('value', '') == '':
            self.my_lg.info("result_data.get('apiStack', [])[0].get('value', '')的值为空....")
            result_data['trade'] = {}
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            return {}
        else:
            result_data['trade'] = result_data.get('apiStack', [])[0].get('value', {}).get('trade', {})     # 用于判断该商品是否已经下架的参数
            # pprint(result_data['trade'])

        self.result_data = result_data
        # pprint(self.result_data)

        return result_data

    def deal_with_data(self, goods_id):
        '''
        处理result_data, 返回需要的信息
        :return: 字典类型
        '''
        data = self.result_data
        if data != {}:
            # 店铺名称
            shop_name = data['seller'].get('shopName', '')      # 可能不存在shopName这个字段

            # 掌柜
            account = data['seller'].get('sellerNick', '')

            # 商品名称
            title = data['item']['title']
            # 子标题
            sub_title = data['item'].get('subtitle', '')
            sub_title = re.compile(r'\n').sub('', sub_title)
            # 店铺主页地址
            # shop_name_url = 'https:' + data['seller']['taoShopUrl']
            # shop_name_url = re.compile(r'.m.').sub('.', shop_name_url)  # 手机版转换为pc版

            # 商品价格
            # price = data['apiStack'][0]['value']['price']['extraPrices'][0]['priceText']
            tmp_taobao_price = data['apiStack'][0].get('value', '').get('price').get('price').get('priceText', '')
            tmp_taobao_price = tmp_taobao_price.split('-')     # 如果是区间的话，分割成两个，单个价格就是一个
            # self.my_lg.info(str(tmp_taobao_price))
            if len(tmp_taobao_price) == 1:
                # 商品最高价
                # price = Decimal(tmp_taobao_price[0]).__round__(2)     # json不能处理decimal所以后期存的时候再处理
                price = tmp_taobao_price[0]
                # 商品最低价
                taobao_price = price
                # self.my_lg.info(str(price))
                # self.my_lg.info(str(taobao_price))
            else:
                # price = Decimal(tmp_taobao_price[1]).__round__(2)
                # taobao_price = Decimal(tmp_taobao_price[0]).__round__(2)
                price = tmp_taobao_price[1]
                taobao_price = tmp_taobao_price[0]
                # self.my_lg.info(str(price))
                # self.my_lg.info(str(taobao_price))

            # 商品库存
            goods_stock = data['apiStack'][0]['value'].get('skuCore', {}).get('sku2info', {}).get('0', {}).get('quantity', '')

            # 商品标签属性名称,及其对应id值
            detail_name_list, detail_value_list = self._get_detail_name_and_value_list(data=data)

            '''
            每个标签对应值的价格及其库存
            '''
            price_info_list = self._get_price_info_list(data=data, detail_value_list=detail_value_list)

            # 所有示例图片地址
            all_img_url = self._get_all_img_url(tmp_all_img_url=data['item']['images'])
            # self.my_lg.info(str(all_img_url))

            # 详细信息p_info
            p_info = self._get_p_info(tmp_p_info=data.get('props').get('groupProps'))   # tmp_p_info 一个list [{'内存容量': '32GB'}, ...]

            '''
            div_desc
            '''
            # 手机端描述地址
            if data.get('item').get('taobaoDescUrl') is not None:
                phone_div_url = 'https:' + data['item']['taobaoDescUrl']
            else:
                phone_div_url = ''

            # pc端描述地址
            if data.get('item').get('taobaoPcDescUrl') is not None:
                pc_div_url = 'https:' + data['item']['taobaoPcDescUrl']
                # self.my_lg.info(phone_div_url)
                # self.my_lg.info(pc_div_url)

                div_desc = self.get_div_from_pc_div_url(pc_div_url, goods_id)
                # self.my_lg.info(div_desc)
                if div_desc == '':
                    self.my_lg.error('该商品的div_desc为空! 出错goods_id: %s' % str(goods_id))
                    self.result_data = {}
                    return {}

                # self.driver.quit()
                gc.collect()
            else:
                pc_div_url = ''
                div_desc = ''

            '''
            后期处理
            '''
            # 后期处理detail_name_list, detail_value_list
            detail_name_list = [{'spec_name': i[0]} for i in detail_name_list]

            # 商品标签属性对应的值, 及其对应id值
            if data.get('skuBase').get('props') is None:
                pass
            else:
                tmp_detail_value_list = [item['values'] for item in data.get('skuBase', '').get('props', '')]
                # self.my_lg.info(str(tmp_detail_value_list))
                detail_value_list = []
                for item in tmp_detail_value_list:
                    tmp = [i['name'] for i in item]
                    # self.my_lg.info(str(tmp))
                    detail_value_list.append(tmp)  # 商品标签属性对应的值
                    # pprint(detail_value_list)

            is_delete = self._get_is_delete(title=title, data=data)
            self.my_lg.info('is_delete = %s' % str(is_delete))

            # 月销量
            try:
                sell_count = str(data.get('apiStack', [])[0].get('value', {}).get('item', {}).get('sellCount', ''))
            except:
                sell_count = '0'
            # self.my_lg.info(sell_count)

            result = {
                'shop_name': shop_name,                             # 店铺名称
                'account': account,                                 # 掌柜
                'title': title,                                     # 商品名称
                'sub_title': sub_title,                             # 子标题
                # 'shop_name_url': shop_name_url,                     # 店铺主页地址
                'price': price,                                     # 商品价格
                'taobao_price': taobao_price,                       # 淘宝价
                'goods_stock': goods_stock,                         # 商品库存
                'detail_name_list': detail_name_list,               # 商品标签属性名称
                'detail_value_list': detail_value_list,             # 商品标签属性对应的值
                'price_info_list': price_info_list,                 # 要存储的每个标签对应规格的价格及其库存
                'all_img_url': all_img_url,                         # 所有示例图片地址
                'p_info': p_info,                                   # 详细信息标签名对应属性
                'phone_div_url': phone_div_url,                     # 手机端描述地址
                'pc_div_url': pc_div_url,                           # pc端描述地址
                'div_desc': div_desc,                               # div_desc
                'sell_count': sell_count,                           # 月销量
                'is_delete': is_delete,                             # 用于判断商品是否已经下架
            }
            # self.my_lg.info(str(result))
            # pprint(result)
            # wait_to_send_data = {
            #     'reason': 'success',
            #     'data': result,
            #     'code': 1
            # }
            # json_data = json.dumps(wait_to_send_data, ensure_ascii=False)
            # self.my_lg.info(json_data)
            return result
        else:
            self.my_lg.info('待处理的data为空的dict, 该商品可能已经转移或者下架')
            # return {
            #     'is_delete': 1,
            # }
            return {}

    def to_right_and_update_data(self, data, pipeline):
        '''
        实时更新数据
        :param data:
        :param pipeline:
        :return:
        '''
        goods_id = data.get('goods_id')
        try:
            tmp = _get_right_model_data(data=data, site_id=1, logger=self.my_lg)
        except:
            self.my_lg.error('遇到错误, 先跳过处理!出错goods_id={0}'.format(goods_id), exc_info=True)
            return None
        params = self._get_db_update_params(item=tmp)
        # 改价格的sql
        # sql_str = r'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, MyShelfAndDownTime=%s, delete_time=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s where GoodsID = %s'
        # 不改价格的sql
        base_sql_str = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, {0} {1} where GoodsID = %s'
        if tmp['delete_time'] == '':
            sql_str = base_sql_str.format('shelf_time=%s', '')
        elif tmp['shelf_time'] == '':
            sql_str = base_sql_str.format('delete_time=%s', '')
        else:
            sql_str = base_sql_str.format('shelf_time=%s,', 'delete_time=%s')

        pipeline._update_table(sql_str=sql_str, params=params, logger=self.my_lg)

    def old_taobao_goods_insert_into_new_table(self, data, pipeline):
        '''
        得到规范格式的data并且存入数据库
        :param data:
        :param pipeline:
        :return:
        '''
        goods_id = data.get('goods_id')
        try:
            tmp = _get_right_model_data(data=data, site_id=1, logger=self.my_lg)
        except:
            self.my_lg.error('遇到错误, 先跳过处理!出错goods_id={0}'.format(goods_id), exc_info=True)
            return
        params = self._get_db_insert_params(item=tmp)
        if tmp.get('main_goods_id') is not None:
            # main_goods_id不为空
            sql_str = r'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete, MainGoodsID) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

        else:
            # main_goods_id为空
            sql_str = r'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

        result = pipeline._insert_into_table_2(sql_str=sql_str, params=params, logger=self.my_lg)

        return result

    def _get_db_insert_params(self, item):
        '''
        得到db待插入的数据
        :param item:
        :return:
        '''
        params = [
            item['goods_id'],
            item['goods_url'],
            item['username'],
            item['create_time'],
            item['modify_time'],
            item['shop_name'],
            item['account'],
            item['title'],
            item['sub_title'],
            item['link_name'],
            item['price'],
            item['taobao_price'],
            dumps(item['price_info'], ensure_ascii=False),
            dumps(item['detail_name_list'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
            dumps(item['price_info_list'], ensure_ascii=False),
            dumps(item['all_img_url'], ensure_ascii=False),
            dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
            item['div_desc'],  # 存入到DetailInfo
            item['all_sell_count'],

            item['site_id'],
            item['is_delete'],
        ]

        if item.get('main_goods_id') is not None:
            params.append(item.get('main_goods_id'))

        return tuple(params)

    def _get_db_update_params(self, item):
        '''
        得到db待更新的数据
        :param item:
        :return:
        '''
        params = [
            item['modify_time'],
            item['shop_name'],
            item['account'],
            item['title'],
            item['sub_title'],
            item['link_name'],
            # item['price'],
            # item['taobao_price'],
            dumps(item['price_info'], ensure_ascii=False),
            dumps(item['detail_name_list'], ensure_ascii=False),
            dumps(item['price_info_list'], ensure_ascii=False),
            dumps(item['all_img_url'], ensure_ascii=False),
            dumps(item['p_info'], ensure_ascii=False),
            item['div_desc'],
            item['all_sell_count'],
            # item['delete_time'],
            item['is_delete'],
            item['is_price_change'],
            dumps(item['price_change_info'], ensure_ascii=False),

            item['goods_id'],
        ]
        if item.get('delete_time', '') == '':
            params.insert(-1, item['shelf_time'])
        elif item.get('shelf_time', '') == '':
            params.insert(-1, item['delete_time'])
        else:
            params.insert(-1, item['shelf_time'])
            params.insert(-1, item['delete_time'])

        return params

    def _set_params(self, goods_id):
        '''
        设置params
        :param goods_id:
        :return:
        '''
        params_data_1 = {
            'id': goods_id
        }
        params_data_2 = {
            'exParams': json.dumps(params_data_1),  # 每层里面的字典都要先转换成json
            'itemNumId': goods_id
        }
        # self.my_lg.info(str(params_data_2))

        ### * 注意这是正确的url地址: right_url = 'https://acs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1508886442888&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2016%40taobao_h5_2.0.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22exParams%22%3A%22%7B%5C%22id%5C%22%3A%5C%22546756179626%5C%22%7D%22%2C%22itemNumId%22%3A%22546756179626%22%7D'
        # right_url = 'https://acs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1508886442888&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2016%40taobao_h5_2.0.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22exParams%22%3A%22%7B%5C%22id%5C%22%3A%5C%22546756179626%5C%22%7D%22%2C%22itemNumId%22%3A%22546756179626%22%7D'
        # right_url = 'https://acs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1508857184835&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2016%40taobao_h5_2.0.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22exParams%22%3A%22%7B%5C%22id%5C%22%3A%5C%2241439519931%5C%22%7D%22%2C%22itemNumId%22%3A%2241439519931%22%7D'
        # self.my_lg.info(right_url)

        params = (
            ('jsv', '2.4.8'),
            ('appKey', '12574478'),
            ('t', str(time.time().__round__()) + str(randint(100, 999))),
            # ('sign', 'b7cd843a2b40b5238d3b53faa3bb605b'),
            ('api', 'mtop.taobao.detail.getdetail'),
            ('v', '6.0'),
            ('ttid', '2016@taobao_h5_2.0.0'),
            ('isSec', '0'),
            ('ecode', '0'),
            ('AntiFlood', 'true'),
            ('AntiCreep', 'true'),
            ('H5Request', 'true'),
            ('type', 'jsonp'),
            ('dataType', 'jsonp'),
            ('callback', 'mtopjsonp1'),
            ('data', json.dumps(params_data_2)),    # 每层里面的字典都要先转换成json
        )

        return params

    def _get_last_url(self, goods_id):
        '''
        获取组合过params的last_url
        :return:
        '''
        # 设置params
        params = self._set_params(goods_id=goods_id)
        tmp_url = 'https://acs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/'
        # tmp_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/'

        params = tuple_or_list_params_2_dict_params(params)
        url = tmp_url + '?' + urlencode(params)
        last_url = re.compile(r'\+').sub('', url)  # 转换后得到正确的url请求地址(替换'+')
        # self.my_lg.info(last_url)

        return last_url

    def _wash_result_data_apiStack_value(self, goods_id, result_data_apiStack_value):
        '''
        清洗result_data_apiStack_value
        :param goods_id:
        :param result_data_apiStack_value:
        :return:
        '''
        try:
            result_data_apiStack_value = json.loads(result_data_apiStack_value)

            result_data_apiStack_value['vertical'] = ''
            result_data_apiStack_value['consumerProtection'] = ''  # 7天无理由退货
            result_data_apiStack_value['feature'] = ''
            result_data_apiStack_value['layout'] = ''
            result_data_apiStack_value['delivery'] = ''  # 发货地到收到地
            result_data_apiStack_value['resource'] = ''  # 优惠券
            # result_data_apiStack_value['item'] = ''       # 不能注释否则得不到月销量
            # pprint(result_data_apiStack_value)
        except Exception:
            self.my_lg.error("json.loads转换出错，得到result_data['apiStack'][0]['value']值可能为空，此处跳过" + ' 出错goods_id: ' + str(goods_id))
            result_data_apiStack_value = ''
            pass

        return result_data_apiStack_value

    def _get_all_img_url(self, tmp_all_img_url):
        '''
        获取所有示例图片
        :param tmp_all_img_url:
        :return:
        '''
        all_img_url = []
        for item in tmp_all_img_url:
            item = 'https:' + item
            all_img_url.append(item)

        return [{'img_url': item} for item in all_img_url]

    def _get_p_info(self, tmp_p_info):
        '''
        得到 p_info
        :param tmp_p_info:
        :return:
        '''
        p_info = []
        if tmp_p_info is not None:
            tmp_p_info = tmp_p_info[0].get('基本信息', [])
            for item in tmp_p_info:
                for key, value in item.items():
                    tmp = {}
                    tmp['p_name'] = key
                    tmp['p_value'] = value
                    tmp['id'] = '0'
                    p_info.append(tmp)
                    # self.my_lg.info(str(p_info))

        return p_info

    def _get_detail_name_and_value_list(self, data):
        '''
        得到detail_name_list, detail_value_list
        :param data:
        :return: detail_name_list, detail_value_list
        '''
        detail_name_list = []
        detail_value_list = []
        if data.get('skuBase') is not None:
            if data.get('skuBase').get('props') is not None:
                detail_name_list = [[item['name'], item['pid']] for item in data['skuBase']['props']]
                # self.my_lg.info(str(detail_name_list))

                # 商品标签属性对应的值, 及其对应id值
                tmp_detail_value_list = [item['values'] for item in data['skuBase']['props']]
                # self.my_lg.info(str(tmp_detail_value_list))
                for item in tmp_detail_value_list:
                    tmp = [[i['name'], i['vid']] for i in item]
                    # self.my_lg.info(str(tmp))
                    detail_value_list.append(tmp)  # 商品标签属性对应的值
                    # pprint(detail_value_list)

        return detail_name_list, detail_value_list

    def _get_price_info_list(self, data, detail_value_list):
        '''
        得到详细规格及其价格信息
        :param data:
        :param detail_value_list:
        :return:
        '''
        if data.get('skuBase').get('skus') is not None:
            skus = data['skuBase']['skus']  # 里面是所有规格的可能值[{'propPath': '20105:4209035;1627207:1710113203;5919063:3266779;122216431:28472', 'skuId': '3335554577910'}, ...]
            pros = data.get('skuBase', {}).get('props', [])
            sku2_info = data['apiStack'][0].get('value').get('skuCore').get('sku2info')
            try:
                sku2_info.pop('0')  # 此处删除总库存的值
            except Exception:
                pass
            # pprint(sku2_info)
            prop_path_list = []  # 要存储的每个标签对应规格的价格及其库存
            for key in sku2_info:
                tmp_prop_path_list = [item for item in skus if item.get('skuId') == key]  # [{'skuId': '3335554577923', 'propPath': '20105:4209035;1627207:1710113207;5919063:3266781;122216431:28473'}]

                # 处理propPath得到可识别的文字
                prop_path = tmp_prop_path_list[0].get('propPath', '').split(';')
                prop_path = [i.split(':') for i in prop_path]
                prop_path_2 = [i[1] for i in prop_path]     # 暂存值
                prop_path = [j[1] for j in prop_path]  # 是每个属性对应的vid值(是按顺序来的)['4209035', '1710113207', '3266781', '28473']
                # self.my_lg.info(str(prop_path))
                # pprint(prop_path_2)

                for index in range(0, len(prop_path)):  # 将每个值对应转换为具体规格
                    for i in detail_value_list:
                        for j in i:
                            if prop_path[index] == j[1]:
                                prop_path[index] = j[0]
                # self.my_lg.info(str(prop_path))                  # 其格式为  ['32GB', '【黑色主机】【红 /  蓝 手柄】', '套餐二', '港版']
                # 再转换为要存储的字符串
                spec_value = '|'.join(prop_path)  # 其规格为  32GB|【黑色主机】【红 /  蓝 手柄】|套餐二|港版
                # self.my_lg.info(prop_path)

                tmp_prop_path_list[0]['sku_price'] = sku2_info[key]['price']['priceText']
                tmp_prop_path_list[0]['quantity'] = sku2_info[key]['quantity']
                # tmp['sku_id'] = tmp_prop_path_list[0]['skuId']      # skuId是定位值，由于不需要就给它注释了
                # tmp['prop_path'] = tmp_prop_path_list[0]['propPath']

                img_url = self._get_spec_value_one_img_url(pros=pros, prop_path_2=prop_path_2)

                tmp = {
                    'spec_value': spec_value,
                    'detail_price': tmp_prop_path_list[0]['sku_price'],  # 每个规格对应的价格
                    'rest_number': tmp_prop_path_list[0]['quantity'],    # 每个规格对应的库存量
                    'img_url': img_url,
                }
                prop_path_list.append(tmp)
            # pprint(prop_path_list)                  # 其格式为  [{'sku_id': '3335554577923', 'prop_path': '32GB|【黑色主机】【红 /  蓝 手柄】|套餐二|港版', 'sku_price': '2740', 'quantity': '284'}, ...]
            price_info_list = prop_path_list
        else:
            price_info_list = []

        return price_info_list

    def _get_spec_value_one_img_url(self, **kwargs):
        '''
        得到一个规格的img_url
        :param kwargs:
        :return: '' | xxxx
        '''
        pros = kwargs.get('pros')
        prop_path_2 = kwargs.get('prop_path_2')

        img_url = ''
        if len(pros) >= 1:  # 得到规格示例图
            # pprint(pros)
            # img_url_list = pros[0].get('values', [])
            img_url_list = []
            for i in pros:
                values = i.get('values', [])
                if len(values) >= 1:
                    if values[0].get('image') is not None:
                        img_url_list = values

            # pprint(img_url_list)
            img_url_list = [(i.get('vid', ''), i.get('image', '')) for i in img_url_list]
            # pprint(img_url_list)
            for k in prop_path_2:
                # print('vid:{0}'.format(k))
                for i in img_url_list:
                    # print(i[0])
                    if k == i[0]:
                        if i[1] != '':
                            img_url = 'https:' + i[1]

        return img_url

    def _get_is_delete(self, **kwargs):
        '''
        得到is_delete
        :param kwargs:
        :return:
        '''
        title = kwargs.get('title')
        data = kwargs.get('data', {})

        is_delete = 0
        # 1. 先通过buyEnable字段来判断商品是否已经下架
        if data.get('trade', {}) != {}:
            if data.get('trade', {}).get('buyEnable', 'true') == 'false':
                is_delete = 1

        if is_delete == 0:  # * 2018-6-29 加个判断防止与上面冲突(修复冲突bug)
            # * 2018-4-17 新增一个判断是否下架
            if not data.get('mockData', {}).get('trade', {}).get('buyEnable', True):
                is_delete = 1

        # 2. 此处再考虑名字中显示下架的商品
        if re.compile(r'下架').findall(title) != []:
            if re.compile(r'待下架').findall(title) != []:
                is_delete = 0
            elif re.compile(r'自动下架').findall(title) != []:
                is_delete = 0
            else:
                is_delete = 1

        return is_delete

    def init_pull_off_shelves_goods(self):
        '''
        状态为已下架商品的初始化
        :return:
        '''
        is_delete = 1
        result = {
            'shop_name': '',  # 店铺名称
            'account': '',  # 掌柜
            'title': '',  # 商品名称
            'sub_title': '',  # 子标题
            # 'shop_name_url': shop_name_url,                     # 店铺主页地址
            'price': 0,  # 商品价格
            'taobao_price': 0,  # 淘宝价
            'goods_stock': '',  # 商品库存
            'detail_name_list': [],  # 商品标签属性名称
            'detail_value_list': [],  # 商品标签属性对应的值
            'price_info_list': [],  # 要存储的每个标签对应规格的价格及其库存
            'all_img_url': [],  # 所有示例图片地址
            'p_info': [],  # 详细信息标签名对应属性
            'phone_div_url': '',  # 手机端描述地址
            'pc_div_url': '',  # pc端描述地址
            'div_desc': '',  # div_desc
            'sell_count': '',  # 月销量
            'is_delete': is_delete,  # 用于判断商品是否已经下架
        }

        return result

    async def insert_into_taobao_tiantiantejia_table(self, data, pipeline):
        data_list = data
        tmp = {}
        tmp['goods_id'] = data_list['goods_id']  # 官方商品id
        tmp['goods_url'] = data_list['goods_url']  # 商品地址
        # now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        '''
        时区处理，时间处理到上海时间
        '''
        tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
        now_time = datetime.datetime.now(tz)

        # 处理为精确到秒位，删除时区信息
        now_time = re.compile(r'\..*').sub('', str(now_time))
        # 将字符串类型转换为datetime类型
        now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')

        tmp['deal_with_time'] = now_time  # 操作时间

        tmp['modfiy_time'] = now_time  # 修改时间

        tmp['shop_name'] = data_list['shop_name']  # 公司名称
        tmp['title'] = data_list['title']  # 商品名称
        tmp['sub_title'] = data_list['sub_title']  # 商品子标题
        tmp['account'] = data_list['account']  # 掌柜名称
        tmp['month_sell_count'] = data_list['sell_count']  # 月销量

        # 设置最高价price， 最低价taobao_price
        try:
            tmp['price'] = Decimal(data_list['price']).__round__(2)
            tmp['taobao_price'] = Decimal(data_list['taobao_price']).__round__(2)
        except Exception:
            self.my_lg.error('遇到错误, 先跳过处理!出错goods_id={0}'.format(tmp['goods_id']), exc_info=True)
            return

        tmp['detail_name_list'] = data_list['detail_name_list']  # 标签属性名称

        """
        得到sku_map
        """
        tmp['price_info_list'] = data_list.get('price_info_list')  # 每个规格对应价格及其库存

        tmp['all_img_url'] = data_list.get('all_img_url')  # 所有示例图片地址

        tmp['p_info'] = data_list.get('p_info')  # 详细信息
        tmp['div_desc'] = data_list.get('div_desc')  # 下方div

        # 采集的来源地
        tmp['site_id'] = 19  # 采集来源地(淘宝)
        tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1

        tmp['schedule'] = data_list.get('schedule')
        tmp['tejia_begin_time'] = data_list.get('tejia_begin_time')
        tmp['tejia_end_time'] = data_list.get('tejia_end_time')
        tmp['block_id'] = data_list.get('block_id')
        tmp['tag_id'] = data_list.get('tag_id')
        tmp['father_sort'] = data_list.get('father_sort')
        tmp['child_sort'] = data_list.get('child_sort')

        # self.my_lg.info('------>>>| 待存储的数据信息为: |' + str(tmp))
        self.my_lg.info('------>>>| 待存储的数据信息为: |' + str(tmp.get('goods_id')))

        params = self._get_db_insert_tejia_params(item=tmp)
        sql_str = 'insert into dbo.taobao_tiantiantejia(goods_id, goods_url, create_time, modfiy_time, shop_name, account, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, month_sell_count, schedule, tejia_begin_time, tejia_end_time, block_id, tag_id, father_sort, child_sort, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        await pipeline._insert_into_table_3(
            sql_str=sql_str,
            params=params,
            logger=self.my_lg,
            error_msg_dict={
                'repeat_error': {
                    'field_name': 'goods_id',
                    'field_value': tmp.get('goods_id', ''),
                },
                'other_error': [{
                    'field_name': 'goods_url',
                    'field_value': tmp.get('goods_url'),
                },]
            })

        return True

    async def update_taobao_tiantiantejia_table(self, data, pipeline):
        '''
        更新天天秒杀特价的商品信息
        :param data:
        :param pipeline:
        :param logger
        :return:
        '''
        data_list = data
        tmp = {}
        tmp['goods_id'] = data_list['goods_id']  # 官方商品id
        '''
        时区处理，时间处理到上海时间
        '''
        tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
        now_time = datetime.datetime.now(tz)

        # 处理为精确到秒位，删除时区信息
        now_time = re.compile(r'\..*').sub('', str(now_time))
        # 将字符串类型转换为datetime类型
        now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')

        tmp['modfiy_time'] = now_time  # 修改时间

        tmp['shop_name'] = data_list['shop_name']  # 公司名称
        tmp['title'] = data_list['title']  # 商品名称
        tmp['sub_title'] = data_list['sub_title']  # 商品子标题
        tmp['account'] = data_list['account']  # 掌柜名称
        tmp['month_sell_count'] = data_list['sell_count']  # 月销量

        # 设置最高价price， 最低价taobao_price
        try:
            tmp['price'] = Decimal(data_list['price']).__round__(2)
            tmp['taobao_price'] = Decimal(data_list['taobao_price']).__round__(2)
        except Exception:
            self.my_lg.error('遇到错误, 先跳过处理!出错goods_id={0}'.format(tmp['goods_id']), exc_info=True)
            return

        tmp['detail_name_list'] = data_list['detail_name_list']  # 标签属性名称

        """
        得到sku_map
        """
        tmp['price_info_list'] = data_list.get('price_info_list')  # 每个规格对应价格及其库存

        tmp['all_img_url'] = data_list.get('all_img_url')  # 所有示例图片地址

        tmp['p_info'] = data_list.get('p_info')  # 详细信息
        tmp['div_desc'] = data_list.get('div_desc')  # 下方div

        tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1

        # tmp['schedule'] = data_list.get('schedule')
        # tmp['tejia_begin_time'] = data_list.get('tejia_begin_time')
        # tmp['tejia_end_time'] = data_list.get('tejia_end_time')

        # self.my_lg.info('------>>>| 待存储的数据信息为: |' + str(tmp))
        self.my_lg.info('------>>>| 待存储的数据信息为: |' + tmp.get('goods_id'))

        params = self._get_db_update_tejia_params(item=tmp)
        sql_str = 'update dbo.taobao_tiantiantejia set modfiy_time = %s, shop_name=%s, account=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, month_sell_count=%s, is_delete=%s where goods_id=%s'

        await pipeline._update_table_3(
            sql_str=sql_str,
            params=params,
            logger=self.my_lg,
            error_msg_dict={
                'other_error': [{
                    'field_name': 'goods_id',
                    'field_value': tmp.get('goods_id', ''),
                }]
            }
        )

    async def update_expired_goods_id_taobao_tiantiantejia_table(self, data, pipeline):
        '''
        更新过期商品的信息，使其转为普通常规商品
        :param data:
        :param pipeline:
        :return:
        '''
        data_list = data
        tmp = {}
        tmp['goods_id'] = data_list['goods_id']  # 官方商品id
        '''
        时区处理，时间处理到上海时间
        '''
        tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
        now_time = datetime.datetime.now(tz)

        # 处理为精确到秒位，删除时区信息
        now_time = re.compile(r'\..*').sub('', str(now_time))
        # 将字符串类型转换为datetime类型
        now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')

        tmp['modfiy_time'] = now_time  # 修改时间

        tmp['shop_name'] = data_list['shop_name']  # 公司名称
        tmp['title'] = data_list['title']  # 商品名称
        tmp['sub_title'] = data_list['sub_title']  # 商品子标题
        tmp['account'] = data_list['account']  # 掌柜名称
        tmp['month_sell_count'] = data_list['sell_count']  # 月销量

        # 设置最高价price， 最低价taobao_price
        try:
            tmp['price'] = Decimal(data_list['price']).__round__(2)
            tmp['taobao_price'] = Decimal(data_list['taobao_price']).__round__(2)
        except Exception:
            self.my_lg.error('遇到错误, 先跳过处理!出错goods_id={0}'.format(tmp['goods_id']), exc_info=True)
            return

        tmp['detail_name_list'] = data_list['detail_name_list']  # 标签属性名称

        """
        得到sku_map
        """
        tmp['price_info_list'] = data_list.get('price_info_list')  # 每个规格对应价格及其库存

        tmp['all_img_url'] = data_list.get('all_img_url')  # 所有示例图片地址

        tmp['p_info'] = data_list.get('p_info')  # 详细信息
        tmp['div_desc'] = data_list.get('div_desc')  # 下方div

        tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1

        # self.my_lg.info('------>>>| 待存储的数据信息为: |' + str(tmp))
        self.my_lg.info('------>>>| 待存储的数据信息为: |' + tmp.get('goods_id'))

        await pipeline.update_expired_goods_id_taobao_tiantiantejia_table(item=tmp, logger=self.my_lg)

    def _get_db_insert_tejia_params(self, item):
        '''
        获得待插入的参数
        :param item:
        :return:
        '''
        params = [
            item['goods_id'],
            item['goods_url'],
            item['deal_with_time'],
            item['modfiy_time'],
            item['shop_name'],
            item['account'],
            item['title'],
            item['sub_title'],
            item['price'],
            item['taobao_price'],
            dumps(item['detail_name_list'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
            dumps(item['price_info_list'], ensure_ascii=False),
            dumps(item['all_img_url'], ensure_ascii=False),
            dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
            item['div_desc'],  # 存入到DetailInfo
            item['month_sell_count'],
            dumps(item['schedule'], ensure_ascii=False),
            item['tejia_begin_time'],
            item['tejia_end_time'],
            item['block_id'],
            item['tag_id'],
            item['father_sort'],
            item['child_sort'],

            item['site_id'],
            item['is_delete'],
        ]

        return tuple(params)

    def _get_db_update_tejia_params(self, item):
        '''
        获取tejia的params
        :param item:
        :return:
        '''
        params = [
            item['modfiy_time'],
            item['shop_name'],
            item['account'],
            item['title'],
            item['sub_title'],
            item['price'],
            item['taobao_price'],
            dumps(item['detail_name_list'], ensure_ascii=False),
            dumps(item['price_info_list'], ensure_ascii=False),
            dumps(item['all_img_url'], ensure_ascii=False),
            dumps(item['p_info'], ensure_ascii=False),
            item['div_desc'],
            item['month_sell_count'],
            # dumps(item['schedule'], ensure_ascii=False),
            # item['tejia_begin_time'],
            # item['tejia_end_time'],
            item['is_delete'],

            item['goods_id'],
        ]

        return tuple(params)

    def get_div_from_pc_div_url(self, url, goods_id):
        '''
        根据pc描述的url模拟请求获取描述的div
        :return: str
        '''
        t = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位

        params_data_1 = {
            'id': goods_id,
            'type': '1',
        }

        tmp_url = 'https://api.m.taobao.com/h5/mtop.taobao.detail.getdesc/6.0/'
        _params = (
            ('appKey', '12574478'),
            ('t', t),
            ('api', 'mtop.taobao.detail.getdesc'),
            ('v', '6.0'),
            ('type', 'jsonp'),
            ('dataType', 'jsonp'),
            ('timeout', '20000'),
            ('callback', 'mtopjsonp1'),
            ('data', json.dumps(params_data_1)),
        )
        url = tmp_url + '?' + urlencode(_params)
        last_url = re.compile(r'\+').sub('', url)  # 转换后得到正确的url请求地址(替换'+')
        # self.my_lg.info(last_url)

        data = MyRequests.get_url_body(url=last_url, headers=self.headers, params=None, timeout=14, num_retries=3)
        if data == '':
            self.my_lg.error('获取到的div_desc为空值!请检查! 出错goods_id: {0}'.format(goods_id))
            return ''

        try:
            data = re.compile('mtopjsonp1\((.*)\)').findall(data)[0]  # 贪婪匹配匹配所有
            # self.my_lg.info(str(data))
        except IndexError as e:
            self.my_lg.error('获取data时, IndexError出错! 出错goods_id: {0}'.format(goods_id))
            self.my_lg.exception(e)
            return ''

        try:
            data = json.loads(data)
            # pprint(data)
        except JSONDecodeError:
            self.my_lg.error('json转换data时出错, 请检查!')
            data = {}

        div = data.get('data', {}).get('pcDescContent', '')
        # self.my_lg.info(str(div))
        div = self.deal_with_div(div)
        # self.my_lg.info(div)

        return div

    def deal_with_div(self, div):
        body = div

        # 过滤
        body = re.compile(r'\n').sub('', body)
        body = re.compile(r'\t').sub('', body)
        body = re.compile(r'  ').sub('', body)
        # self.my_lg.info(str(body))

        body = re.compile(r'src="data:image/png;.*?"').sub('', body)
        body = re.compile(r'data-img').sub('src', body)
        body = re.compile(r'https:').sub('', body)
        body = re.compile(r'src="').sub('src=\"https:', body)
        body = re.compile(r'&nbsp;').sub(' ', body)

        # self.my_lg.info(str(body))
        # 天猫洗广告
        ad = r'<p style="margin:0;width:0;height:0;overflow:hidden;">.*?<table align="center" style="margin:0 auto;">.*?</table> <p style="margin:0 0 5.0px 0;width:0;height:0;overflow:hidden;">.*?</p>'
        body = re.compile(ad).sub('', body, count=1)     # count=0 表示全部匹配，count=1 表示只匹配第一个
        # self.my_lg.info(str(body))

        body = re.compile('<a href=\".*?\" target').sub('<a href="" target', body)     # 防止外链跳转

        return body

    def get_goods_id_from_url(self, taobao_url):
        # https://item.taobao.com/item.htm?id=546756179626&ali_trackid=2:mm_110421961_12506094_47316135:1508678840_202_1930444423&spm=a21bo.7925826.192013.3.57586cc65hdN2V
        is_taobao_url = re.compile(r'https://item.taobao.com/item.htm.*?').findall(taobao_url)
        if is_taobao_url != []:
            if re.compile(r'https://item.taobao.com/item.htm.*?id=(\d+)&{0,20}.*?').findall(taobao_url) != []:
                tmp_taobao_url = re.compile(r'https://item.taobao.com/item.htm.*?id=(\d+)&{0,20}.*?').findall(taobao_url)[0]
                # self.my_lg.info(tmp_taobao_url)
                if tmp_taobao_url != '':
                    goods_id = tmp_taobao_url
                else:
                    taobao_url = re.compile(r';').sub('', taobao_url)
                    goods_id = re.compile(r'https://item.taobao.com/item.htm.*?id=(\d+)').findall(taobao_url)[0]
                    self.my_lg.info('------>>>| 得到的淘宝商品id为:' + goods_id)
                return goods_id
            else:       # 处理存数据库中取出的如: https://item.taobao.com/item.htm?id=560164926470
                # self.my_lg.info('9999')
                taobao_url = re.compile(r';').sub('', taobao_url)
                goods_id = re.compile(r'https://item.taobao.com/item.htm\?id=(\d+)&{0,20}.*?').findall(taobao_url)[0]
                self.my_lg.info('------>>>| 得到的淘宝商品id为:' + goods_id)
                return goods_id
        else:
            self.my_lg.info('淘宝商品url错误, 非正规的url, 请参照格式(https://item.taobao.com/item.htm)开头的...')
            return ''

    def __del__(self):
        try:
            del self.msg
            del self.my_lg
        except: pass
        gc.collect()

if __name__ == '__main__':
    login_taobao = TaoBaoLoginAndParse()
    while True:
        taobao_url = input('请输入待爬取的淘宝商品地址: ')
        taobao_url.strip('\n').strip(';')
        goods_id = login_taobao.get_goods_id_from_url(taobao_url)
        login_taobao.get_goods_data(goods_id=goods_id)
        data = login_taobao.deal_with_data(goods_id=goods_id)
        pprint(data)
