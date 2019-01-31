# coding:utf-8

'''
@author = super_fazai
@File    : ali_1688_parse.py
@Time    : 2017/10/26 11:01
@connect : superonesfazai@gmail.com
'''

from pprint import pprint
import re
from gc import collect
from time import sleep
from decimal import Decimal
from json import dumps

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from scrapy.selector import Selector
from settings import (
    PHANTOMJS_DRIVER_PATH,
    MY_SPIDER_LOGS_PATH,
    IP_POOL_TYPE,
)
from sql_str_controller import (
    al_select_str_1,
    al_update_str_1,
    al_update_str_2,
    al_insert_str_1,
    al_insert_str_2,)

from fzutils.cp_utils import _get_right_model_data
from fzutils.internet_utils import (
    get_random_pc_ua,
    get_random_phone_ua,
    str_cookies_2_dict,
    _get_url_contain_params,
    html_entities_2_standard_html,)
from fzutils.common_utils import json_2_dict
from fzutils.spider.crawler import Crawler
from fzutils.spider.fz_driver import (
    PHONE,
    CHROME,
    PHANTOMJS,
    FIREFOX,)
from fzutils.time_utils import get_shanghai_time
from fzutils.spider.selector import parse_field
from fzutils.spider.fz_requests import Requests

class ALi1688LoginAndParse(Crawler):
    def __init__(self, logger=None):
        super(ALi1688LoginAndParse, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            logger=logger,
            log_save_path=MY_SPIDER_LOGS_PATH + '/1688/_/',

            is_use_driver=True,
            driver_type=PHANTOMJS,
            driver_executable_path=PHANTOMJS_DRIVER_PATH,
            user_agent_type=PHONE,
        )
        self.result_data = {}
        self.is_activity_goods = False

    def _get_phone_headers(self):
        return {
            'authority': 'm.1688.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_phone_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
        }

    def get_ali_1688_data(self, goods_id):
        if goods_id == '':
            return self._data_error_init()

        wait_to_deal_with_url = 'https://m.1688.com/offer/{}.html'.format(goods_id)
        self.lg.info('------>>>| 待处理的阿里1688地址为: {0}'.format(wait_to_deal_with_url))

        self.error_base_record = '出错goods_id:{0}'.format(goods_id)
        # driver
        body = self.driver.get_url_body(
            url=wait_to_deal_with_url,)
            # 注释掉避免driver盲目等待
            # css_selector='div.d-content',)

        # 改用requests
        # body = Requests.get_url_body(
        #     url=wait_to_deal_with_url,
        #     headers=self._get_phone_headers(),
        #     ip_pool_type=self.ip_pool_type,)
        # self.lg.info(str(body))
        if body == '':
            self.lg.error('获取到的body为空str!请检查!' + self.error_base_record)
            return self._data_error_init()

        tmp_body = body
        pull_off_shelves = Selector(text=body).css('div.d-content p.info::text').extract_first() or ''
        if pull_off_shelves == '该商品无法查看或已下架':   # 表示商品已下架, 同样执行插入数据操作
            return self._handle_goods_is_delete(goods_id=goods_id)

        try:
            body = re.compile(r'{"beginAmount"(.*?)</script></div></div>').findall(body)[0]
        except IndexError:
            try:
                # self.lg.info(tmp_body)
                body = re.compile(r'{"activityId"(.*?)</script></div></div>').findall(tmp_body)[0]
                self.lg.info('解析ing..., 该商品正在参与火拼, 此处为火拼价, 为短期活动价格!')
            except IndexError:
                try:
                    # 新版处理
                    _ = self._get_new_data(body=tmp_body, goods_id=goods_id)
                    self.lg.info('正在处理1688新版页面...')
                    return _

                except (IndexError, AssertionError, Exception):
                    self.lg.error('遇到错误:', exc_info=True)
                    self.lg.error('这个商品对应活动属性未知, 此处不解析, 设置为跳过!' + self.error_base_record)
                    return self._data_error_init()

            body = r'{"activityId"' + body
            # self.lg.info(str(body))
            body = json_2_dict(json_str=body)
            # pprint(body)
            if body.get('discountPriceRanges') is not None:
                self.result_data = self._wash_discountPriceRanges(body=body)
                self.is_activity_goods = True

                return self.result_data
            else:
                self.lg.error('data为空!' + self.error_base_record)

                return self._data_error_init()

        body = r'{"beginAmount"' + body
        # self.lg.info(str(body))
        body = json_2_dict(json_str=body)
        # pprint(body)
        if body.get('discountPriceRanges') is not None:
            self.result_data = self._wash_discountPriceRanges(body=body)

            return self.result_data
        else:
            self.lg.error('data为空!' + self.error_base_record)

            return self._data_error_init()

    def _get_new_data(self, body, goods_id) -> dict:
        '''
        获取新版页面的需求信息
        :param body:
        :return:
        '''
        def add_data2_2_data1(data1, data2) -> dict:
            '''增加data2 2 data1'''
            for key, value in data2.items():
                if key == 'showPriceRanges':
                    assert value != [], 'showPriceRanges不等于空list!'
                    tmp_value = []
                    for i in value:
                        begin = i.get('range', '').replace('&ge;', '-').split('-')
                        assert begin != '', 'begin为空值!'
                        try:
                            if begin[0] != '':
                                begin = begin[0]
                            else:
                                begin = begin[1]
                        except IndexError:
                            begin = begin[1]
                        tmp_value.append({
                            'begin': begin,
                            'convertPrice': i.get('convertPrice', ''),
                            'price': i.get('price', ''),
                        })
                    data1.update({
                        'discountPriceRanges': tmp_value,
                    })

                elif key == 'displayPrice':
                    data1.update({
                        'ltPromotionPriceDisplay': value,
                    })

                else:
                    data1.update({
                        key: value,
                    })

            return data1

        def add_goods_name(data1) -> dict:
            # goods_name
            goods_name = data1.get('offerSubject', '')
            assert goods_name != '', 'goods_name为空值!'
            data1.update({
                'subject': goods_name,
            })

            return data1

        def add_company_name(data1) -> dict:
            # 增加company_name
            data1.update({
                'companyName': data1.get('sellerLoginId', ''),
            })

            return data1

        def add_all_img_list(data1) -> dict:
            # 增加示例图
            all_img_list_selector = {
                'method': 'css',
                'selector': 'div#J_Detail_ImageSlides div.swipe-pane img ::attr("swipe-lazy-src")',
            }
            all_img_list = parse_field(parser=all_img_list_selector, target_obj=body, logger=self.lg, is_first=False)
            assert all_img_list != [], 'all_img_list不为空list!'
            all_img_list = [{
                'originalImageURI': i
            } for i in all_img_list]
            data1.update({
                'imageList': all_img_list
            })

            return data1

        def add_div_desc(data1) -> dict:
            # 增加div_desc
            div_desc_selector = {
                'method': 're',
                'selector': '\"detailUrl\": \"(.*?)\"}<',
            }
            div_desc_url = parse_field(parser=div_desc_selector, target_obj=body, logger=self.lg)
            # self.lg.info(div_desc_url)
            assert div_desc_url != '', 'div_desc_url为空值!'
            data1.update({
                'detailUrl': div_desc_url
            })

            return data1

        def add_p_info(data1) -> dict:
            # 增加p_info
            p_info_selector = {
                'method': 'css',
                'selector': 'span.detail-attribute-item ::text',
            }
            p_info = parse_field(parser=p_info_selector, target_obj=body, logger=self.lg, is_first=False)
            assert p_info != [], 'p_info不为空list!'
            p_info = [{
                'name': i.split(':')[0],
                'unit': None,
                'value': i.split(':')[1]
            } for i in p_info]
            data1.update({
                'productFeatureList': p_info,
            })

            return data1

        if '该商品无法查看或已下架' in body:
            self._handle_goods_is_delete(goods_id=goods_id)
            return self._data_error_init()

        # TODO 新版处理 eg: goods_id: 44609651914
        body_1 = re.compile('class=\"module-wap-detail-common-footer\"><script type=\"component-data/json\" data-module-hidden-data-area=\"Y\">(.*)</script><div class=\"takla')\
            .findall(body)[0]
        body_2 = re.compile('id=\"widget-wap-detail-common-price\"><script type=\"component/json\" data-module-hidden-data-area=\"Y\">(.*?)</script>')\
            .findall(body)[0]
        # self.lg.info(body_1)
        # self.lg.info(body_2)

        data1 = json_2_dict(json_str=body_1, logger=self.lg, default_res={})
        data2 = json_2_dict(json_str=body_2, logger=self.lg, default_res={})
        if data1 == {} \
                or data2 == {}:
            self.lg.info('data1 or data2为空dict!异常退出!')
            return self._data_error_init()

        data1 = add_data2_2_data1(data1=data1, data2=data2)
        data1 = add_goods_name(data1)
        data1 = add_company_name(data1)
        data1 = add_all_img_list(data1)
        # 增加是否是限时优惠
        data1.update({
            'isLimitedTimePromotion': 'false',
        })
        data1 = add_div_desc(data1)
        data1 = add_p_info(data1)

        data = data1
        # pprint(data)
        self.result_data = data

        return data

    def deal_with_data(self):
        '''
        处理返回的result_data, 并返回需要的信息
        :return: 字典类型
        '''
        data = self.result_data
        # pprint(data)
        if data == {}:
            self.lg.error('待处理的data为空值!' + self.error_base_record)
            self.is_activity_goods = False

            return self._data_error_init()

        company_name = data.get('companyName', '')
        title = self._wash_sensitive_words(data.get('subject', ''))
        link_name = ''

        # 商品价格信息, 及其对应起批量   [{'price': '119.00', 'begin': '3'}, ...]
        price_info = self._get_price_info(data=data)
        # self.lg.info(str(price_info))

        # 标签属性名称及其对应的值
        # (可能有图片(url), 无图(imageUrl=None))    [{'value': [{'imageUrl': 'https://cbu01.alicdn.com/img/ibank/2017/520/684/4707486025_608602289.jpg', 'name': '白色'}, {'imageUrl': 'https://cbu01.alicdn.com/img/ibank/2017/554/084/4707480455_608602289.jpg', 'name': '卡其色'}, {'imageUrl': 'https://cbu01.alicdn.com/img/ibank/2017/539/381/4705183935_608602289.jpg', 'name': '黑色'}], 'prop': '颜色'}, {'value': [{'imageUrl': None, 'name': 'L'}, {'imageUrl': None, 'name': 'XL'}, {'imageUrl': None, 'name': '2XL'}], 'prop': '尺码'}]
        sku_props = self._get_detail_name_list(data=data)
        # self.lg.info(str(sku_props))

        # 每个规格对应价格, 及其库存量
        try:
            sku_map = self._get_sku_info(data=data, price_info=price_info, detail_name_list=sku_props)
            # pprint(sku_map)
        except Exception:
            self.lg.error('获取sku_map时, 遇到错误!'+self.error_base_record, exc_info=True)
            self.is_activity_goods = False
            return self._data_error_init()

        price, taobao_price = self._get_price_and_taobao_price(price_info=price_info)
        all_img_url = self._get_all_img_url(data=data)
        property_info = self._get_p_info(data=data)     # 即: p_info

        # 即: div_desc
        detail_info_url = data.get('detailUrl', '')
        detail_info = self._get_div_desc(detail_info_url) if detail_info_url != '' else ''
        # self.lg.info(str(detail_info))
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
        # self.lg.info(str(result))

        # wait_to_send_data = {
        #     'reason': 'success',
        #     'data': result,
        #     'code': 1
        # }
        # json_data = json.dumps(wait_to_send_data, ensure_ascii=False)
        # self.lg.info(str(json_data))

        # 重置self.is_activity_goods = False
        self.is_activity_goods = False

        return result

    def _handle_goods_is_delete(self, goods_id):
        '''
        处理商品无法查看或者下架的
        :return:
        '''
        try:
            sql_cli = SqlServerMyPageInfoSaveItemPipeline()
            is_in_db = sql_cli._select_table(sql_str=al_select_str_1, params=(str(goods_id),))
            # self.lg.info(str(is_in_db))
        except Exception:
            self.lg.error('数据库连接失败!' + self.error_base_record, exc_info=True)
            return self._data_error_init()

        self.result_data = {}
        # 初始化下架商品的属性
        tmp_data_s = self.init_pull_off_shelves_goods()
        if is_in_db != []:
            # 表示该goods_id以前已被插入到db中, 于是只需要更改其is_delete的状态即可
            sql_cli._update_table_2(
                sql_str=al_update_str_1,
                params=(str(get_shanghai_time()), goods_id,),
                logger=self.lg)
            self.lg.info('@@@ 该商品goods_id原先存在于db中, 此处将其is_delete=1')
            # 用来判断原先该goods是否在db中
            tmp_data_s['before'] = True

        else:
            # 表示该goods_id没存在于db中
            self.lg.info('@@@ 该商品已下架[但未存在于db中], ** 此处将其插入到db中...')
            tmp_data_s['before'] = False

        return tmp_data_s

    def _data_error_init(self):
        self.result_data = {}

        return {}

    def to_right_and_update_data(self, data, pipeline):
        tmp = _get_right_model_data(data=data, site_id=2)
        params = self._get_db_update_params(item=tmp)
        base_sql_str = al_update_str_2
        if tmp['delete_time'] == '':
            sql_str = base_sql_str.format('shelf_time=%s', '')
        elif tmp['shelf_time'] == '':
            sql_str = base_sql_str.format('delete_time=%s', '')
        else:
            sql_str = base_sql_str.format('shelf_time=%s,', 'delete_time=%s')

        res = pipeline._update_table_2(sql_str=sql_str, params=params, logger=self.lg)

        return res

    def _get_detail_name_list(self, **kwargs):
        '''
        得到sku_props
        :param kwargs:
        :return:
        '''
        data = kwargs.get('data', {})

        sku_props = data.get('skuProps')
        # self.lg.info(str(sku_props))
        if sku_props is not None:  # 这里还是保留unit为单位值
            for i in sku_props:
                value = i.get('value', [])
                i.update({'img_here': 0})       # 用于判断有示例图放在哪个属性
                if value != []:
                    for j in value:
                        if j.get('imageUrl') is not None:
                            i.update({'img_here': 1})
                        else:
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
                price_info = data.get('discountPriceRanges', [])
                for item in price_info:
                    try:
                        item.pop('convertPrice')
                    except KeyError:
                        pass
                        # self.lg.info(str(price_info))
                    if re.compile('-').findall(item.get('price')) != []:
                        # goods_id: 548393536706, 处理类似[{'begin': '2', 'price': '2.39-4.38'}]
                        item['price'] = item.get('price', '').split('-')[0]

            else:  # 限时优惠
                tmp = {
                    'begin': data.get('beginAmount', ''),
                    'price': data.get('skuDiscountPrice', '')
                }
                price_info.append(tmp)

        return price_info

    def _get_sku_info(self, **kwargs):
        '''
        得到sku_map
        :param kwargs:
        :return:
        '''
        # 每个规格对应价格, 及其库存量
        '''skuMap == SKUInfo'''
        data = kwargs.get('data', {})
        price_info = kwargs.get('price_info', [])
        detail_name_list = kwargs.get('detail_name_list', [])
        # pprint(price_info)

        tmp_sku_map = data.get('skuMap')
        # pprint(tmp_sku_map)
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
                        self.lg.error('获取价格失败, 此处跳过!')
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

        # 添加示例图
        if sku_map != []:
            img_url_list = []
            for i in detail_name_list:
                if i.get('img_here', 0) == 1:
                    img_url_list = i.get('value', [])

            # self.lg.info(str(img_url_list))
            for i in img_url_list:
                img_url = i.get('imageUrl', '')
                name = i.get('name', '')
                for j in sku_map:
                    if name in j.get('spec_type', ''):
                        j.update({
                            'img_url': img_url,
                        })
                    else:
                        pass

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
                    # self.lg.info('KeyError, [size310x310URL], 此处设置为跳过')
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
                    # self.lg.info('KeyError, [unit], 此处设置为跳过')
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
            # self.lg.info('KeyError, [skuId, specId, saleCount]错误, 此处跳过')
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
            # self.lg.info('KeyError错误, 此处跳过!')
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
            item['price'],
            item['taobao_price'],
            dumps(item['price_info'], ensure_ascii=False),
            dumps(item['detail_name_list'], ensure_ascii=False),
            dumps(item['price_info_list'], ensure_ascii=False),
            dumps(item['all_img_url'], ensure_ascii=False),
            item['div_desc'],
            dumps(item['p_info'], ensure_ascii=False),
            item['is_delete'],
            item['is_price_change'],
            dumps(item['price_change_info'], ensure_ascii=False),
            item['sku_info_trans_time'],
            item['is_spec_change'],
            item['spec_trans_time'],
            item['is_stock_change'],
            item['stock_trans_time'],
            dumps(item['stock_change_info'], ensure_ascii=False),

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

    def _get_price_and_taobao_price(self, price_info):
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
            'company_name': '',         # 公司名称
            'title': '',                # 商品名称
            'link_name': '',            # 卖家姓名
            'price_info': [],           # 商品价格信息, 及其对应起批量
            'price': 0,
            'taobao_price': 0,
            'sku_props': [],            # 标签属性名称及其对应的值  (可能有图片(url), 无图(imageUrl=None))
            'sku_map': [],              # 每个规格对应价格, 及其库存量
            'all_img_url': [],          # 所有示例图片地址
            'property_info': [],        # 详细信息的标签名, 及其对应的值
            'detail_info': '',          # 下方详细div块
            'is_delete': is_delete,     # 判断是否下架
        }

        return result

    def old_ali_1688_goods_insert_into_new_table(self, data, pipeline):
        tmp = _get_right_model_data(data=data, site_id=2)

        params = self._get_db_insert_params(item=tmp)
        if tmp.get('main_goods_id') is not None:
            sql_str = al_insert_str_1
        else:
            sql_str = al_insert_str_2

        result = pipeline._insert_into_table_2(sql_str=sql_str, params=params, logger=self.lg)

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

    def _get_div_desc(self, detail_info_url):
        '''
        此处过滤得到data_tfs_url的div块
        :return:
        '''
        # self.lg.info(str(detail_info_url))
        if re.compile(r'https').findall(detail_info_url) == []:
            detail_info_url = 'https:' + detail_info_url
            # self.lg.info(str(detail_info_url))
        else:
            pass

        data_tfs_url_body = self.driver.get_url_body(url=detail_info_url)
        is_offer_details = re.compile(r'offer_details').findall(data_tfs_url_body)
        detail_info = ''

        if is_offer_details != []:
            data_tfs_url_body = re.compile(r'.*?{"content":"(.*?)"};').findall(data_tfs_url_body)
            # self.lg.info(str(body))
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
                    detail_info = re.compile(r'src="').sub('src=\"https:', detail_info)      # 再把所欲的换成https的
        # self.lg.info(str(detail_info))

        return detail_info

    def _wash_div_desc(self, detail_info):
        '''
        清洗detail_info
        :param detail_info:
        :return:
        '''
        # self.driver.page_source转码成字符串时'<','>'都被替代成&gt;&lt;此外还有其他也类似被替换
        detail_info = html_entities_2_standard_html(html_body=detail_info)

        return detail_info

    def get_goods_id_from_url(self, ali_1688_url):
        goods_id = ''
        try:
            goods_id = re.compile(r'https://detail.1688.com/offer/(.*?).html.*?').findall(ali_1688_url)[0]
            self.lg.info('------>>>| 得到的阿里1688商品id为:{0}'.format(goods_id))
        except IndexError:
            self.lg.info('阿里1688商品url错误, 非正规的url, 请参照格式(https://detail.1688.com/offer/)开头的...')
            pass

        return goods_id

    def __del__(self):
        try:
            del self.driver
            del self.lg
        except Exception:
            pass
        collect()

if __name__ == '__main__':
    ali_1688 = ALi1688LoginAndParse()
    while True:
        url = input('请输入要爬取的商品界面地址(以英文分号结束): ').strip('\n').strip(';')
        goods_id = ali_1688.get_goods_id_from_url(url)
        ali_1688.get_ali_1688_data(goods_id=goods_id)
        data = ali_1688.deal_with_data()
        pprint(data)