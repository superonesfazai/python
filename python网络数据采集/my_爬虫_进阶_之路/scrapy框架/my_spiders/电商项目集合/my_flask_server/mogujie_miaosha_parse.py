# coding:utf-8

'''
@author = super_fazai
@File    : mogujie_miaosha_parse.py
@Time    : 2018/1/31 13:06
@connect : superonesfazai@gmail.com
'''

from decimal import Decimal
from mogujie_parse import MoGuJieParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from settings import IP_POOL_TYPE
from sql_str_controller import (
    mg_update_str_1,
    mg_insert_str_1,
    mg_update_str_2,
)

from multiplex_code import (
    _get_right_model_data,
    contraband_name_check,
)

from fzutils.spider.async_always import *

class MoGuJieMiaoShaParse(MoGuJieParse, Crawler):
    def __init__(self):
        MoGuJieParse.__init__(self)

    def get_goods_data(self, goods_id:str) -> dict:
        '''
        模拟构造得到data的url
        :param goods_id:
        :return: data dict类型
        '''
        if goods_id == '':
            return self._data_error()

        if re.compile(r'/rushdetail/').findall(goods_id) != []:
            tmp_url = goods_id
            print('------>>>| 原pc地址为: ', tmp_url)

            goods_id = re.compile('https://shop.mogujie.com/rushdetail/(.*?)\?.*?').findall(goods_id)[0]
            print('------>>>| 得到的蘑菇街商品id为:', goods_id)

        else:
            print('获取到的蘑菇街买哦啥地址错误!请检查')
            return self._data_error()

        data = {}
        body = Requests.get_url_body(
            url=tmp_url,
            headers=self.headers,
            had_referer=True,
            ip_pool_type=self.ip_pool_type)
        # print(body)
        if body == '':
            print('获取到的body为空str!')
            return self._data_error()

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

            title = self._get_title(item_info=item_info)
            # print(title)
            data['title'] = title
            data['sub_title'] = ''
            data['shop_name'] = self._get_shop_name(shop_info=shop_info)
            data['all_img_url'] = self._get_all_img_url(item_info=item_info)
            data['p_info'], tmp_p_info_body  = self._get_p_info(goods_id=goods_id)
            data['div_desc'] = self._get_div_desc(tmp_p_info_body)
            data['detail_name_list'] = self._get_detail_name_list(sku_info)

            '''
            获取每个规格对应价格跟规格以及其库存
            '''
            price_info_list = self.get_price_info_list(sku_info=sku_info)
            assert price_info_list != '', 'price_info_list为空值!'
            # pprint(price_info_list)
            data['price_info_list'] = price_info_list
            if price_info_list == []:
                print('该商品已售完, 此处将商品状态改为1')
                my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                try:
                    my_pipeline._update_table(sql_str=mg_update_str_1, params=(goods_id))
                except:
                    print('将该商品逻辑删除时出错!')
                    pass
                print('| +++ 该商品状态已被逻辑is_delete = 1 +++ |')
                return self._data_error()

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
            return self._data_error()

        self.result_data = data

        return data

    def _data_error(self):
        self.result_data = {}

        return {}

    def insert_into_mogujie_xianshimiaosha_table(self, data, pipeline) -> bool:
        try:
            tmp = _get_right_model_data(data=data, site_id=22)  # 采集来源地(蘑菇街秒杀商品)
        except:
            print('此处抓到的可能是蘑菇街券所以跳过')
            return False

        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))
        params = self._get_db_insert_miaosha_params(item=tmp)
        res = pipeline._insert_into_table(sql_str=mg_insert_str_1, params=params)

        return res

    def update_mogujie_xianshimiaosha_table(self, data, pipeline):
        try:
            tmp = _get_right_model_data(data=data, site_id=22)
        except:
            print('此处抓到的可能是蘑菇街券所以跳过')
            return None
        # print('------>>> | 待存储的数据信息为: |', tmp)
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_update_miaosha_params(item=tmp)
        pipeline._update_table(sql_str=mg_update_str_2, params=params)

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

    def get_goods_id_from_url(self, mogujie_url) -> str:
        mogujie_url = re.compile(r'http://').sub('https://', mogujie_url)
        is_mogujie_miaosha_url = re.compile(r'https://shop.mogujie.com/rushdetail/.*?').findall(mogujie_url)
        if is_mogujie_miaosha_url != []:
            # 处理秒杀的地址
            if re.compile(r'https://shop.mogujie.com/rushdetail/(.*?)\?objectId=.*?').findall(mogujie_url) != []:
                return mogujie_url
            else:
                return ''

    def __del__(self):
        collect()

if __name__ == '__main__':
    mogujie_miaosha = MoGuJieMiaoShaParse()
    while True:
        mogujie_url = input('请输入待爬取的蘑菇街商品地址: ')
        mogujie_url.strip('\n').strip(';')
        goods_id = mogujie_miaosha.get_goods_id_from_url(mogujie_url)
        mogujie_miaosha.get_goods_data(goods_id=goods_id)
        data = mogujie_miaosha.deal_with_data()
        pprint(data)