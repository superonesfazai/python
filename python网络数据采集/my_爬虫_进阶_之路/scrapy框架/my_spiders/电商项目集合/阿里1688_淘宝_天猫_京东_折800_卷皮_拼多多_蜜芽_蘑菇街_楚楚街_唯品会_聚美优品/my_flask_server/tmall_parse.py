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

import json
import re
from pprint import pprint
from decimal import Decimal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.expected_conditions import WebDriverException
from urllib.request import urlopen
from PIL import Image
from time import sleep
import gc
from scrapy.selector import Selector

from settings import PHANTOMJS_DRIVER_PATH
from settings import TAOBAO_USERNAME, TAOBAO_PASSWD, _tmall_cookies
import pytz, datetime
from scrapy.selector import Selector

from fzutils.time_utils import get_shanghai_time
from fzutils.internet_utils import get_random_pc_ua
from fzutils.internet_utils import get_random_phone_ua
from fzutils.ip_pools import MyIpPools

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

class TmallParse(object):
    def __init__(self):
        self._set_headers()
        self.result_data = {}
        self.init_phantomjs()

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'detail.m.tmall.com',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    def get_goods_data(self, goods_id):
        '''
        得到data
        :param goods_id:
        :return: data   类型dict
        '''
        self.from_ip_pool_set_proxy_ip_to_phantomjs()

        type = goods_id[0]             # 天猫类型
        # print(type)
        goods_id = goods_id[1]       # 天猫goods_id
        tmp_url = 'https://detail.m.tmall.com/item.htm?id=' + str(goods_id)
        print('------>>>| 得到的移动端地址为: ', tmp_url)

        # 不用requests的原因是要带cookies才能请求到数据
        # response = requests.get(tmp_url, headers=self.headers, allow_redirects=False)
        # print(response.text)

        self.driver.set_page_load_timeout(15)
        try:
            self.driver.get(tmp_url)
            self.driver.implicitly_wait(15)  # 隐式等待和显式等待可以同时使用

            if list(Selector(text=self._wash_body(self.driver.page_source)).css('a.f-left').extract()) != []:
                # 研究发现只有部分商品需要登录，所以先不进行处理
                '''遇到要求登录的 ## 未完成，待续...'''
                print('要求淘宝登录...')
                # 要求淘宝登录就先登录
                self.driver.find_element_by_name('TPL_username').send_keys(TAOBAO_USERNAME)
                self.driver.find_element_by_name('TPL_password').send_keys(TAOBAO_PASSWD)

                self.driver.find_element_by_css_selector('button#btn-submit').click()
                self.driver.find_element_by_css_selector('span.km-dialog-btn').click()
                self.driver.find_element_by_css_selector('div.icon.nc-iconfont.icon-notclick').click()
                print('淘宝登录完成!')
                sleep(3)
                # self.driver.save_screenshot('11.png')
                print('此处打印结果未成功登录! 未完成，待续...')
                # print(self._wash_body(self.driver.page_source))

            locator = (By.CSS_SELECTOR, 'div#J_mod4')
            try:
                WebDriverWait(self.driver, 15, 0.2).until(EC.presence_of_element_located(locator))
            except WebDriverException as e:
                print('遇到错误: ', e)
                body_s = self._wash_body(self.driver.page_source)
                # print(body_s)

                # 下架商品单独处理
                try:
                    pull_off_shelves = str(Selector(text=body_s).css('section.s-error div.message::text').extract_first())
                    print('@@@@@@ 商品页面提示: ', pull_off_shelves)
                except:
                    pull_off_shelves = ''
                if pull_off_shelves == '很抱歉，您查看的宝贝不存在，可能已下架或被转移' or pull_off_shelves == '很抱歉，系统繁忙':
                    '''
                    ## 表示该商品已经下架，注意: 很抱歉，系统繁忙也是商品下架的表现
                    '''
                    print('@@@@@@ 该商品已经下架...')
                    tmp_data_s = self.init_pull_off_shelves_goods(type=type)
                    self.result_data = {}
                    return tmp_data_s

                return 4041  # 未得到div#mod-detail-bd，返回4041
            else:
                print('div#mod-detail-bd已经加载完毕')
            # print('div#mod-detail-bd已经加载完毕')
            # self.driver.save_screenshot('tmp.png')

        except Exception as e:  # 如果超时, 终止加载并继续后续操作
            print('-->>time out after 15 seconds when loading page')
            print('遇到错误:', e)
            self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            # pass

        body = self._wash_body(self.driver.page_source)
        # print(body)

        body_1 = re.compile(r'var _DATA_Detail = (.*?);</script>').findall(body)
        body_2 = re.compile(r'{"addressData"(.*?)</script>').findall(body)
        if body_1 != []:
            data = body_1[0]
            try:
                data = json.loads(data)
            except Exception:
                print(r'json.loads(data)时报错, 此处返回data为{}')
                self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                return {}

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
                try:
                    data_2 = json.loads(data_2)
                except Exception:
                    print(r'json.loads(data_2)时为空, 此处赋值data_2为{}')
                    data_2 = {}
                data_2['delivery'] = ''
                data_2['consumerProtection'] = ''
                data_2['feature'] = ''
                data_2['layout'] = ''
                data_2['modules'] = ''
                data_2['vertical'] = ''
                data_2['weappData'] = ''
                # data_2['item'] = ''       # 不能注释，注释了就拿不来月销量
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
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            return {}

    def deal_with_data(self):
        '''
        处理result_data, 返回需要的信息
        :return: 字典类型
        '''
        data = self.result_data
        if data != {}:
            # 天猫类型
            tmall_type = data.get('type', 33)     # 33用于表示无法正确获取
            # print(tmall_type)

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
                # print('price_1 = ', price_1[0].get('priceText', ''))
                pass
            else:
                price_1 = ''
                # print('price_1 = ', price_1)
                pass
            # print('price_2 = ', price_2)

            '''
            最高价和淘宝价处理
            '''
            # 判断是否有促销价
            if price_2 != '':       # 有促销价的情况
                # print(type(ss_price))
                ss_price = price_2.split('-')
                # print(type(ss_price))
                if len(ss_price) > 1:
                    price = '%.2f' % float(ss_price[1])
                    taobao_price = '%.2f' % float(ss_price[0])
                else:               # 单个
                    price = '%.2f' % float(ss_price[0])
                    taobao_price = price
            else:                   # 没有促销价只是原价
                if price_1 != '':
                    ss_price = price_1[0].get('priceText', '')
                    if ss_price != '':
                        ss_price = ss_price.split('-')
                        if len(ss_price) > 1:
                            price = '%.2f' %float(ss_price[1])
                            taobao_price = '%.2f' % float(ss_price[0])
                        else:       # 单个
                            price = '%.2f' % float(ss_price[0])
                            taobao_price = price
                    else:
                        return {}
                else:
                    return {}
            # print('price=', price)
            # print('taobao_price=', taobao_price)

            # 商品库存  int类型
            try:
                goods_stock = data.get('extra_data', {}).get('skuCore', {}).get('sku2info', {}).get('0', {}).get('quantity')
            except Exception as e:
                print(e)
                print('在获取该商品库存信息时报错, 此处跳过!')
                return {}

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
                        # print(prop_path)
                        # print(value_and_vid_list)
                        for i in prop_path:
                            hh = ''
                            try:
                                hh = str([item[0] for item in value_and_vid_list if i == item[1]][0])
                            except IndexError:      # 处理单个套餐里的
                                hh = str([item[0] for item in value_and_vid_list][0])
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
                        try:    # 处理如生产日期，如https://detail.tmall.hk/hk/item.htm?spm=a222r.10469719.4349468587.5.3b840acbv5B2iG&acm=lb-zebra-273428-2784923.1003.4.2447078&id=555548214750&scm=1003.4.lb-zebra-273428-2784923.ITEM_555548214750_2447078&skuId=3429065976919
                            tmp['value'] = ''.join(list(item.get('value')))
                        except TypeError:
                            tmp['value'] = ''
                        tmp['id'] = '0'
                        p_info.append(tmp)
                    # pprint(p_info)
                else:
                    print('无法正确解析标签名和标签值')
                    p_info = []

            # pc端描述地址
            pc_div_url = data.get('item', {}).get('tmallDescUrl')
            # print(pc_div_url)

            # div_desc
            tmp_goods_id = re.compile(r'id=(\d+)').findall(pc_div_url)
            if tmp_goods_id != []:
                tmp_goods_id = tmp_goods_id[0]
                div_desc = self.deal_with_div(tmp_goods_id)

            else:
                div_desc = ''
            # print(div_desc)

            if div_desc == '':
                print('获取到的div_desc为空str, 此处跳过!')
                return {}

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
            # 1. 先通过buyEnable字段来判断商品是否已经下架
            ## 天猫常规商品，天猫国际, 天猫超市都测试通过
            if data.get('extra_data', {}).get('trade', {}) != {}:
                is_buy_enable = str(data.get('extra_data', {}).get('trade', {}).get('buyEnable'))
                if is_buy_enable == 'True':
                    is_delete = 0
                else:
                    # print(is_buy_enable)
                    is_delete = 1
            else:
                is_delete = 0

            # 分析数据发现，天猫超市的有效buyEnable在data['mock']里
            if tmall_type == 1:   # 单独处理天猫超市的商品
                if data.get('mock', {}).get('trade', {}) != {}:
                    # print('888')
                    is_buy_enable = str(data.get('mock', {}).get('trade', {}).get('buyEnable'))
                    # print(is_buy_enable)
                    if is_buy_enable == 'True':
                        # print('11')
                        is_delete = 0
                    else:
                        # print('22')
                        is_delete = 1

            # 2. 此处再考虑名字中显示下架的商品
            if re.compile(r'下架').findall(title) != []:
                if re.compile(r'待下架').findall(title) != []:
                    is_delete = 0
                elif re.compile(r'自动下架').findall(title) != []:
                    is_delete = 0
                else:
                    is_delete = 1
            # print('is_delete = %d' % is_delete)

            # 月销量
            try:
                sell_count = str(data.get('extra_data', {}).get('item', {}).get('sellCount', '0'))
            except:
                sell_count = '0'
            # print(sell_count)

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
                'sell_count': sell_count,               # 月销量
                'is_delete': is_delete,                 # 是否下架判断
                'type': tmall_type,                     # 天猫类型
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
            gc.collect()
            return result

        else:
            print('待处理的data为空的dict')
            return {}

    def deal_with_div(self, goods_id):
        # 研究分析发现要获取描述div只需要通过下面地址即可
        # https://hws.m.taobao.com/cache/desc/5.0?callback=backToDesc&type=1&id=
        url = 'https://hws.m.taobao.com/cache/desc/5.0?callback=backToDesc&type=1&id=' + str(goods_id)
        # print(url)

        try:
            self.from_ip_pool_set_proxy_ip_to_phantomjs()
            self.driver.get(url)
        except Exception:
            try:
                self.from_ip_pool_set_proxy_ip_to_phantomjs()
                self.driver.get(url)
            except Exception:
                self.from_ip_pool_set_proxy_ip_to_phantomjs()
                self.driver.get(url)

        body = self.driver.page_source
        # print(body)
        try:
            body = re.compile(r'backToDesc\((.*)\)').findall(body)[0]
        except IndexError:
            print('获取详情图片介绍时出错，此处跳过!')
            return ''

        try:
            body = json.loads(body)
        except Exception:
            print('999')
            return ''

        body = body.get('pcDescContent', '')
        body = re.compile(r'&lt;').sub('<', body)  # self.driver.page_source转码成字符串时'<','>'都被替代成&gt;&lt;此外还有其他也类似被替换
        body = re.compile(r'&gt;').sub('>', body)
        body = re.compile(r'&amp;').sub('&', body)
        body = re.compile(r'&nbsp;').sub(' ', body)
        body = re.compile(r'src=\"https:').sub('src=\"', body)  # 先替换部分带有https的
        body = re.compile(r'src="').sub('src=\"https:', body)  # 再把所欲的换成https的
        # print(body)

        return body

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
        now_time = get_shanghai_time()
        tmp['modfiy_time'] = now_time  # 修改时间

        tmp['shop_name'] = data_list['shop_name']  # 公司名称
        tmp['title'] = data_list['title']  # 商品名称
        tmp['sub_title'] = data_list['sub_title']  # 商品子标题
        tmp['link_name'] = ''  # 卖家姓名
        tmp['account'] = data_list['account']  # 掌柜名称
        tmp['month_sell_count'] = data_list['sell_count']  # 月销量

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

        # # 采集的来源地
        # if data_list.get('type') == 0:
        #     tmp['site_id'] = 3  # 采集来源地(天猫)
        # elif data_list.get('type') == 1:
        #     tmp['site_id'] = 4  # 采集来源地(天猫超市)
        # elif data_list.get('type') == 2:
        #     tmp['site_id'] = 6  # 采集来源地(天猫国际)
        tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1

        tmp['my_shelf_and_down_time'] = data_list.get('my_shelf_and_down_time')
        tmp['delete_time'] = data_list.get('delete_time')

        tmp['_is_price_change'] = data_list.get('_is_price_change')
        tmp['_price_change_info'] = data_list.get('_price_change_info')

        pipeline.update_tmall_table(tmp)

    def old_tmall_goods_insert_into_new_table(self, data, pipeline):
        '''
        老库数据规范，然后存入
        :param data:
        :param pipeline:
        :return:
        '''
        data_list = data
        tmp = {}
        tmp['username'] = data_list['username']
        tmp['spider_url'] = data_list['goods_url']
        tmp['main_goods_id'] = data_list['main_goods_id']
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

        tmp['deal_with_time'] = now_time  # 操作时间
        tmp['modfiy_time'] = now_time  # 修改时间

        tmp['shop_name'] = data_list['shop_name']  # 公司名称
        tmp['title'] = data_list['title']  # 商品名称
        tmp['sub_title'] = data_list['sub_title']  # 商品子标题
        tmp['link_name'] = ''  # 卖家姓名
        tmp['account'] = data_list['account']  # 掌柜名称
        tmp['month_sell_count'] = data_list['sell_count']  # 月销量

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

        # # 采集的来源地
        if data_list.get('type') == 0:
            tmp['site_id'] = 3  # 采集来源地(天猫)
        elif data_list.get('type') == 1:
            tmp['site_id'] = 4  # 采集来源地(天猫超市)
        elif data_list.get('type') == 2:
            tmp['site_id'] = 6  # 采集来源地(天猫国际)
        else:
            print('type为未知值, 导致site_id设置失败, 此处跳过!')
            return False

        tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1

        # tmp['my_shelf_and_down_time'] = data_list.get('my_shelf_and_down_time')
        # tmp['delete_time'] = data_list.get('delete_time')

        pipeline.old_tmall_goods_insert_into_new_table(tmp)
        return True

    def init_pull_off_shelves_goods(self, type):
        '''
        初始化下架商品的数据
        :return:
        '''
        is_delete = 1
        result = {
            'shop_name': '',  # 店铺名称
            'account': '',  # 掌柜
            'title': '',  # 商品名称
            'sub_title': '',  # 子标题
            'price': 0,  # 商品价格
            'taobao_price': 0,  # 淘宝价
            'goods_stock': '',  # 商品库存
            'detail_name_list': [],  # 商品标签属性名称
            'detail_value_list': [],  # 商品标签属性对应的值
            'price_info_list': [],  # 要存储的每个标签对应规格的价格及其库存
            'all_img_url': [],  # 所有示例图片地址
            'p_info': [],  # 详细信息标签名对应属性
            'pc_div_url': '',  # pc端描述地址
            'div_desc': '',  # div_desc
            'sell_count': '0',  # 月销量
            'is_delete': is_delete,  # 是否下架判断
            'type': type,  # 天猫类型
        }
        return result

    def init_phantomjs(self):
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
        cap['phantomjs.page.settings.userAgent'] = get_random_pc_ua()  # 随机一个请求头
        # cap['phantomjs.page.settings.userAgent'] = get_random_phone_ua()  # 随机一个请求头

        # cap['phantomjs.page.customHeaders.Cookie'] = _tmall_cookies
        tmp_execute_path = EXECUTABLE_PATH
        self.driver = webdriver.PhantomJS(executable_path=tmp_execute_path, desired_capabilities=cap)
        # self.driver.set_window_size(1200, 2000)      # 设置默认大小，避免默认大小显示
        wait = ui.WebDriverWait(self.driver, 15)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
        print('------->>>初始化完毕<<<-------')

    def _wash_body(self, body_s):
        body_s = re.compile(r'\n').sub('', body_s)
        body_s = re.compile(r'\t').sub('', body_s)
        body_s = re.compile(r'  ').sub('', body_s)

        return body_s

    def from_ip_pool_set_proxy_ip_to_phantomjs(self):
        ip_list = MyIpPools()
        proxy_ip = ip_list._get_random_proxy_ip()
        # print('------>>>| 正在使用的代理ip: {} 进行爬取... |<<<------'.format(proxy_ip))
        proxy_ip = re.compile(r'http://').sub('', proxy_ip)     # 过滤'http://'
        proxy_ip = proxy_ip.split(':')                          # 切割成['xxxx', '端口']

        try:
            tmp_js = {
                'script': 'phantom.setProxy({}, {});'.format(proxy_ip[0], proxy_ip[1]),
                'args': []
            }
            self.driver.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')
            self.driver.execute('executePhantomScript', tmp_js)
        except Exception:
            print('动态切换ip失败')
            pass

    def get_goods_id_from_url(self, tmall_url):
        '''
        得到合法url的goods_id
        :param tmall_url:
        :return: a list [0, '1111111'] [2, '1111111', 'https://ssss'] 0:表示天猫常规商品, 1:表示天猫超市, 2:表示天猫国际, 返回为[]表示解析错误
        '''
        is_tmall_url = re.compile(r'https://detail.tmall.com/item.htm.*?').findall(tmall_url)
        if is_tmall_url != []:                  # 天猫常规商品
            tmp_tmall_url = re.compile(r'https://detail.tmall.com/item.htm.*?id=(\d+)&{0,20}.*?').findall(tmall_url)
            if tmp_tmall_url != []:
                is_tmp_tmp_tmall_url = re.compile(r'https://detail.tmall.com/item.htm.*?&id=(\d+)&{0,20}.*?').findall(tmall_url)
                if is_tmp_tmp_tmall_url != []:
                    goods_id = is_tmp_tmp_tmall_url[0]
                else:
                    goods_id = tmp_tmall_url[0]
            else:
                tmall_url = re.compile(r';').sub('', tmall_url)
                goods_id = re.compile(r'https://detail.tmall.com/item.htm.*?id=(\d+)').findall(tmall_url)[0]
            print('------>>>| 得到的天猫商品id为:', goods_id)
            return [0, goods_id]
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
                return [1, goods_id]
            else:
                is_tmall_hk = re.compile(r'https://detail.tmall.hk/.*?item.htm.*?').findall(tmall_url)      # 因为中间可能有国家的地址 如https://detail.tmall.hk/hk/item.htm?
                if is_tmall_hk != []:           # 天猫国际， 地址中有地域的也能正确解析, 嘿嘿 -_-!!!
                    tmp_tmall_url = re.compile(r'https://detail.tmall.hk/.*?item.htm.*?id=(\d+)&.*?').findall(tmall_url)
                    if tmp_tmall_url != []:
                        goods_id = tmp_tmall_url[0]
                    else:
                        tmall_url = re.compile(r';').sub('', tmall_url)
                        goods_id = re.compile(r'https://detail.tmall.hk/.*?item.htm.*?id=(\d+)').findall(tmall_url)[0]
                    before_url = re.compile(r'https://detail.tmall.hk/.*?item.htm').findall(tmall_url)[0]
                    print('------>>>| 得到的天猫商品id为:', goods_id)
                    return [2, goods_id, before_url]
                else:
                    print('天猫商品url错误, 非正规的url, 请参照格式(https://detail.tmall.com/item.htm)开头的...')
                    return []

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    tmall = TmallParse()
    while True:
        tmall_url = input('请输入待爬取的天猫商品地址: ')
        tmall_url.strip('\n').strip(';')
        goods_id = tmall.get_goods_id_from_url(tmall_url)   # 返回一个dict类型
        # print(goods_id)
        if goods_id != []:
            data = tmall.get_goods_data(goods_id=goods_id)
            result = tmall.deal_with_data()
            # pprint(result)
            # print(result)
            gc.collect()
        else:
            print('获取到的天猫商品地址无法解析，地址错误')
