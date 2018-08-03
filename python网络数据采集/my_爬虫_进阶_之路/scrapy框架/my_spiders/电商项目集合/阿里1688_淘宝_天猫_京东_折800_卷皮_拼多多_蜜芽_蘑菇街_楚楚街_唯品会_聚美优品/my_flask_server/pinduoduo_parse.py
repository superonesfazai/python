# coding:utf-8

'''
@author = super_fazai
@File    : pinduoduo_parse.py
@Time    : 2017/11/24 14:58
@connect : superonesfazai@gmail.com
'''

"""
拼多多页面采集系统(官网地址: http://mobile.yangkeduo.com/)
由于拼多多的pc站，官方早已放弃维护，专注做移动端，所以下面的都是基于移动端地址进行的爬取
直接requests开始时是可以的，后面就只返回错误的信息，估计将我IP过滤了
"""

import time
from random import randint
import json
import requests
from pprint import pprint
from time import sleep
import re
import gc
from json import dumps

from settings import PHANTOMJS_DRIVER_PATH

from fzutils.cp_utils import _get_right_model_data
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests
from fzutils.spider.fz_phantomjs import MyPhantomjs
from fzutils.ip_pools import MyIpPools
from fzutils.common_utils import json_2_dict

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

class PinduoduoParse(object):
    def __init__(self):
        self._set_headers()
        self.result_data = {}
        # self.set_cookies_key_api_uid()  # 设置cookie中的api_uid的值
        self.my_phantomjs = MyPhantomjs(executable_path=PHANTOMJS_DRIVER_PATH)

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'mobile.yangkeduo.com',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
            # 'Cookie': 'api_uid=rBQh+FoXerAjQWaAEOcpAg==;',      # 分析发现需要这个cookie值
        }

    def get_goods_data(self, goods_id):
        '''
        模拟构造得到data的url
        :param goods_id:
        :return: data   类型dict
        '''
        if goods_id == '':
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            return {}
        else:
            tmp_url = 'http://mobile.yangkeduo.com/goods.html?goods_id=' + str(goods_id)
            print('------>>>| 得到的商品手机版地址为: ', tmp_url)

            '''
            1.采用requests，由于经常返回错误的body(即requests.get返回的为空的html), So pass
            '''
            # body = MyRequests.get_url_body(url=tmp_url, headers=self.headers, had_referer=True)

            '''
            2.采用phantomjs来获取
            '''
            body = self.my_phantomjs.use_phantomjs_to_get_url_body(url=tmp_url)

            if body == '':
                print('body中re匹配到的data为空!')
                self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                return {}

            data = re.compile(r'window.rawData= (.*?);</script>').findall(body)  # 贪婪匹配匹配所有

            if data != []:
                data = json_2_dict(json_str=data[0])
                if data == {}:
                    self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                    return {}
                # pprint(data)

                try:
                    data['goods'].pop('localGroups')
                    data['goods'].pop('mallService')
                    data.pop('reviews')             # 评价信息跟相关统计
                except:
                    pass
                # pprint(data)

                '''
                处理detailGallery转换成能被html显示页面信息
                '''
                detail_data = data.get('goods', {}).get('detailGallery', [])
                tmp_div_desc = ''
                if detail_data != []:
                    for index in range(0, len(detail_data)):
                        if index == 0:      # 跳过拼多多的提示
                            pass
                        else:
                            tmp = ''
                            tmp_img_url = detail_data[index].get('url')
                            tmp = r'<img src="{}" style="height:auto;width:100%;"/>'.format(tmp_img_url)
                            tmp_div_desc += tmp

                    detail_data = '<div>' + tmp_div_desc + '</div>'

                else:
                    detail_data = ''
                # print(detail_data)
                try:
                    data['goods'].pop('detailGallery')  # 删除图文介绍的无第二次用途的信息
                except:
                    pass
                data['div_desc'] = detail_data

                # pprint(data)
                self.result_data = data
                return data

            else:
                print('data为空!')
                self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                return {}

    def deal_with_data(self):
        '''
        处理result_data, 返回需要的信息
        :return: 字典类型
        '''
        data = self.result_data
        if data != {}:
            # 店铺名称
            if data.get('mall') is not None:
                shop_name = data.get('mall', {}).get('mallName', '')
            else:
                shop_name = ''

            # 掌柜
            account = ''

            # 商品名称
            title = data.get('goods', {}).get('goodsName', '')

            # 子标题
            sub_title = ''

            # 商品库存
            # 商品标签属性对应的值

            # 商品标签属性名称
            if data.get('goods', {}).get('skus', []) == []:
                detail_name_list = []
            else:
                if data.get('goods', {}).get('skus', [])[0].get('specs') == []:
                    detail_name_list = []
                else:
                    detail_name_list = [{'spec_name': item.get('spec_key')} for item in data.get('goods', {}).get('skus', [])[0].get('specs')]
            # print(detail_name_list)

            # 要存储的每个标签对应规格的价格及其库存
            skus = data.get('goods', {}).get('skus', [])
            # pprint(skus)
            price_info_list = []
            if skus != []:          # ** 注意: 拼多多商品只有一个规格时skus也不会为空的 **
                for index in range(0, len(skus)):
                    tmp = {}
                    price = skus[index].get('groupPrice', '')          # 拼团价
                    normal_price = skus[index].get('normalPrice', '')  # 单独购买价格
                    spec_value = [item.get('spec_value') for item in data.get('goods', {}).get('skus', [])[index].get('specs')]
                    spec_value = '|'.join(spec_value)
                    img_url = skus[index].get('thumbUrl', '')
                    rest_number = skus[index].get('quantity', 0)  # 剩余库存
                    is_on_sale = skus[index].get('isOnSale', 0)        # 用于判断是否在特价销售，1:特价 0:原价(normal_price)
                    tmp['spec_value'] = spec_value
                    tmp['detail_price'] = price
                    tmp['normal_price'] = normal_price
                    tmp['img_url'] = img_url
                    if rest_number <= 0:
                        tmp['rest_number'] = 0
                    else:
                        tmp['rest_number'] = rest_number
                    tmp['is_on_sale'] = is_on_sale
                    price_info_list.append(tmp)

            if price_info_list == []:
                print('price_info_list为空值')
                return {}

            # 商品价格和淘宝价
            tmp_price_list = sorted([round(float(item.get('detail_price', '')), 2) for item in price_info_list])
            price = tmp_price_list[-1]  # 商品价格
            taobao_price = tmp_price_list[0]  # 淘宝价

            if detail_name_list == []:
                print('## detail_name_list为空值 ##')
                price_info_list = []

            # print('最高价为: ', price)
            # print('最低价为: ', taobao_price)
            # print(len(price_info_list))
            # pprint(price_info_list)

            # 所有示例图片地址
            all_img_url = [{'img_url': item} for item in data.get('goods', {}).get('topGallery', [])]
            # print(all_img_url)

            # 详细信息标签名对应属性
            tmp_p_value = re.compile(r'\n').sub('', data.get('goods', {}).get('goodsDesc', ''))
            tmp_p_value = re.compile(r'\t').sub('', tmp_p_value)
            tmp_p_value = re.compile(r'  ').sub('', tmp_p_value)
            p_info = [{'p_name': '商品描述', 'p_value': tmp_p_value}]
            # print(p_info)

            # 总销量
            all_sell_count = data.get('goods', {}).get('sales', 0)

            # div_desc
            div_desc = data.get('div_desc', '')

            # 商品销售时间区间
            schedule = [{
                'begin_time': self.timestamp_to_regulartime(data.get('goods', {}).get('groupTypes', [])[0].get('startTime')),
                'end_time': self.timestamp_to_regulartime(data.get('goods', {}).get('groupTypes', [])[0].get('endTime')),
            }]
            # pprint(schedule)

            # 用于判断商品是否已经下架
            is_delete = 0

            result = {
                'shop_name': shop_name,                 # 店铺名称
                'account': account,                     # 掌柜
                'title': title,                         # 商品名称
                'sub_title': sub_title,                 # 子标题
                # 'shop_name_url': shop_name_url,        # 店铺主页地址
                'price': price,                         # 商品价格
                'taobao_price': taobao_price,           # 淘宝价
                # 'goods_stock': goods_stock,            # 商品库存
                'detail_name_list': detail_name_list,   # 商品标签属性名称
                # 'detail_value_list': detail_value_list,# 商品标签属性对应的值
                'price_info_list': price_info_list,     # 要存储的每个标签对应规格的价格及其库存
                'all_img_url': all_img_url,             # 所有示例图片地址
                'p_info': p_info,                       # 详细信息标签名对应属性
                'div_desc': div_desc,                   # div_desc
                'schedule': schedule,                   # 商品开卖时间和结束开卖时间
                'all_sell_count': all_sell_count,       # 商品总销售量
                'is_delete': is_delete                  # 用于判断商品是否已经下架
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
            return result

        else:
            print('待处理的data为空的dict, 该商品可能已经转移或者下架')
            return {}

    def to_right_and_update_data(self, data, pipeline):
        tmp = _get_right_model_data(data=data, site_id=13)
        params = self._get_db_update_params(item=tmp)
        # 改价格的sql语句
        # sql_str = r'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, MyShelfAndDownTime=%s, delete_time=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s where GoodsID = %s'
        # 不改价格的sql语句
        if tmp['delete_time'] == '':
            sql_str = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s, shelf_time=%s where GoodsID = %s'
        elif tmp['shelf_time'] == '':
            sql_str = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s, delete_time=%s where GoodsID = %s'
        else:
            sql_str = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s, shelf_time=%s, delete_time=%s where GoodsID = %s'

        pipeline._update_table(sql_str=sql_str, params=params)

    def insert_into_pinduoduo_xianshimiaosha_table(self, data, pipeline):
        tmp = _get_right_model_data(data=data, site_id=16)  # 采集来源地(卷皮秒杀商品)
        print('------>>>| 待存储的数据信息为: ', tmp.get('goods_id'))

        params = self._get_db_insert_miaosha_params(item=tmp)
        sql_str = r'insert into dbo.pinduoduo_xianshimiaosha(goods_id, goods_url, username, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_info, all_image_url, property_info, detail_info, schedule, stock_info, miaosha_time, miaosha_begin_time, miaosha_end_time, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        pipeline._insert_into_table(sql_str=sql_str, params=params)

    def to_update_pinduoduo_xianshimiaosha_table(self, data, pipeline):
        tmp = _get_right_model_data(data=data, site_id=16)
        # print('------>>> | 待存储的数据信息为: |', tmp)
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_update_miaosha_params(item=tmp)
        sql_str = 'update dbo.pinduoduo_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, schedule=%s, stock_info=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s where goods_id = %s'
        pipeline._update_table(sql_str=sql_str, params=params)

    def _get_db_update_params(self, item):
        '''
        得到db待存储的数据
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
            dumps(item['schedule'], ensure_ascii=False),
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

        return tuple(params)

    def _get_db_insert_miaosha_params(self, item):
        params = (
            item['goods_id'],
            item['goods_url'],
            item['username'],
            item['create_time'],
            item['modify_time'],
            item['shop_name'],
            item['title'],
            item['sub_title'],
            item['price'],
            item['taobao_price'],
            dumps(item['detail_name_list'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
            dumps(item['price_info_list'], ensure_ascii=False),
            dumps(item['all_img_url'], ensure_ascii=False),
            dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
            item['div_desc'],  # 存入到DetailInfo
            dumps(item['schedule'], ensure_ascii=False),
            dumps(item['stock_info'], ensure_ascii=False),
            dumps(item['miaosha_time'], ensure_ascii=False),
            item['miaosha_begin_time'],
            item['miaosha_end_time'],

            item['site_id'],
            item['is_delete'],
        )

        return params

    def _get_db_update_miaosha_params(self, item):
        params = (
            item['modify_time'],
            item['shop_name'],
            item['title'],
            item['sub_title'],
            item['price'],
            item['taobao_price'],
            dumps(item['detail_name_list'], ensure_ascii=False),
            dumps(item['price_info_list'], ensure_ascii=False),
            dumps(item['all_img_url'], ensure_ascii=False),
            dumps(item['p_info'], ensure_ascii=False),
            item['div_desc'],
            item['is_delete'],
            dumps(item['schedule'], ensure_ascii=False),
            dumps(item['stock_info'], ensure_ascii=False),
            dumps(item['miaosha_time'], ensure_ascii=False),
            item['miaosha_begin_time'],
            item['miaosha_end_time'],

            item['goods_id'],
        )

        return params

    def set_cookies_key_api_uid(self):
        '''
        给headers增加一个cookie, 里面有个key名字为api_uid
        :return:
        '''
        # 设置代理ip
        ip_object = MyIpPools()
        self.proxies = ip_object.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]

        tmp_proxies = {
            'http': self.proxy,
        }
        # 得到cookie中的key名为api_uid的值
        host_url = 'http://mobile.yangkeduo.com'
        try:
            response = requests.get(host_url, headers=self.headers, proxies=tmp_proxies, timeout=10)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            api_uid = response.cookies.get('api_uid')
            # print(response.cookies.items())
            # if api_uid is None:
            #     api_uid = 'rBQh+FoXerAjQWaAEOcpAg=='
            self.headers['Cookie'] = 'api_uid=' + str(api_uid) + ';'
            # print(api_uid)
        except Exception:
            print('requests.get()请求超时....')
            pass

    def timestamp_to_regulartime(self, timestamp):
        '''
        将时间戳转换成时间
        '''
        # 利用localtime()函数将时间戳转化成localtime的格式
        # 利用strftime()函数重新格式化时间

        # 转换成localtime
        time_local = time.localtime(timestamp)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

        return dt

    def get_goods_id_from_url(self, pinduoduo_url):
        '''
        得到goods_id
        :param pinduoduo_url:
        :return: goods_id (类型str)
        '''
        is_pinduoduo_url = re.compile(r'http://mobile.yangkeduo.com/goods.html.*?').findall(pinduoduo_url)
        if is_pinduoduo_url != []:
            if re.compile(r'http://mobile.yangkeduo.com/goods.html\?.*?goods_id=(\d+).*?').findall(pinduoduo_url) != []:
                tmp_pinduoduo_url = re.compile(r'http://mobile.yangkeduo.com/goods.html\?.*?goods_id=(\d+).*?').findall(pinduoduo_url)[0]
                if tmp_pinduoduo_url != '':
                    goods_id = tmp_pinduoduo_url
                else:   # 只是为了在pycharm里面测试，可以不加
                    pinduoduo_url = re.compile(r';').sub('', pinduoduo_url)
                    goods_id = re.compile(r'http://mobile.yangkeduo.com/goods.html\?.*?goods_id=(\d+).*?').findall(pinduoduo_url)[0]
                print('------>>>| 得到的拼多多商品id为:', goods_id)
                return goods_id
            else:
                pass
        else:
            print('拼多多商品url错误, 非正规的url, 请参照格式(http://mobile.yangkeduo.com/goods.html)开头的...')
            return ''

    def __del__(self):
        try:
            del self.my_phantomjs
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    pinduoduo = PinduoduoParse()
    while True:
        pinduoduo_url = input('请输入待爬取的拼多多商品地址: ')
        pinduoduo_url.strip('\n').strip(';')
        goods_id = pinduoduo.get_goods_id_from_url(pinduoduo_url)
        data = pinduoduo.get_goods_data(goods_id=goods_id)
        pinduoduo.deal_with_data()