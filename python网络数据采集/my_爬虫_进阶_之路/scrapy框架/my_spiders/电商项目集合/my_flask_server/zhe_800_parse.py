# coding:utf-8

'''
@author = super_fazai
@File    : zhe_800_parse.py
@Time    : 2017/11/13 12:28
@connect : superonesfazai@gmail.com
'''

"""
折800页面采集系统
"""

import json
import re
from pprint import pprint
from json import dumps
from time import sleep
import re
import gc

from fzutils.cp_utils import _get_right_model_data
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests
from fzutils.common_utils import json_2_dict

class Zhe800Parse(object):
    def __init__(self):
        self._set_headers()
        self.result_data = {}

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'm.zhe800.com',
            'User-Agent': get_random_pc_ua()  # 随机一个请求头
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
            tmp_url = 'https://th5.m.zhe800.com/gateway/app/detail/product?productId=' + str(goods_id)
            # print('------>>>| 得到的detail信息的地址为: ', tmp_url)

            body = MyRequests.get_url_body(url=tmp_url, headers=self.headers, high_conceal=True)
            if body == '':
                self.result_data = {}
                return {}
            else: data = [body]

            if data != []:
                data = json_2_dict(json_str=data[0])
                if data == {}:
                    self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                    return {}
                # pprint(data)

                # 处理base
                base = data.get('/app/detail/product/base', '')
                base = json_2_dict(json_str=base)
                if base == {}:
                    print("json.loads转换出错，得到base值可能为空，此处跳过")
                    base = ''

                # 处理profiles
                profiles = data.get('/app/detail/product/profiles', '')
                profiles = json_2_dict(json_str=profiles)
                if profiles == {}:
                    print("json.loads转换出错，得到profiles值可能为空，此处跳过")
                    profiles = ''

                # 处理score
                score = data.get('/app/detail/product/score', '')
                score = json_2_dict(json_str=score)
                try:
                    score.pop('contents')
                except:
                    pass
                if score == {}:
                    print("json.loads转换出错，得到score值可能为空，此处跳过")
                    score = ''

                # 处理sku
                sku = data.get('/app/detail/product/sku', '')
                sku = json_2_dict(json_str=sku)
                # pprint(sku)
                if sku == {}:
                    print("json.loads转换出错，得到sku值可能为空，此处跳过")
                    sku = ''

                data['/app/detail/product/base'] = base
                data['/app/detail/product/profiles'] = profiles
                data['/app/detail/product/score'] = score
                data['/app/detail/product/sku'] = sku

                # 得到手机版地址
                try:
                    phone_url = 'http://th5.m.zhe800.com/h5/shopdeal?id=' + str(base.get('dealId', ''))
                except AttributeError:
                    print('获取手机版地址失败，此处跳过')
                    self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                    return {}

                print('------>>>| 得到商品手机版地址为: ', phone_url)
                # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))

                # 得到并处理detail(即图文详情显示信息)
                # http://m.zhe800.com/gateway/app/detail/graph?productId=
                tmp_detail_url = 'https://th5.m.zhe800.com/gateway/app/detail/graph?productId=' + str(goods_id)
                detail_data_body = MyRequests.get_url_body(url=tmp_detail_url, headers=self.headers, high_conceal=True)
                if detail_data_body == '':
                    print('detail_data为[]!')
                    self.result_data = {}
                    return {}
                else: detail_data = [detail_data_body]

                if detail_data != []:
                    detail_data = json_2_dict(json_str=detail_data[0])
                    if detail_data == {}:
                        print('json.loads(detail_data)时报错, 此处跳过')
                        self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                        return {}
                    # pprint(detail_data)

                    detail = detail_data.get('/app/detail/graph/detail', '')
                    detail = json_2_dict(json_str=detail)
                    try:
                        detail.pop('small')
                    except:
                        pass
                    if detail == {}:
                        print("json.loads转换出错，得到detail值可能为空，此处跳过")
                        detail = ''
                    # print(detail)

                    # div_desc
                    tmp_div_desc = self._get_div_desc(detail=detail, goods_id=goods_id)
                    if tmp_div_desc == '':
                        self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                        return {}
                    # print(tmp_div_desc)
                    data['/app/detail/graph/detail'] = tmp_div_desc

                    # shop_name
                    shop_name = self._get_shop_name(data=data)
                    if isinstance(shop_name, dict):
                        if shop_name == {}:
                            self.result_data = {}
                            return {}
                    data['shop_name'] = shop_name

                    '''
                    得到秒杀开始时间和结束时间
                    '''
                    schedule_and_stock_url = 'https://th5.m.zhe800.com/gateway/app/detail/status?productId=' + str(goods_id)
                    schedule_and_stock_info_body = MyRequests.get_url_body(url=schedule_and_stock_url, headers=self.headers, high_conceal=True)
                    if schedule_and_stock_info_body == '':
                        print('schedule_and_stock_info为空!')
                        self.result_data = {}
                        return {}
                    else: schedule_and_stock_info = [schedule_and_stock_info_body]

                    if schedule_and_stock_info != []:
                        schedule_and_stock_info = json_2_dict(json_str=schedule_and_stock_info[0])
                        if schedule_and_stock_info == {}:
                            print('得到秒杀开始时间和结束时间时错误, 此处跳过')
                            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                            return {}

                        schedule = schedule_and_stock_info.get('/app/detail/status/schedule')
                        if schedule is None:
                            schedule = {}
                        else:
                            schedule = json_2_dict(json_str=schedule)

                        stock = schedule_and_stock_info.get('/app/detail/status/stock')
                        if stock is None:
                            stock = {}
                        else:
                            stock = json_2_dict(json_str=stock)
                    else:
                        schedule = {}
                        stock = {}
                    data['schedule'] = schedule
                    data['stock'] = stock

                    # pprint(data)
                    self.result_data = data
                    return data

                else:
                    print('detail_data为空!')
                    self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                    return {}

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
            shop_name = data.get('shop_name', '')
            # print(shop_name)

            # 掌柜
            account = ''

            # 商品名称
            title = data.get('/app/detail/product/base', {}).get('title', '')
            # print(title)

            # 子标题
            sub_title = ''

            # 商品库存
            # 商品标签属性对应的值

            # 要存储的每个标签对应规格的价格及其库存
            try:
                tmp_price_info_list = data.get('/app/detail/product/sku', {}).get('items')
            except AttributeError as e:     # 表示获取失败
                print('AttributeError属性报错，为: ', e)
                print("data.get('/app/detail/product/sku', {}).get('items')获取失败, 此处跳过")
                return {}

            # pprint(tmp_price_info_list)
            detail_name_list = []   # 初始化
            price_info_list = []
            price = ''              # 先初始化
            taobao_price = ''
            # pprint(tmp_price_info_list)
            if len(tmp_price_info_list) == 1:     # 说明没有规格属性, 只有价格
                is_spec = False
                if tmp_price_info_list[0].get('curPrice', '') != '':
                    # 商品价格
                    # 淘宝价
                    price = round(float(tmp_price_info_list[0].get('curPrice', '')), 2)
                    taobao_price = price
                else:
                    price = round(float(tmp_price_info_list[0].get('orgPrice', '')), 2)
                    taobao_price = price
            else:                               # 有规格属性
                is_spec = True
                stock_items = data.get('stock', {}).get('stockItems')   # [{'count': 100, 'lockCount': 0, 'skuNum': '1-1001:2-1121'}, ...]
                # pprint(stock_items)
                for index in range(1, len(tmp_price_info_list)):
                    # 商品标签属性名称
                    detail_name_list = [{'spec_name': item.split('-')[0]} for item in tmp_price_info_list[index].get('propertyName').split(':')]
                    tmp_spec_value_1 = [str(item.split('-')[1]) for item in tmp_price_info_list[index].get('propertyName').split(':')]  # ['红格', 'S']
                    tmp_spec_value_2 = '|'.join(tmp_spec_value_1)   # '红格|S'
                    # print(tmp_spec_value_2)
                    property_num = tmp_price_info_list[index].get('propertyNum', '')
                    picture = tmp_price_info_list[index].get('vPictureBig', '')
                    if stock_items is None:     # 没有规格时, price,taobao_price值的设定
                        is_spec = False
                        price_info_list = []
                        if tmp_price_info_list[0].get('curPrice', '') != '':
                            price = tmp_price_info_list[0].get('curPrice', '')
                            taobao_price = price
                        else:
                            price = tmp_price_info_list[0].get('orgPrice', '')
                            taobao_price = price
                    else:   # 有规格的情况
                        is_spec = True
                        # 每个规格对应的库存量
                        count = [item.get('count', 0) for item in stock_items if property_num == item.get('skuNum', '')][0]
                        if tmp_price_info_list[index].get('curPrice', '') != '':    # 促销价不为空
                            tmp = {
                                'spec_value': tmp_spec_value_2,
                                'detail_price': tmp_price_info_list[index].get('curPrice', ''),
                                'normal_price': tmp_price_info_list[index].get('orgPrice', ''),
                                'rest_number': count,
                                'img_url': picture,
                            }
                        else:   # 促销价为空值
                            tmp = {
                                'spec_value': tmp_spec_value_2,
                                'detail_price': tmp_price_info_list[index].get('orgPrice', ''),
                                'normal_price': tmp_price_info_list[index].get('orgPrice', ''),
                                'rest_number': count,
                                'img_url': picture,
                            }
                        price_info_list.append(tmp)

            if is_spec:     # 得到有规格时的最高价和最低价
                tmp_price_list = sorted([round(float(item.get('detail_price', '')), 2) for item in price_info_list])
                price = tmp_price_list[-1]          # 商品价格
                taobao_price = tmp_price_list[0]    # 淘宝价

            # print('最高价为: ', price)
            # print('最低价为: ', taobao_price)
            # print(detail_name_list)
            # pprint(price_info_list)

            # 所有示例图片地址
            tmp_all_img_url = data.get('/app/detail/product/base', {}).get('images', [])
            all_img_url = [{'img_url': item['big']} for item in tmp_all_img_url]
            # pprint(all_img_url)

            # 详细信息标签名对应属性
            try:
                tmp_profiles = data.get('/app/detail/product/profiles')
                if tmp_profiles is None:
                    profiles = None
                else:
                    profiles = data.get('/app/detail/product/profiles', {}).get('profiles')
            except AttributeError as e:
                print('AttributeError属性报错，为: ', e)
                print("data.get('/app/detail/product/profiles', {}).get('profiles')获取失败, 此处跳过")
                return {}

            if profiles is None:
                p_info = []
            else:
                p_info = [{'p_name': item['name'], 'p_value': item['value']} for item in profiles]
            # pprint(p_info)

            # div_desc
            div_desc = data.get('/app/detail/graph/detail', '')

            # 用于判断商品是否已经下架
            is_delete = 0
            if price_info_list != []:
                stock_num = 0
                for _i in price_info_list:
                    stock_num += _i.get('rest_number', 0)
                if stock_num == 0:
                    is_delete = 1

            schedule = data.get('schedule')
            # pprint(schedule)
            if schedule is None:
                is_delete = 1       # 没有活动时间就表示已经下架
                schedule = []
            else:   # 开始的和未开始的都是能拿到时间的，所以没问题，嘿嘿-_-!!
                schedule = [{
                    'begin_time': schedule.get('beginTime', ''),
                    'end_time': schedule.get('endTime', '')
                }]
            # pprint(schedule)

            result = {
                'shop_name': shop_name,                     # 店铺名称
                'account': account,                         # 掌柜
                'title': title,                             # 商品名称
                'sub_title': sub_title,                     # 子标题
                # 'shop_name_url': shop_name_url,            # 店铺主页地址
                'price': price,                             # 商品价格
                'taobao_price': taobao_price,               # 淘宝价
                # 'goods_stock': goods_stock,                # 商品库存
                'detail_name_list': detail_name_list,       # 商品标签属性名称
                # 'detail_value_list': detail_value_list,    # 商品标签属性对应的值
                'price_info_list': price_info_list,         # 要存储的每个标签对应规格的价格及其库存
                'all_img_url': all_img_url,                 # 所有示例图片地址
                'p_info': p_info,                           # 详细信息标签名对应属性
                'div_desc': div_desc,                       # div_desc
                'schedule': schedule,                       # 商品开卖时间和结束开卖时间
                'is_delete': is_delete                      # 用于判断商品是否已经下架
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
            # return {
            #     'is_delete': 1,
            # }
            return {}

    def to_right_and_update_data(self, data, pipeline):
        tmp = _get_right_model_data(data=data, site_id=11)
        params = self._get_db_update_params(item=tmp)
        # 改价格的sql
        # sql_str = r'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, MyShelfAndDownTime=%s, delete_time=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s where GoodsID = %s'
        # 不改价格的sql
        if tmp['delete_time'] == '':
            sql_str = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s, shelf_time=%s where GoodsID = %s'
        elif tmp['shelf_time'] == '':
            sql_str = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s, delete_time=%s where GoodsID = %s'
        else:
            sql_str = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s, shelf_time=%s, delete_time=%s where GoodsID = %s'

        pipeline._update_table(sql_str=sql_str, params=params)

    def _get_div_desc(self, **kwargs):
        '''
        处理detail_data转换成能被html显示页面信息
        :param kwargs:
        :return:
        '''
        detail = kwargs.get('detail')
        goods_id = kwargs.get('goods_id')
        tmp_div_desc = ''
        if isinstance(detail, dict):
            if detail.get('detailImages') is not None:
                for item in detail.get('detailImages', []):
                    tmp_big = item.get('big', '')
                    tmp_height = item.get('height', 0)
                    tmp_width = item.get('width', 0)
                    # tmp = r'<img src="{}" style="height:{}px;width:{}px;"/>'.format(tmp_big, tmp_height, tmp_width)
                    tmp = r'<img src="{}" style="height:auto;width:100%;"/>'.format(tmp_big)
                    tmp_div_desc += tmp

            if detail.get('noticeImage') is not None:
                if isinstance(detail.get('noticeImage'), dict):
                    item = detail.get('noticeImage')
                    tmp_image = item.get('image', '')
                    tmp_height = item.get('height', 0)
                    tmp_width = item.get('width', 0)
                    # tmp = r'<img src="{}" style="height:{}px;width:{}px;"/>'.format(tmp_image, tmp_height, tmp_width)
                    tmp = r'<img src="{}" style="height:auto;width:100%;"/>'.format(tmp_image)
                    tmp_div_desc += tmp
                elif isinstance(detail.get('noticeImage'), list):
                    for item in detail.get('noticeImage', []):
                        tmp_image = item.get('image', '')
                        tmp_height = item.get('height', 0)
                        tmp_width = item.get('width', 0)
                        # tmp = r'<img src="{}" style="height:{}px;width:{}px;"/>'.format(tmp_image, tmp_height, tmp_width)
                        tmp = r'<img src="{}" style="height:auto;width:100%;"/>'.format(tmp_image)
                        tmp_div_desc += tmp
                else:
                    pass

                '''
                处理有尺码的情况(将其加入到div_desc中)
                '''
                tmp_size_url = 'https://th5.m.zhe800.com/app/detail/product/size?productId=' + str(goods_id)
                size_data_body = MyRequests.get_url_body(url=tmp_size_url, headers=self.headers, high_conceal=True)
                if size_data_body == '':
                    print('size_data为空!')
                    return ''

                else:
                    size_data = [size_data_body]

                if size_data != []:
                    size_data = json_2_dict(json_str=size_data[0])
                    if size_data == {}:
                        print('json.loads(size_data)出错, 此处跳过')
                        return ''
                    # pprint(size_data)

                    tmp_div_desc_2 = ''
                    if size_data is not None:
                        charts = size_data.get('charts', [])
                        for item in charts:
                            # print(item)
                            tmp = ''
                            charts_data = item.get('data', [])  # table
                            title = item.get('title', '')
                            for item2 in charts_data:  # item为一个list
                                # print(item2)
                                charts_item = ''
                                for i in item2:  # i为一个dict
                                    # print(i)
                                    data_value = i.get('value', '')
                                    tmp_1 = '<td style="vertical-align:inherit;display:table-cell;font-size:12px;color:#666;border:#666 1px solid;">{}</td>'.format(
                                        data_value)
                                    charts_item += tmp_1
                                charts_item = '<tr style="border:#666 1px solid;">' + charts_item + '</tr>'
                                # print(charts_item)
                                tmp += charts_item
                            tmp = '<div>' + '<strong style="color:#666;">' + title + '</strong>' + '<table style="border-color:grey;border-collapse:collapse;text-align:center;line-height:25px;background:#fff;border-spacing:0;border:#666 1px solid;"><tbody style="border:#666 1px solid;">' + tmp + '</tbody></table></div><br>'
                            tmp_div_desc_2 += tmp
                        # print(tmp_div_desc_2)
                    else:
                        pass
                else:
                    tmp_div_desc_2 = ''

            else:
                tmp_div_desc_2 = ''
                pass
            tmp_div_desc = tmp_div_desc_2 + '<div>' + tmp_div_desc + '</div>'

        return tmp_div_desc

    def _get_shop_name(self, **kwargs):
        '''
        得到shop_name
        '''
        data = kwargs.get('data', {})

        seller_id = data.get('/app/detail/product/base', {}).get('sellerId', 0)
        tmp_seller_id_url = 'https://th5.m.zhe800.com/api/getsellerandswitch?sellerId=' + str(seller_id)
        seller_info_body = MyRequests.get_url_body(url=tmp_seller_id_url, headers=self.headers, high_conceal=True)
        if seller_info_body == '':
            print('seller_info为空!')
            return {}
        else:
            seller_info = [seller_info_body]
        seller_info_str = ''
        for item_ss in seller_info:  # 拼接字符串
            seller_info_str += item_ss

        seller_info = [seller_info_str]
        # print(seller_info)

        if seller_info != []:
            seller_info = json_2_dict(json_str=seller_info[0])
            if seller_info == {}:
                print('卖家信息在转换时出现错误, 此处跳过')
                return {}

            # pprint(seller_info)
            shop_name = seller_info.get('sellerInfo', {}).get('nickName', '')
        else:
            shop_name = ''
        # print(shop_name)

        return shop_name

    def insert_into_zhe_800_xianshimiaosha_table(self, data, pipeline):
        try:
            tmp = _get_right_model_data(data=data, site_id=14)  # 采集来源地(折800秒杀商品)
        except:
            print('此处抓到的可能是折800秒杀券所以跳过')
            return None
        # print('------>>>| 待存储的数据信息为: |', tmp)
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_insert_miaosha_params(item=tmp)
        sql_str = 'insert into dbo.zhe_800_xianshimiaosha(goods_id, goods_url, username, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, schedule, stock_info, miaosha_time, miaosha_begin_time, miaosha_end_time, session_id, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        pipeline._insert_into_table(sql_str=sql_str, params=params)

    def to_update_zhe_800_xianshimiaosha_table(self, data, pipeline):
        try:
            tmp = _get_right_model_data(data=data, site_id=14)
        except:
            print('此处抓到的可能是折800秒杀券所以跳过')
            return None
        print('------>>>| 待存储的数据信息为: {0}'.format(data.get('goods_id')))

        params = self._get_db_update_miaosha_params(item=tmp)
        sql_str = 'update dbo.zhe_800_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, schedule=%s, stock_info=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s where goods_id = %s'
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
            item['session_id'],

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

    def get_goods_id_from_url(self, zhe_800_url):
        '''
        得到goods_id
        :param zhe_800_url:
        :return: goods_id (类型str)
        '''
        is_zhe_800_url = re.compile(r'https://shop.zhe800.com/products/.*?').findall(zhe_800_url)
        if is_zhe_800_url != []:
            if re.compile(r'https://shop.zhe800.com/products/(.*?)\?.*?').findall(zhe_800_url) != []:
                tmp_zhe_800_url = re.compile(r'https://shop.zhe800.com/products/(.*?)\?.*?').findall(zhe_800_url)[0]
                if tmp_zhe_800_url != '':
                    goods_id = tmp_zhe_800_url
                else:
                    zhe_800_url = re.compile(r';').sub('', zhe_800_url)
                    goods_id = re.compile(r'https://shop.zhe800.com/products/(.*?)\?.*?').findall(zhe_800_url)[0]
                print('------>>>| 得到的折800商品id为:', goods_id)
                return goods_id
            else:   # 处理从数据库中取出的数据
                zhe_800_url = re.compile(r';').sub('', zhe_800_url)
                goods_id = re.compile(r'https://shop.zhe800.com/products/(.*)').findall(zhe_800_url)[0]
                print('------>>>| 得到的折800商品id为:', goods_id)
                return goods_id
        else:
            is_miao_sha_url = re.compile(r'https://miao.zhe800.com/products/.*?').findall(zhe_800_url)
            if is_miao_sha_url != []:   # 先不处理这种链接的情况
                if re.compile(r'https://miao.zhe800.com/products/(.*?)\?.*?').findall(zhe_800_url) != []:
                    tmp_zhe_800_url = re.compile(r'https://miao.zhe800.com/products/(.*?)\?.*?').findall(zhe_800_url)[0]
                    if tmp_zhe_800_url != '':
                        goods_id = tmp_zhe_800_url
                    else:
                        zhe_800_url = re.compile(r';').sub('', zhe_800_url)
                        goods_id = re.compile(r'https://miao.zhe800.com/products/(.*?)\?.*?').findall(zhe_800_url)[0]
                    print('------>>>| 得到的限时秒杀折800商品id为:', goods_id)
                    print('由于这种商品开头的量少, 此处先不处理这种开头的')
                    # return goods_id
                    return ''
                else:  # 处理从数据库中取出的数据
                    zhe_800_url = re.compile(r';').sub('', zhe_800_url)
                    goods_id = re.compile(r'https://miao.zhe800.com/products/(.*)').findall(zhe_800_url)[0]
                    print('------>>>| 得到的限时秒杀折800商品id为:', goods_id)
                    print('由于这种商品开头的量少, 此处先不处理这种开头的')
                    # return goods_id
                    return ''
            else:
                print('折800商品url错误, 非正规的url, 请参照格式(https://shop.zhe800.com/products/)开头的...')
                return ''

    def __del__(self):
        gc.collect()

if __name__ == '__main__':
    zhe_800 = Zhe800Parse()
    while True:
        zhe_800_url = input('请输入待爬取的折800商品地址: ')
        zhe_800_url.strip('\n').strip(';')
        goods_id = zhe_800.get_goods_id_from_url(zhe_800_url)
        data = zhe_800.get_goods_data(goods_id=goods_id)
        data = zhe_800.deal_with_data()
        pprint(data)

