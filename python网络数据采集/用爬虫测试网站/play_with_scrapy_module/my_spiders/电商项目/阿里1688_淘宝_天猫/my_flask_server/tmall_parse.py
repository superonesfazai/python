# coding:utf-8

'''
@author = super_fazai
@File    : tmall_parse.py
@Time    : 2017/10/26 22:53
@connect : superonesfazai@gmail.com
'''

"""
tmall爬虫能对应爬取解析对象为: (天猫, 天猫超市, 天猫国际)
"""

import time
from random import randint
import json
import requests
import re
from pprint import pprint
from decimal import Decimal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
from scrapy import Selector
from urllib.request import urlopen
from PIL import Image
from time import sleep
import gc

from settings import PHANTOMJS_DRIVER_PATH, HEADERS

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

class TmallParse(object):
    def __init__(self):
        self.result_data = {}

        """
        初始化带cookie的驱动，之所以用phantomjs是因为其加载速度很快(快过chrome驱动太多)
        """
        '''
        研究发现, 必须以浏览器的形式进行访问才能返回需要的东西
        常规requests模拟请求会被天猫服务器过滤, 并返回请求过于频繁的无用页面
        '''
        print('--->>>初始化phantomjs驱动中<<<---')
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap['phantomjs.page.settings.resourceTimeout'] = 1000  # 1秒
        cap['phantomjs.page.settings.loadImages'] = False
        cap['phantomjs.page.settings.disk-cache'] = True
        cap['phantomjs.page.settings.userAgent'] = HEADERS[randint(0, 34)]      # 随机一个请求头
        # cap['phantomjs.page.customHeaders.Cookie'] = cookies
        tmp_execute_path = EXECUTABLE_PATH
        self.driver = webdriver.PhantomJS(executable_path=tmp_execute_path, desired_capabilities=cap)
        # self.driver.set_window_size(1200, 2000)      # 设置默认大小，避免默认大小显示
        wait = ui.WebDriverWait(self.driver, 6)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
        print('------->>>初始化完毕<<<-------')

    def get_goods_data(self, goods_id):
        '''
        得到data
        :param goods_id:
        :return: data   类型dict
        '''
        type = list(goods_id.keys())[0]             # 天猫类型
        goods_id = list(goods_id.values())[0]       # 天猫goods_id
        tmp_url = 'https://detail.m.tmall.com/item.htm?id=' + str(goods_id)
        print('------>>>| 得到的移动端地址为: ', tmp_url)

        # response = requests.get(tmp_url, headers=self.headers)
        self.driver.set_page_load_timeout(12)
        try:
            self.driver.get(tmp_url)
            self.driver.implicitly_wait(12)  # 隐式等待和显式等待可以同时使用

            locator = (By.CSS_SELECTOR, 'div#J_mod4')
            try:
                WebDriverWait(self.driver, 12, 0.5).until(EC.presence_of_element_located(locator))
            except Exception as e:
                print('遇到错误: ', e)
                return 4041  # 未得到div#mod-detail-bd，返回4041
            else:
                print('div#mod-detail-bd已经加载完毕')
        except Exception as e:  # 如果超时, 终止加载并继续后续操作
            print('-->>time out after 12 seconds when loading page')
            self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            # pass
        body = self.driver.page_source
        body = re.compile(r'\n').sub('', body)
        body = re.compile(r'\t').sub('', body)
        body = re.compile(r'  ').sub('', body)
        # print(body)

        body_1 = re.compile(r'var _DATA_Detail = (.*?);</script>').findall(body)
        body_2 = re.compile(r'{"addressData"(.*?)</script>').findall(body)
        if body_1 != []:
            data = body_1[0]
            data = json.loads(data)
            data['detailDesc'] = ''
            data['modules'] = ''
            data['seller']['evaluates'] = ''
            data['tabBar'] = ''
            data['tags'] = ''
            data['traceDatas'] = ''
            data['jumpUrl'] = ''
            # pprint(data)

            if body_2 != []:
                data_2 = '{"addressData"' + body_2[0]
                data_2 = json.loads(data_2)
                data_2['delivery'] = ''
                data_2['consumerProtection'] = ''
                data_2['feature'] = ''
                data_2['layout'] = ''
                data_2['modules'] = ''
                data_2['vertical'] = ''
                data_2['weappData'] = ''
                data_2['item'] = ''
                data_2['otherInfo'] = ''
                data_2['price']['shopProm'] = ''
                data_2['resource'] = ''
                # pprint(data_2)
            else:
                data_2 = {}
            data['extra_data'] = data_2
            data['type'] = type             # 天猫类型
            # pprint(data)
            self.result_data = data
            return data

        else:
            print('获取到的data为空!')
            return {}

    def deal_with_data(self):
        '''
        处理result_data, 返回需要的信息
        :return: 字典类型
        '''
        data = self.result_data
        if data != {}:
            # 天猫类型
            type = data.get('type', 33)     # 33用于表示无法正确获取

            # 店铺名称
            shop_name = data.get('seller', {}).get('shopName', '')

            # 掌柜
            account = data.get('seller', {}).get('sellerNick', '')

            # 商品名称
            title = data.get('item', {}).get('title', '')

            # 子标题
            sub_title = data.get('item', {}).get('subtitle', '')
            sub_title = re.compile(r'\n').sub('', sub_title)

            # 店铺主页地址
            # shop_name_url = data['seller'].get('shopUrl', '')
            # shop_name_url = re.compile(r'.m.').sub('.', shop_name_url)

            # 商品价格
            price_1 = data.get('extra_data', {}).get('price', {}).get('extraPrices', '')    # 原价
            price_2 = data.get('extra_data', {}).get('price', {}).get('price', {}).get('priceText', '')     # 促销价
            if price_1 != '':
                print('price_1 = ', price_1[0].get('priceText', ''))
            else:
                price_1 = ''
                print('price_1 = ', price_1, type(price_1))
            print('price_2 = ', price_2)
            # 判断是否有促销价
            if price_2 != '':     # 有促销价的情况
                tmp_price = price_2
                if tmp_price != '':
                    ss_price = tmp_price
                    if ss_price != '':
                        # print(type(ss_price))
                        ss_price.split('-')
                        # print(type(ss_price))
                        if len(ss_price) > 1:
                            price = round(float(ss_price[1]), 2)
                            taobao_price = round(float(ss_price[0]), 2)
                        else:  # 单个
                            price = round(float(ss_price[0]), 2)
                            taobao_price = price
                    else:
                        return {}
                else:
                    return {}
            else:   # 没有促销价只是原价
                tmp_price = price_1
                if tmp_price != '':
                    ss_price = tmp_price[0].get('priceText', '')
                    if ss_price != '':
                        ss_price.split('-')
                        if len(ss_price) > 1:
                            price = round(float(ss_price[1]), 2)
                            taobao_price = round(float(ss_price[0]), 2)
                        else:  # 单个
                            price = round(float(ss_price[0]), 2)
                            taobao_price = price
                    else:
                        return {}
                else:
                    return {}
            print('price=', price)
            print('taobao_price=', taobao_price)

            # 商品库存  int类型
            goods_stock = data['extra_data'].get('skuCore').get('sku2info').get('0').get('quantity')

            # 商品标签属性名称, 以及商品标签属性对应的值
            sku_base = data.get('skuBase')
            if sku_base is not None:        # 判断skuBase这个属性是否为None
                props = sku_base.get('props')
                if props is not None:    # 判断props这个属性是否为None
                    # 商品标签属性名称
                    detail_name_list = [{'spec_name': item['name'], 'pid': item['pid']} for item in props]
                    props_values = [item['values'] for item in props]
                    # print(props_values)
                    detail_value_list = []
                    for item in props_values:
                        # [{'type': [{'child_type': {'image': None, 'value': '50mL', 'vid': 75366304}}, {'child_type': {'image': None, 'value': '100mL', 'vid': 75366294}}]}, ...]
                        tmp_s = []
                        for item2 in item:
                            tmp = {}
                            if item2['image'] is None:
                                tmp['image'] = None
                            else:
                                tmp['image'] = 'https:' + item2['image']
                            tmp['value'] = item2['name']
                            tmp['vid'] = item2['vid']
                            tmp_s.append({'child_type': tmp})

                        # 商品标签属性对应的值
                        detail_value_list.append({'type': tmp_s})
                else:
                    detail_name_list = []
                    detail_value_list = []
            else:
                detail_name_list = []
                detail_value_list = []
            # print(detail_name_list)
            # print(detail_value_list)

            '''
            要存储的每个标签对应规格的价格及其库存
            '''
            tmp_detail_name_list = detail_name_list

            # [{'type': [{'child_type': {'image': None, 'value': '50mL', 'vid': 75366304}}, {'child_type': {'image': None, 'value': '100mL', 'vid': 75366294}}]}, ...]
            tmp_detail_value_list = detail_value_list

            # 得到规格对应vid的list    如: [['50mL', '75366304'], ['100mL', '75366294'], ['淡粉色', '3986333'], ['绿色', '28335'], ['黄色', '28324']]
            value_and_vid_list = []
            for item in tmp_detail_value_list:
                type = item['type']
                # print(type)             # [{'child_type': {'image': None, 'value': '50mL', 'vid': 75366304}}, {'child_type': {'image': None, 'value': '100mL', 'vid': 75366294}}]
                for item2 in type:
                    child_type = item2['child_type']
                    # print(child_type)       # {'image': None, 'value': '50mL', 'vid': 75366304}
                    tmp = []
                    tmp = [child_type['value'], str(child_type['vid'])]
                    value_and_vid_list.append(tmp)
            # print(value_and_vid_list)  # [['50mL', '75366304'], ['100mL', '75366294'], ['淡粉色', '3986333'], ['绿色', '28335'], ['黄色', '28324']]

            extra_data = data['extra_data']    # 里面是所有规格的可能值   [{'propPath': '1627207:3986333;33993:75366304', 'skuId': 56681142803}, ..]

            sku_base = data['extra_data'].get('skuBase')
            if sku_base is not None:
                skus = sku_base.get('skus')
                # print(skus)
                if skus is not None:
                    sku2_info = data.get('extra_data', {}).get('skuCore', {}).get('sku2info', {})
                    try:
                        sku2_info.pop('0')  # 此处删除总库存的值
                    except Exception:
                        pass
                    prop_path_list = []  # 要存储的每个标签对应规格的价格及其库存

                    for key in sku2_info:
                        tmp = {}
                        # 这里有个坑, item['skuId']得先转换为字符串再与key进行比较
                        tmp_prop_path_list = [item for item in skus if str(item['skuId']) == key]

                        # 处理propPath得到可识别的文字
                        prop_path = tmp_prop_path_list[0]['propPath']
                        prop_path = prop_path.split(';')
                        prop_path = [i.split(':') for i in prop_path]
                        prop_path = [j[1] for j in prop_path]  # 是每个属性对应的vid值(是按顺序来的)['4209035', '1710113207', '3266781', '28473']
                        # print(prop_path)

                        for index in range(0, len(prop_path)):  # 将每个值对应转换为具体规格
                            for i in detail_value_list:
                                for j in i:
                                    if prop_path[index] == j[1]:
                                        prop_path[index] = j[0]
                        # print(prop_path)                  # 其格式为  ['3986333', '75366304']

                        # ['3986333', '75366304']
                        # 3986333 | 75366304

                        uu = []
                        for i in prop_path:
                            hh = ''
                            hh = str([item[0] for item in value_and_vid_list if i == item[1]][0])
                            uu.append(hh)
                        # print(uu)       # ['淡粉色', '50mL']

                        # 再转换为要存储的字符串
                        prop_path = '|'.join(uu)  # 其规格为  3986333|75366304
                        # print(prop_path)    # 淡粉色|50mL

                        # tmp['sku_id'] = tmp_prop_path_list[0]['skuId']      # skuId是定位值，由于不需要就给它注释了
                        # tmp['prop_path'] = tmp_prop_path_list[0]['propPath']
                        tmp['spec_value'] = prop_path
                        tmp['detail_price'] = sku2_info[key]['price']['priceText']  # 每个规格对应的价格
                        tmp['rest_number'] = sku2_info[key]['quantity']  # 每个规格对应的库存量
                        prop_path_list.append(tmp)
                        # pprint(prop_path_list)
                    price_info_list = prop_path_list        # [{'detail_price': '349', 'rest_number': 418, 'spec_value': '红酒紫E21|155/76A/XS'}, ...]
                else:
                    price_info_list = []
            else:
                price_info_list = []

            # pprint(price_info_list)

            # 所有示例图片地址
            tmp_all_img_url = data.get('item', {}).get('images', [])
            all_img_url = []
            if tmp_all_img_url != []:
                for item in tmp_all_img_url:
                    tmp = {}
                    i = 'https:' + item
                    tmp['img_url'] = i
                    all_img_url.append(tmp)
                # pprint(all_img_url)
            else:
                pass

            # 详细信息标签名对应属性
            is_groupprops = data.get('props', {}).get('groupProps')
            if is_groupprops is not None:
                tmp_p_info = data['props'].get('groupProps')[0].get('基本信息')
                p_info = []
                for item in tmp_p_info:
                    # print(item)
                    tmp = {}
                    tmp['name'] = list(item.keys())[0]
                    tmp['value'] = list(item.values())[0]
                    tmp['id'] = '0'
                    p_info.append(tmp)
                # pprint(p_info)
            else:   # 是props->propsList->[0]->baseProps
                is_propslist = data['props'].get('propsList')
                if is_propslist is not None:
                    tmp_p_info = data['props'].get('propsList')[0].get('baseProps')
                    p_info = []
                    for item in tmp_p_info:
                        # print(item)
                        tmp = {}
                        tmp['name'] = ''.join(list(item.get('key')))
                        tmp['value'] = ''.join(list(item.get('value')))
                        tmp['id'] = '0'
                        p_info.append(tmp)
                    # pprint(p_info)
                else:
                    print('无法正确解析标签名和标签值')
                    p_info = []

            # pc端描述地址
            pc_div_url = data.get('item', {}).get('tmallDescUrl')

            # div_desc
            div_desc = self.deal_with_div(pc_div_url)

            '''
            后期处理
            '''
            if detail_name_list != []:
                for item in detail_name_list:   # 移除pid key值
                    try:
                        item.pop('pid')
                    except KeyError:
                        pass
            if detail_value_list != []:
                for i in detail_value_list:     # 移除vid key值
                    for j in i['type']:
                        try:
                            j['child_type'].pop('vid')
                        except KeyError:
                            pass

            '''
            是否下架判断
            '''
            is_delete = 0

            result = {
                'shop_name': shop_name,                 # 店铺名称
                'account': account,                     # 掌柜
                'title': title,                         # 商品名称
                'sub_title': sub_title,                 # 子标题
                'price': price,                         # 商品价格
                'taobao_price': taobao_price,           # 淘宝价
                'goods_stock': goods_stock,             # 商品库存
                'detail_name_list': detail_name_list,   # 商品标签属性名称
                'detail_value_list': detail_value_list, # 商品标签属性对应的值
                'price_info_list': price_info_list,     # 要存储的每个标签对应规格的价格及其库存
                'all_img_url': all_img_url,             # 所有示例图片地址
                'p_info': p_info,                       # 详细信息标签名对应属性
                'pc_div_url': pc_div_url,               # pc端描述地址
                'div_desc': div_desc,                   # div_desc
                'is_delete': is_delete,                 # 是否下架判断
                'type': type,                           # 天猫类型
            }
            # pprint(result)
            # wait_to_send_data = {
            #     'reason': 'success',
            #     'data': result,
            #     'code': 1
            # }
            # json_data = json.dumps(wait_to_send_data, ensure_ascii=False)
            # print(json_data)
            gc.collect()
            return result

        else:
            print('待处理的data为空的dict')
            return {}

    def deal_with_div(self, url):
        self.driver.set_page_load_timeout(12)
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(12)
            # self.driver.save_screenshot('tmp_login1.png')

            locator = (By.CSS_SELECTOR, 'div#description')
            try:
                WebDriverWait(self.driver, 12, 0.5).until(EC.presence_of_element_located(locator))
            except Exception as e:
                print('获取div#description错误: ', e)
            else:
                print('div#description加载完毕...')
                pass
        except Exception as e:  # 如果超时, 终止加载并继续后续操作
            print('-->>time out after 12 seconds(当获取div#description时)')
            self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            # pass

        body = self.driver.page_source

        # 过滤
        body = re.compile(r'\n').sub('', body)
        body = re.compile(r'\t').sub('', body)
        body = re.compile(r'  ').sub('', body)
        # print(body)

        body = re.compile(r'<div id="description".*?>.*</body>').findall(body)[0]
        body = re.compile(r'src="data:image/png;.*?"').sub('', body)
        body = re.compile(r'data-ks-lazyload').sub('src', body)
        body = re.compile(r'https:').sub('', body)
        body = re.compile(r'src="').sub('src=\"https:', body)

        body = re.compile(r'<table.*?>.*?</table>').sub('', body)  # 防止字段太长
        body = re.compile(r'<div class="rmsp rmsp-bl rmsp-bl">.*</div>').sub('', body)
        # body = re.compile(r'<div class="rmsp rmsp-bl rmsp-bl">')

        return body

    def get_goods_id_from_url(self, tmall_url):
        '''
        得到合法url的goods_id
        :param tmall_url:
        :return: dict {0:'1111111'}  0:表示天猫常规商品, 1:表示天猫超市, 2:表示天猫国际, 返回为{}表示解析错误
        '''
        is_tmall_url = re.compile(r'https://detail.tmall.com/item.htm.*?').findall(tmall_url)
        if is_tmall_url != []:                  # 天猫常规商品
            tmp_tmall_url = re.compile(r'https://detail.tmall.com/item.htm.*?id=(\d+)&{0,20}.*?').findall(tmall_url)
            if tmp_tmall_url != []:
                goods_id = tmp_tmall_url[0]
            else:
                tmall_url = re.compile(r';').sub('', tmall_url)
                goods_id = re.compile(r'https://detail.tmall.com/item.htm.*?id=(\d+)').findall(tmall_url)[0]
            print('------>>>| 得到的天猫商品id为:', goods_id)
            return {
                0: goods_id
            }
        else:
            is_tmall_supermarket = re.compile(r'https://chaoshi.detail.tmall.com/item.htm.*?').findall(tmall_url)
            if is_tmall_supermarket != []:      # 天猫超市
                tmp_tmall_url = re.compile(r'https://chaoshi.detail.tmall.com/item.htm.*?id=(\d+)&.*?').findall(tmall_url)
                if tmp_tmall_url != []:
                    goods_id = tmp_tmall_url[0]
                else:
                    tmall_url = re.compile(r';').sub('', tmall_url)
                    goods_id = re.compile(r'https://chaoshi.detail.tmall.com/item.htm.*?id=(\d+)').findall(tmall_url)[0]
                print('------>>>| 得到的天猫商品id为:', goods_id)
                return {
                    1: goods_id
                }
            else:
                is_tmall_hk = re.compile(r'https://detail.tmall.hk/.*?item.htm.*?').findall(tmall_url)      # 因为中间可能有国家的地址 如https://detail.tmall.hk/hk/item.htm?
                if is_tmall_hk != []:           # 天猫国际， 地址中有地域的也能正确解析, 嘿嘿 -_-!!!
                    tmp_tmall_url = re.compile(r'https://detail.tmall.hk/.*?item.htm.*?id=(\d+)&.*?').findall(tmall_url)
                    if tmp_tmall_url != []:
                        goods_id = tmp_tmall_url[0]
                    else:
                        tmall_url = re.compile(r';').sub('', tmall_url)
                        goods_id = re.compile(r'https://detail.tmall.hk/.*?item.htm.*?id=(\d+)').findall(tmall_url)[0]
                    print('------>>>| 得到的天猫商品id为:', goods_id)
                    return {
                        2: goods_id
                    }
                else:
                    print('天猫商品url错误, 非正规的url, 请参照格式(https://detail.tmall.com/item.htm)开头的...')
                    return {}

    def __del__(self):
        self.driver.quit()
        gc.collect()

if __name__ == '__main__':
    tmall = TmallParse()
    while True:
        tmall_url = input('请输入待爬取的天猫商品地址: ')
        tmall_url.strip('\n').strip(';')
        goods_id = tmall.get_goods_id_from_url(tmall_url)   # 返回一个dict类型
        if goods_id != {}:
            data = tmall.get_goods_data(goods_id=goods_id)
            result = tmall.deal_with_data()
            # pprint(result)
            gc.collect()
        else:
            print('获取到的天猫商品地址无法解析，地址错误')
    del tmall
    gc.collect()

# https://detail.m.tmall.com/item.htm?id=43979920132&sku_properties=1627207:28320