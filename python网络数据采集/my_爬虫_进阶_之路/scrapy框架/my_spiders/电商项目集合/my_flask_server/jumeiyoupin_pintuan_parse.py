# coding:utf-8

'''
@author = super_fazai
@File    : jumeiyoupin_pintuan_parse.py
@Time    : 2018/3/24 09:33
@connect : superonesfazai@gmail.com
'''

"""
聚美优品拼团页面解析类
"""

from pprint import pprint
from json import dumps
from time import sleep
import re
import gc

import asyncio
import aiohttp
from scrapy.selector import Selector
from settings import (
    MY_SPIDER_LOGS_PATH,
    JUMEIYOUPIN_PINTUAN_GOODS_TIMEOUT,
    PHANTOMJS_DRIVER_PATH,
)
from logging import INFO, ERROR
import pytz
import datetime

from fzutils.cp_utils import _get_right_model_data
from fzutils.log_utils import set_logger
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_phantomjs import MyPhantomjs
from fzutils.spider.fz_aiohttp import MyAiohttp
from fzutils.common_utils import json_2_dict

class JuMeiYouPinPinTuanParse(object):
    def __init__(self, logger=None):
        self._set_headers()
        self.result_data = {}
        self._set_logger(logger)
        self.msg = ''

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 's.h5.jumei.com',
            'Referer': 'https://s.h5.jumei.com/yiqituan/detail?item_id=ht180321p2453550t4&type=global_deal',
            'User-Agent': get_random_pc_ua(),
            'X-Requested-With': 'XMLHttpRequest',
        }

    def _set_logger(self, logger):
        if logger is None:
            self.my_lg = set_logger(
                log_file_name=MY_SPIDER_LOGS_PATH + '/聚美优品/拼团/' + self.get_log_file_name_from_time() + '.txt',
                console_log_level=INFO,
                file_log_level=ERROR
            )
        else:
            self.my_lg = logger

    async def get_goods_data(self, jumei_pintuan_url):
        '''
        异步模拟得到原始data
        :param goods_id:
        :return:
        '''
        goods_id = await self.get_goods_id_from_url(jumei_pintuan_url)
        if goods_id == []:
            self.result_data = {}
            return {}

        '''
        原先采用requests被过滤无返回结果, 于是用aiohttp无奈速度过慢, 换用phantomjs
        '''
        # 拼团商品手机地址
        goods_url = 'https://s.h5.jumei.com/yiqituan/detail?item_id={0}&type={1}'.format(goods_id[0], goods_id[1])
        self.msg = '------>>>| 对应手机端地址为: ' + goods_url
        self.my_lg.info(self.msg)

        #** 获取ajaxDetail请求中的数据
        tmp_url = 'https://s.h5.jumei.com/yiqituan/ajaxDetail?item_id={0}&type={1}'.format(str(goods_id[0]), [goods_id[1]][0])
        # self.headers['Referer'] = goods_url
        # params = {
        #     'item_id': str(goods_id[0]),
        #     'type': [goods_id[1]][0],
        # }
        # body = await MyAiohttp.aio_get_url_body(url=tmp_url, headers=self.headers, params=params, timeout=JUMEIYOUPIN_PINTUAN_GOODS_TIMEOUT)
        # # 获取原始url的tmp_body
        # tmp_body = await MyAiohttp.aio_get_url_body(url=goods_url, headers=self.headers, timeout=JUMEIYOUPIN_PINTUAN_GOODS_TIMEOUT)
        # # print(tmp_body)

        '''
        换用phantomjs
        '''
        my_phantomjs = MyPhantomjs(executable_path=PHANTOMJS_DRIVER_PATH, logger=self.my_lg)
        body = my_phantomjs.use_phantomjs_to_get_url_body(url=tmp_url)
        # print(body)
        try:
            body = re.compile('<pre .*?>(.*)</pre>').findall(body)[0]
            # print(body)
        except IndexError: body = ''
        tmp_body = my_phantomjs.use_phantomjs_to_get_url_body(url=goods_url)
        # print(tmp_body)
        try: del my_phantomjs
        except: pass

        if body == '' or tmp_body == '':
            self.msg = '获取到的body为空str!' + ' 出错地址: ' + goods_url
            self.my_lg.error(self.msg)
            self.result_data = {}
            return {}

        data = await self.json_2_dict(json_str=body)
        if data == {}:
            self.msg = '出错地址: ' + goods_url
            self.my_lg.error(self.msg)
            self.result_data = {}
            return {}
        data = await self.wash_data(data=data)
        data = data.get('data', {})
        # pprint(data)

        try:
            data['title'] = data.get('share_info', [])[1].get('text', '')
            data['title'] = re.compile(r'聚美').sub('', data['title'])
            if len(data.get('buy_alone', {})) == 1:
                data['sub_title'] = ''
            else:
                data['sub_title'] = data.get('buy_alone', {}).get('name', '')
                data['sub_title'] = re.compile(r'聚美').sub('', data['sub_title'])
            # print(data['title'])
            if data['title'] == '':
                self.my_lg.error('获取到的title为空值, 请检查!')
                raise Exception

            # shop_name
            if data.get('shop_info') == []:
                data['shop_name'] = ''
            else:
                data['shop_name'] = data.get('shop_info', {}).get('store_title', '')
            # print(data['shop_name'])

            # 获取所有示例图片
            all_img_url = await self.get_all_img_url(data=data)
            data['all_img_url'] = all_img_url

            # 获取p_info
            p_info = await self.get_p_info(body=tmp_body)
            data['p_info'] = p_info

            # 获取div_desc
            div_desc = await self.get_div_desc(body=tmp_body)
            div_desc = await MyAiohttp.wash_html(div_desc)
            # print(div_desc)
            data['div_desc'] = div_desc

            # 上下架时间(拼团列表数据接口里面有这里先不获取)

            # 设置detail_name_list
            detail_name_list = await self.get_detail_name_list(size_attr=data.get('buy_alone', {}).get('size_attr', []))
            data['detail_name_list'] = detail_name_list

            # 获取每个规格对应价格以及库存
            true_sku_info = await self.get_true_sku_info(buy_alone_size=data.get('buy_alone', {}).get('size', []), size=data.get('size', []), group_single_price=data.get('group_single_price', ''))
            data['price_info_list'] = true_sku_info

            # is_delete
            product_status = data.get('product_status', '')
            is_delete = await self.get_is_delete(product_status=product_status, true_sku_info=true_sku_info)
            data['is_delete'] = is_delete

            # all_sell_count
            all_sell_count = data.get('buyer_number_text', '')
            if all_sell_count != '':
                all_sell_count = re.compile(r'(\d+\.?\d*)').findall(all_sell_count)[0]
                is_W = re.compile(r'万').findall(all_sell_count)
                if is_W != []:
                    all_sell_count = str(int(float(all_sell_count) * 10000))
            else: all_sell_count = '0'
            data['all_sell_count'] = all_sell_count

            data['goods_url'] = goods_url

        except Exception as e:
            self.msg = '遇到错误如下: ' + str(e) + ' 出错地址: ' + goods_url
            self.my_lg.error(self.msg)
            self.my_lg.exception(e)
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            return {}

        if data != {}:
            # pprint(data)
            self.result_data = data
            return data

        else:
            self.msg = 'data为空!' + ' 出错地址: ' + goods_url
            self.my_lg.error(self.msg)
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            return {}

    async def deal_with_data(self, jumei_pintuan_url):
        '''
        得到规范数据并处理
        :return:
        '''
        data = await self.get_goods_data(jumei_pintuan_url=jumei_pintuan_url)
        if data != {}:
            # 店铺名称
            shop_name = data['shop_name']

            # 掌柜
            account = ''

            # 商品名称
            title = data['title']

            # 子标题
            sub_title = data['sub_title']

            # 商品价格和淘宝价
            try:
                tmp_price_list = sorted([round(float(item.get('pintuan_price', '')), 2) for item in data['price_info_list']])
                price = tmp_price_list[-1]  # 商品价格
                taobao_price = tmp_price_list[0]  # 淘宝价
            except IndexError:
                self.msg = '获取price or taobao_price时出错请检查!' + ' 出错地址: ' + data['goods_url']
                self.my_lg.error(self.msg)
                self.result_data = {}
                return {}

            # 商品标签属性名称
            detail_name_list = data['detail_name_list']

            # 要存储的每个标签对应规格的价格及其库存
            price_info_list = data['price_info_list']

            # 所有示例图片地址
            all_img_url = data['all_img_url']

            # 详细信息标签名对应属性
            p_info = data['p_info']

            # div_desc
            div_desc = data['div_desc']

            # 用于判断商品是否已经下架
            is_delete = data['is_delete']

            result = {
                'goods_url': data['goods_url'],         # goods_url
                'shop_name': shop_name,                 # 店铺名称
                'account': account,                     # 掌柜
                'title': title,                         # 商品名称
                'sub_title': sub_title,                 # 子标题
                'price': price,                         # 商品价格
                'taobao_price': taobao_price,           # 淘宝价
                'detail_name_list': detail_name_list,   # 商品标签属性名称
                'price_info_list': price_info_list,     # 要存储的每个标签对应规格的价格及其库存
                'all_img_url': all_img_url,             # 所有示例图片地址
                'p_info': p_info,                       # 详细信息标签名对应属性
                'div_desc': div_desc,                   # div_desc
                'all_sell_count': data['all_sell_count'], # 总销量
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
            try:
                self.msg = '待处理的data为空的dict, 该商品可能已经转移或者下架' + ' 出错地址: ' + data['goods_url']
                self.my_lg.error(self.msg)
            except KeyError:
                pass
            return {}

    async def insert_into_jumeiyoupin_pintuan_table(self, data, pipeline, logger):
        '''
        存储数据
        :param data:
        :param pipeline:
        :param logger
        :return:
        '''
        try:
            tmp = _get_right_model_data(data=data, site_id=27, logger=self.my_lg)  # 采集来源地(聚美优品拼团商品)
        except:
            self.my_lg.error('此处抓到的可能是聚美优品拼团券所以跳过')
            return None
        # print('------>>> | 待存储的数据信息为: |', tmp)
        self.msg = '------>>>| 待存储的数据信息为: |' + str(tmp.get('goods_id'))
        logger.info(self.msg)

        params = await self._get_db_insert_pintuan_params(item=tmp)
        sql_str = r'insert into dbo.jumeiyoupin_pintuan(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, all_sell_count, page, sort, tab, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        try:
            pipeline._insert_into_table_2(sql_str=sql_str, params=params, logger=logger)
            return True
        except Exception as e:
            logger.exception(e)
            return False

    async def update_jumeiyoupin_pintuan_table(self, data, pipeline, logger):
        '''
        异步更新数据
        :param data:
        :param pipeline:
        :param logger:
        :return:
        '''
        try:
            tmp = _get_right_model_data(data=data, site_id=27, logger=self.my_lg)
        except:
            self.my_lg.error('此处抓到的可能是聚美优品拼团券所以跳过')
            return None
        # print('------>>> | 待存储的数据信息为: |', tmp)
        self.msg = '------>>>| 待存储的数据信息为: |' + str(tmp.get('goods_id'))
        logger.info(self.msg)

        params = await self._get_db_update_pintuan_params(item=tmp)
        sql_str = 'update dbo.jumeiyoupin_pintuan set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s, all_sell_count=%s where goods_id = %s'
        try:
            pipeline._update_table_2(sql_str=sql_str, params=params, logger=logger)
            return True
        except Exception as e:
            logger.exception(e)
            return False

    async def update_jumeiyoupin_pintuan_table_2(self, data, pipeline, logger):
        '''
        异步更新数据
        :param data:
        :param pipeline:
        :param logger:
        :return:
        '''
        try:
            tmp = _get_right_model_data(data=data, site_id=27, logger=self.my_lg)
        except:
            self.my_lg.error('此处抓到的可能是聚美优品拼团券所以跳过')
            return None
        # print('------>>> | 待存储的数据信息为: |', tmp)
        self.msg = '------>>>| 待存储的数据信息为: |' + str(tmp.get('goods_id'))
        logger.info(self.msg)

        params = self._get_db_update_pintuan_params_2(item=tmp)
        sql_str = 'update dbo.jumeiyoupin_pintuan set modfiy_time=%s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, all_sell_count=%s where goods_id = %s'
        try:
            result = pipeline._update_table_2(sql_str=sql_str, params=params, logger=logger)
            return result
        except Exception as e:
            logger.exception(e)
            return False

    async def _get_db_insert_pintuan_params(self, item):
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
            dumps(item['pintuan_time'], ensure_ascii=False),
            item['pintuan_begin_time'],
            item['pintuan_end_time'],
            item['all_sell_count'],
            item['page'],
            item['sort'],
            item['tab'],

            item['site_id'],
            item['is_delete'],
        )

        return params

    async def _get_db_update_pintuan_params(self, item):
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
            dumps(item['pintuan_time'], ensure_ascii=False),
            item['pintuan_begin_time'],
            item['pintuan_end_time'],
            item['all_sell_count'],

            item['goods_id'],
        )

        return params

    async def _get_db_update_pintuan_params_2(self, item):
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
            item['all_sell_count'],

            item['goods_id'],
        )

        return params

    async def get_all_img_url(self, data):
        '''
        得到all_img_url
        :param data:
        :return:
        '''
        if len(data.get('buy_alone', {})) == 1:
            all_img_url = data.get('share_info', [])[1].get('image_url_set', {}).get('url', {}).get('800', '')
            if all_img_url == '':
                self.my_lg.error('all_img_url获取失败!')
                raise Exception
        else:
            all_img_url = data.get('buy_alone', {}).get('image_url_set', {}).get('single', {}).get('800', '')

        all_img_url = [{
            'img_url': all_img_url,
        }]

        return all_img_url

    async def get_p_info(self, body):
        '''
        得到p_info
        :param body:
        :return:
        '''
        p_info = []
        for item in list(Selector(text=body).css('ul.detail_arg li').extract()):
            p_name = str(Selector(text=item).css('span.arg_title::text').extract_first())
            p_value = str(Selector(text=item).css('span.arg_content::text').extract_first())
            p_info.append({
                'p_name': p_name,
                'p_value': p_value,
            })

        return p_info

    async def get_div_desc(self, body):
        '''
        获取div_desc
        :param body:
        :return:
        '''
        try:
            tmp_div_desc = str(Selector(text=body).css('section#detailImg').extract_first())
        except:
            self.my_lg.error('获取到的div_desc出错,请检查!')
            raise Exception

        tmp_div_desc = re.compile(r'src="http://p0.jmstatic.com/templates/jumei/images/baoxian_pop.jpg"').sub('', tmp_div_desc)

        return '<div>' + tmp_div_desc + '</div>'

    async def get_detail_name_list(self, size_attr):
        '''
        获取detail_name_list
        :param size_attr:
        :return:
        '''
        detail_name_list = [{'spec_name': item.get('title', '')} for item in size_attr]
        if size_attr == []:
            # print('获取detail_name_list失败!')
            detail_name_list = [{'spec_name': '规格'}]

        return detail_name_list

    async def get_true_sku_info(self, **kwargs):
        '''
        获取每个规格对应价格跟库存
        :param kwargs:
        :return:
        '''
        buy_alone_size = kwargs.get('buy_alone_size')
        size = kwargs.get('size')
        try:
            group_single_price = re.compile(r'(\d+)').findall(kwargs.get('group_single_price'))[0]  # 单独购买价格
        except IndexError:
            group_single_price = ''
        if size == []:
            self.my_lg.error('size为空[]')
            raise Exception

        if buy_alone_size == []:
            alone_size = []
        else:
            alone_size = [{
                'spec_value': item.get('name', '').replace(',', '|'),
                'alone_price': item.get('jumei_price', '')
            } for item in buy_alone_size]

        true_sku_info = [{
            'spec_value': item.get('name', '').replace(',', '|'),
            'pintuan_price': item.get('jumei_price', ''),
            'detail_price': item.get('market_price', ''),
            'normal_price': '',
            'img_url': item.get('img', ''),
            'rest_number': int(item.get('stock', '0')),
        } for item in size]

        if alone_size != []:
            for item_1 in alone_size:
                for item_2 in true_sku_info:
                    if item_1.get('spec_value') == item_2.get('spec_value'):
                        item_2['detail_price'] = item_1['alone_price']

        else:   # 拿单独购买价来设置detail_price
            for item in true_sku_info:      # alone_size为空，表示: 单独无法购买 可能出现小于拼团价的情况 eg: http://s.h5.jumei.com/yiqituan/detail?item_id=df1803156441482p3810742&type=jumei_pop&selltype=coutuanlist&selllabel=coutuan_home
                item['detail_price'] = '单价模式无法购买'

        return true_sku_info

    async def get_is_delete(self, **kwargs):
        '''
        获取商品上下架状态
        :param params:
        :return:
        '''
        is_delete = 0
        product_status = kwargs.get('product_status', '')
        true_sku_info = kwargs.get('true_sku_info')

        all_stock = 0
        for item in true_sku_info:
            all_stock += item.get('rest_number', 0)
        if all_stock == 0: is_delete = 1            # 总库存为0
        if product_status == 'end': is_delete = 1   # 商品状态为end

        return is_delete

    async def wash_data(self, data):
        '''
        清洗数据
        :param data:
        :return:
        '''
        try:
            del data['data']['address_list']
            del data['data']['default_address']
            del data['data']['fen_qi']
            del data['data']['icon_tag']
            del data['data']['price_detail']
            del data['data']['recommend_data']
            del data['data']['recommend_group']
            # del data['data']['share_info']
            del data['data']['wechat_switches']
        except Exception:
            pass

        return data

    def get_log_file_name_from_time(self):
        '''
        得到log文件的时间名字
        :return: 格式: 2016-03-25 类型str
        '''
        # 时区处理，时间处理到上海时间
        # pytz查询某个国家时区
        country_timezones_list = pytz.country_timezones('cn')
        # print(country_timezones_list)

        tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
        now_time = datetime.datetime.now(tz)
        # print(type(now_time))

        # 处理为精确到秒位，删除时区信息
        now_time = re.compile(r'\..*').sub('', str(now_time))
        # 将字符串类型转换为datetime类型
        now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
        # print(now_time)

        return str(now_time)[0:10]

    async def json_2_dict(self, json_str):
        '''
        异步json_2_dict
        :param json_str:
        :return: {} | {...}
        '''
        return json_2_dict(json_str=json_str, logger=self.my_lg)

    async def get_goods_id_from_url(self, jumei_url):
        '''
        得到goods_id
        :param jumei_url:
        :return: goods_id 类型list eg: [] 表示非法url | ['xxxx', 'type=yyyy']
        '''
        jumei_url = re.compile(r'http://').sub(r'https://', jumei_url)
        jumei_url = re.compile(r';').sub('', jumei_url)
        is_jumei_url = re.compile(r'https://s.h5.jumei.com/yiqituan/detail').findall(jumei_url)
        if is_jumei_url != []:
            if re.compile('$&').findall(jumei_url) == []:   # 先加个&再做re筛选
                jumei_url += '&'

            if re.compile(r'item_id=(\w+)&{1,}.*?').findall(jumei_url) != []:
                goods_id = re.compile(r'item_id=(\w+)&{1,}.*').findall(jumei_url)[0]
                # print(goods_id)
                try:
                    type = re.compile(r'&type=(.*?)&{1,}.*').findall(jumei_url)[0]
                except IndexError:
                    self.msg = '获取url的type时出错, 请检查!' + ' 出错地址: ' + jumei_url
                    self.my_lg.error(self.msg)
                    return []
                self.msg = '------>>>| 得到的聚美商品id为: ' + goods_id + ' type为: ' + type
                self.my_lg.info(self.msg)

                return [goods_id, type]
            else:
                self.msg = '获取goods_id时出错, 请检查!' + '出错地址:' + jumei_url
                self.my_lg.error(self.msg)
                return []

        else:
            self.msg = '聚美优品商品url错误, 非正规的url, 请参照格式(https://s.h5.jumei.com/yiqituan/detail)开头的...' + ' 出错地址: ' + jumei_url
            self.my_lg.error(self.msg)
            return []

    def __del__(self):
        try:
            del self.my_lg
            del self.msg
        except: pass
        gc.collect()

if __name__ == '__main__':
    jumei_pintuan = JuMeiYouPinPinTuanParse()
    while True:
        try:
            jumei_url = input('请输入待爬取的聚美优品商品地址: ')
            jumei_url.strip('\n').strip(';')
            loop = asyncio.get_event_loop()
            result = loop.run_until_complete(jumei_pintuan.deal_with_data(jumei_url))
            pprint(result)
        except KeyboardInterrupt:
            print('\nKeyboardInterrupt')
            try: loop.close()
            except NameError: pass

