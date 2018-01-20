# coding:utf-8

'''
@author = super_fazai
@File    : mia_pintuan_parse.py
@Time    : 2018/1/20 11:33
@connect : superonesfazai@gmail.com
'''

'''
蜜芽拼团页面解析系统
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
import re
import gc
import pytz
from scrapy import Selector

from mia_parse import MiaParse

class MiaPintuanParse(MiaParse):
    def __init__(self):
        MiaParse.__init__(self)

    def get_goods_data(self, goods_id) -> '重载方法':
        '''
        模拟构造得到data的url
        :param goods_id:
        :return: data dict类型
        '''
        if goods_id == '':
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            return {}
        else:
            data = {}
            # 常规商品手机地址
            goods_url = 'https://m.mia.com/item-' + str(goods_id) + '.html'
            # 常规商品pc地址
            # goods_url = 'https://www.mia.com/item-' + str(goods_id) + '.html'
            print('------>>>| 待抓取的地址为: ', goods_url)

            body = self.get_url_body(tmp_url=goods_url)
            # print(body)

            if body == '':
                self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                return {}

            # 判断是否跳转，并得到跳转url, 跳转url的body, 以及is_hk(用于判断是否是全球购的商品)
            body, sign_direct_url, is_hk = self.get_jump_to_url_and_is_hk(body=body)

            try:
                # title, sub_title
                data['title'], data['sub_title'] = self.get_title_and_sub_title(body=body)

                # 获取所有示例图片
                all_img_url = self.get_all_img_url(goods_id=goods_id, is_hk=is_hk)
                if all_img_url == '':
                    self.result_data = {}
                    return {}

                '''
                获取p_info
                '''
                tmp_p_info = Selector(text=body).css('div.showblock div p').extract_first()

                if tmp_p_info == '':
                    print('获取到的tmp_p_info为空值, 请检查!')
                    self.result_data = {}
                    return {}
                else:
                    tmp_p_info = re.compile('<p>|</p>').sub('', tmp_p_info)
                    tmp_p_info = re.compile(r'<!--思源品牌，隐藏品牌-->').sub('', tmp_p_info)
                    p_info = [{'p_name': item.split('：')[0], 'p_value': item.split('：')[1]} for item in tmp_p_info.split('<br>') if item != '']

                # pprint(p_info)
                data['p_info'] = p_info

                # 获取每个商品的div_desc
                div_desc = self.get_goods_div_desc(body=body)

                if div_desc == '':
                    print('获取到的div_desc为空值! 请检查')
                    self.result_data = {}
                    return {}
                data['div_desc'] = div_desc

                '''
                获取每个规格的goods_id，跟规格名，以及img_url, 用于后面的处理
                '''
                sku_info = self.get_tmp_sku_info(body, goods_id, sign_direct_url, is_hk)
                if sku_info == {}:
                    return {}

                '''
                由于这个拿到的都是小图，分辨率相当低，所以采用获取每个goods_id的phone端地址来获取每个规格的高清规格图
                '''
                # # print(Selector(text=body).css('dd.color_list li').extract())
                # for item in Selector(text=body).css('dd.color_list li').extract():
                #     # print(item)
                #     try:
                #         # 该颜色的商品的goods_id
                #         color_goods_id = Selector(text=item).css('a::attr("href")').extract_first()
                #         # 该颜色的名字
                #         color_name = Selector(text=item).css('a::attr("title")').extract_first()
                #         # 该颜色的img_url
                #         color_goods_img_url = Selector(text=item).css('img::attr("src")').extract_first()
                #
                #         color_goods_id = re.compile('(\d+)').findall(color_goods_id)[0]
                #     except IndexError:      # 表示该li为这个tmp_url的地址 (单独处理goods_id)
                #         color_goods_id = goods_id
                #         color_name = Selector(text=item).css('a::attr("title")').extract_first()
                #         color_goods_img_url = Selector(text=item).css('img::attr("src")').extract_first()
                #     print(color_goods_id, ' ', color_name, ' ', color_goods_img_url)

                '''
                获取每个规格对应价格跟规格以及其库存
                '''
                if self.get_true_sku_info(sku_info=sku_info) == {}:     # 表示出错退出
                    return {}
                else:                                                   # 成功获取
                    true_sku_info, i_s = self.get_true_sku_info(sku_info=sku_info)
                    data['price_info_list'] = true_sku_info
                # pprint(true_sku_info)

                # 设置detail_name_list
                data['detail_name_list'] = self.get_detail_name_list(i_s=i_s)
                # print(detail_name_list)

                '''单独处理all_img_url为[]的情况'''
                if all_img_url == []:
                    all_img_url = [{'img_url': true_sku_info[0].get('img_url')}]

                data['all_img_url'] = all_img_url
                # pprint(all_img_url)

                '''
                单独处理得到goods_url
                '''
                if sign_direct_url != '':
                    goods_url = sign_direct_url

                data['goods_url'] = goods_url

            except Exception as e:
                print('遇到错误如下: ', e)
                self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                return {}

            if data != {}:
                # pprint(data)
                self.result_data = data
                return data

            else:
                print('data为空!')
                self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                return {}

    def deal_with_data(self) -> '重载数据处理方法':
        '''
        处理得到规范的data数据
        :return: result 类型 dict
        '''
        data = self.result_data
        if data != {}:
            # 店铺名称
            shop_name = ''

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
            is_delete = 0

            result = {
                'goods_url': data['goods_url'],         # goods_url
                'shop_name': shop_name,                 # 店铺名称
                'account': account,                     # 掌柜
                'title': title,                         # 商品名称
                'sub_title': sub_title,                 # 子标题
                'price': price,                         # 商品价格
                'taobao_price': taobao_price,           # 淘宝价
                # 'goods_stock': goods_stock,            # 商品库存
                'detail_name_list': detail_name_list,   # 商品标签属性名称
                # 'detail_value_list': detail_value_list,# 商品标签属性对应的值
                'price_info_list': price_info_list,     # 要存储的每个标签对应规格的价格及其库存
                'all_img_url': all_img_url,             # 所有示例图片地址
                'p_info': p_info,                       # 详细信息标签名对应属性
                'div_desc': div_desc,                   # div_desc
                'is_delete': is_delete                  # 用于判断商品是否已经下架
            }
            pprint(result)
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

    def get_true_sku_info(self, sku_info) -> '重载得到true_sku_info的方法':
        '''
        获取每个规格对应价格跟规格以及其库存
        :param sku_info:
        :return: {} 空字典表示出错 | (true_sku_info, i_s)
        '''
        goods_id_str = '-'.join([item.get('goods_id') for item in sku_info])
        # print(goods_id_str)
        tmp_url = 'https://p.mia.com/item/list/' + goods_id_str
        # print(tmp_url)

        tmp_body = self.get_url_body(tmp_url=tmp_url)
        # print(tmp_body)

        try:
            tmp_data = json.loads(tmp_body).get('data', [])
            # pprint(tmp_data)
        except Exception as e:
            print('json.loads转换tmp_body时出错!')
            tmp_data = []
            self.result_data = {}
            return {}

        true_sku_info = []
        i_s = {}
        for item_1 in sku_info:
            for item_2 in tmp_data:
                if item_1.get('goods_id') == str(item_2.get('id', '')):
                    i_s = item_2.get('i_s', {})
                    # print(i_s)
                    for item_3 in i_s.keys():
                        tmp = {}
                        if item_3 == 'SINGLE':
                            spec_value = item_1.get('color_name')
                        else:
                            spec_value = item_1.get('color_name') + '|' + item_3
                        normal_price = str(item_2.get('mp'))
                        detail_price = str(item_2.get('sp'))
                        try:
                            pintuan_price = str(item_2.get('g_l', [])[0].get('gp', ''))
                            # print(pintuan_price)
                        except:
                            print('获取该规格拼团价pintuan_price时出错!')
                            self.result_data = {}
                            return {}

                        img_url = item_1.get('img_url')
                        rest_number = i_s.get(item_3)
                        if rest_number == 0:
                            pass
                        else:
                            tmp['spec_value'] = spec_value
                            tmp['pintuan_price'] = pintuan_price
                            tmp['detail_price'] = detail_price
                            tmp['normal_price'] = normal_price
                            tmp['img_url'] = img_url
                            tmp['rest_number'] = rest_number
                            true_sku_info.append(tmp)

        return (true_sku_info, i_s)

if __name__ == '__main__':
    mia_pintuan = MiaPintuanParse()
    while True:
        mia_url = input('请输入待爬取的蜜芽商品地址: ')
        mia_url.strip('\n').strip(';')
        goods_id = mia_pintuan.get_goods_id_from_url(mia_url)
        data = mia_pintuan.get_goods_data(goods_id=goods_id)
        mia_pintuan.deal_with_data()