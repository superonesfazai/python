# coding:utf-8

'''
@author = super_fazai
@File    : test_ali_1688_phone.py
@Time    : 2017/10/26 11:01
@connect : superonesfazai@gmail.com
'''

import requests
from pprint import pprint
import re
import gc
from time import sleep
import json

class ALi1688LoginAndParse(object):
    def __init__(self):
        super().__init__()
        self.result_data = {}
        self.is_activity_goods = False

    def get_ali_1688_data(self, goods_id):
        # 阿里1688手机版地址: https://m.1688.com/offer/559836312862.html
        wait_to_deal_with_url = 'https://m.1688.com/offer/' + str(goods_id) + '.html'
        print('------>>>| 待处理的阿里1688地址为: ', wait_to_deal_with_url)
        response = requests.get(wait_to_deal_with_url)

        body = response.content.decode('utf-8')
        body = re.compile(r'\n').sub('', body)
        body = re.compile(r'\t').sub('', body)
        body = re.compile(r'  ').sub('', body)
        tmp_body = body
        # print(body)
        body = re.compile(r'{"beginAmount"(.*?)</script></div></div>').findall(body)
        if body != []:
            body = body[0]
            body = r'{"beginAmount"' + body
            # print(body)
            body = json.loads(body)
            # pprint(body)

            if body.get('discountPriceRanges') is not None:
                # 过滤无用属性
                try:
                    body.pop('action')
                    body.pop('offerSign')
                    body.pop('rateDsrItems')
                    body.pop('rateStarLevelMapOfMerge')
                    body.pop('wirelessVideoInfo')
                    body.pop('freightCost')
                except KeyError as e:
                    print('KeyError错误, 此处跳过!')
                    pass

                # pprint(body)
                self.result_data = body
                return self.result_data
            else:
                print('data为空!')
                return {}
        else:
            print('解析错误, 该商品可能正在参与火拼, 此处为火拼价, 为短期价格, 对应爬取失败, 此处我设为跳过!')
            body = re.compile(r'{"activityId"(.*?)</script></div></div>').findall(tmp_body)
            if body != []:
                body = body[0]
                body = r'{"activityId"' + body
                # print(body)
                body = json.loads(body)
                # pprint(body)

                if body.get('discountPriceRanges') is not None:
                    # 过滤无用属性
                    try:
                        body.pop('action')
                        body.pop('offerSign')
                        body.pop('rateDsrItems')
                        body.pop('rateStarLevelMapOfMerge')
                        body.pop('wirelessVideoInfo')
                        body.pop('freightCost')
                    except KeyError as e:
                        print('KeyError错误, 此处跳过!')
                        pass

                    # pprint(body)
                    self.result_data = body
                    self.is_activity_goods = True
                    return self.result_data
                else:
                    print('data为空!')
                    return {}
            else:
                print('这个商品对应活动属性未知, 此处不解析, 设置为跳过!')
                return {}

    def deal_with_data(self):
        '''
        处理返回的result_data, 并返回需要的信息
        :return: 字典类型
        '''
        data = self.result_data

        if data != {}:
            # 公司名称
            company_name = data.get('companyName')
            # 商品名称
            title = data.get('subject')
            # 卖家姓名
            link_name = ''

            # 商品价格信息, 及其对应起批量   [{'price': '119.00', 'begin': '3'}, ...]
            price_info = []
            if self.is_activity_goods:      # 火拼商品处理
                tmp = {}
                tmp_price = data.get('ltPromotionPriceDisplay')
                tmp_trade_number = data.get('beginAmount')
                tmp['begin'] = tmp_price
                tmp['price'] = tmp_trade_number
                price_info.append(tmp)
            else:   # 常规商品处理
                price_info = data.get('discountPriceRanges')
                for item in price_info:
                    try:
                        item.pop('convertPrice')
                    except KeyError:
                        # print('KeyError, [convertPrice], 此处跳过')
                        pass
                # print(price_info)

            # 标签属性名称及其对应的值  (可能有图片(url), 无图(imageUrl=None))    [{'value': [{'imageUrl': 'https://cbu01.alicdn.com/img/ibank/2017/520/684/4707486025_608602289.jpg', 'name': '白色'}, {'imageUrl': 'https://cbu01.alicdn.com/img/ibank/2017/554/084/4707480455_608602289.jpg', 'name': '卡其色'}, {'imageUrl': 'https://cbu01.alicdn.com/img/ibank/2017/539/381/4705183935_608602289.jpg', 'name': '黑色'}], 'prop': '颜色'}, {'value': [{'imageUrl': None, 'name': 'L'}, {'imageUrl': None, 'name': 'XL'}, {'imageUrl': None, 'name': '2XL'}], 'prop': '尺码'}]
            sku_props = data.get('skuProps')

            # print(sku_props)
            if sku_props is not None:   # 这里还是保留unit为单位值
                # for item in sku_props:
                #     try:
                #         item.pop('unit')
                #     except KeyError:
                #         print('KeyError, [unit], 此处跳过')
                pass
            else:
                sku_props = []      # 存在没有规格属性的
            # print(sku_props)

            # 每个规格对应价格, 及其库存量
            '''
            skuMap  == SKUInfo
            '''
            tmp_sku_map = data.get('skuMap')
            if tmp_sku_map is not None:
                sku_map = []
                for key, value in tmp_sku_map.items():
                    tmp = {}

                    # 处理key得到需要的值
                    key = re.compile(r'&gt;').sub('|', key)
                    tmp['spec_type'] = key

                    # 处理value得到需要的值
                    if value.get('discountPrice') is None:  # 如果没有折扣价, 价格就为起批价
                        value['discountPrice'] = price_info[0].get('price')
                    else:
                        if self.is_activity_goods:
                            pass
                        else:
                            if float(value.get('discountPrice')) < float(price_info[0].get('price')):
                                value['discountPrice'] = price_info[0].get('price')
                            else:
                                pass
                    try:
                        value.pop('skuId')
                    except KeyError:
                        pass
                    try:
                        value.pop('specId')
                    except KeyError:
                        pass
                    try:
                        value.pop('saleCount')
                    except KeyError:
                        pass
                    try:
                        value.pop('discountStandardPrice')
                    except KeyError:
                        pass
                    try:
                        value.pop('price')
                    except KeyError:
                        pass
                    try:
                        value.pop('retailPrice')
                    except KeyError:
                        pass
                    try:
                        value.pop('standardPrice')
                    except KeyError:
                        # print('KeyError, [skuId, specId, saleCount]错误, 此处跳过')
                        pass

                    tmp['spec_value'] = value
                    sku_map.append(tmp)

            else:
                sku_map = []        # 存在没有规格时的情况
            # pprint(sku_map)

            # 所有示例图片地址
            tmp_all_img_url = data.get('imageList')
            if tmp_all_img_url is not None:
                all_img_url = []
                for item in tmp_all_img_url:
                    tmp = {}
                    try:
                        item.pop('size310x310URL')
                    except KeyError:
                        # print('KeyError, [size310x310URL], 此处设置为跳过')
                        pass
                    tmp['img_url'] = item['originalImageURI']
                    all_img_url.append(tmp)
            else:
                all_img_url = []
            # pprint(all_img_url)

            # 详细信息的标签名, 及其对应的值
            tmp_property_info = data.get('productFeatureList')
            if tmp_property_info is not None:
                property_info = []
                for item in tmp_property_info:
                    try:
                        item.pop('unit')
                    except KeyError:
                        # print('KeyError, [unit], 此处设置为跳过')
                        pass
                property_info = tmp_property_info
            else:
                property_info = []
            # pprint(property_info)

            # 下方详细div块
            detail_info_url = data.get('detailUrl')
            if detail_info_url is not None:
                detail_info = self.get_detail_info_url_div(detail_info_url)
            else:
                detail_info = ''
            # print(detail_info)

            result = {
                'company_name': company_name,               # 公司名称
                'title': title,                             # 商品名称
                'link_name': link_name,                     # 卖家姓名
                'price_info': price_info,                   # 商品价格信息, 及其对应起批量
                'sku_props': sku_props,                     # 标签属性名称及其对应的值  (可能有图片(url), 无图(imageUrl=None))
                'sku_map': sku_map,                         # 每个规格对应价格, 及其库存量
                'all_img_url': all_img_url,                 # 所有示例图片地址
                'property_info': property_info,             # 详细信息的标签名, 及其对应的值
                'detail_info': detail_info,                 # 下方详细div块
            }
            print(('------>>>| 爬到goods_id(%s)对应的数据: |') % goods_id, result)
            print()
            # wait_to_send_data = {
            #     'reason': 'success',
            #     'data': result,
            #     'code': 1
            # }
            # json_data = json.dumps(wait_to_send_data, ensure_ascii=False)
            # print(json_data)

            # 重置self.is_activity_goods = False
            self.is_activity_goods = False
            return result
        else:
            print('待处理的data为空值!')
            self.is_activity_goods = False
            return {}

    def get_detail_info_url_div(self, detail_info_url):
        '''
        此处过滤得到data_tfs_url的div块
        :return:
        '''
        detail_info = ''
        # print(detail_info_url)
        if re.compile(r'https').findall(detail_info_url) == []:
            detail_info_url = 'https:' + detail_info_url
        else:
            pass
        data_tfs_url_response = requests.get(detail_info_url)
        data_tfs_url_body = data_tfs_url_response.content.decode('gbk')
        data_tfs_url_body = re.compile(r'\n').sub('', data_tfs_url_body)
        data_tfs_url_body = re.compile(r'\t').sub('', data_tfs_url_body)
        data_tfs_url_body = re.compile(r'  ').sub('', data_tfs_url_body)
        # print(body)
        is_offer_details = re.compile(r'offer_details').findall(data_tfs_url_body)
        if is_offer_details != []:
            data_tfs_url_body = re.compile(r'.*?{"content":"(.*?)"};').findall(data_tfs_url_body)
            # print(body)
            if data_tfs_url_body != []:
                detail_info = data_tfs_url_body[0]
                detail_info = re.compile(r'\\').sub('', detail_info)
            else:
                detail_info = ''
        else:
            is_desc = re.compile(r'var desc=').findall(data_tfs_url_body)
            if is_desc != []:
                desc = re.compile(r'var desc=\'(.*)\';').findall(data_tfs_url_body)
                if desc != []:
                    detail_info = desc[0]
            else:
                detail_info = ''
        # print(detail_info)

        return  detail_info

    def get_goods_id_from_url(self, ali_1688_url):
        # https://detail.1688.com/offer/559526148757.html?spm=b26110380.sw1688.mof001.28.sBWF6s
        is_ali_1688_url = re.compile(r'https://detail.1688.com/offer/.*?').findall(ali_1688_url)
        if is_ali_1688_url != []:
            ali_1688_url = re.compile(r'https://detail.1688.com/offer/(.*?).html.*?').findall(ali_1688_url)[0]
            print('------>>>| 得到的阿里1688商品id为:', ali_1688_url)
            return ali_1688_url
        else:
            print('阿里1688商品url错误, 非正规的url, 请参照格式(https://detail.1688.com/offer/)开头的...')
            return ''

if __name__ == '__main__':
    ali_1688 = ALi1688LoginAndParse()
    while True:
        url = input('请输入要爬取的商品界面地址(以英文分号结束): ')
        url.strip('\n').strip(';')
        goods_id = ali_1688.get_goods_id_from_url(url)
        ali_1688.get_ali_1688_data(goods_id=goods_id)
        ali_1688.deal_with_data()
        gc.collect()

