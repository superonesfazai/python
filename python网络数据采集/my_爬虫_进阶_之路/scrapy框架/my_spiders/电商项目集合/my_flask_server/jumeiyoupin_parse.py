# coding:utf-8

'''
@author = super_fazai
@File    : jumeiyoupin_parse.py
@Time    : 2018/3/10 10:01
@connect : superonesfazai@gmail.com
'''

"""
聚美优品常规商品页面解析系统
"""

import re
from pprint import pprint
from json import dumps
from gc import collect

from settings import IP_POOL_TYPE
from sql_str_controller import (
    jm_insert_str_1,
    jm_update_str_1,)

from fzutils.cp_utils import _get_right_model_data
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import Requests
from fzutils.spider.crawler import Crawler
from fzutils.common_utils import (
    json_2_dict,
    wash_sensitive_info,)
from fzutils.time_utils import *

class JuMeiYouPinParse(Crawler):
    def __init__(self):
        super(JuMeiYouPinParse, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
        )
        self._set_headers()
        self.result_data = {}

    def _set_headers(self):
        self.headers = {
            'Accept': 'application/json,text/javascript,*/*;q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'h5.jumei.com',
            'Referer': 'http://h5.jumei.com/product/detail?item_id=ht180310p3365132t1&type=global_deal',
            'Cache-Control': 'max-age=0',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
            'X-Requested-With': 'XMLHttpRequest',
        }

    def get_goods_data(self, goods_id):
        '''
        模拟构造得到data的url, 并得到相应数据
        :param goods_id:
        :return: data 类型dict
        '''
        if goods_id == []:
            return self._data_error()

        goods_url = 'https://h5.jumei.com/product/detail?item_id=' + str(goods_id[0]) + '&type=' + str(goods_id[1])
        print('------>>>| 对应的手机端地址为: ', goods_url)

        #** 获取ajaxStaticDetail请求中的数据
        tmp_url = 'https://h5.jumei.com/product/ajaxStaticDetail?item_id=' + goods_id[0] + '&type=' + str(goods_id[1])
        self.headers['Referer'] = goods_url
        body = Requests.get_url_body(
            url=tmp_url,
            headers=self.headers,
            ip_pool_type=self.ip_pool_type)
        # print(body)
        if body == '' or json_2_dict(json_str=body) == {}:
            print('获取到的body为空str! 或者 tmp_data为空dict!')
            return self._data_error()

        tmp_data = self.wash_data(data=json_2_dict(json_str=body))
        # pprint(tmp_data)

        #** 获取ajaxDynamicDetail请求中的数据
        tmp_url_2 = 'https://h5.jumei.com/product/ajaxDynamicDetail?item_id=' + str(goods_id[0]) + '&type=' + str(goods_id[1])
        body_2 = Requests.get_url_body(url=tmp_url_2, headers=self.headers, ip_pool_type=self.ip_pool_type)
        # print(body)
        if body_2 == '':
            print('获取到的body为空str!')
            return self._data_error()

        tmp_data_2 = json_2_dict(json_str=body_2)
        if tmp_data_2 == {}:
            return self._data_error()

        tmp_data_2 = self.wash_data_2(data=tmp_data_2)
        # pprint(tmp_data_2)
        tmp_data['data_2'] = tmp_data_2.get('data', {}).get('result', {})
        if tmp_data['data_2'] == {}:
            print('获取到的ajaxDynamicDetail中的数据为空值!请检查!')
            return self._data_error()

        # pprint(tmp_data)
        return self._get_target_data(tmp_data=tmp_data)

    def _get_target_data(self, tmp_data):
        data = {}
        try:
            data['title'] = self._wash_sensitive_info(tmp_data.get('data', {}).get('name', ''))
            assert data['title'] != '', '获取到的title为空值, 请检查!'
            data['sub_title'] = ''
            # print(data['title'])

            data['shop_name'] = tmp_data.get('data_2', {}).get('shop_info', {}).get('store_title', '') if tmp_data.get('data_2', {}).get('shop_info') != [] else ''
            # print(data['shop_name'])
            data['all_img_url'] = self._get_all_img_url(tmp_data)

            # 获取p_info
            p_info = self.get_p_info(tmp_data=tmp_data)
            # pprint(p_info)
            data['p_info'] = p_info

            # 获取每个商品的div_desc
            # 注意其商品的div_desc = description + description_usage + description_images
            div_desc = self.get_goods_div_desc(tmp_data=tmp_data)
            assert div_desc != '', '获取到的div_desc为空值! 请检查'
            # print(div_desc)
            data['div_desc'] = div_desc

            # 上下架时间 (注意:聚美优品常规今日10点上新商品，销售时长都是24小时)
            sell_time = self.get_sell_time(
                begin_time=tmp_data.get('data_2', {}).get('start_time'),
                end_time=tmp_data.get('data_2', {}).get('end_time')
            )
            # pprint(sell_time)
            data['sell_time'] = sell_time

            # 设置detail_name_list
            detail_name_list = self.get_detail_name_list(
                size_attr=tmp_data.get('data_2', {}).get('size_attr', []),
                size=tmp_data.get('data_2', {}).get('size', []))
            # print(detail_name_list)
            data['detail_name_list'] = detail_name_list

            true_sku_info = self.get_true_sku_info(size=tmp_data.get('data_2', {}).get('size', []))
            assert true_sku_info != [], '获取到的sku_info为空值, 请检查!'
            # pprint(true_sku_info)
            data['price_info_list'] = true_sku_info
            data['is_delete'] = self._get_is_delete(tmp_data, true_sku_info)

            all_sell_count = tmp_data.get('data_2', {}).get('buyer_number', '0')
            data['all_sell_count'] = all_sell_count

        except Exception as e:
            print('遇到错误如下: ', e)
            return self._data_error()

        # pprint(data)
        self.result_data = data
        return data

    def deal_with_data(self):
        '''
        处理得到规范的data数据
        :return: result 类型 dict
        '''
        data = self.result_data
        if data != {}:
            shop_name = data['shop_name']
            account = ''
            title = data['title']
            sub_title = data['sub_title']
            detail_name_list = data['detail_name_list']
            price_info_list = data['price_info_list']
            all_img_url = data['all_img_url']
            p_info = data['p_info']
            div_desc = data['div_desc']
            is_delete = data['is_delete']
            # 上下架时间
            schedule = data['sell_time']
            # 销售总量
            all_sell_count = data['all_sell_count']

            # 商品价格和淘宝价
            # pprint(data['price_info_list'])
            try:
                tmp_price_list = sorted([round(float(item.get('detail_price', '')), 2) for item in data['price_info_list']])
                price = tmp_price_list[-1]  # 商品价格
                taobao_price = tmp_price_list[0]  # 淘宝价
            except IndexError:
                print('获取price和taobao_price时出错, 请检查!')  # 商品下架时, detail_price为空str, 所以会IndexError报错
                self.result_data = {}
                price = 0.
                taobao_price = 0.
                is_delete = 1
                # return {}

            result = {
                'shop_name': shop_name,  # 店铺名称
                'account': account,  # 掌柜
                'title': title,  # 商品名称
                'sub_title': sub_title,  # 子标题
                'price': price,  # 商品价格
                'taobao_price': taobao_price,  # 淘宝价
                # 'goods_stock': goods_stock,           # 商品库存
                'detail_name_list': detail_name_list,  # 商品标签属性名称
                # 'detail_value_list': detail_value_list,# 商品标签属性对应的值
                'price_info_list': price_info_list,  # 要存储的每个标签对应规格的价格及其库存
                'all_img_url': all_img_url,  # 所有示例图片地址
                'p_info': p_info,  # 详细信息标签名对应属性
                'div_desc': div_desc,  # div_desc
                'schedule': schedule,  # 商品特价销售时间段
                'all_sell_count': all_sell_count,  # 销售总量
                'is_delete': is_delete  # 用于判断商品是否已经下架
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
            self.result_data = {}
            return result

        else:
            print('待处理的data为空的dict, 该商品可能已经转移或者下架')
            self.result_data = {}
            return {}

    def _data_error(self):
        self.result_data = {}

        return {}

    def _get_is_delete(self, tmp_data, true_sku_info):
        is_delete = 0
        if int(tmp_data.get('data_2', {}).get('end_time')) < datetime_to_timestamp(get_shanghai_time()):
            is_delete = 1
        else:
            all_stock = 0
            for item in true_sku_info:
                all_stock += item.get('rest_number', 0)
            # print(all_stock)
            if all_stock == 0:
                is_delete = 1
        # print(is_delete)

        return is_delete

    def _get_all_img_url(self, tmp_data):
        all_img_url = tmp_data.get('data', {}).get('image_url_set', {}).get('single_many', [])
        assert all_img_url != [], '获取到的all_img_url为空[], 请检查!'
        all_img_url = [{
            'img_url': item.get('800', ''),
        } for item in all_img_url]
        # pprint(all_img_url)

        return all_img_url

    def _wash_sensitive_info(self, data):
        add_sensitive_str_list = [
            '【官方授权】',
        ]

        return wash_sensitive_info(
            data,
            add_sensitive_str_list=add_sensitive_str_list,
        )

    def _set_detail_price_to_miaosha_price(self, tmp):
        '''
        将detail_price设置为miaosha_price
        :param tmp:
        :return:
        '''
        # 将detail_price设置为秒杀价, 使其提前能购买
        price = tmp['price']                # Decimal
        taobao_price = tmp['taobao_price']  # Decimal
        price_info_list = tmp['price_info_list']
        for item in price_info_list:
            if float(price) == float(item.get('detail_price')):
                item['detail_price'] = str(float(taobao_price))
        tmp['price_info_list'] = price_info_list

        return tmp

    def insert_into_jumeiyoupin_xianshimiaosha_table(self, data, pipeline) -> bool:
        try:
            tmp = _get_right_model_data(data=data, site_id=26)  # 采集来源地(聚美优品10点上新的秒杀商品)
        except:
            print('此处抓到的可能是聚美优品券所以跳过')
            return False

        tmp = self._set_detail_price_to_miaosha_price(tmp=tmp)
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_insert_miaosha_params(item=tmp)
        res = pipeline._insert_into_table(sql_str=jm_insert_str_1, params=params)

        return res

    def update_jumeiyoupin_xianshimiaosha_table(self, data, pipeline) -> bool:
        try:
            tmp = _get_right_model_data(data=data, site_id=26)
        except:
            print('此处抓到的可能是聚美优品券所以跳过')
            return False

        tmp = self._set_detail_price_to_miaosha_price(tmp=tmp)
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_update_miaosha_params(item=tmp)
        res = pipeline._update_table(sql_str=jm_update_str_1, params=params)

        return res

    def _get_db_insert_miaosha_params(self, item):
        params = (
            item['goods_id'],
            item['goods_url'],
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
            dumps(item['miaosha_time'], ensure_ascii=False),
            item['miaosha_begin_time'],
            item['miaosha_end_time'],
            item['page'],

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
            dumps(item['miaosha_time'], ensure_ascii=False),
            item['miaosha_begin_time'],
            item['miaosha_end_time'],

            item['goods_id'],
        )

        return params

    def wash_data(self, data):
        '''
        清洗数据
        :param data:
        :return:
        '''
        '''
        分开del, 避免都放在一块，一个del失败就跳出无法进行继续再往下的清洗
        '''
        try:
            del data['data']['area_icon']
            del data['data']['area_icon_v2']
        except: pass
        try: del data['data']['consumer_notice_data']
        except: pass
        try:
            del data['data']['description_url']
            del data['data']['description_url_set']
        except: pass
        try: del data['data']['guarantee']
        except: pass
        try: del data['data']['image_url_set']['dx_image']
        except: pass
        try: del data['data']['share_info']
        except: pass

        return data

    def wash_data_2(self, data):
        '''
        清洗数据
        :param data:
        :return:
        '''
        try:
            del data['data']['result']['address_list']
            del data['data']['result']['bottom_button']
            del data['data']['result']['default_address']
            del data['data']['result']['fen_qi']
            del data['data']['result']['icon_tag']
        except: pass
        try:
            del data['data']['result']['shop_info']['follow_num']
            del data['data']['result']['shop_info']['logo_url']
        except: pass

        return data

    def get_p_info(self, tmp_data):
        '''
        得到p_info
        :param tmp_data:
        :return: [xxx, ...] 表示success
        '''
        p_info = tmp_data.get('data', {}).get('properties', [])
        p_info = [{
            'p_name': item.get('name', ''),
            'p_value': item.get('value', ''),
        } for item in p_info]

        return p_info

    def get_goods_div_desc(self, tmp_data):
        '''
        获取div_desc
        :param tmp_data:
        :return: '' 表示出错
        '''
        tmp_div_desc = tmp_data.get('data', {}).get('description_info', {})
        if tmp_div_desc == {}:
            return ''

        description = tmp_div_desc.get('description', '')
        description_usage = tmp_div_desc.get('description_usage', '')
        description_images = tmp_div_desc.get('description_images', '')

        div_desc = '<div>' + description + description_usage + description_images + '</div>'

        return div_desc

    def get_sell_time(self, begin_time, end_time):
        '''
        得到上下架时间 (注意:聚美优品常规今日10点上新商品，销售时长都是24小时)
        :param begin_time: 类型int
        :param end_time: 类型int
        :return: [] 表示出错 | {'xx':'yyy'} 表示success
        '''
        assert begin_time is not None, '获取到该商品的begin_time是None'
        assert isinstance(begin_time, int), '获取该商品的begin_time类型错误, 请检查!'

        sell_time = {
            'begin_time': timestamp_to_regulartime(int(begin_time)),
            'end_time': timestamp_to_regulartime(int(end_time)),
        }

        return sell_time

    def get_detail_name_list(self, size_attr, size):
        '''
        得到detail_name_list
        :param size_attr: 规格的说明的list
        :return:
        '''
        # pprint(size_attr)
        # pprint(size)
        assert size_attr is not None or size_attr != [], 'size_attr为空[]'
        detail_name_list = []
        for item in size_attr:
            detail_name_list.append({
                'spec_name': item.get('title', ''),
                'img_here': 1 if int(item.get('show_sku_img')) == 1 else 0,     # '1' or '0'
            })

        return detail_name_list

    def get_true_sku_info(self, size):
        '''
        得到每个规格对应的库存, 价格, 图片等详细信息
        :param size:
        :return:
        '''
        if size is None or size == []:
            return []

        price_info_list = []
        for item in size:
            tmp_spec_value = item.get('name', '')   # 830白色2件,均码
            spec_value = tmp_spec_value.replace(',', '|')
            detail_price = item.get('jumei_price', '')
            normal_price = item.get('market_price', '')
            img_url = item.get('img', '')
            rest_number = int(item.get('stock', '0'))

            price_info_list.append({
                'spec_value': spec_value,
                'detail_price': detail_price,
                'normal_price': normal_price,
                'img_url': img_url,
                'rest_number': rest_number,
            })

        return price_info_list

    def get_goods_id_from_url(self, jumei_url):
        '''
        得到goods_id
        :param jumei_url:
        :return: goods_id 类型list eg: [] 表示非法url | ['xxxx', 'type=yyyy']
        '''
        jumei_url = re.compile(r'http://').sub(r'https://', jumei_url).replace(';', '')
        try:
            re.compile(r'https://h5.jumei.com/product/detail').findall(jumei_url)[0]
        except IndexError:
            print('聚美优品商品url错误, 非正规的url, 请参照格式(https://h5.jumei.com/product/detail)开头的...')
            return []

        if re.compile(r'https://h5.jumei.com/product/detail\?.*?item_id=(\w+)&{1,}.*?').findall(jumei_url) != []:
            goods_id = re.compile(r'item_id=(\w+)&{1,}').findall(jumei_url)[0]
            # print(goods_id)
            try:
                type = re.compile(r'type=(.*)').findall(jumei_url)[0]
            except IndexError:
                print('获取url的type时出错, 请检查!')
                return []
            print('------>>>| 得到的聚美商品id为: ', goods_id, 'type为: ', type)

            return [goods_id, type]
        else:
            print('获取goods_id时出错, 请检查!')
            return []

    def __del__(self):
        collect()

if __name__ == '__main__':
    jumei = JuMeiYouPinParse()
    while True:
        jumei_url = input('请输入待爬取的聚美优品商品地址: ')
        jumei_url.strip('\n').strip(';')
        goods_id = jumei.get_goods_id_from_url(jumei_url)
        data = jumei.get_goods_data(goods_id=goods_id)
        jumei.deal_with_data()
        pprint(data)
