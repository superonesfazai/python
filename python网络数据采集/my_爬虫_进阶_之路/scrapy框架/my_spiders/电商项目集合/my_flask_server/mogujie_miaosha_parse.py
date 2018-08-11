# coding:utf-8

'''
@author = super_fazai
@File    : mogujie_miaosha_parse.py
@Time    : 2018/1/31 13:06
@connect : superonesfazai@gmail.com
'''

import re
from pprint import pprint
from decimal import Decimal
from json import dumps

from time import sleep
import gc

from mogujie_parse import MoGuJieParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from fzutils.cp_utils import _get_right_model_data
from fzutils.spider.fz_requests import MyRequests
from fzutils.common_utils import json_2_dict

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

            body = MyRequests.get_url_body(url=tmp_url, headers=self.headers, had_referer=True)
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

                item_info = json_2_dict(json_str=item_info)
                sku_info = json_2_dict(json_str=sku_info)
                shop_info = json_2_dict(json_str=shop_info)
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
                tmp_p_info_body = MyRequests.get_url_body(url=p_info_api_url, headers=self.headers, had_referer=True)
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
                        sql_str = r'update dbo.mogujie_xianshimiaosha set is_delete=1 where goods_id = %s'
                        my_pipeline._update_table(sql_str=sql_str, params=(goods_id))
                    except:
                        print('将该商品逻辑删除时出错!')
                        pass
                    print('| +++ 该商品状态已被逻辑is_delete = 1 +++ |')
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
        try:
            tmp = _get_right_model_data(data=data, site_id=22)  # 采集来源地(蘑菇街秒杀商品)
        except:
            print('此处抓到的可能是蘑菇街券所以跳过')
            return None
        # print('------>>> | 待存储的数据信息为: |', tmp)
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_insert_miaosha_params(item=tmp)
        sql_str = r'insert into dbo.mogujie_xianshimiaosha(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, event_time, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

        pipeline._insert_into_table(sql_str=sql_str, params=params)

    def update_mogujie_xianshimiaosha_table(self, data, pipeline):
        try:
            tmp = _get_right_model_data(data=data, site_id=22)
        except:
            print('此处抓到的可能是蘑菇街券所以跳过')
            return None
        # print('------>>> | 待存储的数据信息为: |', tmp)
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_update_miaosha_params(item=tmp)
        sql_str = r'update dbo.mogujie_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s where goods_id = %s'
        pipeline._update_table(sql_str=sql_str, params=params)

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
            item['event_time'],

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

    def get_goods_id_from_url(self, mogujie_url) -> '重载获取goods_id的方法':
        mogujie_url = re.compile(r'http://').sub('https://', mogujie_url)
        is_mogujie_miaosha_url = re.compile(r'https://shop.mogujie.com/rushdetail/.*?').findall(mogujie_url)
        if is_mogujie_miaosha_url != []:
            # 处理秒杀的地址
            if re.compile(r'https://shop.mogujie.com/rushdetail/(.*?)\?objectId=.*?').findall(mogujie_url) != []:
                return mogujie_url
            else:
                return ''

    def __del__(self):
        gc.collect()

if __name__ == '__main__':
    mogujie_miaosha = MoGuJieMiaoShaParse()
    while True:
        mogujie_url = input('请输入待爬取的蘑菇街商品地址: ')
        mogujie_url.strip('\n').strip(';')
        goods_id = mogujie_miaosha.get_goods_id_from_url(mogujie_url)
        data = mogujie_miaosha.get_goods_data(goods_id=goods_id)
        data = mogujie_miaosha.deal_with_data()
        # pprint(data)