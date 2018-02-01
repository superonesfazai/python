# coding:utf-8

'''
@author = super_fazai
@File    : mogujie_miaosha_parse.py
@Time    : 2018/1/31 13:06
@connect : superonesfazai@gmail.com
'''

import time
from random import randint
import json
import requests
import re
from pprint import pprint
from decimal import Decimal

from time import sleep
import datetime
import gc

from settings import HEADERS
import pytz

from mogujie_parse import MoGuJieParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

class MoGuJieMiaoShaParse(MoGuJieParse):
    def __init__(self):
        MoGuJieParse.__init__(self)

    def get_goods_data(self, goods_id:str) -> '重载获取数据的方法':
        '''
        模拟构造得到data的url
        :param goods_id:
        :return: data dict类型
        '''
        if goods_id == '':
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            return {}
        else:
            if re.compile(r'/rushdetail/').findall(goods_id) != []:
                tmp_url = goods_id
                print('------>>>| 原pc地址为: ', tmp_url)

                goods_id = re.compile('https://shop.mogujie.com/rushdetail/(.*?)\?.*?').findall(goods_id)[0]
                print('------>>>| 得到的蘑菇街商品id为:', goods_id)

            else:
                print('获取到的蘑菇街买哦啥地址错误!请检查')
                self.result_data = {}
                return {}

            data = {}

            body = self.get_url_body(tmp_url=tmp_url)
            # print(body)

            if body == '':
                print('获取到的body为空str!')
                self.result_data = {}
                return {}

            try:
                goods_info = re.compile(r'var detailInfo = (.*?);</script>').findall(body)[0]
                # print(goods_info)

                item_info = re.compile(r'itemInfo:(.*?) ,priceRuleImg').findall(goods_info)[0]
                # print(item_info)

                sku_info = re.compile(r'skuInfo:(.*?),pinTuanInfo').findall(goods_info)[0]
                # print(sku_info)

                shop_info = re.compile(r'shopInfo:(.*?),skuInfo').findall(goods_info)[0]
                # print(shop_info)

                item_info = json.loads(item_info)
                sku_info = json.loads(sku_info)
                shop_info = json.loads(shop_info)
                # pprint(item_info)
                # pprint(sku_info)
                # pprint(shop_info)

                data['title'] = item_info.get('title', '')
                if data['title'] == '':
                    print('title为空!')
                    raise Exception

                data['sub_title'] = ''

                data['shop_name'] = shop_info.get('name', '')
                # print(data['shop_name'])

                # 获取所有示例图片
                all_img_url = [{'img_url': item} for item in item_info.get('topImages', [])]
                # pprint(all_img_url)
                data['all_img_url'] = all_img_url

                '''
                获取p_info
                '''
                p_info_api_url = 'https://shop.mogujie.com/ajax/mgj.pc.detailinfo/v1?_ajax=1&itemId=' + str(goods_id)
                tmp_p_info_body = self.get_url_body(tmp_url=p_info_api_url)
                # print(tmp_p_info_body)
                if tmp_p_info_body == '':
                    print('获取到的tmp_p_info_body为空值, 请检查!')
                    raise Exception

                p_info = self.get_goods_p_info(tmp_p_info_body=tmp_p_info_body)
                # pprint(p_info)
                # if p_info == []:
                #     print('获取到的p_info为空list')
                #     self.result_data = {}
                #     return {}
                # else:
                # 不做上面判断了因为存在没有p_info的商品
                data['p_info'] = p_info

                # 获取每个商品的div_desc
                div_desc = self.get_goods_div_desc(tmp_p_info_body=tmp_p_info_body)
                # print(div_desc)
                if div_desc == '':
                    print('获取到的div_desc为空str, 请检查!')
                    self.result_data = {}
                    return {}
                else:
                    data['div_desc'] = div_desc

                '''
                获取去detail_name_list
                '''
                detail_name_list = self.get_goods_detail_name_list(sku_info=sku_info)
                # print(detail_name_list)
                if detail_name_list == '':
                    print('获取detail_name_list出错, 请检查!')
                    self.result_data = {}
                    return {}
                else:
                    data['detail_name_list'] = detail_name_list

                '''
                获取每个规格对应价格跟规格以及其库存
                '''
                price_info_list = self.get_price_info_list(sku_info=sku_info)
                # pprint(price_info_list)
                if price_info_list == '':
                    raise Exception
                else:
                    # pprint(price_info_list)
                    data['price_info_list'] = price_info_list


                if price_info_list == []:
                    print('该商品已售完，此处将商品状态改为1')
                    my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                    try:
                        my_pipeline.update_mogujie_miaosha_table_is_delete(goods_id=goods_id)
                    except:
                        print('将该商品逻辑删除时出错!')
                        pass
                    self.result_data = {}
                    return {}

                # 商品价格和淘宝价
                try:
                    tmp_price_list = sorted([round(float(item.get('detail_price', '')), 2) for item in data['price_info_list']])
                    price = Decimal(tmp_price_list[-1]).__round__(2)  # 商品价格
                    taobao_price = Decimal(tmp_price_list[0]).__round__(2)  # 淘宝价
                    # print('商品的最高价: ', price, ' 最低价: ', taobao_price)
                except IndexError:
                    print('获取price和taobao_price时出错! 请检查')
                    raise Exception

                data['price'] = price
                data['taobao_price'] = taobao_price

            except Exception as e:
                print('遇到错误: ', e)
                self.result_data = {}
                return {}

            if data != {}:
                # pprint(data)
                self.result_data = data
                return data

            else:
                print('data为空!')
                self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                return {}

    def insert_into_mogujie_xianshimiaosha_table(self, data, pipeline):
        data_list = data
        tmp = {}
        tmp['goods_id'] = data_list['goods_id']  # 官方商品id
        tmp['spider_url'] = data_list['goods_url']  # 商品地址

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
        tmp['sub_title'] = data_list['sub_title']

        # 设置最高价price， 最低价taobao_price
        try:
            tmp['price'] = Decimal(data_list['price']).__round__(2)
            tmp['taobao_price'] = Decimal(data_list['taobao_price']).__round__(2)
        except:
            print('此处抓到的可能是蘑菇街券所以跳过')
            return None

        tmp['detail_name_list'] = data_list['detail_name_list']  # 标签属性名称

        """
        得到sku_map
        """
        tmp['price_info_list'] = data_list.get('price_info_list')  # 每个规格对应价格及其库存

        tmp['all_img_url'] = data_list.get('all_img_url')  # 所有示例图片地址

        tmp['p_info'] = data_list.get('p_info')  # 详细信息
        tmp['div_desc'] = data_list.get('div_desc')  # 下方div

        tmp['miaosha_time'] = data_list.get('miaosha_time')
        tmp['event_time'] = data_list.get('event_time')

        # 采集的来源地
        tmp['site_id'] = 22  # 采集来源地(蘑菇街秒杀商品)

        tmp['miaosha_begin_time'] = data_list.get('miaosha_begin_time')
        tmp['miaosha_end_time'] = data_list.get('miaosha_end_time')

        tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1
        # print('is_delete=', tmp['is_delete'])

        # print('------>>> | 待存储的数据信息为: |', tmp)
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        pipeline.insert_into_mogujie_xianshimiaosha_table(tmp)

    def update_mogujie_xianshimiaosha_table(self, data, pipeline):
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
        try:
            tmp['price'] = Decimal(data_list['price']).__round__(2)
            tmp['taobao_price'] = Decimal(data_list['taobao_price']).__round__(2)
        except:
            print('此处抓到的可能是蘑菇街券所以跳过')
            return None

        tmp['detail_name_list'] = data_list['detail_name_list']  # 标签属性名称

        """
        得到sku_map
        """
        tmp['price_info_list'] = data_list.get('price_info_list')  # 每个规格对应价格及其库存

        tmp['all_img_url'] = data_list.get('all_img_url')  # 所有示例图片地址

        tmp['p_info'] = data_list.get('p_info')  # 详细信息
        tmp['div_desc'] = data_list.get('div_desc')  # 下方div

        tmp['miaosha_time'] = data_list.get('miaosha_time')

        # 采集的来源地
        # tmp['site_id'] = 22  # 采集来源地(蘑菇街秒杀商品)

        tmp['miaosha_begin_time'] = data_list.get('miaosha_begin_time')
        tmp['miaosha_end_time'] = data_list.get('miaosha_end_time')

        tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1
        # print('is_delete=', tmp['is_delete'])

        # print('------>>> | 待存储的数据信息为: |', tmp)
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        pipeline.update_mogujie_xianshimiaosha_table(tmp)

    def get_goods_id_from_url(self, mogujie_url) -> '重载获取goods_id的方法':
        mogujie_url = re.compile(r'http://').sub('https://', mogujie_url)
        is_mogujie_miaosha_url = re.compile(r'https://shop.mogujie.com/rushdetail/.*?').findall(mogujie_url)
        if is_mogujie_miaosha_url != []:
            # 处理秒杀的地址
            if re.compile(r'https://shop.mogujie.com/rushdetail/(.*?)\?objectId=.*?').findall(mogujie_url) != []:
                return mogujie_url
            else:
                return ''

if __name__ == '__main__':
    mogujie_miaosha = MoGuJieMiaoShaParse()
    while True:
        mogujie_url = input('请输入待爬取的蘑菇街商品地址: ')
        mogujie_url.strip('\n').strip(';')
        goods_id = mogujie_miaosha.get_goods_id_from_url(mogujie_url)
        data = mogujie_miaosha.get_goods_data(goods_id=goods_id)
        data = mogujie_miaosha.deal_with_data()
        # pprint(data)