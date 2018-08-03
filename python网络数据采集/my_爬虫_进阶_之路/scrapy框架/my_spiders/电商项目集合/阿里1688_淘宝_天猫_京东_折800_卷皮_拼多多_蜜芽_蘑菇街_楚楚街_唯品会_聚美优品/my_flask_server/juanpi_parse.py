# coding:utf-8

'''
@author = super_fazai
@File    : juanpi_parse.py
@Time    : 2017/11/17 17:26
@connect : superonesfazai@gmail.com
'''

"""
卷皮页面采集系统(别翻墙使用)
"""

import time
import json
from pprint import pprint
from json import dumps
from time import sleep
import re
import gc

from settings import PHANTOMJS_DRIVER_PATH
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from fzutils.cp_utils import _get_right_model_data
from fzutils.time_utils import (
    timestamp_to_regulartime,
)
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests
from fzutils.spider.fz_phantomjs import MyPhantomjs
from fzutils.common_utils import json_2_dict

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

class JuanPiParse(object):
    def __init__(self):
        super(JuanPiParse, self).__init__()
        self._set_headers()
        self.result_data = {}
        self.my_phantomjs = MyPhantomjs(executable_path=PHANTOMJS_DRIVER_PATH)

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'web.juanpi.com',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    def get_goods_data(self, goods_id):
        '''
        模拟构造得到data的url
        :param goods_id:
        :return: data   类型dict
        '''
        if goods_id == '':
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            return {}
        else:
            tmp_url = 'https://web.juanpi.com/pintuan/shop/' + str(goods_id)
            print('------>>>| 得到的商品手机版的地址为: ', tmp_url)

            '''
            1.原先使用requests来模拟(起初安全的运行了一个月)，但是后来发现光requests会not Found，记住使用前别翻墙
            '''
            # try:
            #     response = requests.get(tmp_url, headers=self.headers, proxies=tmp_proxies, timeout=12)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            #     main_body = response.content.decode('utf-8')
            #     # print(main_body)
            #     # main_body = re.compile(r'\n').sub('', main_body)
            #     main_body = re.compile(r'\t').sub('', main_body)
            #     main_body = re.compile(r'  ').sub('', main_body)
            #     print(main_body)
            #     data = re.compile(r'__PRELOADED_STATE__=(.*),window\.__SERVER_TIME__=').findall(main_body)  # 贪婪匹配匹配所有
            #     print(data)
            # except Exception:
            #     print('requests.get()请求超时....')
            #     print('data为空!')
            #     self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            #     return {}

            '''
            2.采用phantomjs来处理，记住使用前别翻墙
            '''
            body = self.my_phantomjs.use_phantomjs_to_get_url_body(url=tmp_url, css_selector='div.sc-kgoBCf.bTQvTk')    # 该css为手机端标题块
            if body == '':
                print('获取到的body为空str!请检查!')
                self.result_data = {}
                return {}

            data = re.compile(r'__PRELOADED_STATE__ = (.*);</script> <style ').findall(body)  # 贪婪匹配匹配所有

            # 得到skudata
            # 卷皮原先的skudata请求地址1(官方放弃)
            # skudata_url = 'https://webservice.juanpi.com/api/getOtherInfo?goods_id=' + str(goods_id)
            # 现在卷皮skudata请求地址2
            skudata_url = 'https://webservice.juanpi.com/api/getMemberAboutInfo?goods_id=' + str(goods_id)

            self.skudata_headers = self.headers
            self.skudata_headers.update({'Host': 'webservice.juanpi.com'})
            skudata_body = MyRequests.get_url_body(url=skudata_url, headers=self.skudata_headers)
            if skudata_body == '':
                print('获取到的skudata_body为空str!请检查!')
                self.result_data = {}
                return {}
            skudata = re.compile(r'(.*)').findall(skudata_body)  # 贪婪匹配匹配所有

            if skudata != []:
                skudata = skudata[0]
                skudata = json_2_dict(json_str=skudata)
                if skudata == {}:
                    self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                    return {}
                skudata = skudata.get('skudata', {})
                # pprint(skudata)

                try:
                    if skudata.get('info') is not None:
                        pass    # 说明得到正确的skudata

                    else:       # 否则跳出
                        print('skudata中info的key为None, 返回空dict')
                        self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                        return {}

                except AttributeError as e:
                    print('遇到错误如下(先跳过!): ', e)
                    self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                    return {}

            else:
                print('skudata为空!')
                self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                return {}

            if data != []:
                main_data = json_2_dict(json_str=data[0])
                if main_data == {}:
                    self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                    return {}

                if main_data.get('detail') is not None:
                    main_data = self._wash_main_data(main_data.get('detail', {}))

                    main_data['skudata'] = skudata
                    # pprint(main_data)
                    # print(main_data)
                    main_data['goods_id'] = goods_id
                    self.result_data = main_data
                    return main_data

                else:
                    print('data中detail的key为None, 返回空dict')
                    self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                    return {}
            else:
                print('data为空!')
                self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                return {}

    def deal_with_data(self):
        '''
        解析data数据,得到需要的东西
        :return: dict
        '''
        data = self.result_data
        if data != {}:
            # 店铺名称
            shop_name = self._get_shop_name(data=data)

            # 掌柜
            account = ''

            # 商品名称
            title = data.get('baseInfo', {}).get('title', '')

            # 子标题
            sub_title = ''

            # 商品库存

            # 商品标签属性名称
            detail_name_list = self._get_detail_name_list(data=data)
            if isinstance(detail_name_list, str):       # 单独处理下架的情况
                if detail_name_list == 'is_delete=1':
                    print('该商品已下架...')
                    sql_str = 'update dbo.GoodsInfoAutoGet set IsDelete=1 where GoodsID=%s'
                    params = (self.result_data.get('goods_id', ''),)
                    _ = SqlServerMyPageInfoSaveItemPipeline()
                    result = _._update_table(sql_str=sql_str, params=params)
                    if result:
                        print('### 该商品已经is_delete=1 ###')
                    else:
                        print('is_delete=1标记失败!')

            if detail_name_list == {}:
                self.result_data = {}
                return {}
            # print(detail_name_list)

            # 商品标签属性对应的值(pass不采集)

            # 要存储的每个标签对应的规格的价格及其库存
            price_info_list, price, taobao_price = self._get_price_info_list_and_price_and_taobao_price(data=data)
            # print('最高价为: ', price)
            # print('最低价为: ', taobao_price)
            # pprint(price_info_list)

            # 所有示例图片的地址
            # pprint(data.get('goodImages'))
            all_img_url = [{'img_url': item} for item in data.get('goodImages')]
            # print(all_img_url)

            # 详细信息标签名对应的属性
            p_info = self._get_p_info(data=data)

            # pprint(p_info)

            # div_desc
            div_desc = self._get_div_desc(data=data)
            # print(div_desc)

            # 商品销售时间段
            schedule = self._get_goods_schedule(data=data)
            # pprint(schedule)

            is_delete = self._get_is_delete(data=data, schedule=schedule)
            if price == 0 or taobao_price == 0:     # 没有获取到价格说明商品已经下架了
                is_delete = 1
            # print('is_delete = ', is_delete)

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
        tmp = _get_right_model_data(data=data, site_id=12)
        params = self._get_db_update_params(item=tmp)
        # 改价格的sql语句
        # sql_str = r'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, MyShelfAndDownTime=%s, delete_time=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s where GoodsID = %s'
        # 不改价格的sql语句
        if tmp['delete_time'] == '':
            sql_str = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s, shelf_time=%s where GoodsID = %s'
        elif tmp['shelf_time'] == '':
            sql_str = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s, delete_time=%s where GoodsID = %s'
        else:
            sql_str = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, IsDelete=%s, Schedule=%s, IsPriceChange=%s, PriceChangeInfo=%s, shelf_time=%s, delete_time=%s where GoodsID = %s'

        pipeline._update_table(sql_str=sql_str, params=params)

    def insert_into_juanpi_xianshimiaosha_table(self, data, pipeline):
        tmp = _get_right_model_data(data=data, site_id=15)
        # print('------>>> | 待存储的数据信息为: |', tmp)
        print('------>>> | 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_insert_miaosha_params(item=tmp)
        sql_str = 'insert into dbo.juanpi_xianshimiaosha(goods_id, goods_url, username, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_info, all_image_url, property_info, detail_info, schedule, stock_info, miaosha_time, miaosha_begin_time, miaosha_end_time, tab_id, page, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        pipeline._insert_into_table(sql_str=sql_str, params=params)

    def to_update_juanpi_xianshimiaosha_table(self, data, pipeline):
        tmp = _get_right_model_data(data=data, site_id=15)
        # print('------>>> | 待存储的数据信息为: |', tmp)
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_update_miaosha_params(item=tmp)
        sql_str = 'update dbo.juanpi_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, schedule=%s, stock_info=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s where goods_id = %s'
        pipeline._update_table(sql_str=sql_str, params=params)

    def insert_into_juuanpi_pintuan_table(self, data, pipeline):
        try:
            tmp = _get_right_model_data(data=data, site_id=18)
        except:
            print('此处抓到的可能是卷皮拼团券所以跳过')
            return None

        # print('------>>> | 待存储的数据信息为: |', tmp)
        print('------>>> | 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_insert_pintuan_params(item=tmp)
        sql_str = 'insert into dbo.juanpi_pintuan(goods_id, goods_url, username, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_info, all_image_url, all_sell_count, property_info, detail_info, schedule, miaosha_begin_time, miaosha_end_time, page, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        _r = pipeline._insert_into_table(sql_str=sql_str, params=params)

        return _r

    def to_right_and_update_pintuan_data(self, data, pipeline):
        try:
            tmp = _get_right_model_data(data=data, site_id=18)
        except:
            print('此处抓到的可能是卷皮拼团券所以跳过')
            return None
        # print('------>>>| 待存储的数据信息为: |', tmp)
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_update_pintuan_params(item=tmp)
        sql_str = r'update dbo.juanpi_pintuan set modfiy_time=%s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, schedule=%s, is_delete=%s where goods_id = %s'
        pipeline._update_table(sql_str=sql_str, params=params)

    def _get_shop_name(self, data):
        '''
        获取shop_name
        :param data:
        :return:
        '''
        if data.get('brand_info') is not None:
            shop_name = data.get('brand_info', {}).get('title', '')
        else:
            shop_name = data.get('schedule_info', {}).get('brand_title', '')

        return shop_name

    def _get_detail_name_list(self, data):
        '''
        获取detail_name_list
        :param data:
        :return: {} 表示出错 | [] 非空正常
        '''
        sku = data.get('skudata', {}).get('sku', [])
        # pprint(sku)
        detail_name_list = []
        if sku != []:
            try:
                if sku[0].get('av_fvalue', '') == '':
                    fav_name = ''
                    pass
                else:
                    tmp = {}
                    fav_name = data.get('skudata', {}).get('info', {}).get('fav_name', '')
                    tmp['spec_name'] = fav_name
                    detail_name_list.append(tmp)
            except IndexError:
                print('IndexError错误，此处跳过!')
                # print(sku)
                if isinstance(sku, str):    # 单独处理下架的
                    if sku == '':
                        return 'is_delete=1'

                return {}

            if sku[0].get('av_zvalue', '') == '':
                zav_name = ''
            else:
                tmp = {}
                zav_name = data.get('skudata', {}).get('info', {}).get('zav_name', '')
                tmp['spec_name'] = zav_name
                detail_name_list.append(tmp)

        return detail_name_list

    def _get_price_info_list_and_price_and_taobao_price(self, data):
        '''
        获取price_info_list, price, taobao_price
        :param data:
        :return: a tuple
        '''
        sku = data.get('skudata', {}).get('sku', [])  # 分析得到sku肯定不为[]
        # pprint(sku)
        price_info_list = []
        if len(sku) == 1 and sku[0].get('av_fvalue', '') == '' and sku[0].get('av_zvalue') == '':  # 没有规格的默认只有一个{}
            # price最高价, taobao_price最低价
            price = round(float(sku[0].get('cprice')), 2)
            taobao_price = price

        else:  # 有规格的
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
                    tmp['pintuan_price'] = item.get('cprice')
                    tmp['detail_price'] = item.get('sprice', '')
                    tmp['normal_price'] = item.get('price')
                else:
                    tmp['pintuan_price'] = item.get('price')
                    if item.get('sprice', '') != '':
                        tmp['detail_price'] = item.get('sprice', '')
                    else:
                        tmp['detail_price'] = item.get('price')
                    tmp['normal_price'] = item.get('price')

                if item.get('stock') == '0':  # 跳过
                    rest_number = '0'
                else:  # 即'stock'='1'
                    rest_number = '50'

                    if item.get('stock_tips', '') != '' and item.get('stock_tips', '') == '库存紧张':
                        # 库存紧张的时候设置下
                        rest_number = '10'

                    tmp['spec_value'] = tmp_1
                    tmp['rest_number'] = rest_number
                    price_info_list.append(tmp)

            # 得到有规格时的最高价和最低价
            tmp_price_list = sorted([round(float(item.get('pintuan_price', '')), 2) for item in price_info_list])
            # print(tmp_price_list)
            if tmp_price_list == []:
                price = 0
                taobao_price = 0
            else:
                price = tmp_price_list[-1]  # 商品价格
                taobao_price = tmp_price_list[0]  # 淘宝价

        return price_info_list, price, taobao_price

    def _get_p_info(self, data):
        '''
        获取p_info
        :param data:
        :return:
        '''
        p_info = []
        attr = data.get('goodsDetail', {}).get('attr', [])
        # print(attr)
        if attr != []:
            # item是str时跳过
            p_info = [{'p_name': item.get('st_key'), 'p_value': item.get('st_value')} for item in attr if isinstance(item, dict)]
            for item in p_info:
                if item.get('p_name') == '运费':
                    # 过滤掉颜色的html代码
                    item['p_value'] = '全国包邮(偏远地区除外)'

                # 过滤清洗
                tmp_p_value = item.get('p_value', '')
                tmp_p_value = re.compile(r'\xa0').sub(' ', tmp_p_value)  # 替换为一个空格
                item['p_value'] = tmp_p_value

        return p_info

    def _get_div_desc(self, data):
        '''
        获取div_desc
        :param data:
        :return:
        '''
        div_images_list = data.get('goodsDetail', {}).get('images', [])
        tmp_div_desc = ''
        for item in div_images_list:
            tmp = r'<img src="{}" style="height:auto;width:100%;"/>'.format(item)
            tmp_div_desc += tmp

        return '<div>' + tmp_div_desc + '</div>'

    def _get_goods_schedule(self, data):
        '''
        获取商品销售时间段
        :param data:
        :return:
        '''
        # print(data.get('skudata', {}).get('info', {}))
        # print(data.get('skudata', {}))
        begin_time = data.get('skudata', {}).get('info', {}).get('start_time')  # 取这个时间段才是正确的销售时间, 之前baseInfo是虚假的
        end_time = data.get('skudata', {}).get('info', {}).get('end_time')
        if begin_time is None or end_time is None:
            schedule = []
        else:
            schedule = [{
                'begin_time': timestamp_to_regulartime(begin_time),
                'end_time': timestamp_to_regulartime(end_time),
            }]

        return schedule

    def _get_is_delete(self, data, schedule):
        '''
        得到商品的上下架状态
        :param data:
        :param schedule:
        :return:
        '''
        end_time = data.get('skudata', {}).get('info', {}).get('end_time')
        is_delete = 0
        # 是否下架判断
        # 结束时间戳小于当前时间戳则表示已经删除无法购买, 另外每个规格卖光也不显示is_delete=1(在上面已经判断, 这个就跟销售时间段没关系了)
        if schedule != []:
            if data.get('baseInfo', {}).get('end_time') is not None:
                '''
                先判断如果baseInfo中的end_time=='0'表示已经下架
                '''
                # base_info_end_time = data.get('baseInfo', {}).get('end_time')
                # self.my_lg.info(base_info_end_time)
                # if base_info_end_time == '0':
                #     is_delete = 1
                pass

            if float(end_time) < time.time():
                '''
                再判断日期过期的
                '''
                is_delete = 1

        '''
        卷皮-新增下架判断:
        time: 2018-5-12 
        '''
        if data.get('skudata', {}).get('info', {}).get('gstatus', '1') == '2':
            # 'gstatus'在售状态为'1'
            is_delete = 1

        return is_delete

    def _wash_main_data(self, main_data):
        '''
        清洗main_data
        :param main_data:
        :return:
        '''
        # 处理commitments
        try:
            main_data['commitments'] = ''
            main_data.get('discount', {})['coupon'] = ''
            main_data.get('discount', {})['coupon_index'] = ''
            main_data.get('discount', {})['vip_info'] = ''
            main_data['topbanner'] = ''
        except:
            pass
        try:
            main_data.get('brand_info')['sub_goods'] = ''
        except:
            pass

        return main_data

    def _get_db_update_params(self, item):
        '''
        得到待更新的db数据
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
            # item['price'],
            # item['taobao_price'],
            dumps(item['price_info'], ensure_ascii=False),
            dumps(item['detail_name_list'], ensure_ascii=False),
            dumps(item['price_info_list'], ensure_ascii=False),
            dumps(item['all_img_url'], ensure_ascii=False),
            dumps(item['p_info'], ensure_ascii=False),
            item['div_desc'],
            # item['delete_time'],
            item['is_delete'],
            dumps(item['schedule'], ensure_ascii=False),
            item['is_price_change'],
            dumps(item['price_change_info'], ensure_ascii=False),

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
            item['tab_id'],
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
            dumps(item['schedule'], ensure_ascii=False),
            dumps(item['stock_info'], ensure_ascii=False),
            dumps(item['miaosha_time'], ensure_ascii=False),
            item['miaosha_begin_time'],
            item['miaosha_end_time'],

            item['goods_id'],
        )

        return params

    def _get_db_insert_pintuan_params(self, item):
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
            item['all_sell_count'],
            dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
            item['div_desc'],  # 存入到DetailInfo
            dumps(item['schedule'], ensure_ascii=False),
            item['pintuan_begin_time'],
            item['pintuan_end_time'],
            item['page'],

            item['site_id'],
            item['is_delete'],
        )

        return params

    def _get_db_update_pintuan_params(self, item):
        params = (
            item['modify_time'],
            item['shop_name'],
            item['title'],
            item['sub_title'],
            item['price'],
            item['taobao_price'],
            dumps(item['detail_name_list'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
            dumps(item['price_info_list'], ensure_ascii=False),
            dumps(item['all_img_url'], ensure_ascii=False),
            # item['all_sell_count'],
            dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
            item['div_desc'],  # 存入到DetailInfo
            dumps(item['schedule'], ensure_ascii=False),
            item['is_delete'],

            item['goods_id']
        )

        return params

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
                else:   # 只是为了在pycharm运行时不跳到chrome，其实else完全可以不要的
                    juanpi_url = re.compile(r';').sub('', juanpi_url)
                    goods_id = re.compile(r'http://shop.juanpi.com/deal/(\d+).*?').findall(juanpi_url)[0]
                print('------>>>| 得到的卷皮商品的地址为:', goods_id)
                return goods_id

        else:
            print('卷皮商品url错误, 非正规的url, 请参照格式(http://shop.juanpi.com/deal/)开头的...')
            return ''

    def __del__(self):
        try:
            del self.my_phantomjs
            del self.result_data
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    juanpi = JuanPiParse()
    while True:
        juanpi_url = input('请输入待爬取的卷皮商品地址: ')
        juanpi_url.strip('\n').strip(';')
        goods_id = juanpi.get_goods_id_from_url(juanpi_url)
        juanpi.get_goods_data(goods_id=goods_id)
        data = juanpi.deal_with_data()
        # pprint(data)