# coding:utf-8

'''
@author = super_fazai
@File    : tmall_parse_2.py
@Time    : 2018/4/14 20:59
@connect : superonesfazai@gmail.com
'''

from random import randint
import json
from gc import collect

from settings import (
    MY_SPIDER_LOGS_PATH,
    IP_POOL_TYPE,)
from urllib.parse import urlencode

from taobao_parse import TaoBaoLoginAndParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from sql_str_controller import (
    tm_update_str_1,
    tm_insert_str_1,
    tm_insert_str_2,
    tm_insert_str_3,
    tm_update_str_2,
    tm_update_str_3,)
from multiplex_code import (
    _handle_goods_shelves_in_auto_goods_table,
    from_tmall_type_get_site_id,)
from my_exceptions import (
    GoodsShelvesException,
)

from fzutils.cp_utils import _get_right_model_data
from fzutils.spider.fz_requests import (
    PROXY_TYPE_HTTPS,
    PROXY_TYPE_HTTP,)
from fzutils.spider.async_always import *

class TmallParse(Crawler):
    def __init__(self, logger=None):
        super(TmallParse, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            logger=logger,
            log_save_path=MY_SPIDER_LOGS_PATH + '/天猫/_/',
        )
        self._set_headers()
        self.result_data = {}
        self.msg = ''
        self.proxy_type = PROXY_TYPE_HTTP

    def _set_headers(self):
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
            'Accept': '*/*',
            'Referer': 'https://detail.m.tmall.com/item.htm?id=541107920538',
            'Connection': 'keep-alive',
        }

    def get_goods_data(self, goods_id):
        '''
        得到data
        :param goods_id:
        :return: data 类型dict
        '''
        if goods_id == []:
            return self._data_error_init()

        type = goods_id[0]  # 天猫类型
        # self.lg.info(str(type))
        goods_id = goods_id[1]  # 天猫goods_id
        tmp_url = 'https://detail.m.tmall.com/item.htm?id=' + str(goods_id)
        # self.lg.info('------>>>| phone_url: {}'.format(tmp_url))

        self.headers.update({
            'Referer': tmp_url
        })
        last_url = self._get_last_url(goods_id=goods_id)
        body = Requests.get_url_body(
            url=last_url,
            headers=self.headers,
            timeout=14,
            ip_pool_type=self.ip_pool_type,
            proxy_type=self.proxy_type,)

        try:
            assert body != '', '获取到的body为空值, 此处跳过! 出错type %s: , goods_id: %s' % (str(type), goods_id)
            data = json_2_dict(
                json_str=re.compile('mtopjsonp3\((.*)\)').findall(body)[0],
                default_res={},
                logger=self.lg)
            assert data != {}, 'data为空dict, 出错type: {}, goods_id: {}'.format(str(type), str(goods_id))
            # pprint(data)
            if data.get('data', {}).get('trade', {}).get('redirectUrl', '') != '' \
                    and data.get('data', {}).get('seller', {}).get('evaluates') is None:
                raise GoodsShelvesException

        except GoodsShelvesException:
            ## 表示该商品已经下架, 原地址被重定向到新页面
            self.lg.info('@@@@@@ 该商品已经下架...')
            _handle_goods_shelves_in_auto_goods_table(
                goods_id=goods_id,
                logger=self.lg)
            tmp_data_s = self.init_pull_off_shelves_goods(type)
            self.result_data = {}
            return tmp_data_s

        except (AssertionError, IndexError):
            self.lg.error('遇到错误:', exc_info=True)
            return self._data_error_init()

        # 处理商品被转移或者下架导致页面不存在的商品
        if data.get('data', {}).get('seller', {}).get('evaluates') is None:
            self.lg.error('data为空, 地址被重定向, 该商品可能已经被转移或下架, 出错type: {}, goods_id: {}'.format(
                type,
                goods_id))
            return self._data_error_init()

        data['data']['rate'] = ''  # 这是宝贝评价
        data['data']['resource'] = ''  # 买家询问别人
        data['data']['vertical'] = ''  # 也是问和回答
        data['data']['seller']['evaluates'] = ''  # 宝贝描述, 卖家服务, 物流服务的评价值...
        result_data = data['data']

        # 处理result_data['apiStack'][0]['value']
        # self.lg.info(result_data.get('apiStack', [])[0].get('value', ''))
        result_data_apiStack_value = result_data.get('apiStack', [])[0].get('value', {})

        # 将处理后的result_data['apiStack'][0]['value']重新赋值给result_data['apiStack'][0]['value']
        result_data['apiStack'][0]['value'] = self._wash_result_data_apiStack_value(
            goods_id=goods_id,
            result_data_apiStack_value=result_data_apiStack_value)

        # 处理mockData
        mock_data = result_data['mockData']
        mock_data = json_2_dict(
            json_str=mock_data,
            logger=self.lg)
        if mock_data == {}:
            self.lg.error('出错type: {0}, goods_id: {1}'.format(type, goods_id))
            return self._data_error_init()

        mock_data['feature'] = ''
        # pprint(mock_data)
        result_data['mockData'] = mock_data

        # self.lg.info(str(result_data.get('apiStack', [])[0]))   # 可能会有{'name': 'esi', 'value': ''}的情况
        if result_data.get('apiStack', [])[0].get('value', '') == '':
            self.lg.error("result_data.get('apiStack', [])[0].get('value', '')的值为空....出错type: {}, goods_id: {}".format(
                str(type),
                goods_id))
            result_data['trade'] = {}
            return self._data_error_init()
        else:
            result_data['trade'] = result_data.get('apiStack', [])[0].get('value', {}).get('trade', {})     # 用于判断该商品是否已经下架的参数
            # pprint(result_data['trade'])

        result_data['type'] = type
        result_data['goods_id'] = goods_id
        self.result_data = result_data
        # pprint(self.result_data)

        return result_data

    def deal_with_data(self):
        '''
        得到需求数据
        :return:
        '''
        data = self.result_data
        # pprint(data)
        if data != {}:
            taobao = TaoBaoLoginAndParse(logger=self.lg)
            goods_id = data['goods_id']
            # 天猫类型
            tmall_type = data.get('type', 33)  # 33用于表示无法正确获取
            # self.lg.info(str(tmall_type))
            shop_name = data['seller'].get('shopName', '')      # 可能不存在shopName这个字段
            account = data['seller'].get('sellerNick', '')
            title = data['item']['title']
            sub_title = data['item'].get('subtitle', '')
            sub_title = re.compile(r'\n').sub('', sub_title)

            price, taobao_price = taobao._get_price_and_taobao_price(data=data)
            # 商品库存
            goods_stock = data['apiStack'][0]['value'].get('skuCore', {}).get('sku2info', {}).get('0', {}).get('quantity', '')
            # 商品标签属性名称,及其对应id值
            detail_name_list, detail_value_list = taobao._get_detail_name_and_value_list(data=data)

            '''
            每个标签对应值的价格及其库存
            '''
            price_info_list = taobao._get_price_info_list(data=data, detail_value_list=detail_value_list)
            # 多规格进行重新赋值
            price, taobao_price = taobao._get_new_price_and_taobao_price_when_price_info_list_not_null_list(
                price_info_list=price_info_list,
                price=price,
                taobao_price=taobao_price)

            # 所有示例图片地址
            all_img_url = taobao._get_all_img_url(tmp_all_img_url=data['item']['images'])
            # self.lg.info(str(all_img_url))

            # 详细信息p_info
            p_info = taobao._get_p_info(tmp_p_info=data.get('props').get('groupProps'))  # tmp_p_info 一个list [{'内存容量': '32GB'}, ...]
            if p_info != []:
                p_info = [{
                    'id': 0,
                    'name': _i.get('p_name', ''),
                    'value': _i.get('p_value', ''),
                } for _i in p_info]

            '''
            div_desc
            '''
            # 手机端描述地址
            phone_div_url = ''
            if data.get('item', {}).get('taobaoDescUrl') is not None:
                phone_div_url = 'https:' + data['item']['taobaoDescUrl']

            # pc端描述地址
            pc_div_url = ''
            div_desc = ''
            if data.get('item', {}).get('taobaoPcDescUrl') is not None:
                pc_div_url = 'https:' + data['item']['taobaoPcDescUrl']
                # self.lg.info(phone_div_url)
                # self.lg.info(pc_div_url)

                div_desc = taobao.get_div_from_pc_div_url(pc_div_url, goods_id)
                # self.lg.info(div_desc)
                if div_desc == '':
                    self.lg.error('该商品的div_desc为空! 出错goods_id: %s' % str(goods_id))
                    return self._data_error_init()

                collect()

            '''
            后期处理
            '''
            # 后期处理detail_name_list, detail_value_list
            detail_name_list = [{
                'spec_name': i[0],
                'img_here': i[2],
            } for i in detail_name_list]

            # 商品标签属性对应的值, 及其对应id值
            if data.get('skuBase').get('props') is None:
                pass
            else:
                tmp_detail_value_list = [item['values'] for item in data.get('skuBase', '').get('props', '')]
                # self.lg.info(str(tmp_detail_value_list))
                detail_value_list = []
                for item in tmp_detail_value_list:
                    tmp = [i['name'] for i in item]
                    # self.lg.info(str(tmp))
                    detail_value_list.append(tmp)  # 商品标签属性对应的值
                    # pprint(detail_value_list)

            is_delete = self._get_is_delete(data=data, title=title)
            # self.lg.info('is_delete = %s' % str(is_delete))
            if is_delete == 1:
                self.lg.info('@@@ 该商品已下架...')

            # 月销量
            try:
                sell_count = str(data.get('apiStack', [])[0].get('value', {}).get('item', {}).get('sellCount', ''))
            except:
                sell_count = '0'
                # self.lg.info(sell_count)

            try: del taobao
            except: pass
            result = {
                'shop_name': shop_name,                 # 店铺名称
                'account': account,                     # 掌柜
                'title': title,                         # 商品名称
                'sub_title': sub_title,                 # 子标题
                'price': price,                         # 商品价格
                'taobao_price': taobao_price,           # 淘宝价
                'goods_stock': goods_stock,             # 商品库存
                'detail_name_list': detail_name_list,   # 商品标签属性名称
                'detail_value_list': detail_value_list, # 商品标签属性对应的值
                'price_info_list': price_info_list,     # 要存储的每个标签对应规格的价格及其库存
                'all_img_url': all_img_url,             # 所有示例图片地址
                'p_info': p_info,                       # 详细信息标签名对应属性
                'pc_div_url': pc_div_url,               # pc端描述地址
                'div_desc': div_desc,                   # div_desc
                'sell_count': sell_count,               # 月销量
                'is_delete': is_delete,                 # 是否下架判断
                'type': tmall_type,                     # 天猫类型
            }
            # pprint(result)
            # self.lg.info(str(result))
            # wait_to_send_data = {
            #     'reason': 'success',
            #     'data': result,
            #     'code': 1
            # }
            # json_data = dumps(wait_to_send_data, ensure_ascii=False)
            # print(json_data)
            collect()

            return result

        else:
            self.lg.info('待处理的data为空的dict, 该商品可能已经转移或者下架')
            # return {
            #     'is_delete': 1,
            # }
            return {}

    def _data_error_init(self):
        '''
        数据获取错误初始化
        :return:
        '''
        self.result_data = {}

        return {}

    def old_tmall_goods_insert_into_new_table(self, data, pipeline):
        '''
        老库数据规范，然后存入
        :param data:
        :param pipeline:
        :return:
        '''
        site_id = from_tmall_type_get_site_id(type=data.get('type'))
        if site_id is False:
            self.lg.error('获取到的site_id为False!出错!请检查!出错goods_id: {0}'.format(data.get('goods_id')))
            return None
        tmp = _get_right_model_data(data=data, site_id=site_id, logger=self.lg)

        params = self._get_db_insert_params(item=tmp)
        if tmp.get('main_goods_id') is not None:
            sql_str = tm_insert_str_1
        else:
            sql_str = tm_insert_str_2

        result = pipeline._insert_into_table_2(sql_str=sql_str, params=params, logger=self.lg)

        return result

    def insert_into_taoqianggou_xianshimiaosha_table(self, data, pipeline) -> bool:
        '''
        将数据规范化插入淘抢购表
        :param data:
        :param pipeline:
        :return:
        '''
        try:
            tmp = _get_right_model_data(data=data, site_id=28, logger=self.lg)   # 采集来源地(淘抢购)
        except:
            print('此处抓到的可能是淘宝秒杀券所以跳过')
            return False

        self.lg.info('------>>>| 待存储的数据信息为: {0}'.format(data.get('goods_id')))
        params = self._get_db_insert_taoqianggou_miaosha_params(item=tmp)
        res = pipeline._insert_into_table_2(sql_str=tm_insert_str_3, params=params, logger=self.lg)

        return res

    async def _update_taoqianggou_xianshimiaosha_table(self, data, pipeline):
        '''
        update对应表的数据
        :param data:
        :param pipeline:
        :return:
        '''
        try:
            tmp = _get_right_model_data(data=data, site_id=28, logger=self.lg)
        except:
            self.lg.error('获取规范化数据失败!出错goods_id:{0}'.format(data.get('goods_id')))
            return None

        self.lg.info('------>>>| 待存储的数据信息为: {0}'.format(data.get('goods_id')))

        params = await self._get_db_update_miaosha_params(item=tmp)
        pipeline._update_table_2(sql_str=tm_update_str_2, params=params, logger=self.lg)

        return

    def _get_is_delete(self, **kwargs):
        '''
        得到is_delete
        :param kwargs:
        :return:
        '''
        data = kwargs.get('data', {})
        title = kwargs.get('title', '')

        # 天猫
        '''
        bug: 部分商品 存在一个bug, 本地抓取is_delete=0, server则为1!
        预估: 是允许配送范围的问题, server在加拿大!
        eg: https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.16.3a476095nAD0gh&id=541895028241&skuId=3556559472007&areaId=330700&user_id=732956498&cat_id=2&is_b=1&rn=5435e2e903312b0cf8422e9938dff7ac
        '''
        is_delete = 0
        # * 2017-10-16 先通过buyEnable字段来判断商品是否已经下架
        if data.get('trade', {}) != {}:
            if data.get('trade', {}).get('buyEnable', 'true') == 'false':
                is_delete = 1

        if is_delete == 0:      # * 2018-6-29 加个判断防止与上面冲突(修复冲突bug)
            # * 2018-4-17 新增一个判断是否下架
            if not data.get('mockData', {}).get('trade', {}).get('buyEnable', True):
                    is_delete = 1

        # 2017-10-16 此处再考虑名字中显示下架的商品
        if re.compile(r'下架').findall(title) != []:
            if re.compile(r'待下架').findall(title) != []:
                is_delete = 0
            elif re.compile(r'自动下架').findall(title) != []:
                is_delete = 0
            else:
                is_delete = 1

        return is_delete

    def _get_db_insert_params(self, item):
        '''
        得到待插入的数据
        :param item:
        :return:
        '''
        params = [
            item['goods_id'],
            item['goods_url'],
            item['username'],
            item['create_time'],
            item['modify_time'],
            item['shop_name'],
            item['account'],
            item['title'],
            item['sub_title'],
            item['link_name'],
            item['price'],
            item['taobao_price'],
            dumps(item['price_info'], ensure_ascii=False),
            dumps(item['detail_name_list'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
            dumps(item['price_info_list'], ensure_ascii=False),
            dumps(item['all_img_url'], ensure_ascii=False),
            dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
            item['div_desc'],  # 存入到DetailInfo
            item['all_sell_count'],

            item['site_id'],
            item['is_delete'],
        ]

        if item.get('main_goods_id') is not None:
            params.append(item.get('main_goods_id'))

        return tuple(params)

    def _get_db_insert_taoqianggou_miaosha_params(self, item):
        '''
        得到db待插入的数据
        :param item:
        :return:
        '''
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
            dumps(item['schedule'], ensure_ascii=False),
            dumps(item['miaosha_time'], ensure_ascii=False),
            item['miaosha_begin_time'],
            item['miaosha_end_time'],
            item['page'],
            item['spider_time'],

            item['site_id'],
            item['is_delete'],
        )

        return params

    async def _get_db_update_miaosha_params(self, item):
        '''
        规范待插入数据
        :param item:
        :return:
        '''
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
            item['goods_id'],
        )

        return params

    def init_pull_off_shelves_goods(self, type):
        '''
        初始化下架商品的数据
        :return:
        '''
        is_delete = 1
        result = {
            'shop_name': '',  # 店铺名称
            'account': '',  # 掌柜
            'title': '',  # 商品名称
            'sub_title': '',  # 子标题
            'price': 0,  # 商品价格
            'taobao_price': 0,  # 淘宝价
            'goods_stock': '',  # 商品库存
            'detail_name_list': [],  # 商品标签属性名称
            'detail_value_list': [],  # 商品标签属性对应的值
            'price_info_list': [],  # 要存储的每个标签对应规格的价格及其库存
            'all_img_url': [],  # 所有示例图片地址
            'p_info': [],  # 详细信息标签名对应属性
            'pc_div_url': '',  # pc端描述地址
            'div_desc': '',  # div_desc
            'sell_count': '0',  # 月销量
            'is_delete': is_delete,  # 是否下架判断
            'type': type,  # 天猫类型
        }
        return result

    def _wash_result_data_apiStack_value(self, goods_id, result_data_apiStack_value):
        '''
        清洗result_data_apiStack_value
        :param goods_id:
        :param result_data_apiStack_value:
        :return:
        '''
        try:
            result_data_apiStack_value = json_2_dict(
                json_str=result_data_apiStack_value,
                logger=self.lg,)

            result_data_apiStack_value['vertical'] = ''
            result_data_apiStack_value['consumerProtection'] = ''  # 7天无理由退货
            result_data_apiStack_value['feature'] = ''
            result_data_apiStack_value['layout'] = ''
            result_data_apiStack_value['delivery'] = ''  # 发货地到收到地
            result_data_apiStack_value['resource'] = ''  # 优惠券
            # result_data_apiStack_value['item'] = ''       # 不能注释否则得不到月销量
            # pprint(result_data_apiStack_value)
        except Exception:
            self.lg.error("json转换出错，得到result_data['apiStack'][0]['value']值可能为空，此处跳过 出错goods_id: %s" % str(goods_id))
            result_data_apiStack_value = ''
            pass

        return result_data_apiStack_value

    def _set_params(self, goods_id):
        '''
        设置params
        :param goods_id:
        :return:
        '''
        params = (
            ('jsv', '2.4.8'),
            ('appKey', '12574478'),
            ('t', str(datetime_to_timestamp(get_shanghai_time())) + str(randint(100, 999))),
            # ('sign', 'de765f1adf3bdc4a07687d45fd10a6b3'),
            ('api', 'mtop.taobao.detail.getdetail'),
            ('v', '6.0'),
            ('dataType', 'jsonp'),
            ('ttid', '2017@taobao_h5_6.6.0'),
            ('AntiCreep', 'true'),
            ('type', 'jsonp'),
            ('callback', 'mtopjsonp3'),
            ('data', dumps({'itemNumId': goods_id})),
        )

        return params

    def _get_last_url(self, goods_id):
        '''
        得到组合params的last_url
        :param goods_id:
        :return:
        '''
        params = self._set_params(goods_id=goods_id)
        tmp_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/'

        params = tuple_or_list_params_2_dict_params(params)
        url = tmp_url + '?' + urlencode(params)
        last_url = re.compile(r'\+').sub('', url)  # 转换后得到正确的url请求地址(替换'+')
        # self.lg.info(last_url)

        return last_url

    def _from_tmall_type_get_tmall_url(self, type, goods_id):
        '''
        根据天猫的type来获取正确的url
        :param type:
        :param goods_id:
        :return: a str
        '''
        if type == 0:
            # 天猫常规商品
            goods_url = 'https://detail.tmall.com/item.htm?id=' + str(goods_id)
        elif type == 1:
            # 天猫超市
            goods_url = 'https://chaoshi.detail.tmall.com/item.htm?id=' + str(goods_id)
        elif type == 2:
            # 天猫国际
            goods_url = 'https://detail.tmall.hk/item.htm?id=' + str(goods_id)
        else:
            goods_url = ''

        return goods_url

    def get_goods_id_from_url(self, tmall_url):
        '''
        得到合法url的goods_id
        :param tmall_url:
        :return: a list [0, '1111111'] [2, '1111111', 'https://ssss'] 0:表示天猫常规商品, 1:表示天猫超市, 2:表示天猫国际, 返回为[]表示解析错误
        '''
        is_tmall_url = re.compile(r'https://detail.tmall.com/item.htm.*?').findall(tmall_url)
        if is_tmall_url != []:                  # 天猫常规商品
            tmp_tmall_url = re.compile(r'https://detail.tmall.com/item.htm.*?id=(\d+)&{0,20}.*?').findall(tmall_url)
            if tmp_tmall_url != []:
                is_tmp_tmp_tmall_url = re.compile(r'https://detail.tmall.com/item.htm.*?&id=(\d+)&{0,20}.*?').findall(tmall_url)
                if is_tmp_tmp_tmall_url != []:
                    goods_id = is_tmp_tmp_tmall_url[0]
                else:
                    goods_id = tmp_tmall_url[0]
            else:
                tmall_url = re.compile(r';').sub('', tmall_url)
                goods_id = re.compile(r'https://detail.tmall.com/item.htm.*?id=(\d+)').findall(tmall_url)[0]
            self.lg.info('------>>>| 得到的天猫商品id为:%s' % goods_id)
            return [0, goods_id]

        else:
            is_tmall_supermarket = re.compile(r'https://chaoshi.detail.tmall.com/item.htm.*?').findall(tmall_url)
            if is_tmall_supermarket != []:      # 天猫超市
                tmp_tmall_url = re.compile(r'https://chaoshi.detail.tmall.com/item.htm.*?id=(\d+)&.*?').findall(tmall_url)
                if tmp_tmall_url != []:
                    goods_id = tmp_tmall_url[0]
                else:
                    tmall_url = re.compile(r';').sub('', tmall_url)
                    goods_id = re.compile(r'https://chaoshi.detail.tmall.com/item.htm.*?id=(\d+)').findall(tmall_url)[0]
                self.lg.info('------>>>| 得到的天猫商品id为:%s' % goods_id)
                return [1, goods_id]

            else:
                is_tmall_hk = re.compile(r'https://detail.tmall.hk/.*?item.htm.*?').findall(tmall_url)      # 因为中间可能有国家的地址 如https://detail.tmall.hk/hk/item.htm?
                if is_tmall_hk != []:           # 天猫国际， 地址中有地域的也能正确解析, 嘿嘿 -_-!!!
                    tmp_tmall_url = re.compile(r'https://detail.tmall.hk/.*?item.htm.*?id=(\d+)&.*?').findall(tmall_url)
                    if tmp_tmall_url != []:
                        goods_id = tmp_tmall_url[0]
                    else:
                        tmall_url = re.compile(r';').sub('', tmall_url)
                        goods_id = re.compile(r'https://detail.tmall.hk/.*?item.htm.*?id=(\d+)').findall(tmall_url)[0]
                    before_url = re.compile(r'https://detail.tmall.hk/.*?item.htm').findall(tmall_url)[0]
                    self.lg.info('------>>>| 得到的天猫商品id为:%s' % goods_id)
                    return [2, goods_id, before_url]
                else:
                    self.lg.info('天猫商品url错误, 非正规的url, 请参照格式(https://detail.tmall.com/item.htm)开头的...')
                    return []

    def __del__(self):
        try:
            del self.lg
            del self.msg
        except:
            pass
        collect()

if __name__ == '__main__':
    tmall = TmallParse()
    while True:
        tmall_url = input('请输入待爬取的天猫商品地址: ')
        tmall_url = tmall_url.strip('\n').strip(';')
        goods_id = tmall.get_goods_id_from_url(tmall_url)   # 返回一个dict类型
        # print(goods_id)
        if goods_id != []:
            data = tmall.get_goods_data(goods_id=goods_id)
            result = tmall.deal_with_data()
            pprint(result)
            # print(result)
            collect()
        else:
            print('获取到的天猫商品地址无法解析，地址错误')

