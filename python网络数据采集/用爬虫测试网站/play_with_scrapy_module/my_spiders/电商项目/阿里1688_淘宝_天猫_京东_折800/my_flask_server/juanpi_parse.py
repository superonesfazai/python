# coding:utf-8

'''
@author = super_fazai
@File    : juanpi_parse.py
@Time    : 2017/11/17 17:26
@connect : superonesfazai@gmail.com
'''

"""
卷皮页面采集系统
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

class JuanPiParse(object):
    def __init__(self):
        super(JuanPiParse, self).__init__()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'web.juanpi.com',
            'User-Agent': HEADERS[randint(0, 34)]  # 随机一个请求头
        }

        self.skudata_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'webservice.juanpi.com',
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
            tmp_url = 'https://web.juanpi.com/pintuan/shop/' + str(goods_id)
            print('------>>>| 得到的商品手机版的地址为: ', tmp_url)

            # 设置代理ip
            self.proxies = self.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
            self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]

            tmp_proxies = {
                'http': self.proxy,
            }
            # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))

            try:
                response = requests.get(tmp_url, headers=self.headers, proxies=tmp_proxies, timeout=10)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
                data = response.content.decode('utf-8')
                # print(data)
                data = re.compile(r'__PRELOADED_STATE__=(.*),window.').findall(data)  # 贪婪匹配匹配所有
                # print(data)
            except Exception:
                print('requests.get()请求超时....')
                print('data为空!')
                return {}

            # 得到skudata
            skudata_url = 'https://webservice.juanpi.com/api/getOtherInfo?goods_id=' + str(goods_id)
            try:
                response = requests.get(skudata_url, headers=self.skudata_headers, proxies=tmp_proxies, timeout=10)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
                skudata = response.content.decode('utf-8')
                # print(skudata)
                skudata = re.compile(r'(.*)').findall(skudata)  # 贪婪匹配匹配所有
                # print(skudata)
            except Exception:
                print('requests.get()请求超时....')
                print('skudata为空!')
                return {}

            if skudata != []:
                skudata = skudata[0]
                try:
                    skudata = json.loads(skudata)
                except:
                    return {}
                skudata = skudata.get('skudata', {})
                # pprint(skudata)
                if skudata.get('info') is not None:
                    pass    # 说明得到正确的skudata

                else:       # 否则跳出
                    print('skudata中info的key为None, 返回空dict')
                    return {}

            else:
                print('skudata为空!')
                return {}

            if data != []:
                data = data[0]
                try:
                    data = json.loads(data)
                except:
                    return {}
                # pprint(data)

                if data.get('detail') is not None:
                    data = data.get('detail', {})
                    # 处理commitments
                    try:
                        data['commitments'] = ''
                        data.get('discount', {})['coupon'] = ''
                        data.get('discount', {})['coupon_index'] = ''
                        data.get('discount', {})['vip_info'] = ''
                        data['topbanner'] = ''
                    except:
                        pass
                    try:
                        data.get('brand_info')['sub_goods'] = ''
                    except:
                        pass

                    data['skudata'] = skudata
                    # pprint(data)
                    # print(data)
                    self.result_data = data
                    return data

                else:
                    print('data中detail的key为None, 返回空dict')
                    return {}
            else:
                print('data为空!')
                return {}

    def deal_with_data(self):
        '''
        解析data数据,得到需要的东西
        :return: dict
        '''
        data = self.result_data
        if data != {}:
            # 店铺名称
            if data.get('brand_info') is not None:
                shop_name = data.get('brand_info', {}).get('title', '')
            else:
                shop_name = data.get('schedule_info', {}).get('brand_title', '')

            # 掌柜
            account = ''

            # 商品名称
            title = data.get('baseInfo', {}).get('title', '')

            # 子标题
            sub_title = ''

            # 商品库存

            # 商品标签属性名称
            sku = data.get('skudata', {}).get('sku', [])
            # pprint(sku)
            detail_name_list = []
            if sku != []:
                if sku[0].get('av_fvalue', '') == '':
                    fav_name = ''
                    pass
                else:
                    tmp = {}
                    fav_name = data.get('skudata', {}).get('info', {}).get('fav_name', '')
                    tmp['spec_name'] = fav_name
                    detail_name_list.append(tmp)

                if sku[0].get('av_zvalue', '') == '':
                    zav_name = ''
                else:
                    tmp = {}
                    zav_name = data.get('skudata', {}).get('info', {}).get('zav_name', '')
                    tmp['spec_name'] = zav_name
                    detail_name_list.append(tmp)
            # print(detail_name_list)

            # 商品标签属性对应的值(pass不采集)

            # 是否下架的初始化
            is_delete = 0

            # 要存储的每个标签对应的规格的价格及其库存
            sku = data.get('skudata', {}).get('sku', [])    # 分析得到sku肯定不为[]
            # pprint(sku)
            price_info_list = []
            if len(sku) == 1 and sku[0].get('av_fvalue', '') == '' and sku[0].get('av_zvalue') == '':   # 没有规格的默认只有一个{}
                # 最高价
                price = round(float(sku[0].get('cprice')), 2)
                # 最低价
                taobao_price = price

            else:   # 有规格的
                # 通过'stock'='1'来判断是否有库存, ='0'表示无库存
                # '由于卷皮不给返回库存值, 所以 'stock_tips'='库存紧张', 我就设置剩余库存为10, 如果'stock_tips'='', 就默认设置库存量为50
                # print('777')
                for item in sku:
                    tmp = {}
                    tmp_1 = []
                    if item.get('av_fvalue', '') == '':
                        pass
                    else:
                        tmp_1.append(item.get('av_fvalue'))

                    if item.get('av_zvalue', '') == '':
                        pass
                    else:
                        tmp_1.append(item.get('av_zvalue'))
                    tmp_1 = '|'.join(tmp_1)

                    if item.get('av_origin_zpic', '') != '':
                        tmp['img_url'] = item.get('av_origin_zpic', '')
                    else:
                        tmp['img_url'] = ''

                    if item.get('cprice', '') != '':
                        tmp['detail_price'] = item.get('cprice')
                    else:
                        tmp['detail_price'] = item.get('price')

                    if item.get('stock') == '0':    # 跳过
                        rest_number = '0'
                    else:   # 即'stock'='1'
                        rest_number = '50'

                        if item.get('stock_tips', '') != '' and item.get('stock_tips', '') == '库存紧张':
                            # 库存紧张的时候设置下
                            rest_number = '10'

                        tmp['spec_value'] = tmp_1
                        tmp['rest_number'] = rest_number
                        price_info_list.append(tmp)

                # 得到有规格时的最高价和最低价
                tmp_price_list = sorted([round(float(item.get('detail_price', '')), 2) for item in price_info_list])
                # print(tmp_price_list)
                if tmp_price_list == []:
                    is_delete = 1       # 没有获取到价格说明商品已经下架了
                    price = 0
                    taobao_price = 0
                else:
                    price = tmp_price_list[-1]  # 商品价格
                    taobao_price = tmp_price_list[0]  # 淘宝价
            # print('最高价为: ', price)
            # print('最低价为: ', taobao_price)
            # pprint(price_info_list)


            # 所有示例图片的地址
            all_img_url = [{'img_url': item} for item in data.get('goodImages')]
            # print(all_img_url)

            # 详细信息标签名对应的属性
            p_info = []
            attr = data.get('goodsDetail', {}).get('attr', [])
            if attr != []:
                p_info = [{'p_name': item.get('st_key'), 'p_value': item.get('st_value')} for item in attr]
                for item in p_info:
                    if item.get('p_name') == '运费':  # 过滤掉颜色的html代码
                        item['p_value'] = '全国包邮(偏远地区除外)'
            # pprint(p_info)

            # div_desc
            div_images_list = data.get('goodsDetail', {}).get('images', [])
            tmp_div_desc = ''
            for item in div_images_list:
                tmp = r'<img src="{}" style="height:auto;width:100%;"/>'.format(item)
                tmp_div_desc += tmp
            div_desc = '<div>' + tmp_div_desc + '</div>'
            # print(div_desc)

            # 商品销售时间段
            # print(data.get('skudata', {}).get('info', {}))
            # print(data.get('skudata', {}))
            begin_time = data.get('skudata', {}).get('info', {}).get('start_time')  # 取这个时间段才是正确的销售时间, 之前baseInfo是虚假的
            end_time = data.get('skudata', {}).get('info', {}).get('end_time')
            if begin_time is None or end_time is None:
                schedule = []
            else:
                schedule = [{
                    'begin_time': self.timestamp_to_regulartime(begin_time),
                    'end_time': self.timestamp_to_regulartime(end_time),
                }]
            # pprint(schedule)

            # 是否下架判断
            # 结束时间戳小于当前时间戳则表示已经删除无法购买, 另外每个规格卖光也不显示is_delete=1(在上面已经判断, 这个就跟销售时间段没关系了)
            if schedule != []:
                if data.get('baseInfo', {}).get('end_time') is not None:
                    '''
                    先判断如果baseInfo中的end_time=='0'表示已经下架
                    '''
                    base_info_end_time = data.get('baseInfo', {}).get('end_time')
                    # print(base_info_end_time)
                    if base_info_end_time == '0':
                        is_delete = 1

                if float(end_time) < time.time():
                    '''
                    再判断日期过期的
                    '''
                    is_delete = 1
                # print(is_delete)
            else:
                pass

            result = {
                'shop_name': shop_name,                 # 店铺名称
                'account': account,                     # 掌柜
                'title': title,                         # 商品名称
                'sub_title': sub_title,                 # 子标题
                'price': price,                         # 商品价格
                'taobao_price': taobao_price,           # 淘宝价
                # 'goods_stock': goods_stock,           # 商品库存
                'detail_name_list': detail_name_list,   # 商品标签属性名称
                # 'detail_value_list': detail_value_list, # 商品标签属性对应的值
                'price_info_list': price_info_list,     # 要存储的每个标签对应规格的价格及其库存
                'all_img_url': all_img_url,             # 所有示例图片地址
                'p_info': p_info,                       # 详细信息标签名对应属性
                'div_desc': div_desc,                   # div_desc
                'is_delete': is_delete,                 # 是否下架判断
                'schedule': schedule,                   # 商品销售时间段
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

        tmp['schedule'] = data_list.get('schedule')

        # 采集的来源地
        # tmp['site_id'] = 12  # 采集来源地(卷皮常规商品)

        tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1

        pipeline.update_juanpi_table(item=tmp)

    def insert_into_juanpi_xianshimiaosha_table(self, data, pipeline):
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
        tmp['sub_title'] = data_list['sub_title']  # 商品子标题

        # 设置最高价price， 最低价taobao_price
        tmp['price'] = Decimal(data_list['price']).__round__(2)
        tmp['taobao_price'] = Decimal(data_list['taobao_price']).__round__(2)

        tmp['detail_name_list'] = data_list['detail_name_list']  # 标签属性名称

        """
        得到sku_map
        """
        tmp['price_info_list'] = data_list.get('price_info_list')  # 每个规格对应价格及其库存

        tmp['all_img_url'] = data_list.get('all_img_url')  # 所有示例图片地址

        tmp['p_info'] = data_list.get('p_info')  # 详细信息
        tmp['div_desc'] = data_list.get('div_desc')  # 下方div

        tmp['schedule'] = data_list.get('schedule')
        tmp['stock_info'] = data_list.get('stock_info')
        tmp['miaosha_time'] = data_list.get('miaosha_time')
        tmp['tab_id'] = data_list.get('tab_id')
        tmp['page'] = data_list.get('page')

        # 采集的来源地
        tmp['site_id'] = 1  # 采集来源地(卷皮秒杀商品)

        tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1
        # print('is_delete=', tmp['is_delete'])

        # print('------>>> | 待存储的数据信息为: |', tmp)
        print('------>>> | 待存储的数据信息为: |', tmp.get('goods_id'))

        pipeline.insert_into_juanpi_xianshimiaosha_table(item=tmp)

    def to_update_juanpi_xianshimiaosha_table(self, data, pipeline):
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
        tmp['price'] = Decimal(data_list['price']).__round__(2)
        tmp['taobao_price'] = Decimal(data_list['taobao_price']).__round__(2)

        tmp['detail_name_list'] = data_list['detail_name_list']  # 标签属性名称

        """
        得到sku_map
        """
        tmp['price_info_list'] = data_list.get('price_info_list')  # 每个规格对应价格及其库存

        tmp['all_img_url'] = data_list.get('all_img_url')  # 所有示例图片地址

        tmp['p_info'] = data_list.get('p_info')  # 详细信息
        tmp['div_desc'] = data_list.get('div_desc')  # 下方div

        tmp['schedule'] = data_list.get('schedule')
        tmp['stock_info'] = data_list.get('stock_info')
        tmp['miaosha_time'] = data_list.get('miaosha_time')

        tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1
        # print('is_delete=', tmp['is_delete'])

        # print('------>>> | 待存储的数据信息为: |', tmp)
        print('------>>> | 待存储的数据信息为: |', tmp.get('goods_id'))

        pipeline.update_juanpi_xianshimiaosha_table(tmp)

    def timestamp_to_regulartime(self, timestamp):
        '''
        将时间戳转换成时间
        '''
        # 利用localtime()函数将时间戳转化成localtime的格式
        # 利用strftime()函数重新格式化时间

        # 转换成localtime
        time_local = time.localtime(int(timestamp))
        # print(time_local)
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

    def get_goods_id_from_url(self, juanpi_url):
        '''
        得到goods_id
        :param juanpi_url:
        :return: goods_id (类型str)
        '''
        is_juanpi_url = re.compile(r'http://shop.juanpi.com/deal/.*?').findall(juanpi_url)
        if is_juanpi_url != []:
            if re.compile(r'http://shop.juanpi.com/deal/(\d+).*?').findall(juanpi_url) != []:
                tmp_juanpi_url = re.compile(r'http://shop.juanpi.com/deal/(\d+).*?').findall(juanpi_url)[0]
                if tmp_juanpi_url != '':
                    goods_id = tmp_juanpi_url
                else:   # 只是为了在pycharm运行时不调到chrome，其实else完全可以不要的
                    juanpi_url = re.compile(r';').sub('', juanpi_url)
                    goods_id = re.compile(r'http://shop.juanpi.com/deal/(\d+).*?').findall(juanpi_url)[0]
                print('------>>>| 得到的卷皮商品的地址为:', goods_id)
                return goods_id

        else:
            print('卷皮商品url错误, 非正规的url, 请参照格式(http://shop.juanpi.com/deal/)开头的...')
            return ''

if __name__ == '__main__':
    juanpi = JuanPiParse()
    while True:
        juanpi_url = input('请输入待爬取的卷皮商品地址: ')
        juanpi_url.strip('\n').strip(';')
        goods_id = juanpi.get_goods_id_from_url(juanpi_url)
        data = juanpi.get_goods_data(goods_id=goods_id)
        juanpi.deal_with_data()