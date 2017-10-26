# coding:utf-8

'''
@author = super_fazai
@File    : taobao_login_and_parse_idea2.py
@Time    : 2017/10/25 07:40
@connect : superonesfazai@gmail.com
'''

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

from settings import CHROME_DRIVER_PATH, TAOBAO_COOKIES_FILE_PATH, HEADERS

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

        # 设置无运行界面版chrome
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')

        # 注意：测试发现还是得设置成加载图片要不然就无法得到超5张的示例图片完整地址
        # 设置chrome不加载图片
        prefs = {
            'profile.managed_default_content_settings.images': 2,
        }
        chrome_options.add_experimental_option('prefs', prefs)

        self.driver = webdriver.Chrome(executable_path=my_chrome_driver_path, chrome_options=chrome_options)
        self.start_url = 'https://login.taobao.com/member/login.jhtml?spm=2013.1.1997563269.1.793cab65Edp2ty&full_redirect=true&redirect_url=https://www.taobao.com'
        self.img_url = ''  # 用来保存二维码的url

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
        response = requests.get(tmp_url, headers=self.headers, params=params)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
        last_url = re.compile(r'\+').sub('', response.url)  # 转换后得到正确的url请求地址
        # print(last_url)
        response = requests.get(last_url, headers=self.headers)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
        data = response.content.decode('utf-8')
        # print(data)
        data = re.compile(r'mtopjsonp1\((.*)\)').findall(data)[0]  # 贪婪匹配匹配所有
        data = json.loads(data)
        if data != []:
            data['data']['rate'] = ''  # 这是宝贝评价
            data['data']['resource'] = ''  # 买家询问别人
            data['data']['vertical'] = ''  # 也是问和回答
            data['data']['seller']['evaluates'] = ''  # 宝贝描述, 卖家服务, 物流服务的评价值...
            result_data = data['data']

            # 处理result_data['apiStack'][0]['value']
            # print(result_data['apiStack'][0]['value'])
            result_data_apiStack_value = result_data['apiStack'][0]['value']
            result_data_apiStack_value = json.loads(result_data_apiStack_value)
            result_data_apiStack_value['vertical'] = ''
            result_data_apiStack_value['consumerProtection'] = ''  # 7天无理由退货
            result_data_apiStack_value['feature'] = ''
            result_data_apiStack_value['layout'] = ''
            result_data_apiStack_value['delivery'] = ''     # 发货地到收到地
            result_data_apiStack_value['resource'] = ''     # 优惠券
            result_data_apiStack_value['item'] = ''
            # pprint(result_data_apiStack_value)

            # 将处理后的result_data['apiStack'][0]['value']重新赋值给result_data['apiStack'][0]['value']
            result_data['apiStack'][0]['value'] = result_data_apiStack_value

            # 处理mockData
            mock_data = result_data['mockData']
            mock_data = json.loads(mock_data)
            mock_data['feature'] = ''
            # pprint(mock_data)
            result_data['mockData'] = mock_data

            self.result_data = result_data
            # pprint(self.result_data)
            return result_data
        else:
            print('data为空!')
            return {}

    def deal_with_data(self):
        '''
        处理result_data, 返回需要的信息
        :return: 字典类型
        '''
        data = self.result_data
        if data != {}:
            # 店铺名称
            shop_name = data['seller']['shopName']
            # 掌柜
            account = data['seller']['sellerNick']
            # 商品名称
            title = data['item']['title']
            # 子标题
            sub_title = data['item']['subtitle']
            sub_title = re.compile(r'\n').sub('', sub_title)
            # 店铺主页地址
            shop_name_url = 'https:' + data['seller']['taoShopUrl']
            # 商品价格
            # price = data['apiStack'][0]['value']['price']['extraPrices'][0]['priceText']
            tmp_taobao_price = data['apiStack'][0]['value']['price']['price']['priceText']
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
            goods_stock = data['apiStack'][0]['value']['skuCore']['sku2info']['0']['quantity']

            # 商品标签属性名称,及其对应id值
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

            '''
            每个标签对应值的价格及其库存
            '''
            skus = data['skuBase']['skus']      # 里面是所有规格的可能值[{'propPath': '20105:4209035;1627207:1710113203;5919063:3266779;122216431:28472', 'skuId': '3335554577910'}, ...]
            sku2_info = data['apiStack'][0]['value']['skuCore']['sku2info']
            sku2_info.pop('0')      # 此处删除总库存的值
            # pprint(sku2_info)
            prop_path_list = []     # 要存储的每个标签对应规格的价格及其库存
            for key in sku2_info:
                tmp = {}
                tmp_prop_path_list = [item for item in skus if item['skuId'] == key]    # [{'skuId': '3335554577923', 'propPath': '20105:4209035;1627207:1710113207;5919063:3266781;122216431:28473'}]

                # 处理propPath得到可识别的文字
                prop_path = tmp_prop_path_list[0]['propPath']
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

            # 所有示例图片地址
            tmp_all_img_url = data['item']['images']
            all_img_url = []
            for item in tmp_all_img_url:
                item = 'https:' + item
                all_img_url.append(item)
            # print(all_img_url)

            # 详细信息p_info
            tmp_p_info = data['props']['groupProps'][0]['基本信息']     # 一个list [{'内存容量': '32GB'}, ...]
            p_info = []
            for item in tmp_p_info:
                for key, value in item.items():
                    tmp = {}
                    tmp['p_name'] = key
                    tmp['p_value'] = value
                    p_info.append(tmp)
            # print(p_info)

            # print(p_info)

            '''
            下方div图片文字介绍区
            '''
            # 手机端描述地址
            phone_div_url = 'https:' + data['item']['taobaoDescUrl']
            # div.des

            # pc端描述地址
            pc_div_url = 'https:' + data['item']['taobaoPcDescUrl']
            # print(phone_div_url)
            # print(pc_div_url)

            div_desc = self.deal_with_div(pc_div_url)
            # print(div_desc)

            self.driver.quit()
            gc.collect()

            '''
            后期处理
            '''
            tmp = []
            tmp_1 = []
            # 后期处理detail_name_list, detail_value_list
            detail_name_list = [i[0] for i in detail_name_list]

            # 商品标签属性对应的值, 及其对应id值
            tmp_detail_value_list = [item['values'] for item in data['skuBase']['props']]
            # print(tmp_detail_value_list)
            detail_value_list = []
            for item in tmp_detail_value_list:
                tmp = [i['name'] for i in item]
                # print(tmp)
                detail_value_list.append(tmp)  # 商品标签属性对应的值
                # pprint(detail_value_list)

            result = {
                'shop_name': shop_name,                             # 店铺名称
                'account': account,                                 # 掌柜
                'title': title,                                     # 商品名称
                'sub_title': sub_title,                             # 子标题
                'shop_name_url': shop_name_url,                     # 店铺主页地址
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
            }
            pprint(result)
            # wait_to_send_data = {
            #     'reason': 'success',
            #     'data': result,
            #     'code': 1
            # }
            # json_data = json.dumps(wait_to_send_data, ensure_ascii=False)
            # print(json_data)
            return result
        else:
            print('待处理的data为空的dict')
            return {}

    def deal_with_div(self, url):
        self.driver.set_page_load_timeout(5)
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(8)
            # self.driver.save_screenshot('tmp_login1.png')

            locator = (By.CSS_SELECTOR, 'div.des')
            try:
                WebDriverWait(self.driver, 8, 0.5).until(EC.presence_of_element_located(locator))
            except Exception as e:
                print('获取验证码时错误: ', e)
            else:
                print('div.des加载完毕...')
                pass
        except Exception as e:  # 如果超时, 终止加载并继续后续操作
            print('-->>time out after 5 seconds(当获取验证码时)')
            self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            # pass

        # time.sleep(1.5)
        # self.driver.save_screenshot('tmp_login1.png')
        body = self.driver.page_source

        # 过滤
        body = re.compile(r'\n').sub('', body)
        body = re.compile(r'\t').sub('', body)
        body = re.compile(r'  ').sub('', body)
        # print(body)

        body = re.compile(r'<div class="des" id="J_des">.*</div></div>').findall(body)[0]
        body = re.compile(r'src="data:image/png;.*?"').sub('', body)
        body = re.compile(r'data-img').sub('src', body)
        body = re.compile(r'https:').sub('', body)
        body = re.compile(r'src="').sub('src=\"https:', body)

        body = re.compile(r'<table.*?>.*?</table>').sub('', body)   # 防止字段太长
        body = re.compile(r'<div class="rmsp rmsp-bl rmsp-bl">.*</div>').sub('', body)
        # body = re.compile(r'<div class="rmsp rmsp-bl rmsp-bl">')

        return body

    def get_goods_id_from_url(self, taobao_url):
        # https://item.taobao.com/item.htm?id=546756179626&ali_trackid=2:mm_110421961_12506094_47316135:1508678840_202_1930444423&spm=a21bo.7925826.192013.3.57586cc65hdN2V
        is_taobao_url = re.compile(r'https://item.taobao.com/item.htm.*?').findall(taobao_url)
        if is_taobao_url != []:
            taobao_url = re.compile(r'https://item.taobao.com/item.htm.*?id=(.*?)&.*?').findall(taobao_url)[0]
            print('------>>>| 得到的淘宝商品id为:', taobao_url)
            return taobao_url
        else:
            print('淘宝商品url错误, 非正规的url, 请参照格式(https://item.taobao.com/item.htm)开头的...')
            return ''

if __name__ == '__main__':
    login_taobao = TaoBaoLoginAndParse()
    # taobao_url = 'https://item.taobao.com/item.htm?spm=a1z10.1-c-s.w5003-17214421641.7.18523e33avyJ0I&id=560164926470&scene=taobao_shop'
    taobao_url = 'https://item.taobao.com/item.htm?id=546756179626&ali_trackid=2:mm_110421961_12506094_47316135:1508678840_202_1930444423&spm=a21bo.7925826.192013.3.57586cc65hdN2V'
    # taobao_url = 'https://item.taobao.com/item.htm?id=41439519931&ali_trackid=2:mm_16523910_13792193_55526825:1508736405_285_336954940&spm=a21bo.7925826.192013.3.581a6bcdrBLQjt'
    # taobao_url = 'https://item.taobao.com/item.htm?spm=a1z10.1-c-s.w5003-17224945007.1.4ce05564PrcnUf&id=560249078162&scene=taobao_shop'
    # taobao_url = 'https://item.taobao.com/item.htm?spm=a1z10.1-c-s.w5003-17214421641.7.18523e33avyJ0I&id=560164926470&scene=taobao_shop'
    goods_id = login_taobao.get_goods_id_from_url(taobao_url)
    data = login_taobao.get_goods_data(goods_id=goods_id)
    login_taobao.deal_with_data()
    # pprint(data)





