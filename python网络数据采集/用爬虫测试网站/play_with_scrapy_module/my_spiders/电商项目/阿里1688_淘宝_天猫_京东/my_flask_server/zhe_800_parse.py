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

import time
from random import randint
import json
import requests
import re
from pprint import pprint
from decimal import Decimal
from time import sleep
import datetime
import re
import gc
import pytz

from settings import HEADERS

class Zhe800Parse(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'm.zhe800.com',
            'User-Agent': HEADERS[randint(0, 34)]  # 随机一个请求头
        }
        self.result_data = {}

    def get_goods_data(self, goods_id):
        '''
        模拟构造得到data的url
        :param goods_id:
        :return: data   类型dict
        '''
        if goods_id == '':
            return {}
        else:
            tmp_url = 'https://m.zhe800.com/gateway/app/detail/product?productId=' + str(goods_id)
            # print('------>>>| 得到的detail信息的地址为: ', tmp_url)

            # 设置代理ip
            self.proxies = self.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
            self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]

            tmp_proxies = {
                'http': self.proxy,
            }
            # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))

            try:
                response = requests.get(tmp_url, headers=self.headers, proxies=tmp_proxies, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
                data = response.content.decode('utf-8')
                # print(data)
                data = re.compile(r'(.*)').findall(data)  # 贪婪匹配匹配所有
                # print(data)
            except Exception:
                print('requests.get()请求超时....')
                print('data为空!')
                return {}

            if data != []:
                data = data[0]
                data = json.loads(data)
                # pprint(data)

                # 处理base
                base = data.get('/app/detail/product/base', '')
                try:
                    base = json.loads(base)
                except Exception:
                    print("json.loads转换出错，得到base值可能为空，此处跳过")
                    base = ''
                    pass

                # 处理profiles
                profiles = data.get('/app/detail/product/profiles', '')
                try:
                    profiles = json.loads(profiles)
                except Exception:
                    print("json.loads转换出错，得到profiles值可能为空，此处跳过")
                    profiles = ''
                    pass

                # 处理score
                score = data.get('/app/detail/product/score', '')
                try:
                    score = json.loads(score)
                    try:
                        score.pop('contents')
                    except:
                        pass
                except Exception:
                    print("json.loads转换出错，得到score值可能为空，此处跳过")
                    score = ''
                    pass

                # 处理sku
                sku = data.get('/app/detail/product/sku', '')
                try:
                    sku = json.loads(sku)
                except Exception:
                    print("json.loads转换出错，得到sku值可能为空，此处跳过")
                    sku = ''
                    pass

                data['/app/detail/product/base'] = base
                data['/app/detail/product/profiles'] = profiles
                data['/app/detail/product/score'] = score
                data['/app/detail/product/sku'] = sku

                # 得到手机版地址
                phone_url = 'http://th5.m.zhe800.com/h5/shopdeal?id=' + str(base.get('dealId', ''))
                print('------>>>| 得到商品手机版地址为: ', phone_url)
                print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))

                # 得到并处理detail(即图文详情显示信息)
                # http://m.zhe800.com/gateway/app/detail/graph?productId=
                tmp_detail_url = 'http://m.zhe800.com/gateway/app/detail/graph?productId=' + str(goods_id)
                try:
                    response = requests.get(tmp_detail_url, headers=self.headers, proxies=tmp_proxies, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
                    detail_data = response.content.decode('utf-8')
                    # print(detail_data)
                    detail_data = re.compile(r'(.*)').findall(detail_data)  # 贪婪匹配匹配所有
                    # print(detail_data)
                except Exception:   # 未拿到图文详情就跳出
                    print('requests.get()请求超时....')
                    print('detail_data为空!')
                    return {}

                if detail_data != []:
                    detail_data = detail_data[0]
                    detail_data = json.loads(detail_data)
                    # pprint(detail_data)

                    detail = detail_data.get('/app/detail/graph/detail', '')
                    try:
                        detail = json.loads(detail)
                        try:
                            detail.pop('small')
                        except:
                            pass
                    except:
                        print("json.loads转换出错，得到detail值可能为空，此处跳过")
                        detail = ''
                        pass
                    # print(detail)

                    '''
                    处理detail_data转换成能被html显示页面信息
                    '''
                    tmp_div_desc = ''
                    if isinstance(detail, dict):
                        if detail.get('detailImages') is not None:
                            for item in detail.get('detailImages', []):
                                tmp = ''
                                tmp_big = item.get('big', '')
                                tmp_height = item.get('height', 0)
                                tmp_width = item.get('width', 0)
                                tmp = r'<img src="{}" style="height:{}px;width:{}px;"/>'.format(
                                    tmp_big, tmp_height, tmp_width
                                )
                                tmp_div_desc += tmp

                        if detail.get('noticeImage') is not None:
                            if isinstance(detail.get('noticeImage'), dict):
                                item = detail.get('noticeImage')
                                tmp = ''
                                tmp_image = item.get('image', '')
                                tmp_height = item.get('height', 0)
                                tmp_width = item.get('width', 0)
                                tmp = r'<img src="{}" style="height:{}px;width:{}px;"/>'.format(
                                    tmp_image, tmp_height, tmp_width
                                )
                                tmp_div_desc += tmp
                            elif isinstance(detail.get('noticeImage'), list):
                                for item in detail.get('noticeImage', []):
                                    tmp = ''
                                    tmp_image = item.get('image', '')
                                    tmp_height = item.get('height', 0)
                                    tmp_width = item.get('width', 0)
                                    tmp = r'<img src="{}" style="height:{}px;width:{}px;"/>'.format(
                                        tmp_image, tmp_height, tmp_width
                                    )
                                    tmp_div_desc += tmp
                            else:
                                pass

                            '''
                            处理有尺码的情况(将其加入到div_desc中)
                            '''
                            tmp_size_url = 'https://m.zhe800.com/app/detail/product/size?productId=' + str(goods_id)
                            try:
                                response = requests.get(tmp_size_url, headers=self.headers, proxies=tmp_proxies, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
                                size_data = response.content.decode('utf-8')
                                size_data = re.compile(r'(.*)').findall(size_data)  # 贪婪匹配匹配所有
                                # print(size_data)
                            except Exception:  # 未拿到图文详情就跳出
                                print('requests.get()请求超时....')
                                print('size_data为空!')
                                return {}

                            if size_data != []:
                                size_data = size_data[0]
                                size_data = json.loads(size_data)
                                # pprint(size_data)

                                tmp_div_desc_2 = ''
                                if size_data is not None:
                                    charts = size_data.get('charts', [])
                                    for item in charts:
                                        # print(item)
                                        tmp = ''
                                        charts_data = item.get('data', [])     # table
                                        title = item.get('title', '')
                                        for item2 in charts_data:        # item为一个list
                                            # print(item2)
                                            charts_item = ''
                                            for i in item2:              # i为一个dict
                                                # print(i)
                                                data_value = i.get('value', '')
                                                tmp_1 = '<td style="vertical-align:inherit;display:table-cell;font-size:12px;color:#666;">{}</td>'.format(data_value)
                                                charts_item += tmp_1
                                            charts_item = '<tr style="border-bottom:#333 1px solid;">' + charts_item + '</tr>'
                                            # print(charts_item)
                                            tmp += charts_item
                                        tmp = '<div>' + '<strong style="color:#666;">'+ title + '</strong>' + '<table style="border-color:grey;border-collapse:collapse;text-align:center;line-height:25px;background:#fff;border-spacing:0;" border="1"><tbody>' + tmp + '</tbody></table></div><br>'
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

                    # print(tmp_div_desc)
                    data['/app/detail/graph/detail'] = tmp_div_desc

                    '''
                    得到shop_name
                    '''
                    seller_id = data.get('/app/detail/product/base', {}).get('sellerId', 0)
                    tmp_seller_id_url = 'https://m.zhe800.com/api/getsellerandswitch?sellerId=' + str(seller_id)

                    try:
                        response = requests.get(tmp_seller_id_url, headers=self.headers, proxies=tmp_proxies, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
                        seller_info = response.content.decode('utf-8')
                        seller_info = re.compile(r'(.*)').findall(seller_info)  # 贪婪匹配匹配所有
                        # print(seller_info)
                    except Exception:  # 未拿到图文详情就跳出
                        print('requests.get()请求超时....')
                        print('seller_info为空!')
                        return {}

                    if seller_info != []:
                        seller_info = seller_info[0]
                        seller_info = json.loads(seller_info)
                        # pprint(seller_info)
                        shop_name = seller_info.get('sellerInfo', {}).get('nickName', '')
                    else:
                        shop_name = ''
                    # print(shop_name)
                    data['shop_name'] = shop_name

                    '''
                    得到秒杀开始时间和结束时间
                    '''
                    schedule_and_stock_url = 'https://m.zhe800.com/gateway/app/detail/status?productId=' + str(goods_id)
                    try:
                        response = requests.get(schedule_and_stock_url, headers=self.headers, proxies=tmp_proxies, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
                        schedule_and_stock_info = response.content.decode('utf-8')
                        schedule_and_stock_info = re.compile(r'(.*)').findall(schedule_and_stock_info)  # 贪婪匹配匹配所有
                        # print(schedule_and_stock_info)
                    except Exception:  # 未拿到图文详情就跳出
                        print('requests.get()请求超时....')
                        print('schedule_and_stock_info为空!')
                        return {}

                    if schedule_and_stock_info != []:
                        schedule_and_stock_info = schedule_and_stock_info[0]
                        schedule_and_stock_info = json.loads(schedule_and_stock_info)

                        schedule = schedule_and_stock_info.get('/app/detail/status/schedule')
                        if schedule is None:
                            schedule = {}
                        else:
                            schedule = json.loads(schedule)

                        stock = schedule_and_stock_info.get('/app/detail/status/stock')
                        if stock is None:
                            stock = {}
                        else:
                            stock = json.loads(stock)
                    else:
                        schedule = {}
                        stock = {}
                    data['schedule'] = schedule
                    data['stock'] = stock

                    pprint(data)
                    self.result_data = data
                    return data

                else:
                    print('detail_data为空!')
                    return {}

            else:
                print('data为空!')
                return {}

    def deal_with_data(self):
        '''
        处理result_data, 返回需要的信息
        :return: 字典类型
        '''
        """
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
            'div_desc': div_desc,                               # div_desc
            'is_delete': is_delete                              # 用于判断商品是否已经下架
        }
        """
        data = self.result_data
        if data != {}:
            # 店铺名称
            shop_name = data.get('shop_name', '')

            # 掌柜
            account = ''

            # 商品名称
            title = data.get('/app/detail/product/base', {}).get('title', '')

            # 子标题
            sub_title = ''

            # 商品价格
            # 淘宝价


            # 商品库存


            # 商品标签属性对应的值

            # 要存储的每个标签对应规格的价格及其库存
            tmp_price_info_list = data.get('/app/detail/product/sku', {}).get('items')
            # pprint(tmp_price_info_list)
            if tmp_price_info_list is None:     # 说明没有规格属性
                detail_name_list = []
                price_info_list = []
            else:                               # 有规格属性
                for index in range(1, len(tmp_price_info_list)-1):
                    # 商品标签属性名称
                    detail_name_list = [{'spec_name': item.split('-')[0]} for item in tmp_price_info_list[index].get('propertyName').split(':')]
                    property_num = tmp_price_info_list[index].get('propertyNum', '')
                    stock_items = data.get('stock', {}).get('stockItems')
                    if stock_items is None:
                        pass
                    else:
                        pass

            # print(detail_name_list)

            # 所有示例图片地址
            tmp_all_img_url = data.get('/app/detail/product/base', {}).get('images', [])
            all_img_url = [{'img_url': item['big']} for item in tmp_all_img_url]
            # pprint(all_img_url)

            # 详细信息标签名对应属性
            profiles = data.get('/app/detail/product/profiles', {}).get('profiles')
            if profiles is None:
                p_info = []
            else:
                p_info = [{'p_name': item['name'], 'p_value': item['value']} for item in profiles]
            # pprint(p_info)

            # div_desc
            div_desc = data.get('/app/detail/graph/detail', '')

            # 用于判断商品是否已经下架
            is_delete = 0


        else:
            print('待处理的data为空的dict, 该商品可能已经转移或者下架')
            # return {
            #     'is_delete': 1,
            # }
            return {}

    def get_proxy_ip_from_ip_pool(self):
        '''
        从代理ip池中获取到对应ip
        :return: dict类型 {'http': ['http://183.136.218.253:80', ...]}
        '''
        base_url = 'http://127.0.0.1:8000'
        result = requests.get(base_url).json()

        result_ip_list = {}
        result_ip_list['http'] = []
        for item in result:
            if item[2] > 7:
                tmp_url = 'http://' + str(item[0]) + ':' + str(item[1])
                result_ip_list['http'].append(tmp_url)
            else:
                delete_url = 'http://127.0.0.1:8000/delete?ip='
                delete_info = requests.get(delete_url + item[0])
        # pprint(result_ip_list)
        return result_ip_list

    def get_goods_id_from_url(self, zhe_800_url):
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
        zhe_800.deal_with_data()
        # pprint(data)

