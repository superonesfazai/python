# coding:utf-8

'''
@author = super_fazai
@File    : taobao_parse.py
@Time    : 2017/10/25 07:40
@connect : superonesfazai@gmail.com
'''

"""
可爬取淘宝，全球购
"""

import time
from random import randint
import json
import requests
import re
from pprint import pprint
from decimal import Decimal
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import selenium.webdriver.support.ui as ui
# from selenium.webdriver.common.proxy import Proxy
# from selenium.webdriver.common.proxy import ProxyType
# from scrapy import Selector
# from urllib.request import urlopen
# from PIL import Image
from time import sleep
import datetime
import gc
# import pycurl
# from io import StringIO
# import traceback
# from io import BytesIO

from settings import TAOBAO_COOKIES_FILE_PATH, HEADERS
from settings import PHANTOMJS_DRIVER_PATH, CHROME_DRIVER_PATH
import pytz

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

# chrome驱动地址
my_chrome_driver_path = CHROME_DRIVER_PATH

class TaoBaoLoginAndParse(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'acs.m.taobao.com',
            'User-Agent': HEADERS[randint(0, 34)]      # 随机一个请求头
        }
        self.result_data = {}

    def get_goods_data(self, goods_id):
        '''
        模拟构造得到data的url
        :param goods_id:
        :return: data   类型dict
        '''
        """     这些是url的参数
        appKey = '12574478'
        t = str(time.time().__round__()) + str(randint(100, 999))    # time.time().__round__() 表示保留到个位
        # sign = '24b2e987fce9c84d2fc0cebd44be49ef'     # sign可以为空
        api = 'mtop.taobao.detail.getdetail'
        v = '6.0'
        ttid = '2016@taobao_h5_2.0.0'
        isSec = str(0)
        ecode = str(0)
        AntiFlood = 'true'
        AntiCreep = 'true'
        H5Request = 'true'
        type = 'jsonp'
        callback = 'mtopjsonp1'
        """

        appKey = '12574478'
        t = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位

        '''
        下面是构造params
        '''
        goods_id = goods_id
        # print(goods_id)
        params_data_1 = {
            'id': goods_id
        }
        params_data_2 = {
            'exParams': json.dumps(params_data_1),  # 每层里面的字典都要先转换成json
            'itemNumId': goods_id
        }
        # print(params_data_2)
        params = {
            'data': json.dumps(params_data_2)  # 每层里面的字典都要先转换成json
        }

        ### * 注意这是正确的url地址: right_url = 'https://acs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1508886442888&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2016%40taobao_h5_2.0.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22exParams%22%3A%22%7B%5C%22id%5C%22%3A%5C%22546756179626%5C%22%7D%22%2C%22itemNumId%22%3A%22546756179626%22%7D'
        # right_url = 'https://acs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1508886442888&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2016%40taobao_h5_2.0.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22exParams%22%3A%22%7B%5C%22id%5C%22%3A%5C%22546756179626%5C%22%7D%22%2C%22itemNumId%22%3A%22546756179626%22%7D'
        # right_url = 'https://acs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1508857184835&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2016%40taobao_h5_2.0.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22exParams%22%3A%22%7B%5C%22id%5C%22%3A%5C%2241439519931%5C%22%7D%22%2C%22itemNumId%22%3A%2241439519931%22%7D'
        # print(right_url)

        tmp_url = "https://acs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey={}&t={}&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2016%40taobao_h5_2.0.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1".format(
            appKey, t
        )

        # 设置代理ip
        self.proxies = self.get_proxy_ip_from_ip_pool()     # {'http': ['xx', 'yy', ...]}
        self.proxy = self.proxies['http'][randint(0, len(self.proxies)-1)]

        tmp_proxies = {
            'http': self.proxy,
        }
        # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))

        try:
            response = requests.get(tmp_url, headers=self.headers, params=params, proxies=tmp_proxies, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            last_url = re.compile(r'\+').sub('', response.url)  # 转换后得到正确的url请求地址
            # print(last_url)
            response = requests.get(last_url, headers=self.headers, proxies=tmp_proxies, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            data = response.content.decode('utf-8')
            # print(data)
            data = re.compile(r'mtopjsonp1\((.*)\)').findall(data)  # 贪婪匹配匹配所有
            # print(data)
        except Exception:
            print('requests.get()请求超时....')
            print('data为空!')
            return {}

        if data != []:
            data = data[0]
            data = json.loads(data)
            # pprint(data)

            # 处理商品被转移或者下架导致页面不存在的商品
            if data.get('data').get('seller', {}).get('evaluates') is None:
                print('data为空, 地址被重定向, 该商品可能已经被转移或下架')
                return {}

            data['data']['rate'] = ''           # 这是宝贝评价
            data['data']['resource'] = ''       # 买家询问别人
            data['data']['vertical'] = ''       # 也是问和回答
            data['data']['seller']['evaluates'] = ''  # 宝贝描述, 卖家服务, 物流服务的评价值...
            result_data = data['data']

            # 处理result_data['apiStack'][0]['value']
            # print(result_data.get('apiStack', [])[0].get('value', ''))
            result_data_apiStack_value = result_data.get('apiStack', [])[0].get('value', {})
            try:
                result_data_apiStack_value = json.loads(result_data_apiStack_value)

                result_data_apiStack_value['vertical'] = ''
                result_data_apiStack_value['consumerProtection'] = ''  # 7天无理由退货
                result_data_apiStack_value['feature'] = ''
                result_data_apiStack_value['layout'] = ''
                result_data_apiStack_value['delivery'] = ''     # 发货地到收到地
                result_data_apiStack_value['resource'] = ''     # 优惠券
                result_data_apiStack_value['item'] = ''
                # pprint(result_data_apiStack_value)
            except Exception:
                print("json.loads转换出错，得到result_data['apiStack'][0]['value']值可能为空，此处跳过")
                result_data_apiStack_value = ''
                pass

            # 将处理后的result_data['apiStack'][0]['value']重新赋值给result_data['apiStack'][0]['value']
            result_data['apiStack'][0]['value'] = result_data_apiStack_value

            # 处理mockData
            mock_data = result_data['mockData']
            mock_data = json.loads(mock_data)
            mock_data['feature'] = ''
            # pprint(mock_data)
            result_data['mockData'] = mock_data

            # print(result_data.get('apiStack', [])[0])   # 可能会有{'name': 'esi', 'value': ''}的情况
            if result_data.get('apiStack', [])[0].get('value', '') == '':
                print("result_data.get('apiStack', [])[0].get('value', '')的值为空....")
                result_data['trade'] = {}
                return {}
            else:
                result_data['trade'] = result_data.get('apiStack', [])[0].get('value', {}).get('trade', {})     # 用于判断该商品是否已经下架的参数
                # pprint(result_data['trade'])

            self.result_data = result_data
            # pprint(self.result_data)
            return result_data
        else:
            print('data为空!')
            return {}

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
            # print(tmp_taobao_price)
            if len(tmp_taobao_price) == 1:
                # 商品最高价
                # price = Decimal(tmp_taobao_price[0]).__round__(2)     # json不能处理decimal所以后期存的时候再处理
                price = tmp_taobao_price[0]
                # 商品最低价
                taobao_price = price
                # print(price)
                # print(taobao_price)
            else:
                # price = Decimal(tmp_taobao_price[1]).__round__(2)
                # taobao_price = Decimal(tmp_taobao_price[0]).__round__(2)
                price = tmp_taobao_price[1]
                taobao_price = tmp_taobao_price[0]
                # print(price)
                # print(taobao_price)

            # 淘宝价
            # taobao_price = data['apiStack'][0]['value']['price']['price']['priceText']
            # taobao_price = Decimal(taobao_price).__round__(2)

            # 商品库存
            goods_stock = data['apiStack'][0]['value'].get('skuCore', {}).get('sku2info', {}).get('0', {}).get('quantity', '')

            # 商品标签属性名称,及其对应id值
            if data.get('skuBase') is not None:
                if data.get('skuBase').get('props') is not None:
                    detail_name_list = [[item['name'],item['pid']] for item in data['skuBase']['props']]
                    # print(detail_name_list)

                    # 商品标签属性对应的值, 及其对应id值
                    tmp_detail_value_list = [item['values'] for item in data['skuBase']['props']]
                    # print(tmp_detail_value_list)
                    detail_value_list = []
                    for item in tmp_detail_value_list:
                        tmp = [[i['name'], i['vid']] for i in item]
                        # print(tmp)
                        detail_value_list.append(tmp)       # 商品标签属性对应的值
                    # pprint(detail_value_list)
                else:
                    detail_name_list = []
                    detail_value_list = []
            else:
                detail_name_list = []
                detail_value_list = []

            '''
            每个标签对应值的价格及其库存
            '''
            if data.get('skuBase').get('skus') is not None:
                skus = data['skuBase']['skus']      # 里面是所有规格的可能值[{'propPath': '20105:4209035;1627207:1710113203;5919063:3266779;122216431:28472', 'skuId': '3335554577910'}, ...]
                sku2_info = data['apiStack'][0].get('value').get('skuCore').get('sku2info')
                try:
                    sku2_info.pop('0')      # 此处删除总库存的值
                except Exception:
                    pass
                # pprint(sku2_info)
                prop_path_list = []     # 要存储的每个标签对应规格的价格及其库存
                for key in sku2_info:
                    tmp = {}
                    tmp_prop_path_list = [item for item in skus if item.get('skuId') == key]    # [{'skuId': '3335554577923', 'propPath': '20105:4209035;1627207:1710113207;5919063:3266781;122216431:28473'}]

                    # 处理propPath得到可识别的文字
                    prop_path = tmp_prop_path_list[0].get('propPath')
                    prop_path = prop_path.split(';')
                    prop_path = [i.split(':') for i in prop_path]
                    prop_path = [j[1] for j in prop_path]           # 是每个属性对应的vid值(是按顺序来的)['4209035', '1710113207', '3266781', '28473']
                    # print(prop_path)

                    for index in range(0, len(prop_path)):      # 将每个值对应转换为具体规格
                        for i in detail_value_list:
                            for j in i:
                                if prop_path[index] == j[1]:
                                    prop_path[index] = j[0]
                    # print(prop_path)                  # 其格式为  ['32GB', '【黑色主机】【红 /  蓝 手柄】', '套餐二', '港版']
                    # 再转换为要存储的字符串
                    prop_path = '|'.join(prop_path)     # 其规格为  32GB|【黑色主机】【红 /  蓝 手柄】|套餐二|港版
                    # print(prop_path)

                    tmp_prop_path_list[0]['sku_price'] = sku2_info[key]['price']['priceText']
                    tmp_prop_path_list[0]['quantity'] = sku2_info[key]['quantity']
                    # tmp['sku_id'] = tmp_prop_path_list[0]['skuId']      # skuId是定位值，由于不需要就给它注释了
                    # tmp['prop_path'] = tmp_prop_path_list[0]['propPath']
                    tmp['spec_value'] = prop_path
                    tmp['detail_price'] = tmp_prop_path_list[0]['sku_price']       # 每个规格对应的价格
                    tmp['rest_number'] = tmp_prop_path_list[0]['quantity']         # 每个规格对应的库存量
                    prop_path_list.append(tmp)
                # pprint(prop_path_list)                  # 其格式为  [{'sku_id': '3335554577923', 'prop_path': '32GB|【黑色主机】【红 /  蓝 手柄】|套餐二|港版', 'sku_price': '2740', 'quantity': '284'}, ...]
                price_info_list = prop_path_list
            else:
                price_info_list = []

            # 所有示例图片地址
            tmp_all_img_url = data['item']['images']
            all_img_url = []
            for item in tmp_all_img_url:
                item = 'https:' + item
                all_img_url.append(item)
            all_img_url = [{'img_url': item} for item in all_img_url]
            # print(all_img_url)

            # 详细信息p_info
            tmp_p_info = data.get('props').get('groupProps')     # 一个list [{'内存容量': '32GB'}, ...]
            if tmp_p_info is not None:
                tmp_p_info = tmp_p_info[0].get('基本信息', [])
                p_info = []
                for item in tmp_p_info:
                    for key, value in item.items():
                        tmp = {}
                        tmp['p_name'] = key
                        tmp['p_value'] = value
                        tmp['id'] = '0'
                        p_info.append(tmp)
                # print(p_info)
            else:
                p_info = []

            '''
            下方div图片文字介绍区
            '''
            # 手机端描述地址
            if data.get('item').get('taobaoDescUrl') is not None:
                phone_div_url = 'https:' + data['item']['taobaoDescUrl']
            else:
                phone_div_url = ''

            # pc端描述地址
            if data.get('item').get('taobaoPcDescUrl') is not None:
                pc_div_url = 'https:' + data['item']['taobaoPcDescUrl']
                # print(phone_div_url)
                # print(pc_div_url)

                # self.init_chrome_driver()
                # self.from_ip_pool_set_proxy_ip_to_chrome_driver()
                # div_desc = self.deal_with_div(pc_div_url)
                div_desc = self.get_div_from_pc_div_url(pc_div_url, goods_id)
                # print(div_desc)

                # self.driver.quit()
                gc.collect()
            else:
                pc_div_url = ''
                div_desc = ''

            '''
            后期处理
            '''
            tmp = []
            tmp_1 = []
            # 后期处理detail_name_list, detail_value_list
            detail_name_list = [{'spec_name': i[0]} for i in detail_name_list]

            # 商品标签属性对应的值, 及其对应id值
            if data.get('skuBase').get('props') is None:
                pass
            else:
                tmp_detail_value_list = [item['values'] for item in data.get('skuBase', '').get('props', '')]
                # print(tmp_detail_value_list)
                detail_value_list = []
                for item in tmp_detail_value_list:
                    tmp = [i['name'] for i in item]
                    # print(tmp)
                    detail_value_list.append(tmp)  # 商品标签属性对应的值
                    # pprint(detail_value_list)

            # 1. 先通过buyEnable字段来判断商品是否已经下架
            if data.get('trade', {}) != {}:
                is_buy_enable = data.get('trade', {}).get('buyEnable')
                if is_buy_enable == 'true':
                    is_delete = 0
                else:
                    is_delete = 1
            else:
                is_delete = 0
                pass

            # 2. 此处再考虑名字中显示下架的商品
            if re.compile(r'下架').findall(title) != []:
                if re.compile(r'待下架').findall(title) != []:
                    is_delete = 0
                elif re.compile(r'自动下架').findall(title) != []:
                    is_delete = 0
                else:
                    is_delete = 1
            print('is_delete = %d' % is_delete)

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
                'is_delete': is_delete                              # 用于判断商品是否已经下架
            }
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
        '''
        实时更新数据
        :param data:
        :param pipeline:
        :return:
        '''
        data_list = data
        tmp = {}
        tmp['goods_id'] = data_list['goods_id']  # 官方商品id
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

        # tmp['deal_with_time'] = now_time  # 操作时间
        tmp['modfiy_time'] = now_time  # 修改时间

        tmp['shop_name'] = data_list['shop_name']  # 公司名称
        tmp['title'] = data_list['title']  # 商品名称
        tmp['sub_title'] = data_list['sub_title']  # 商品子标题
        tmp['link_name'] = ''  # 卖家姓名
        tmp['account'] = data_list['account']  # 掌柜名称

        # 设置最高价price， 最低价taobao_price
        tmp['price'] = Decimal(data_list['price']).__round__(2)
        tmp['taobao_price'] = Decimal(data_list['taobao_price']).__round__(2)
        tmp['price_info'] = []  # 价格信息

        tmp['detail_name_list'] = data_list['detail_name_list']  # 标签属性名称

        """
        得到sku_map
        """
        tmp['price_info_list'] = data_list.get('price_info_list')  # 每个规格对应价格及其库存

        tmp['all_img_url'] = data_list.get('all_img_url')  # 所有示例图片地址

        tmp['p_info'] = data_list.get('p_info')  # 详细信息
        tmp['div_desc'] = data_list.get('div_desc')  # 下方div

        # 采集的来源地
        # tmp['site_id'] = 1  # 采集来源地(淘宝)
        tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1

        pipeline.update_taobao_table(tmp)

    def get_div_from_pc_div_url(self, url, goods_id):
        '''
        根据pc描述的url模拟请求获取描述的div
        :return: str
        '''
        '''
        appKey:12574478
        t:1509513791232
        api:mtop.taobao.detail.getdesc
        v:6.0
        type:jsonp
        dataType:jsonp
        timeout:20000
        callback:mtopjsonp1
        data:{"id":"546818961702","type":"1"}
        '''
        appKey = '12574478'
        t = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位

        '''
        下面是构造params
        '''
        goods_id = goods_id
        # print(goods_id)
        params_data_1 = {
            'id': goods_id,
            'type': '1',
        }

        # print(params_data_2)
        params = {
            'data': json.dumps(params_data_1)  # 每层里面的字典都要先转换成json
        }

        tmp_url = 'https://api.m.taobao.com/h5/mtop.taobao.detail.getdesc/6.0/?appKey={}&t={}&api=mtop.taobao.detail.getdesc&v=6.0&type=jsonp&dataType=jsonp&timeout=20000&callback=mtopjsonp1'.format(
            appKey, t
        )

        tmp_proxies = {
            'http': self.proxy,
        }
        # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))

        # 设置2层避免报错退出
        try:
            response = requests.get(tmp_url, headers=self.headers, params=params, proxies=tmp_proxies, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
        except Exception:
            # 设置代理ip
            self.proxies = self.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
            self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]

            tmp_proxies = {
                'http': self.proxy,
            }
            response = requests.get(tmp_url, headers=self.headers, params=params, proxies=tmp_proxies, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造

        last_url = re.compile(r'\+').sub('', response.url)      # 转换后得到正确的url请求地址
        # print(last_url)
        try:
            response = requests.get(last_url, headers=self.headers, proxies=tmp_proxies, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
        except Exception:
            self.proxies = self.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
            self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]

            tmp_proxies = {
                'http': self.proxy,
            }
            response = requests.get(last_url, headers=self.headers, proxies=tmp_proxies, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造

        data = response.content.decode('utf-8')
        # print(data)
        data = re.compile(r'mtopjsonp1\((.*)\)').findall(data)  # 贪婪匹配匹配所有
        if data != []:
            data = data[0]
            data = json.loads(data)

            if data != []:
                div = data.get('data', '').get('pcDescContent', '')
                div = self.deal_with_div(div)
                # print(div)
            else:
                div = ''
        else:
            div = ''

        return div
    """
    def init_chrome_driver(self):
        '''
        初始化chromedriver驱动
        :return:
        '''
        # 设置无运行界面版chrome, 测试发现淘宝过滤了phantomjs, 所有此处不用
        print('--->>>初始化chromedriver驱动中<<<---')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')

        # 注意：测试发现还是得设置成加载图片要不然就无法得到超5张的示例图片完整地址
        # 设置chrome不加载图片
        prefs = {
            'profile.managed_default_content_settings.images': 2,
        }
        chrome_options.add_experimental_option('prefs', prefs)
        # chrome_options.add_argument('--proxy-server=http://183.136.218.253:80')

        self.driver = webdriver.Chrome(executable_path=my_chrome_driver_path, chrome_options=chrome_options)

        print('--->>>初始化化完毕<<<---')
        # self.driver.get('http://httpbin.org/ip')
        # print(self.driver.page_source)
        # self.driver.get('https://www.baidu.com')

        # print('--->>>初始化phantomjs驱动中<<<---')
        # cap = webdriver.DesiredCapabilities.PHANTOMJS
        # cap['phantomjs.page.settings.resourceTimeout'] = 1000  # 1秒
        # cap['phantomjs.page.settings.loadImages'] = False
        # cap['phantomjs.page.settings.disk-cache'] = True
        # cap['phantomjs.page.settings.userAgent'] = HEADERS[randint(0, 34)]  # 随机一个请求头
        # # cap['phantomjs.page.customHeaders.Cookie'] = cookies
        # tmp_execute_path = EXECUTABLE_PATH
        #
        # self.driver = webdriver.PhantomJS(executable_path=tmp_execute_path, desired_capabilities=cap)
        #
        # wait = ui.WebDriverWait(self.driver, 10)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
        # print('------->>>初始化完毕<<<-------')
    """

    def deal_with_div(self, div):
        body = div

        # 过滤
        body = re.compile(r'\n').sub('', body)
        body = re.compile(r'\t').sub('', body)
        body = re.compile(r'  ').sub('', body)
        # print(body)

        body = re.compile(r'src="data:image/png;.*?"').sub('', body)
        body = re.compile(r'data-img').sub('src', body)
        body = re.compile(r'https:').sub('', body)
        body = re.compile(r'src="').sub('src=\"https:', body)
        body = re.compile(r'&nbsp;').sub(' ', body)

        return body

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

    def get_goods_id_from_url(self, taobao_url):
        # https://item.taobao.com/item.htm?id=546756179626&ali_trackid=2:mm_110421961_12506094_47316135:1508678840_202_1930444423&spm=a21bo.7925826.192013.3.57586cc65hdN2V
        is_taobao_url = re.compile(r'https://item.taobao.com/item.htm.*?').findall(taobao_url)
        if is_taobao_url != []:
            if re.compile(r'https://item.taobao.com/item.htm.*?id=(\d+)&{0,20}.*?').findall(taobao_url) != []:
                tmp_taobao_url = re.compile(r'https://item.taobao.com/item.htm.*?id=(\d+)&{0,20}.*?').findall(taobao_url)[0]
                # print(tmp_taobao_url)
                if tmp_taobao_url != []:
                    goods_id = tmp_taobao_url
                else:
                    taobao_url = re.compile(r';').sub('', taobao_url)
                    goods_id = re.compile(r'https://item.taobao.com/item.htm.*?id=(\d+)').findall(taobao_url)[0]
                print('------>>>| 得到的淘宝商品id为:', goods_id)
                return goods_id
            else:       # 处理存数据库中取出的如: https://item.taobao.com/item.htm?id=560164926470
                print('9999')
                taobao_url = re.compile(r';').sub('', taobao_url)
                goods_id = re.compile(r'https://item.taobao.com/item.htm\?id=(\d+)&{0,20}.*?').findall(taobao_url)[0]
                print('------>>>| 得到的淘宝商品id为:', goods_id)
                return goods_id
        else:
            print('淘宝商品url错误, 非正规的url, 请参照格式(https://item.taobao.com/item.htm)开头的...')
            return ''

    def __del__(self):
        # self.driver.quit()
        gc.collect()

if __name__ == '__main__':
    login_taobao = TaoBaoLoginAndParse()
    while True:
        taobao_url = input('请输入待爬取的淘宝商品地址: ')
        taobao_url.strip('\n').strip(';')
        goods_id = login_taobao.get_goods_id_from_url(taobao_url)
        data = login_taobao.get_goods_data(goods_id=goods_id)
        login_taobao.deal_with_data(goods_id=goods_id)
        # pprint(data)





