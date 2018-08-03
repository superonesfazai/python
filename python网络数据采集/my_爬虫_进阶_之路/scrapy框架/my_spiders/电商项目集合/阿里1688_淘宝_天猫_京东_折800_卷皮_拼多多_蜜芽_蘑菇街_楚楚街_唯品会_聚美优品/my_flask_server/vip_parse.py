# coding:utf-8

'''
@author = super_fazai
@File    : vip_parse.py
@Time    : 2018/3/5 09:47
@connect : superonesfazai@gmail.com
'''

"""
唯品会常规商品页面解析系统(也可采集预售商品)
"""

import time
from random import randint
import json
from pprint import pprint
from time import sleep
import re
import gc
from scrapy import Selector
from json import dumps

from fzutils.cp_utils import _get_right_model_data
from fzutils.time_utils import (
    timestamp_to_regulartime,
)
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests
from fzutils.common_utils import json_2_dict

'''
改版抓包微信唯品会商品数据接口
'''
def test():
    # 抓包: 唯品会微信小程序
    url = 'https://m.vip.com/server.html'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':	'gzip',
        'Accept-Language': 'zh-cn',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'm.vip.com',
        'Referer': 'https://servicewechat.com/wxe9714e742209d35f/284/page-frame.html',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Mobile/15A5341f MicroMessenger/6.6.5 NetType/WIFI Language/zh_CN',
    }

    t = str(time.time().__round__()) + str(randint(100, 999))
    params = {
        'serv':	'getGoodsActiveMsg',
        '_xcxid': t,
    }

    goods_id = '460143743'
    page = 'product-0-' + str(goods_id) + '.html'
    data = dumps([
        {
            "method":"getGoodsActiveMsg",
            "params":{
                "page": page,
                "query":""
            },
            # "id":4884390025335,
            'id': 1,
            "jsonrpc":"2.0"
        },{
            "method":"getCoupon",
            "params":{
                "page": page,
                "query":""
            },
            # "id":4884390025336,
            'id': 2,
            "jsonrpc":"2.0"
        },{
            "method":"getProductDetail",
            "params":{
                "page": page,
                "query":""
            },
            # "id":4884390025337,
            'id': 3,
            "jsonrpc":"2.0"
        },{
            "method":"getProductMeta",
            "params":{
                "page": page,
                "query":""
            },
            # "id":4884390025338,
            'id': 4,
            "jsonrpc":"2.0"
        },{
            "method":"getProductSlide",
            "params":{
                "page": page,
                "query":""
            },
            # "id":4884390025339,
            'id': 5,
            "jsonrpc":"2.0"
        },{
            "method":"getProductMultiColor",
            "params":{
                "page": page,
                "query":""
            },
            # "id":4884390025340,
            'id': 6,
            "jsonrpc":"2.0"
        },{
            "method":"getProductSize",
            "params":{
                "page": page,
                "query":""
            },
            # "id":4884390025341,
            'id': 7,
            "jsonrpc":"2.0"
        },{
            "method":"getProductCountdown",
            "params":{
                "page": page,
                "query":""
            },
            # "id":4884390025342,
            'id': 8,
            "jsonrpc":"2.0"
        },{
            "method":"ProductRpc.getProductLicense",
            "params":{
                "page": page,
                "query":""
            },
            # "id":4884390025343,
            'id': 9,
            "jsonrpc":"2.0"
        },
    ])

    body = MyRequests.get_url_body(method='post', url=url, headers=headers, params=params, data=data)
    # print(body)
    data = json_2_dict(json_str=body)

    return data

# _ = test()
# pprint(_)

class VipParse(object):
    def __init__(self):
        self._set_headers()
        self.result_data = {}

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':	'gzip',
            'Accept-Language': 'zh-cn',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'm.vip.com',
            'Referer': 'https://servicewechat.com/wxe9714e742209d35f/284/page-frame.html',
            'User-Agent': get_random_pc_ua(),
        }

    def _set_params(self):
        '''
        设置params
        :return:
        '''
        t = str(time.time().__round__()) + str(randint(100, 999))

        params = {
            'serv': 'getGoodsActiveMsg',
            '_xcxid': t,
        }

        return params

    def _set_post_data(self, page):
        '''
        设置待post的data
        :param page:
        :return:
        '''
        data = dumps([
            {
                "method": "getGoodsActiveMsg",
                "params": {
                    "page": page,
                    "query": ""
                },
                # "id":4884390025335,
                'id': 1,
                "jsonrpc": "2.0"
            }, {
                "method": "getCoupon",
                "params": {
                    "page": page,
                    "query": ""
                },
                # "id":4884390025336,
                'id': 2,
                "jsonrpc": "2.0"
            }, {
                "method": "getProductDetail",
                "params": {
                    "page": page,
                    "query": ""
                },
                # "id":4884390025337,
                'id': 3,
                "jsonrpc": "2.0"
            }, {
                "method": "getProductMeta",
                "params": {
                    "page": page,
                    "query": ""
                },
                # "id":4884390025338,
                'id': 4,
                "jsonrpc": "2.0"
            }, {
                "method": "getProductSlide",
                "params": {
                    "page": page,
                    "query": ""
                },
                # "id":4884390025339,
                'id': 5,
                "jsonrpc": "2.0"
            }, {
                "method": "getProductMultiColor",
                "params": {
                    "page": page,
                    "query": ""
                },
                # "id":4884390025340,
                'id': 6,
                "jsonrpc": "2.0"
            }, {
                "method": "getProductSize",
                "params": {
                    "page": page,
                    "query": ""
                },
                # "id":4884390025341,
                'id': 7,
                "jsonrpc": "2.0"
            }, {
                "method": "getProductCountdown",
                "params": {
                    "page": page,
                    "query": ""
                },
                # "id":4884390025342,
                'id': 8,
                "jsonrpc": "2.0"
            }, {
                "method": "ProductRpc.getProductLicense",
                "params": {
                    "page": page,
                    "query": ""
                },
                # "id":4884390025343,
                'id': 9,
                "jsonrpc": "2.0"
            },
        ])

        return data

    def get_goods_data(self, goods_id):
        '''
        模拟构造得到data的url
        :param goods_id: 类型 list
        :return: data dict类型
        '''
        if goods_id == []:
            self.result_data = {}
            return {}
        else:
            data = {}
            # 抓包: 唯品会微信小程序
            url = 'https://m.vip.com/server.html'
            params = self._set_params()

            page = 'product-0-' + str(goods_id[1]) + '.html'
            post_data = self._set_post_data(page=page)

            body = MyRequests.get_url_body(method='post', url=url, headers=self.headers, params=params, data=post_data)
            # print(body)

            if body == '':
                self.result_data = {}
                return {}

            else:
                tmp_data = json_2_dict(json_str=body)
                if tmp_data == {}:
                    self.result_data = {}
                    return {}

                try:
                    # title, sub_title
                    data['title'] = tmp_data[2].get('result', {}).get('product_name', '')
                    assert data['title'] != '', '获取到的title为空值, 请检查!'
                    data['sub_title'] = ''

                    # shop_name
                    data['shop_name'] = tmp_data[2].get('result', {}).get('brand_info', {}).get('brand_name', '')

                    # 获取所有示例图片
                    all_img_url = tmp_data[2].get('result', {}).get('img_pre', [])
                    assert all_img_url != [], '获取到的all_img_url为空[], 请检查!'
                    all_img_url = [{
                        'img_url': 'https:' + item.get('b_img', '')
                    } for item in all_img_url]
                    # pprint(all_img_url)
                    data['all_img_url'] = all_img_url

                    # 获取p_info
                    p_info = self._get_p_info(tmp_data=tmp_data)
                    assert p_info != [], 'p_info为空list, 请检查!'
                    # pprint(p_info)
                    data['p_info'] = p_info

                    # 获取每个商品的div_desc
                    div_desc = self.get_goods_div_desc(tmp_data=tmp_data[2].get('result', {}).get('detailImages', []))
                    assert div_desc != '', '获取到的div_desc为空值! 请检查'
                    data['div_desc'] = div_desc

                    '''
                    上下架时间
                    '''
                    data['sell_time'] = {
                        'begin_time': tmp_data[2].get('result', {}).get('sell_time_from', {}),
                        'end_time': tmp_data[2].get('result', {}).get('sell_time_to', {}),
                    }
                    if int(data['sell_time'].get('begin_time')) > int(time.time()):
                        # *** 先根据上下架时间来判断是否为预售商品，如果是预售商品就按预售商品的method来去对应规格的价格
                        goods_id = [1, goods_id[1]]     # 设置成预售的商品goods_id格式

                    # 设置detail_name_list
                    detail_name_list = self._get_detail_name_list(tmp_data=tmp_data)
                    # print(detail_name_list)
                    data['detail_name_list'] = detail_name_list

                    '''
                    获取每个规格对应价格跟规格以及库存
                    '''
                    true_sku_info = self._get_true_sku_info(goods_id=goods_id, tmp_data=tmp_data)
                    # pprint(true_sku_info)
                    if true_sku_info == []:     # 也可能是 表示没有库存, 买完或者下架
                        print('获取到的sku_info为空值, 请检查!')
                        print('*** 注意可能是卖完了，库存为0 导致!! ***')
                        # raise Exception
                        data['price_info_list'] = true_sku_info
                    else:
                        data['price_info_list'] = true_sku_info

                except Exception as e:
                    print('遇到错误如下: ', e)
                    self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                    return {}

                if data != {}:
                    # pprint(data)
                    self.result_data = data
                    return data

                else:
                    print('data为空!')
                    self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                    return {}

    def deal_with_data(self):
        '''
        处理得到规范的data数据
        :return: result 类型 dict
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

            '''
            用于判断商品是否已经下架
            '''
            is_delete = 0
            all_rest_number = 0
            for item in price_info_list:
                all_rest_number += item.get('rest_number', 0)
            if all_rest_number == 0:
                is_delete = 1
            # 当官方下架时间< int(time.time()) 则商品已下架 is_delete = 1
            if int(data.get('sell_time', {}).get('end_time', '')) < int(time.time()):
                print('该商品已经过期下架...! 进行逻辑删除 is_delete=1')
                is_delete = 1
            # print(is_delete)

            # 上下架时间
            schedule = [{
                'begin_time': timestamp_to_regulartime(int(data.get('sell_time', {}).get('begin_time', ''))),
                'end_time': timestamp_to_regulartime(int(data.get('sell_time', {}).get('end_time', ''))),
            }]

            # 销售总量
            all_sell_count = ''

            # 商品价格和淘宝价
            # pprint(data['price_info_list'])
            try:
                tmp_price_list = sorted([round(float(item.get('detail_price', '')), 2) for item in data['price_info_list']])
                price = tmp_price_list[-1]  # 商品价格
                taobao_price = tmp_price_list[0]  # 淘宝价
            except IndexError:
                print('获取price和taobao_price时出错, 请检查!')  # 商品下架时, detail_price为空str, 所以会IndexError报错
                print('@@@@@@ 此处对该商品进行逻辑删除! @@@@@@')
                self.result_data = {}
                price = 0.
                taobao_price = 0.
                is_delete = 1
                # return {}

            result = {
                'shop_name': shop_name,                 # 店铺名称
                'account': account,                     # 掌柜
                'title': title,                         # 商品名称
                'sub_title': sub_title,                 # 子标题
                'price': price,                         # 商品价格
                'taobao_price': taobao_price,           # 淘宝价
                # 'goods_stock': goods_stock,           # 商品库存
                'detail_name_list': detail_name_list,   # 商品标签属性名称
                # 'detail_value_list': detail_value_list,# 商品标签属性对应的值
                'price_info_list': price_info_list,     # 要存储的每个标签对应规格的价格及其库存
                'all_img_url': all_img_url,             # 所有示例图片地址
                'p_info': p_info,                       # 详细信息标签名对应属性
                'div_desc': div_desc,                   # div_desc
                'schedule': schedule,                   # 商品特价销售时间段
                'all_sell_count': all_sell_count,       # 销售总量
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
            self.result_data = {}
            return result

        else:
            print('待处理的data为空的dict, 该商品可能已经转移或者下架')
            self.result_data = {}
            return {}

    def to_right_and_update_data(self, data, pipeline):
        '''
        更新商品数据
        :param data:
        :param pipeline:
        :return:
        '''
        tmp = _get_right_model_data(data=data, site_id=25)
        params = self._get_db_update_params(item=tmp)
        # 改价格的sql
        # sql_str = r'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, MyShelfAndDownTime=%s, delete_time=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s where GoodsID = %s'
        # 不改价格的sql
        if tmp['delete_time'] == '':
            sql_str = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s, shelf_time=%s where GoodsID = %s'
        elif tmp['shelf_time'] == '':
            sql_str = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s, delete_time=%s where GoodsID = %s'
        else:
            sql_str = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s, shelf_time=%s, delete_time=%s where GoodsID = %s'

        pipeline._update_table(sql_str=sql_str, params=params)

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

    def _get_detail_name_list(self, tmp_data):
        '''
        得到detail_name_list
        :param tmp_data:
        :return: Exception 表示异常退出 | [xx, ...] 表示success
        '''
        detail_name_list = []
        multiColor = tmp_data[5].get('result', {})     # 新接口在'method': 'getProductMultiColor',里面
        # pprint(multiColor)
        productSku = tmp_data[6].get('result', {}).get('productSku', {})

        if multiColor == {} or productSku == {}:
            print('获取detail_name_list失败, 请检查!')
            raise Exception
        else:
            if multiColor.get('items') is None:
                pass
            elif multiColor.get('items', []).__len__() == 1:
                pass
            else:
                detail_name_list.append({'spec_name': multiColor.get('name', '')})

            other_spec_name = productSku.get('name', '')
            assert other_spec_name != '', '获取detail_name_list失败, 原因other_spec_name为空值, 请检查!'
            detail_name_list.append({'spec_name': other_spec_name})

        return detail_name_list

    def _get_true_sku_info(self, goods_id, tmp_data):
        '''
        得到每个规格对应的库存, 价格, 图片等详细信息
        :param tmp_data:
        :return:
        '''
        multiColor = tmp_data[5].get('result', {})
        # sku_price = tmp_data[2].get('result', {}).get('sku_price', [])
        ## ** 研究发现multiColor以及productSku中的type为1时，表示该商品规格库存为0
        productSku = tmp_data[6].get('result', {}).get('productSku', {})
        # tmp = {
        #     'multiColor': multiColor,
        #     # 'sku_price': sku_price,
        #     'productSku': productSku,
        # }
        # pprint(tmp)

        true_sku_info = []
        if multiColor == {} or productSku == {}:
            return []
        else:
            if multiColor.get('items') is None:
                color_ = None
            else:
                tmp_color_items = multiColor.get('items', [])
                color_ = []
                for item in tmp_color_items:
                    if item.get('type', 0) == 1:    # 该颜色无库存
                        continue
                    else:                           # 为0，表示有库存
                        # 先获取到有库存的对应规格, 是否有颜色属性后面再判断
                        color_.append({
                            'goods_id': item.get('product_id', ''),
                            'name': item.get('name', ''),
                            'img_url': 'https:' + item.get('icon', {}).get('imageUrl', '')
                        })

            if color_ == []:    # 没有规格 也可能是 # 表示没有库存, 买完或者下架
                print('获取到的color_为空[], 请检查!')
                return []
            else:
                if productSku.get('items') is None:
                    print('获取到的others_items为None')
                    return []

                else:
                    other_items = productSku.get('items', [])
                    other_ = []
                    for item in other_items:
                        if item.get('type', 0) == 1:    # 该规格无库存
                            continue
                        else:                           # 该规格有库存
                            detail_price = item.get('promotion_price', '')
                            # 还是选择所有商品都拿最优惠的价格
                            # if detail_price == '' or goods_id[0] == 1:      # 为空就改为获取vipshop_price字段
                            if detail_price == '':      # 为空就改为获取vipshop_price字段
                                detail_price = item.get('vipshop_price', '')
                            else:
                                pass
                            normal_price = item.get('market_price', '')
                            if normal_price == '':
                                normal_price = detail_price
                            other_.append({
                                'spec_value': item.get('sku_name', ''),
                                'detail_price': detail_price,
                                'normal_price': normal_price,
                                'img_url': '',      # 设置默认为空值
                                'rest_number': item.get('leavings', 0),  # 该规格的剩余库存量
                            })

                if color_ is None:
                    for item_2 in other_:
                        spec_value = item_2.get('spec_value', '')
                        item_2['spec_value'] = spec_value
                        item_2['img_url'] = ''
                        true_sku_info.append(item_2)

                elif len(color_) == 1:    # 颜色长度为1时，表示唯品会默认选择的属性，不需要将color_相关的值添加到spec_value里面
                    true_sku_info = other_

                else:
                    for item in color_:
                        if item.get('goods_id') == goods_id[1]:    # 表示为原先的那个goods_id
                            if item.get('name', '') == '无':     # 表示无颜色属性
                                pass
                            else:
                                for item_2 in other_:
                                    spec_value = item.get('name', '') + '|' + item_2.get('spec_value', '')
                                    item_2['spec_value'] = spec_value
                                    item_2['img_url'] = item.get('img_url', '')
                                    true_sku_info.append(item_2)

                        else:                                   # 表示是其他颜色对应的goods_id
                            '''
                            下面是获取该颜色对应goods_id的所有可售的规格价格信息
                            '''
                            url = 'https://m.vip.com/server.html'
                            params = self._set_params()

                            page = 'product-0-' + str(goods_id[1]) + '.html'
                            post_data = self._set_post_data(page=page)

                            tmp_data_2 = MyRequests.get_url_body(method='post', url=url, headers=self.headers, params=params, data=post_data)
                            # print(tmp_data_2)

                            # 先处理得到dict数据
                            if tmp_data_2 == '':
                                print('获取其他颜色规格的url的body时为空值')
                                return []
                            else:
                                tmp_data_2 = json_2_dict(json_str=tmp_data_2)
                                if tmp_data_2 == {}:
                                    return []

                                other_items_2 = tmp_data_2[6].get('result', {}).get('productSku', {}).get('items', [])
                                other_2 = []
                                for item_3 in other_items_2:
                                    if item_3.get('type', 0) == 1:  # 该规格无库存
                                        continue
                                    else:  # 该规格有库存
                                        detail_price = item_3.get('promotion_price', '')
                                        # 还是都拿最优惠的价格 不管限时2小时时间问题的折扣
                                        # if detail_price == '' or goods_id[0] == 1:  # 为空就改为获取vipshop_price字段
                                        if detail_price == '':  # 为空就改为获取vipshop_price字段
                                            detail_price = item_3.get('vipshop_price', '')
                                        normal_price = item_3.get('market_price', '')
                                        if normal_price == '':
                                            normal_price = detail_price
                                        other_2.append({
                                            'spec_value': item_3.get('sku_name', ''),
                                            'detail_price': detail_price,
                                            'normal_price': normal_price,
                                            'rest_number': item_3.get('leavings', 0),  # 设置默认的值
                                            'img_url': '',  # 设置默认为空值
                                        })

                                for item_4 in other_2:
                                    spec_value = item.get('name', '') + '|' + item_4.get('spec_value', '')
                                    item_4['spec_value'] = spec_value
                                    item_4['img_url'] = item.get('img_url', '')
                                    true_sku_info.append(item_4)

        return true_sku_info

    def get_goods_div_desc(self, tmp_data):
        '''
        得到div_desc
        :param tmp_data:
        :return: '' | 非空字符串
        '''
        tmp_div_desc = ''
        if tmp_data == []:
            print('获取到的div_desc的图片list为空[]')
            return ''
        else:
            for item in tmp_data:
                tmp_img_url = 'https:' + item.get('imageUrl', '')
                tmp = r'<img src="{}" style="height:auto;width:100%;"/>'.format(tmp_img_url)
                tmp_div_desc += tmp

            detail_data = '<div>' + tmp_div_desc + '</div>'

        return detail_data

    def _get_p_info(self, tmp_data):
        '''
        得到p_info
        :param tmp_data:
        :return: [] 表示出错 | [xxx, ...] 表示success
        '''
        p_info = []
        try:
            tmp_p_info = tmp_data[2].get('result', {}).get('attrSpecProps', [])
            assert tmp_p_info != [], '获取到的p_info为空[], 请检查!'
            # pprint(tmp_p_info)

            brandStoreName = tmp_data[2].get('result', {}).get('brandStoreName', '')
            if brandStoreName != '':
                p_info.append({'p_name': '品牌名称', 'p_value': brandStoreName})

            p_info.append({'p_name': '商品名称', 'p_value': tmp_data[2].get('result', {}).get('product_name', '')})

            # 产地
            areaOutput = tmp_data[2].get('result', {}).get('areaOutput', '')
            if areaOutput != '':
                p_info.append({'p_name': '产地', 'p_value': areaOutput})

            # 材质相关
            itemProperties = tmp_data[2].get('result', {}).get('itemProperties', [])
            if itemProperties != []:
                for item in itemProperties:
                    p_info.append({'p_name': item.get('name', ''), 'p_value': item.get('value', '')})

            # 洗涤说明相关
            itemDetailModules = tmp_data[2].get('result', {}).get('itemDetailModules', [])
            if itemDetailModules != []:
                for item in itemDetailModules:
                    p_info.append({'p_name': item.get('name', ''), 'p_value': item.get('value', '')})

            for item in tmp_p_info:
                try:
                    p_value = item.get('values', [])
                    if p_value != [] and p_value.__len__() > 1:
                        p_value = [item_6.get('optionName', '') for item_6 in p_value]
                        p_value = ' '.join(p_value)

                    elif p_value.__len__() == 1:
                        p_value = item.get('values', [])[0].get('optionName', '')

                    else:
                        p_value = ''
                    p_info.append({
                        'p_name': item.get('attributeName', ''),
                        'p_value': p_value
                    })
                except IndexError:
                    print('在解析p_info时索引出错, 请检查!')
                    return []
        except Exception as e:
            print('遇到错误:', e)

        finally:
            return p_info

    def get_goods_id_from_url(self, vip_url):
        '''
        得到goods_id
        :param vip_url:
        :return: goods_id (类型list)
        '''
        is_vip_url = re.compile(r'https://m.vip.com/product-(\d*)-.*?.html.*?').findall(vip_url)
        if is_vip_url != []:
            if re.compile(r'https://m.vip.com/product-.*?-(\d+).html.*?').findall(vip_url) != []:
                tmp_vip_url = re.compile(r'https://m.vip.com/product-.*?-(\d+).html.*?').findall(vip_url)[0]
                if tmp_vip_url != '':
                    goods_id = tmp_vip_url
                else:   # 只是为了在pycharm运行时不跳到chrome，其实else完全可以不要的
                    vip_url = re.compile(r';').sub('', vip_url)
                    goods_id = re.compile(r'https://m.vip.com/product-.*?-(\d+).html.*?').findall(vip_url)[0]
                print('------>>>| 得到的唯品会商品的goods_id为:', goods_id)
                return [0, goods_id]
        else:
            # 是否是预售商品
            is_vip_preheading = re.compile(r'https://m.vip.com/preheating-product-(\d+)-.*?.html.*?').findall(vip_url)
            if is_vip_preheading != []:
                if re.compile(r'https://m.vip.com/preheating-product-.*?-(\d+).html.*?').findall(vip_url) != []:
                    tmp_vip_url = re.compile(r'https://m.vip.com/preheating-product-.*?-(\d+).html.*?').findall(vip_url)[0]
                    if tmp_vip_url != '':
                        goods_id = tmp_vip_url
                    else:  # 只是为了在pycharm运行时不跳到chrome，其实else完全可以不要的
                        vip_url = re.compile(r';').sub('', vip_url)
                        goods_id = re.compile(r'https://m.vip.com/preheating-product-.*?-(\d+).html.*?').findall(vip_url)[0]
                    print('------>>>| 得到的唯品会 预售商品 的goods_id为:', goods_id)
                    return [1, goods_id]
            else:
                print('唯品会商品url错误, 非正规的url, 请参照格式(https://m.vip.com/product-0-xxxxxxx.html) or (https://m.vip.com/preheating-product-xxxx-xxxx.html)开头的...')
                return []

    def __del__(self):
        gc.collect()

if __name__ == '__main__':
    vip = VipParse()
    while True:
        vip_url = input('请输入待爬取的唯品会商品地址: ')
        vip_url.strip('\n').strip(';')
        goods_id = vip.get_goods_id_from_url(vip_url)
        vip.get_goods_data(goods_id=goods_id)
        data = vip.deal_with_data()
        # pprint(data)