# coding:utf-8

'''
@author = super_fazai
@File    : pinduoduo_parse.py
@Time    : 2017/11/24 14:58
@connect : superonesfazai@gmail.com
'''

"""
拼多多页面采集系统(官网地址: http://mobile.yangkeduo.com/)
由于拼多多的pc站，官方早已放弃维护，专注做移动端，所以下面的都是基于移动端地址进行的爬取
直接requests开始时是可以的，后面就只返回错误的信息，估计将我IP过滤了
"""

from random import randint
import requests
from pprint import pprint
from time import sleep
import re
import gc
from json import dumps

from settings import (
    PHANTOMJS_DRIVER_PATH,
    IP_POOL_TYPE,)

from sql_str_controller import (
    pd_update_str_1,
    pd_insert_str_1,
    pd_update_str_2,)

from fzutils.cp_utils import _get_right_model_data
from fzutils.internet_utils import get_random_pc_ua
from fzutils.ip_pools import IpPools
from fzutils.common_utils import json_2_dict
from fzutils.time_utils import timestamp_to_regulartime
from fzutils.spider.crawler import Crawler

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

class PinduoduoParse(Crawler):
    def __init__(self):
        super(PinduoduoParse, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
            
            is_use_driver=True,
            driver_executable_path=PHANTOMJS_DRIVER_PATH,
        )
        self._set_headers()
        self.result_data = {}
        # self.set_cookies_key_api_uid()  # 设置cookie中的api_uid的值

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'mobile.yangkeduo.com',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
            # 'Cookie': 'api_uid=rBQh+FoXerAjQWaAEOcpAg==;',      # 分析发现需要这个cookie值
        }

    def get_goods_data(self, goods_id):
        '''
        模拟构造得到data的url
        :param goods_id:
        :return: data   类型dict
        '''
        if goods_id == '':
            return self._data_error()

        tmp_url = 'http://mobile.yangkeduo.com/goods.html?goods_id=' + str(goods_id)
        print('------>>>| 得到的商品手机版地址为: ', tmp_url)
        '''
        1.采用requests，由于经常返回错误的body(即requests.get返回的为空的html), So pass
        '''
        # body = Requests.get_url_body(url=tmp_url, headers=self.headers, had_referer=True)
        '''
        2.采用phantomjs来获取
        '''
        body = self.driver.use_phantomjs_to_get_url_body(url=tmp_url)
        if body == '':
            print('body中re匹配到的data为空!')
            return self._data_error()

        data = re.compile(r'window.rawData= (.*?);</script>').findall(body)  # 贪婪匹配匹配所有
        if data != []:
            data = json_2_dict(json_str=data[0]).get('initDataObj', {})
            if data == {}:
                return self._data_error()
            # pprint(data)

            try:
                data['goods'].pop('localGroups')
                data['goods'].pop('mallService')
                data.pop('reviews')             # 评价信息跟相关统计
            except:
                pass
            # pprint(data)

            '''
            处理detailGallery转换成能被html显示页面信息
            '''
            detail_data = data.get('goods', {}).get('detailGallery', [])
            tmp_div_desc = ''
            if detail_data != []:
                for index in range(0, len(detail_data)):
                    if index == 0:      # 跳过拼多多的提示
                        pass
                    else:
                        tmp = ''
                        tmp_img_url = detail_data[index].get('url')
                        tmp = r'<img src="{}" style="height:auto;width:100%;"/>'.format(tmp_img_url)
                        tmp_div_desc += tmp

                detail_data = '<div>' + tmp_div_desc + '</div>'

            else:
                detail_data = ''
            # print(detail_data)
            try:
                data['goods'].pop('detailGallery')  # 删除图文介绍的无第二次用途的信息
            except:
                pass
            data['div_desc'] = detail_data

            # pprint(data)
            self.result_data = data
            return data

        else:
            print('data为空!')
            return self._data_error()

    def _data_error(self):
        self.result_data = {}

        return {}

    def deal_with_data(self):
        '''
        处理result_data, 返回需要的信息
        :return: 字典类型
        '''
        data = self.result_data
        if data != {}:
            shop_name = data.get('mall', {}).get('mallName', '') \
                if data.get('mall') is not None else ''
            account = ''
            title = data.get('goods', {}).get('goodsName', '')
            sub_title = ''
            detail_name_list = self._get_detail_name_list(data=data)
            # print(detail_name_list)

            price_info_list = self._get_price_info_list(data=data)
            if price_info_list == []:
                print('price_info_list为空值')
                return {}

            # 商品价格和淘宝价
            tmp_price_list = sorted([round(float(item.get('detail_price', '')), 2) for item in price_info_list])
            price = tmp_price_list[-1]  # 商品价格
            taobao_price = tmp_price_list[0]  # 淘宝价

            if detail_name_list == []:
                print('## detail_name_list为空值 ##')
                price_info_list = []

            # print('最高价为: ', price)
            # print('最低价为: ', taobao_price)
            # print(len(price_info_list))
            # pprint(price_info_list)

            all_img_url = self._get_all_img_url(data=data)
            # print(all_img_url)

            p_info = self._get_p_info(data=data)
            # print(p_info)

            # 总销量
            all_sell_count = data.get('goods', {}).get('sales', 0)
            div_desc = data.get('div_desc', '')

            # 商品销售时间区间
            schedule = [{
                'begin_time': timestamp_to_regulartime(data.get('goods', {}).get('groupTypes', [])[0].get('startTime')),
                'end_time': timestamp_to_regulartime(data.get('goods', {}).get('groupTypes', [])[0].get('endTime')),
            }]
            # pprint(schedule)

            # 用于判断商品是否已经下架
            is_delete = 0

            result = {
                'shop_name': shop_name,                 # 店铺名称
                'account': account,                     # 掌柜
                'title': title,                         # 商品名称
                'sub_title': sub_title,                 # 子标题
                # 'shop_name_url': shop_name_url,        # 店铺主页地址
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

    def to_right_and_update_data(self, data, pipeline):
        tmp = _get_right_model_data(data=data, site_id=13)
        params = self._get_db_update_params(item=tmp)
        base_sql_str = pd_update_str_1
        if tmp['delete_time'] == '':
            sql_str = base_sql_str.format('shelf_time=%s', '')
        elif tmp['shelf_time'] == '':
            sql_str = base_sql_str.format('delete_time=%s', '')
        else:
            sql_str = base_sql_str.format('shelf_time=%s,', 'delete_time=%s')

        pipeline._update_table(sql_str=sql_str, params=params)

    def _get_price_info_list(self, data):
        skus = data.get('goods', {}).get('skus', [])
        # pprint(skus)
        price_info_list = []
        if skus != []:  # ** 注意: 拼多多商品只有一个规格时skus也不会为空的 **
            for index in range(0, len(skus)):
                s_item = skus[index]
                price = s_item.get('groupPrice', '')  # 拼团价
                normal_price = s_item.get('normalPrice', '')  # 单独购买价格
                spec_value = [item.get('spec_value') for item in data.get('goods', {}).get('skus', [])[index].get('specs')]
                spec_value = '|'.join(spec_value)
                img_url = s_item.get('thumbUrl', '')
                rest_number = s_item.get('quantity', 0)  # 剩余库存
                is_on_sale = s_item.get('isOnSale', 0)  # 用于判断是否在特价销售，1:特价 0:原价(normal_price)
                price_info_list.append({
                    'spec_value': spec_value,
                    'detail_price': price,
                    'normal_price': normal_price,
                    'img_url': img_url if re.compile(r'http').findall(img_url) != [] else 'http:' + img_url,
                    'rest_number': rest_number if rest_number > 0 else 0,
                    'is_on_sale': is_on_sale,
                })

        return price_info_list

    def _get_p_info(self, data):
        tmp_p_value = re.compile('\n|\t|  ').sub('', data.get('goods', {}).get('goodsDesc', ''))

        return [{
            'p_name': '商品描述',
            'p_value': tmp_p_value
        }]

    def _get_detail_name_list(self, data):
        detail_name_list = []
        skus = data.get('goods', {}).get('skus', [])
        # pprint(skus)
        if skus == []:
            pass
        else:
            if skus[0].get('specs', []) == []:
                pass
            else:
                for item in skus[0].get('specs', []):
                    img_here = 0
                    spec_name = item.get('spec_key', '')
                    if spec_name == '颜色':
                        img_here = 1

                    detail_name_list.append({
                        'spec_name': spec_name,
                        'img_here': img_here,
                    })

        return detail_name_list

    def _get_all_img_url(self, data):
        all_img_url = []
        for item in data.get('goods', {}).get('topGallery', []):
            if re.compile('http').findall(item) == []:
                item = 'http:' + item
            else:
                pass
            all_img_url.append({'img_url': item})

        return all_img_url

    def insert_into_pinduoduo_xianshimiaosha_table(self, data, pipeline):
        tmp = _get_right_model_data(data=data, site_id=16)  # 采集来源地(卷皮秒杀商品)
        print('------>>>| 待存储的数据信息为: ', tmp.get('goods_id'))

        params = self._get_db_insert_miaosha_params(item=tmp)
        pipeline._insert_into_table(sql_str=pd_insert_str_1, params=params)

    def to_update_pinduoduo_xianshimiaosha_table(self, data, pipeline):
        tmp = _get_right_model_data(data=data, site_id=16)
        # print('------>>> | 待存储的数据信息为: |', tmp)
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_update_miaosha_params(item=tmp)
        pipeline._update_table(sql_str=pd_update_str_2, params=params)

    def _get_db_update_params(self, item):
        '''
        得到db待存储的数据
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
            item['price'],
            item['taobao_price'],
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
            item['sku_info_trans_time'],
            item['is_spec_change'],
            item['spec_trans_time'],

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

    def set_cookies_key_api_uid(self):
        '''
        给headers增加一个cookie, 里面有个key名字为api_uid
        :return:
        '''
        # 设置代理ip
        ip_object = IpPools()
        self.proxies = ip_object.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]

        tmp_proxies = {
            'http': self.proxy,
        }
        # 得到cookie中的key名为api_uid的值
        host_url = 'http://mobile.yangkeduo.com'
        try:
            response = requests.get(host_url, headers=self.headers, proxies=tmp_proxies, timeout=10)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            api_uid = response.cookies.get('api_uid')
            # print(response.cookies.items())
            # if api_uid is None:
            #     api_uid = 'rBQh+FoXerAjQWaAEOcpAg=='
            self.headers['Cookie'] = 'api_uid=' + str(api_uid) + ';'
            # print(api_uid)
        except Exception:
            print('requests.get()请求超时....')
            pass

    def get_goods_id_from_url(self, pinduoduo_url):
        '''
        得到goods_id
        :param pinduoduo_url:
        :return: goods_id (类型str)
        '''
        is_pinduoduo_url = re.compile(r'http://mobile.yangkeduo.com/goods.html.*?').findall(pinduoduo_url)
        if is_pinduoduo_url != []:
            if re.compile(r'http://mobile.yangkeduo.com/goods.html\?.*?goods_id=(\d+).*?').findall(pinduoduo_url) != []:
                tmp_pinduoduo_url = re.compile(r'http://mobile.yangkeduo.com/goods.html\?.*?goods_id=(\d+).*?').findall(pinduoduo_url)[0]
                if tmp_pinduoduo_url != '':
                    goods_id = tmp_pinduoduo_url
                else:   # 只是为了在pycharm里面测试，可以不加
                    pinduoduo_url = re.compile(r';').sub('', pinduoduo_url)
                    goods_id = re.compile(r'http://mobile.yangkeduo.com/goods.html\?.*?goods_id=(\d+).*?').findall(pinduoduo_url)[0]
                print('------>>>| 得到的拼多多商品id为:', goods_id)
                return goods_id
            else:
                pass
        else:
            print('拼多多商品url错误, 非正规的url, 请参照格式(http://mobile.yangkeduo.com/goods.html)开头的...')
            return ''

    def __del__(self):
        try:
            del self.driver
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    pinduoduo = PinduoduoParse()
    while True:
        pinduoduo_url = input('请输入待爬取的拼多多商品地址: ')
        pinduoduo_url.strip('\n').strip(';')
        goods_id = pinduoduo.get_goods_id_from_url(pinduoduo_url)
        pinduoduo.get_goods_data(goods_id=goods_id)
        data = pinduoduo.deal_with_data()
        pprint(data)