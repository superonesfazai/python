# coding:utf-8

'''
@author = super_fazai
@File    : zhe_800_pintuan_parse.py
@Time    : 2017/12/18 09:37
@connect : superonesfazai@gmail.com
'''


"""
折800常规拼团商品页面采集解析系统(官网地址:https://pina.m.zhe800.com)
由于pc版折800没有拼团的页面，只有手机版有，所以是基于手机版的页面采集
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
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

class Zhe800PintuanParse(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'pina.m.zhe800.com',
            'User-Agent': HEADERS[randint(0, 34)],  # 随机一个请求头
            # 'Cookie': 'api_uid=rBQh+FoXerAjQWaAEOcpAg==;',      # 分析发现需要这个cookie值
        }
        self.result_data = {}

    def get_goods_data(self, goods_id):
        '''
        模拟构造得到data的url
        :param goods_id:
        :return: data   类型dict
        '''
        if goods_id == '':
            self.result_data = {}
            return {}
        else:
            tmp_url = 'https://pina.m.zhe800.com/detail/detail.html?zid=' + str(goods_id)
            print('------>>>| 得到的商品手机版地址为: ', tmp_url)

            # 设置代理ip
            self.proxies = self.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
            self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]

            tmp_proxies = {
                'http': self.proxy,
            }
            # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))

            try:
                response = requests.get(tmp_url, headers=self.headers, proxies=tmp_proxies, timeout=10)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
                body = response.content.decode('utf-8')
                # print(body)

                # 过滤
                body = re.compile(r'\n').sub('', body)
                body = re.compile(r'\t').sub('', body)
                body = re.compile(r'  ').sub('', body)
                # print(body)
                data = re.compile(r'window.prod_info = (.*?);seajs.use\(.*?\);</script>').findall(body)  # 贪婪匹配匹配所有
                # print(data)
            except Exception:
                print('requests.get()请求超时....')
                print('body中re匹配到的data为空!')
                self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                return {}

            if data != []:
                data = data[0]
                try:
                    data = json.loads(data)
                except Exception:
                    self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                    return {}
                # pprint(data)

                '''
                得到div_desc的html页面
                '''
                div_desc_url = 'https://pina.m.zhe800.com/nnc/product/detail_content.json?zid=' + str(goods_id)

                div_desc_body = self.get_div_desc_body(div_desc_url=div_desc_url)
                # print(div_desc_body)

                if div_desc_body == '':
                    print('获取到的div_desc_body为空!')
                    return {}

                '''
                获取到详情介绍页面
                '''
                p_info_url = 'https://pina.m.zhe800.com/cns/products/get_product_properties_list.json?productId=' + str(goods_id)
                p_info = self.get_p_info_list(p_info_url=p_info_url)
                # pprint(p_info)

                '''
                获取商品实时库存信息
                '''
                stock_info_url = 'https://pina.m.zhe800.com/cns/products/' + str(goods_id) + '/realtime_info.json'
                stock_info = self.get_stock_info_dict(stock_info_url=stock_info_url)

                if stock_info == {}:
                    print('获取到的库存信息为{}!')
                    return {}
                # pprint(stock_info)

                data['div_desc'] = div_desc_body
                data['p_info'] = p_info
                data['stock_info'] = stock_info

                self.result_data = data
                # pprint(data)
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
            shop_name = data.get('sellerName', '')

            # 商品名称
            title = data.get('title', '')

            # 子标题
            sub_title = data.get('desc', '')
            sub_title = re.compile(r'  ').sub('', sub_title)
            sub_title = re.compile(r'\n').sub('', sub_title)

            # 商品库存
            # 商品标签属性对应的值

            # 商品标签属性名称
            img_name = data.get('sku', {}).get('img_name', '')
            size_name = data.get('sku', {}).get('size_name', '')
            if img_name != '':
                tmp_detail_name_list_1 = [{'spec_name': img_name}]
            else:
                tmp_detail_name_list_1 = []

            if size_name != '':
                tmp_detail_name_list_2 = [{'spec_name': size_name}]
            else:
                tmp_detail_name_list_2 = []

            detail_name_list = tmp_detail_name_list_1 + tmp_detail_name_list_2
            # print(detail_name_list)

            '''
            要存储的每个标签对应规格的价格及其库存
            '''
            if detail_name_list == []:
                print('## detail_name_list为空值 ##')
                price_info_list = []

            else:
                sku_map = data.get('sku', {}).get('sku_map', {})
                # 每个规格的照片
                sku_img_list = [{item.get('pId', '')+'-'+item.get('vId', ''): item.get('vPicture', '')} for item in data.get('sku', {}).get('img_list', [])]
                # pprint(sku_img_list)

                # 规格list
                tmp_sku_map = [value for value in sku_map.values()]
                # pprint(tmp_sku_map)

                # 每个规格的库存list
                sku_stock_info = data.get('stock_info', {}).get('product_sku', {}).get('sku_map', {})
                # pprint(sku_stock_info)

                price_info_list = []
                for item in tmp_sku_map:
                    tmp = {}
                    sku_key = item.get('sku', '')

                    # 处理得到每个规格对应的图片地址
                    tmp_sku_key_1 = sku_key.split(':')[0]
                    img_url = [list(item1.values())[0] for item1 in sku_img_list if tmp_sku_key_1 == list(item1.keys())[0]][0]
                    # print(img_url)

                    # 处理得到每个规格
                    spec_value = item.get('sku_desc', '')                       # 颜色-265咸菜:尺码-180
                    spec_value = spec_value.split(':')                          # ['颜色-265咸菜', '尺码-180']
                    spec_value = [item2.split('-')[1] for item2 in spec_value]  # ['265咸菜', '180']
                    spec_value = '|'.join(spec_value)                           # '265咸菜|180'

                    # 处理得到每个规格对应的库存值
                    tmp_sku_key_2 = sku_key.split(':')
                    tmp_sku_key_2 = [item3.split('-')[1] for item3 in tmp_sku_key_2]
                    tmp_sku_key_2 = ':'.join(tmp_sku_key_2)  # 1011:1108
                    # print(tmp_sku_key_2)
                    rest_number = [sku_stock_info[key] for key in sku_stock_info if tmp_sku_key_2 == key][0]
                    # print(rest_number)

                    if rest_number > 0:
                        # 该规格库存大于0时再进行赋值否则跳过
                        tmp['spec_value'] = spec_value
                        tmp['detail_price'] = str(item.get('pinPrice', ''))
                        tmp['normal_price'] = str(item.get('curPrice', ''))
                        tmp['img_url'] = img_url
                        tmp['rest_number'] = rest_number
                        price_info_list.append(tmp)
                    else:
                        pass

            # 商品价格和淘宝价
            try:
                tmp_price_list = sorted([round(float(item.get('detail_price', '')), 2) for item in price_info_list])
                price = tmp_price_list[-1]  # 商品价格
                taobao_price = tmp_price_list[0]  # 淘宝价
            except:     # 单独处理无规格的商品
                print('此商品无规格!所以我给它单独处理')
                price_info_list = [{
                    'spec_value': '',
                    'detail_price': str(data.get('pin_price', '')),
                    'normal_price': str(data.get('real_cur_price', '')),
                    'img_url': '',
                    'rest_number': 100
                }]
                tmp_price_list = sorted([round(float(item.get('detail_price', '')), 2) for item in price_info_list])
                price = tmp_price_list[-1]  # 商品价格
                taobao_price = tmp_price_list[0]  # 淘宝价

            # print('最高价为: ', price)
            # print('最低价为: ', taobao_price)
            # print(len(price_info_list))
            # pprint(price_info_list)

            # 所有示例图片地址
            all_img_url = [{'img_url': item} for item in data.get('shop_images', [])]
            # pprint(all_img_url)

            # 详细信息标签名对应属性
            p_info = data.get('p_info', [])
            # pprint(p_info)

            # 总销量(shop_sales字段)
            all_sell_count = str(data.get('shop_sales', ''))

            # div_desc
            div_desc = data.get('div_desc', '')

            # 商品销售时间区间(sale_begin_time和sale_end_time字段)
            schedule = [{
                'begin_time': data.get('sale_begin_time', ''),
                'end_time': data.get('sale_end_time', ''),
            }]
            # pprint(schedule)

            # 用于判断商品是否下架
            is_delete = 0
            if schedule != []:
                if data.get('sale_end_time') is not None:
                    end_time = data.get('sale_end_time')
                    try:
                        end_time = int(str(time.mktime(time.strptime(end_time,'%Y-%m-%d %H:%M:%S')))[0:10])
                        # print(end_time)
                    except:
                        print('end_time由str时间转换为时间戳时出错, 此处跳过!')
                        return {}

                    if float(end_time) < time.time():
                        # 结束时间戳小于当前时间戳则表示已经删除无法购买
                        is_delete = 1
            else:
                pass
            # print(is_delete)

            result = {
                'shop_name': shop_name,                 # 店铺名称
                'title': title,                         # 商品名称
                'sub_title': sub_title,                 # 子标题
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

    def insert_into_zhe_800_pintuan_table(self, data, pipeline):
        data_list = data
        tmp = {}
        tmp['goods_id'] = data_list['goods_id']  # 官方商品id
        tmp['spider_url'] = data_list['spider_url']  # 商品地址
        tmp['username'] = data_list['username']  # 操作人员username

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
        tmp['sub_title'] = data_list['sub_title']

        # 设置最高价price， 最低价taobao_price
        try:
            tmp['price'] = Decimal(data_list['price']).__round__(2)
            tmp['taobao_price'] = Decimal(data_list['taobao_price']).__round__(2)
        except:  # 此处抓到的可能是折800拼团券所以跳过
            print('此处抓到的可能是折800拼团券所以跳过')
            return None

        tmp['detail_name_list'] = data_list['detail_name_list']  # 标签属性名称

        """
        得到sku_map
        """
        tmp['price_info_list'] = data_list.get('price_info_list')  # 每个规格对应价格及其库存

        tmp['all_img_url'] = data_list.get('all_img_url')  # 所有示例图片地址
        tmp['all_sell_count'] = data_list.get('all_sell_count')     # 总销量

        tmp['p_info'] = data_list.get('p_info')  # 详细信息
        tmp['div_desc'] = data_list.get('div_desc')  # 下方div

        tmp['schedule'] = data_list.get('schedule')
        tmp['page'] = data_list.get('page')

        # 采集的来源地
        tmp['site_id'] = 17  # 采集来源地(折800拼团商品)

        tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1
        # print('is_delete=', tmp['is_delete'])

        # print('------>>> | 待存储的数据信息为: |', tmp)
        print('------>>> | 待存储的数据信息为: |', tmp.get('goods_id'))

        pipeline.insert_into_zhe_800_pintuan_table(tmp)

    def to_right_and_update_data(self, data, pipeline):
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
        tmp['sub_title'] = data_list['sub_title']

        # 设置最高价price， 最低价taobao_price
        try:
            tmp['price'] = Decimal(data_list['price']).__round__(2)
            tmp['taobao_price'] = Decimal(data_list['taobao_price']).__round__(2)
        except:  # 此处抓到的可能是折800拼团券所以跳过
            print('此处抓到的可能是折800拼团券所以跳过')
            return None

        tmp['detail_name_list'] = data_list['detail_name_list']  # 标签属性名称

        """
        得到sku_map
        """
        tmp['price_info_list'] = data_list.get('price_info_list')  # 每个规格对应价格及其库存

        tmp['all_img_url'] = data_list.get('all_img_url')  # 所有示例图片地址
        tmp['all_sell_count'] = data_list.get('all_sell_count')  # 总销量

        tmp['p_info'] = data_list.get('p_info')  # 详细信息
        tmp['div_desc'] = data_list.get('div_desc')  # 下方div

        tmp['schedule'] = data_list.get('schedule')

        # 采集的来源地
        # tmp['site_id'] = 17  # 采集来源地(折800拼团商品)

        tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1
        # print('is_delete=', tmp['is_delete'])

        # print('------>>>| 待存储的数据信息为: |', tmp)
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        pipeline.update_zhe_800_pintuan_table(tmp)

    def get_div_desc_body(self, div_desc_url):
        '''
        得到div_desc的html页面
        :param div_desc_url:
        :return: str类型的data, 出错的情况下返回{}
        '''
        # 设置代理ip
        self.proxies = self.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]

        tmp_proxies = {
            'http': self.proxy,
        }
        try:
            response = requests.get(div_desc_url, headers=self.headers, proxies=tmp_proxies, timeout=10)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            div_desc_body = response.content.decode('utf-8')
            # print(div_desc_body)

            # 过滤
            div_desc_body = re.compile(r'\n').sub('', div_desc_body)
            div_desc_body = re.compile(r'\t').sub('', div_desc_body)
            div_desc_body = re.compile(r'  ').sub('', div_desc_body)
            # print(div_desc_body)
        except Exception:
            print('requests.get()请求超时....')
            print('div_desc_body中re匹配到的data为空!')
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            div_desc_body = '{}'

        try:
            div_desc_data = json.loads(div_desc_body)
            tmp_body = div_desc_data.get('data', '')
        except Exception:
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            tmp_body = ''

        # 清洗
        tmp_body = re.compile(r'<div class=\"by_deliver\">.*?</div></div>').sub('', tmp_body)
        tmp_body = re.compile(r'src=.*? />').sub('/>', tmp_body)
        tmp_body = re.compile(r'data-url=').sub('src=\"', tmp_body)
        tmp_body = re.compile(r' />').sub('\" style="height:auto;width:100%;"/>', tmp_body)

        if tmp_body != '':
            tmp_body = '<div>' + tmp_body + '</div>'

        return tmp_body

    def get_p_info_list(self, p_info_url):
        '''
        得到详情介绍信息
        :param p_info_url:
        :return: 返回一个list
        '''
        # 设置代理ip
        self.proxies = self.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]

        tmp_proxies = {
            'http': self.proxy,
        }
        try:
            response = requests.get(p_info_url, headers=self.headers, proxies=tmp_proxies, timeout=10)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            p_info_body = response.content.decode('utf-8')
            # print(p_info_body)

            # 过滤
            p_info_body = re.compile(r'\n').sub('', p_info_body)
            p_info_body = re.compile(r'\t').sub('', p_info_body)
            p_info_body = re.compile(r'  ').sub('', p_info_body)
            # print(p_info_body)
        except Exception:
            print('requests.get()请求超时....')
            print('P_info_body中re匹配到的data为空!')
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            p_info_body = '{}'

        try:
            p_info_data = json.loads(p_info_body)
            tmp_p_info = p_info_data.get('perportieslist', [])
        except Exception:
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            tmp_p_info = []

        if tmp_p_info != []:
            p_info = [{
                'p_name': item.get('name', ''),
                'p_value': item.get('value'),
            } for item in tmp_p_info]
        else:
            p_info = tmp_p_info

        return p_info

    def get_stock_info_dict(self, stock_info_url):
        '''
        得到实时库存信息
        :param stock_info_url:
        :return: 返回dict类型
        '''
        # 设置代理ip
        self.proxies = self.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]

        tmp_proxies = {
            'http': self.proxy,
        }
        try:
            response = requests.get(stock_info_url, headers=self.headers, proxies=tmp_proxies, timeout=10)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            stock_info_body = response.content.decode('utf-8')
            # print(stock_info_body)

            # 过滤
            stock_info_body = re.compile(r'\n').sub('', stock_info_body)
            stock_info_body = re.compile(r'\t').sub('', stock_info_body)
            stock_info_body = re.compile(r'  ').sub('', stock_info_body)
            # print(stock_info_body)
        except Exception:
            print('requests.get()请求超时....')
            print('stock_info_body中re匹配到的data为空!')
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            stock_info_body = '{}'

        try:
            stock_info_data = json.loads(stock_info_body)
            tmp_stock_info = stock_info_data.get('data', {})
        except Exception:
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            tmp_stock_info = {}

        return tmp_stock_info

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

    def get_goods_id_from_url(self, zhe_800_pintuan_url):
        '''
        得到goods_id
        :param pinduoduo_url:
        :return: goods_id (类型str)
        '''
        is_zhe_800_pintuan_url = re.compile(r'https://pina.m.zhe800.com/detail/detail.html.*?').findall(zhe_800_pintuan_url)
        if is_zhe_800_pintuan_url != []:
            if re.compile(r'https://pina.m.zhe800.com/detail/detail.html\?.*?zid=ze(\d+).*?').findall(zhe_800_pintuan_url) != []:
                tmp_zhe_800_pintuan_url = 'ze' + re.compile(r'https://pina.m.zhe800.com/detail/detail.html\?.*?zid=ze(\d+).*?').findall(zhe_800_pintuan_url)[0]
                if tmp_zhe_800_pintuan_url != '':
                    goods_id = tmp_zhe_800_pintuan_url
                else:  # 只是为了在pycharm里面测试，可以不加
                    zhe_800_pintuan_url = re.compile(r';').sub('', tmp_zhe_800_pintuan_url)
                    goods_id = re.compile(r'https://pina.m.zhe800.com/detail/detail.html\?.*?zid=ze(\d+).*?').findall(zhe_800_pintuan_url)[0]
                print('------>>>| 得到的折800拼团商品id为:', goods_id)
                return goods_id
            else:
                pass
        else:
            print('折800拼团商品url错误, 非正规的url, 请参照格式(https://pina.m.zhe800.com/detail/detail.htm)开头的...')
            return ''

    def __del__(self):
        gc.collect()

if __name__ == '__main__':
    zhe_800_pintuan = Zhe800PintuanParse()
    while True:
        zhe_800_pintuan_url = input('请输入待爬取的拼多多商品地址: ')
        zhe_800_pintuan_url.strip('\n').strip(';')
        goods_id = zhe_800_pintuan.get_goods_id_from_url(zhe_800_pintuan_url)
        data = zhe_800_pintuan.get_goods_data(goods_id=goods_id)
        zhe_800_pintuan.deal_with_data()
