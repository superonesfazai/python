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

from settings import TAOBAO_COOKIES_FILE_PATH, HEADERS
from settings import PHANTOMJS_DRIVER_PATH, CHROME_DRIVER_PATH

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
        print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))

        response = requests.get(tmp_url, headers=self.headers, params=params, proxies=tmp_proxies)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
        last_url = re.compile(r'\+').sub('', response.url)  # 转换后得到正确的url请求地址
        # print(last_url)
        response = requests.get(last_url, headers=self.headers, proxies=tmp_proxies)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
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
            # shop_name_url = 'https:' + data['seller']['taoShopUrl']
            # shop_name_url = re.compile(r'.m.').sub('.', shop_name_url)  # 手机版转换为pc版

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
            goods_stock = data['apiStack'][0]['value'].get('skuCore', '').get('sku2info', '').get('0', '').get('quantity', '')

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
            if data.get('item').get('taobaoDescUrl') is not None:
                phone_div_url = 'https:' + data['item']['taobaoDescUrl']
            else:
                phone_div_url = ''

            # pc端描述地址
            if data.get('item').get('taobaoPcDescUrl') is not None:
                pc_div_url = 'https:' + data['item']['taobaoPcDescUrl']
                # print(phone_div_url)
                # print(pc_div_url)

                self.init_chrome_driver()
                # self.from_ip_pool_set_proxy_ip_to_chrome_driver()
                div_desc = self.deal_with_div(pc_div_url)
                # print(div_desc)

                self.driver.quit()
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
            }
            # print(result)
            wait_to_send_data = {
                'reason': 'success',
                'data': result,
                'code': 1
            }
            json_data = json.dumps(wait_to_send_data, ensure_ascii=False)
            print(json_data)
            return result
        else:
            print('待处理的data为空的dict')
            return {}

    def to_right_and_update_data(self, data, pipeline):
        pass

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

    def from_ip_pool_set_proxy_ip_to_chrome_driver(self):
        ip_list = self.get_proxy_ip_from_ip_pool().get('http')
        proxy_ip = ''
        try:
            proxy_ip = ip_list[randint(0, len(ip_list) - 1)]        # 随机一个代理ip
        except Exception:
            print('从ip池获取随机ip失败...正在使用本机ip进行爬取!')
        print('------>>>| chromedriver正在使用的代理ip: {} 进行爬取... |<<<------'.format(proxy_ip))
        proxy_ip = re.compile(r'http://').sub('', proxy_ip)     # 过滤'http://'

        try:
            tmp_js = r'''
            function setProxy(tmp_proxy){
                var FindProxyForUrl = function(url, host) {
                        return 'PROXY' + tmp_proxy};
                }
                var pac = FindProxyForUrl
                var config = {
                    mode: "pac_script",
                    pacScript: {
                        data: pac
                    }
                }
                chrome.proxy.settings.set({value: config, scope: 'regular'}, function(){});
            }
            setProxy(%s);
            ''' % proxy_ip
            print(tmp_js)
            self.driver.execute_script(tmp_js)
            self.driver.get('http://httpbin.org/ip')
            print(self.driver.page_source)
        except Exception:
            print('动态切换ip失败')
            pass

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
                print('获取div.des错误: ', e)
            else:
                print('div.des加载完毕...')
                pass
        except Exception as e:  # 如果超时, 终止加载并继续后续操作
            print('-->>time out after 5 seconds(当获取div.des时)')
            self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            # pass

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
                pass
        # pprint(result_ip_list)

        return result_ip_list

    def get_goods_id_from_url(self, taobao_url):
        # https://item.taobao.com/item.htm?id=546756179626&ali_trackid=2:mm_110421961_12506094_47316135:1508678840_202_1930444423&spm=a21bo.7925826.192013.3.57586cc65hdN2V
        is_taobao_url = re.compile(r'https://item.taobao.com/item.htm.*?').findall(taobao_url)
        if is_taobao_url != []:
            tmp_taobao_url = re.compile(r'https://item.taobao.com/item.htm.*?id=(.*?)&.*?').findall(taobao_url)[0]
            # print(tmp_taobao_url)
            if tmp_taobao_url != []:
                goods_id = tmp_taobao_url
            else:
                taobao_url = re.compile(r';').sub('', taobao_url)
                goods_id = re.compile(r'https://item.taobao.com/item.htm.*?id=(.+)').findall(taobao_url)[0]
            print('------>>>| 得到的淘宝商品id为:', goods_id)
            return goods_id
        else:
            print('淘宝商品url错误, 非正规的url, 请参照格式(https://item.taobao.com/item.htm)开头的...')
            return ''

    def __del__(self):
        self.driver.quit()
        gc.collect()

if __name__ == '__main__':
    login_taobao = TaoBaoLoginAndParse()
    while True:
        taobao_url = input('请输入待爬取的淘宝商品地址: ')
        taobao_url.strip('\n').strip(';')
        goods_id = login_taobao.get_goods_id_from_url(taobao_url)
        data = login_taobao.get_goods_data(goods_id=goods_id)
        login_taobao.deal_with_data()
        # pprint(data)





