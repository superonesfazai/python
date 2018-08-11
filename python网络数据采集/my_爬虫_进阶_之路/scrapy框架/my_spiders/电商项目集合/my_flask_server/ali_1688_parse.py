# coding:utf-8

'''
@author = super_fazai
@File    : ali_1688_parse.py
@Time    : 2017/10/26 11:01
@connect : superonesfazai@gmail.com
'''

from pprint import pprint
import re
import gc
from time import sleep
import json
from decimal import Decimal
from json import dumps

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from scrapy.selector import Selector
from settings import PHANTOMJS_DRIVER_PATH

from fzutils.cp_utils import _get_right_model_data
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_phantomjs import MyPhantomjs
from fzutils.common_utils import json_2_dict

class ALi1688LoginAndParse(object):
    def __init__(self):
        super().__init__()
        self._set_headers()
        self.result_data = {}
        self.is_activity_goods = False
        self.my_phantomjs = MyPhantomjs(executable_path=PHANTOMJS_DRIVER_PATH)

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': '1688.com',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    def get_ali_1688_data(self, goods_id):
        if goods_id == '':
            self.result_data = {}
            return {}

        # 阿里1688手机版地址: https://m.1688.com/offer/559836312862.html
        wait_to_deal_with_url = 'https://m.1688.com/offer/' + str(goods_id) + '.html'
        print('------>>>| 待处理的阿里1688地址为: ', wait_to_deal_with_url)

        body = self.my_phantomjs.use_phantomjs_to_get_url_body(url=wait_to_deal_with_url, css_selector='div.d-content')
        # print(body)
        if body == '':
            print('获取到的body为空str!请检查!')
            self.result_data = {}
            return {}

        # '''
        # 改用requests
        # '''
        # body = MyRequests.get_url_body(url=wait_to_deal_with_url, headers=self.headers)
        # # print(body)
        #
        # if body == '':
        #     return {}
        # print(body)

        tmp_body = body

        try:
            pull_off_shelves = Selector(text=body).css('div.d-content p.info::text').extract_first()
        except:
            pull_off_shelves = ''
        if pull_off_shelves == '该商品无法查看或已下架':   # 表示商品已下架, 同样执行插入数据操作
            # print('test')
            try:
                tmp_my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                sql_str = 'select GoodsID from dbo.GoodsInfoAutoGet where SiteID=2 and GoodsID=%s'
                is_in_db = tmp_my_pipeline._select_table(sql_str=sql_str, params=(str(goods_id),))
                # print(is_in_db)
            except Exception as e:
                print('遇到错误:', e)
                print('数据库连接失败!')
                self.result_data = {}
                return {}

            if is_in_db != []:        # 表示该goods_id以前已被插入到db中, 于是只需要更改其is_delete的状态即可
                sql_str = 'update dbo.GoodsInfoAutoGet set IsDelete=1 where GoodsID=%s'
                tmp_my_pipeline._update_table(sql_str=sql_str, params=(goods_id))
                print('@@@ 该商品goods_id原先存在于db中, 此处将其is_delete=1')
                tmp_data_s = self.init_pull_off_shelves_goods()  # 初始化下架商品的属性
                tmp_data_s['before'] = True     # 用来判断原先该goods是否在db中
                self.result_data = {}

                return tmp_data_s

            else:       # 表示该goods_id没存在于db中
                print('@@@ 该商品已下架[但未存在于db中], ** 此处将其插入到db中...')
                tmp_data_s = self.init_pull_off_shelves_goods()      # 初始化下架商品的属性
                tmp_data_s['before'] = False
                self.result_data = {}

                return tmp_data_s

        body = re.compile(r'{"beginAmount"(.*?)</script></div></div>').findall(body)
        if body != []:
            body = body[0]
            body = r'{"beginAmount"' + body
            # print(body)
            body = json_2_dict(json_str=body)
            # pprint(body)

            if body.get('discountPriceRanges') is not None:
                self.result_data = self._wash_discountPriceRanges(body=body)
                return self.result_data
            else:
                print('data为空!')
                self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                return {}

        else:
            print('解析ing..., 该商品正在参与火拼, 此处为火拼价, 为短期活动价格!')
            body = re.compile(r'{"activityId"(.*?)</script></div></div>').findall(tmp_body)
            if body != []:
                body = body[0]
                body = r'{"activityId"' + body
                # print(body)
                body = json_2_dict(json_str=body)
                # pprint(body)

                if body.get('discountPriceRanges') is not None:
                    self.result_data = self._wash_discountPriceRanges(body=body)
                    self.is_activity_goods = True
                    return self.result_data
                else:
                    print('data为空!')
                    self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                    return {}
            else:
                print('这个商品对应活动属性未知, 此处不解析, 设置为跳过!')
                self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                return {}

    def deal_with_data(self):
        '''
        处理返回的result_data, 并返回需要的信息
        :return: 字典类型
        '''
        data = self.result_data

        if data != {}:
            # 公司名称
            company_name = data.get('companyName', '')
            title = self._wash_sensitive_words(data.get('subject', ''))
            # 卖家姓名
            link_name = ''

            # 商品价格信息, 及其对应起批量   [{'price': '119.00', 'begin': '3'}, ...]
            price_info = self._get_price_info(data=data)
            # print(price_info)

            # 标签属性名称及其对应的值
            # (可能有图片(url), 无图(imageUrl=None))    [{'value': [{'imageUrl': 'https://cbu01.alicdn.com/img/ibank/2017/520/684/4707486025_608602289.jpg', 'name': '白色'}, {'imageUrl': 'https://cbu01.alicdn.com/img/ibank/2017/554/084/4707480455_608602289.jpg', 'name': '卡其色'}, {'imageUrl': 'https://cbu01.alicdn.com/img/ibank/2017/539/381/4705183935_608602289.jpg', 'name': '黑色'}], 'prop': '颜色'}, {'value': [{'imageUrl': None, 'name': 'L'}, {'imageUrl': None, 'name': 'XL'}, {'imageUrl': None, 'name': '2XL'}], 'prop': '尺码'}]
            sku_props = self._get_sku_props(data=data)
            # print(sku_props)

            # 每个规格对应价格, 及其库存量
            try:
                sku_map = self._get_sku_map(data=data, price_info=price_info)
                # pprint(sku_map)
            except Exception as e:
                print('获取sku_map时, 遇到错误:', e)
                self.is_activity_goods = False
                self.result_data = {}
                return {}

            price, taobao_price = self._get_price(price_info=price_info)

            all_img_url = self._get_all_img_url(data=data)
            # pprint(all_img_url)

            # 即: p_info
            property_info = self._get_p_info(data=data)
            # pprint(property_info)

            # 即: div_desc
            detail_info_url = data.get('detailUrl')
            if detail_info_url is not None:
                # print(detail_info_url)
                detail_info = self.get_detail_info_url_div(detail_info_url)
            else:
                detail_info = ''
            # print(detail_info)

            is_delete = self._get_is_delete(title=title)

            result = {
                'company_name': company_name,               # 公司名称
                'title': title,                             # 商品名称
                'link_name': link_name,                     # 卖家姓名
                'price_info': price_info,                   # 商品价格信息, 及其对应起批量
                'price': price,                             # 起批的最高价
                'taobao_price': taobao_price,               # 起批的最低价
                'sku_props': sku_props,                     # 标签属性名称及其对应的值  (可能有图片(url), 无图(imageUrl=None))
                'sku_map': sku_map,                         # 每个规格对应价格, 及其库存量
                'all_img_url': all_img_url,                 # 所有示例图片地址
                'property_info': property_info,             # 详细信息的标签名, 及其对应的值
                'detail_info': detail_info,                 # 下方详细div块
                'is_delete': is_delete,                     # 判断是否下架
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

            # 重置self.is_activity_goods = False
            self.is_activity_goods = False

            return result
        else:
            print('待处理的data为空值!')
            self.is_activity_goods = False

            return {}

    def to_right_and_update_data(self, data, pipeline):
        tmp = _get_right_model_data(data=data, site_id=2)

        # print('------>>> | 待存储的数据信息为: |', tmp)
        params = self._get_db_update_params(item=tmp)
        # 改价格的sql语句
        # sql_str = r'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, GoodsName=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, DetailInfo=%s, PropertyInfo=%s, MyShelfAndDownTime=%s, delete_time=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s where GoodsID = %s'
        # 不改价格的sql语句
        base_sql_str = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, GoodsName=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, DetailInfo=%s, PropertyInfo=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, {0} {1} where GoodsID = %s'
        if tmp['delete_time'] == '':
            sql_str = base_sql_str.format('shelf_time=%s', '')
        elif tmp['shelf_time'] == '':
            sql_str = base_sql_str.format('delete_time=%s', '')
        else:
            sql_str = base_sql_str.format('shelf_time=%s,', 'delete_time=%s')

        pipeline._update_table(sql_str=sql_str, params=params)

    def _get_sku_props(self, **kwargs):
        '''
        得到sku_props
        :param kwargs:
        :return:
        '''
        data = kwargs.get('data', {})

        sku_props = data.get('skuProps')
        # print(sku_props)
        if sku_props is not None:  # 这里还是保留unit为单位值
            # for item in sku_props:
            #     try:
            #         item.pop('unit')
            #     except KeyError:
            #         print('KeyError, [unit], 此处跳过')
            pass
        else:
            sku_props = []  # 存在没有规格属性的

        return sku_props

    def _get_price_info(self, **kwargs):
        '''
        得到price_info
        :return:
        '''
        data = kwargs.get('data', {})

        # 商品价格信息, 及其对应起批量   [{'price': '119.00', 'begin': '3'}, ...]
        price_info = []
        if self.is_activity_goods:  # 火拼商品处理
            tmp = {}
            tmp_price = data.get('ltPromotionPriceDisplay')
            tmp_trade_number = data.get('beginAmount')
            tmp['begin'] = tmp_trade_number
            tmp['price'] = tmp_price
            price_info.append(tmp)
        else:  # 常规商品处理
            if data.get('isLimitedTimePromotion', 'true') == 'false':  # isLimitedTimePromotion 限时优惠, 'true'表示限时优惠价, 'flase'表示非限时优惠
                price_info = data.get('discountPriceRanges')
                for item in price_info:
                    try:
                        item.pop('convertPrice')
                    except KeyError:
                        pass
                        # print(price_info)
            else:  # 限时优惠
                tmp = {
                    'begin': data.get('beginAmount', ''),
                    'price': data.get('skuDiscountPrice', '')
                }
                price_info.append(tmp)

        return price_info

    def _get_sku_map(self, **kwargs):
        '''
        得到sku_map
        :param kwargs:
        :return:
        '''
        # 每个规格对应价格, 及其库存量
        '''skuMap == SKUInfo'''
        data = kwargs.get('data', {})
        price_info = kwargs.get('price_info', [])

        tmp_sku_map = data.get('skuMap')
        if tmp_sku_map is not None:
            sku_map = []
            for key, value in tmp_sku_map.items():
                tmp = {}
                # 处理key得到需要的值
                key = re.compile(r'&gt;').sub('|', key)
                tmp['spec_type'] = key

                # 处理value得到需要的值
                # pprint(price_info)
                if value.get('discountPrice') is None:  # 如果没有折扣价, 价格就为起批价
                    try:
                        value['discountPrice'] = price_info[0].get('price')
                    except IndexError:
                        print('获取价格失败, 此处跳过!')
                        raise IndexError

                else:
                    if self.is_activity_goods:
                        pass
                    else:
                        if data.get('isLimitedTimePromotion') == 'false':
                            if float(value.get('discountPrice')) < float(price_info[0].get('price')):
                                value['discountPrice'] = price_info[0].get('price')
                            else:
                                pass
                        else:
                            pass

                tmp['spec_value'] = self._wash_sku_value(value=value)
                sku_map.append(tmp)

        else:
            sku_map = []  # 存在没有规格时的情况

        return sku_map

    def _get_all_img_url(self, **kwargs):
        '''
        得到all_img_url
        :param kwargs:
        :return:
        '''
        data = kwargs.get('data', {})

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

        return all_img_url

    def _get_p_info(self, **kwargs):
        '''
        得到p_info
        :param kwargs:
        :return:
        '''
        data = kwargs.get('data', {})

        property_info = []
        tmp_property_info = data.get('productFeatureList')
        if tmp_property_info is not None:
            for item in tmp_property_info:
                try:
                    item.pop('unit')
                except KeyError:
                    # print('KeyError, [unit], 此处设置为跳过')
                    pass
                item['id'] = '0'

            property_info = tmp_property_info
        else:
            pass

        return property_info

    def _get_is_delete(self, **kwargs):
        '''
        得到is_delete
        :param kwargs:
        :return:
        '''
        title = kwargs.get('title')

        is_delete = 0
        if re.compile(r'下架').findall(title) != []:
            if re.compile(r'待下架').findall(title) != []:
                pass
            else:
                is_delete = 1
        else:
            pass

        return is_delete

    def _wash_sku_value(self, value):
        '''
        清洗value
        :param value:
        :return:
        '''
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

        return value

    def _wash_sensitive_words(self, word):
        '''
        清洗敏感字眼
        :param word:
        :return:
        '''
        word = re.compile(r'淘宝网').sub('', word)

        return word

    def _wash_discountPriceRanges(self, body):
        '''
        清洗discountPriceRanges
        :param body:
        :return:
        '''
        # 过滤无用属性
        try:
            body.pop('action')
            body.pop('offerSign')
            body.pop('rateDsrItems')
            body.pop('rateStarLevelMapOfMerge')
            body.pop('wirelessVideoInfo')
            body.pop('freightCost')
        except KeyError:
            print('KeyError错误, 此处跳过!')
            pass

        return body

    def _get_db_update_params(self, item):
        '''
        得到待存储的params
        :param item:
        :return: tuple
        '''
        params = [
            item['modify_time'],
            item['shop_name'],
            item['title'],
            item['link_name'],
            # item['price'],
            # item['taobao_price'],
            dumps(item['price_info'], ensure_ascii=False),
            dumps(item['detail_name_list'], ensure_ascii=False),
            dumps(item['price_info_list'], ensure_ascii=False),
            dumps(item['all_img_url'], ensure_ascii=False),
            item['div_desc'],
            dumps(item['p_info'], ensure_ascii=False),
            # item['delete_time'],
            item['is_delete'],
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

    def _get_price(self, price_info):
        '''
        获取商品的最高价跟最低价
        :param price_info:
        :return: price, taobao_price type float
        '''
        # 设置最高价price， 最低价taobao_price
        if len(price_info) > 1:
            tmp_ali_price = []
            for item in price_info:
                tmp_ali_price.append(float(item.get('price')))

            if tmp_ali_price == []:
                price = Decimal(0).__round__(2)
                taobao_price = Decimal(0).__round__(2)

            else:
                price = Decimal(sorted(tmp_ali_price)[-1]).__round__(2)  # 得到最大值并转换为精度为2的decimal类型
                taobao_price = Decimal(sorted(tmp_ali_price)[0]).__round__(2)

        elif len(price_info) == 1:  # 由于可能是促销价, 只有一组然后价格 类似[{'begin': '1', 'price': '485.46-555.06'}]
            if re.compile(r'-').findall(price_info[0].get('price')) != []:
                tmp_price_range = price_info[0].get('price')
                tmp_price_range = tmp_price_range.split('-')
                price = tmp_price_range[1]
                taobao_price = tmp_price_range[0]

            else:
                price = Decimal(price_info[0].get('price')).__round__(2)  # 得到最大值并转换为精度为2的decimal类型
                taobao_price = price

        else:  # 少于1
            price = Decimal(0).__round__(2)
            taobao_price = Decimal(0).__round__(2)

        return float(price), float(taobao_price)

    def init_pull_off_shelves_goods(self):
        '''
        初始化原先就下架的商品信息
        :return:
        '''
        is_delete = 1
        result = {
            'company_name': '',  # 公司名称
            'title': '',  # 商品名称
            'link_name': '',  # 卖家姓名
            'price_info': [],  # 商品价格信息, 及其对应起批量
            'price': 0,
            'taobao_price': 0,
            'sku_props': [],  # 标签属性名称及其对应的值  (可能有图片(url), 无图(imageUrl=None))
            'sku_map': [],  # 每个规格对应价格, 及其库存量
            'all_img_url': [],  # 所有示例图片地址
            'property_info': [],  # 详细信息的标签名, 及其对应的值
            'detail_info': '',  # 下方详细div块
            'is_delete': is_delete,  # 判断是否下架
        }

        return result

    def old_ali_1688_goods_insert_into_new_table(self, data, pipeline):
        tmp = _get_right_model_data(data=data, site_id=2)

        # print('------>>> | 待存储的数据信息为: |', tmp)
        params = self._get_db_insert_params(item=tmp)
        if tmp.get('main_goods_id') is not None:
            sql_str = r'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, GoodsName, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, DetailInfo, PropertyInfo, SiteID, IsDelete, MainGoodsID) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        else:
            sql_str = r'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, GoodsName, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, DetailInfo, PropertyInfo, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

        result = pipeline._insert_into_table(sql_str=sql_str, params=params)

        return result

    def _get_db_insert_params(self, item):
        params = [
            item['goods_id'],
            item['goods_url'],
            item['username'],
            item['create_time'],
            item['modify_time'],
            item['shop_name'],
            item['title'],
            item['link_name'],
            item['price'],
            item['taobao_price'],
            dumps(item['price_info'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
            dumps(item['detail_name_list'], ensure_ascii=False),
            dumps(item['price_info_list'], ensure_ascii=False),
            dumps(item['all_img_url'], ensure_ascii=False),
            item['div_desc'],  # 存入到DetailInfo
            dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo

            item['site_id'],
            item['is_delete'],
        ]

        if item.get('main_goods_id') is not None:
            params.append(item.get('main_goods_id'))

        return tuple(params)

    def get_detail_info_url_div(self, detail_info_url):
        '''
        此处过滤得到data_tfs_url的div块
        :return:
        '''
        detail_info = ''
        # print(detail_info_url)
        if re.compile(r'https').findall(detail_info_url) == []:
            detail_info_url = 'https:' + detail_info_url
            # print(detail_info_url)
        else:
            pass
        # data_tfs_url_response = requests.get(detail_info_url, headers=self.headers)
        # data_tfs_url_body = data_tfs_url_response.content.decode('gbk')

        data_tfs_url_body = self.my_phantomjs.use_phantomjs_to_get_url_body(url=detail_info_url)

        # '''
        # 改用requests
        # '''
        # body = MyRequests.get_url_body(url=detail_info_url, headers=self.headers)
        # print(body)
        # if  body == '':
        #     detail_info = ''
        #
        # data_tfs_url_body = body

        is_offer_details = re.compile(r'offer_details').findall(data_tfs_url_body)
        detail_info = ''

        if is_offer_details != []:
            data_tfs_url_body = re.compile(r'.*?{"content":"(.*?)"};').findall(data_tfs_url_body)
            # print(body)
            if data_tfs_url_body != []:
                detail_info = data_tfs_url_body[0]
                detail_info = re.compile(r'\\').sub('', detail_info)
                detail_info = self._wash_div_desc(detail_info=detail_info)

        else:
            is_desc = re.compile(r'var desc=').findall(data_tfs_url_body)
            if is_desc != []:
                desc = re.compile(r'var desc=\'(.*)\';').findall(data_tfs_url_body)
                if desc != []:
                    detail_info = desc[0]
                    detail_info = self._wash_div_desc(detail_info=detail_info)
                    detail_info = re.compile(r'src=\"https:').sub('src=\"', detail_info)     # 先替换部分带有https的
                    detail_info = re.compile(r'src="').sub('src=\"https:', detail_info)     # 再把所欲的换成https的

        # print(detail_info)

        return detail_info

    def _wash_div_desc(self, detail_info):
        '''
        清洗detail_info
        :param detail_info:
        :return:
        '''
        detail_info = re.compile(r'&lt;').sub('<', detail_info)  # self.driver.page_source转码成字符串时'<','>'都被替代成&gt;&lt;此外还有其他也类似被替换
        detail_info = re.compile(r'&gt;').sub('>', detail_info)
        detail_info = re.compile(r'&amp;').sub('&', detail_info)
        detail_info = re.compile(r'&nbsp;').sub(' ', detail_info)

        return detail_info

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

    def __del__(self):
        try:
            del self.my_phantomjs
        except Exception:
            print("self.my_phantomjs释放失败!")
            pass
        gc.collect()

if __name__ == '__main__':
    ali_1688 = ALi1688LoginAndParse()
    while True:
        url = input('请输入要爬取的商品界面地址(以英文分号结束): ')
        url.strip('\n').strip(';')
        goods_id = ali_1688.get_goods_id_from_url(url)
        ali_1688.get_ali_1688_data(goods_id=goods_id)
        ali_1688.deal_with_data()

        gc.collect()


