# coding:utf-8

'''
@author = super_fazai
@File    : jd_parse.py
@Time    : 2017/11/9 10:41
@connect : superonesfazai@gmail.com
'''

"""
可对应爬取 京东常规商品(7)，京东超市(8)，京东生鲜，京东秒杀('miaosha'字段)，京东闪购, 京东大药房(在本地测试通过, 服务器data为空)
无法抓取: 京东拼购
"""

from settings import (
    PHANTOMJS_DRIVER_PATH,
    CHROME_DRIVER_PATH,
    MY_SPIDER_LOGS_PATH,
    IP_POOL_TYPE,)

import re
from time import sleep
from gc import collect
from pprint import pprint
from json import dumps
from random import randint
from scrapy.selector import Selector

from sql_str_controller import (
    jd_update_str_1,
    jd_insert_str_1,
    jd_insert_str_2,)

from fzutils.cp_utils import _get_right_model_data
from fzutils.internet_utils import (
    get_random_pc_ua,
    get_random_phone_ua,)
from fzutils.common_utils import (
    json_2_dict,
    delete_list_null_str,
    wash_sensitive_info,)
from fzutils.spider.crawler import Crawler
from fzutils.spider.fz_requests import Requests
from fzutils.safe_utils import get_uuid3

class JdParse(Crawler):
    def __init__(self, logger=None):
        super(JdParse, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            logger=logger,
            log_save_path=MY_SPIDER_LOGS_PATH + '/jd/_/',
            
            is_use_driver=False,
            driver_executable_path=PHANTOMJS_DRIVER_PATH,
        )
        self.result_data = {}

    def _get_pc_headers(self):
        return {
            'authority': 'item.jd.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_pc_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
        }

    def _get_phone_headers(self):
        return {
            'authority': 'item.m.jd.com',
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_phone_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
        }

    def get_goods_data(self, goods_id):
        '''
        新版api
        :param goods_id:
        :return:
        '''
        self.error_record = '出错goods_id:{0}'.format(goods_id[1])
        if goods_id == []:
            self.lg.error('goods_id为空list' + self.error_record)
            return self._data_error_init()

        url = 'https://item.m.jd.com/product/{}.html'.format(goods_id[1])
        # self.lg.info(url)
        body = Requests.get_url_body(url=url, headers=self._get_phone_headers())
        # self.lg.info(body)
        if '暂无定价' in body or '403 Forbidden' in body:      # 下架商品处理
            self._data_error_init()
            return {'is_delete': 1}

        all_data, _1, _2 = {}, {}, {}
        try:
            _1 = json_2_dict(re.compile('window\._itemOnly =\((.*?)\);').findall(body)[0])
            # self.lg.info(str(_1))
            # pprint(_1)
            _2 = json_2_dict(re.compile('window\._itemInfo = \((.*?)\);').findall(body)[0])
            # self.lg.info(str(_2))
            # pprint(_2)
        except IndexError:
            self.lg.error('re索引body时异常!')
            return self._data_error_init()

        try:
            description_id = _1.get('item', {}).get('description', '')
            assert description_id != '', 'description_id为空值!'
        except AssertionError:
            self.lg.error(exc_info=True)
            return self._data_error_init()

        base_price_info = self._get_base_price_info(_2=_2)
        # pprint(base_price_info)
        if base_price_info == {}:
            return self._data_error_init()

        '''p_info'''
        # 取m站接口总是会出现无响应
        # 改为解析取pc站html
        p_info = self._get_pc_p_info(goods_id=goods_id[1])

        # div_desc
        _4 = self._get_div_desc_oir_data(goods_id=goods_id[1], description_id=description_id)
        # self.lg.info(str(_4))
        if _4 == '':
            return self._data_error_init()

        _5 = self._get_this_goods_all_goods_id_data(_1=_1)
        if _5 == []:
            return self._data_error_init()

        all_sell_count = self._get_all_sell_count(goods_id=goods_id[1])
        all_data.update({
            '1': _1,
            '2': _2,
            '4': _4,        # div_desc
            '5': _5,        # all_goods_id_list的data
            'p_info': p_info,
            'base_price_info': base_price_info,
            'all_sell_count': all_sell_count,
            'is_delete': 0,
        })
        self.result_data = all_data

        return all_data

    def deal_with_data(self, goods_id) -> dict:
        '''
        处理数据
        :param goods_id:
        :return: {'is_delete': 1} 表示下架商品
        '''
        data = self.result_data
        # pprint(data)
        if data == {}:
            self.lg.info('待处理的data为空的dict' + self.error_record)
            return {}

        if data.get('is_delete', 1) == 1:
            self.lg.info('**** 该商品{}已下架...'.format(goods_id[1]))
            return {'is_delete': 1}

        try:
            title = self._get_title(data=data)
            sub_title = self._get_sub_title(data=data)
            shop_name = self._get_shop_name(data=data)
            account = ''
            all_img_url = self._get_all_img_url(data=data)
            detail_name_list = self._get_detail_name_list(data=data)
            price_info_list = self._get_price_info_list(data=data)
            if price_info_list == []:   # 避免手机有规格但是电脑没有规格的bug
                detail_name_list = []
            p_info = self._get_p_info(data=data)
            div_desc = self._get_div_desc(data=data)
            price, taobao_price = self._get_price_and_taobao_price(
                price_info_list=price_info_list,
                base_price_info=data.get('base_price_info', {}))
            is_delete = self._get_is_delete(data=data)
        except (AssertionError, Exception):
            self.lg.error('遇到错误:', exc_info=True)
            return self._data_error_init()

        jd_type = 7     # 不进行区分全部都为7, 即京东常规商品
        all_sell_count = data.get('all_sell_count', '600')
        res = {
            'shop_name': shop_name,                     # 店铺名称
            'account': account,                         # 掌柜
            'title': title,                             # 商品名称
            'sub_title': sub_title,                     # 子标题
            'price': price,                             # 商品价格
            'taobao_price': taobao_price,               # 淘宝价
            # 'goods_stock': goods_stock,               # 商品库存
            'detail_name_list': detail_name_list,       # 商品标签属性名称
            # 'detail_value_list': detail_value_list,   # 商品标签属性对应的值
            'price_info_list': price_info_list,         # 要存储的每个标签对应规格的价格及其库存(京东隐藏库存无法爬取，只能能买或不能买)
            'all_img_url': all_img_url,                 # 所有示例图片地址
            'p_info': p_info,                           # 详细信息标签名对应属性
            # 'pc_div_url': pc_div_url,                 # pc端描述地址
            'div_desc': div_desc,                       # div_desc
            'is_delete': is_delete,                     # 是否下架判断
            'jd_type': jd_type,                         # 京东类型，(京东常规商品为7,京东超市为8)
            'all_sell_count': all_sell_count,           # 商品总销售量
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
        collect()

        return res

    def _get_base_price_info(self, _2):
        '''
        获取基础的价格信息
        :param _2:
        :return:
        '''
        # 获取该规格的base_price, 避免单规格获取不到价格
        base_price_info = {}
        try:
            detail_price = _2.get('price', {}).get('p', '')
            normal_price = _2.get('price', {}).get('m', '')
            assert detail_price != '' or normal_price != '', 'detail_price或normal_price为空值!'
            base_price_info.update({
                'detail_price': detail_price,
                'normal_price': normal_price,
            })
        except AssertionError:
            self.lg.error('遇到错误: {}'.format(self.error_record), exc_info=True)

        return base_price_info

    def _get_all_sell_count(self, goods_id):
        '''
        得到总好评数
        :return:
        '''
        params = (
            ('sorttype', '5'),
            ('sceneval', '2'),
            ('sku', str(goods_id)),
            ('page', '1'),
            ('pagesize', '10'),
            ('score', '0'),
            ('callback', 'skuJDEvalA'),
            # ('t', '0.31518758092351407'),
        )
        url = 'https://wq.jd.com/commodity/comment/getcommentlist'
        body = Requests.get_url_body(url=url, headers=self._get_phone_headers(), params=params)
        # self.lg.info(str(body))
        all_sell_count = str(randint(800, 2000))
        try:
            _ = json_2_dict(re.compile('\((.*)\)').findall(body)[0], default_res={}).get('result', {})
        except:
            self.lg.error('获取all_sell_count失败!')
            return all_sell_count

        all_sell_count = str(_.get('productCommentSummary', {}).get('CommentCount', randint(800, 2000)))
        # self.lg.info(all_sell_count)

        return all_sell_count

    def _get_this_goods_all_goods_id_data(self, _1) -> list:
        '''
        获取该商品所有的goods_id的data信息
        :return:
        '''
        # 获取所有goods_id
        self.lg.info('------>>>| 正在获取所有goods_id的data...')
        all_goods_id_list = _1.get('item', {}).get('newColorSize', [])
        # pprint(all_goods_id_list)
        _5 = []
        if all_goods_id_list == []:
            self.lg.error('all_goods_id_list为空list!')
            return _5

        for item in all_goods_id_list:
            tmp_goods_id = item.get('skuId', '')
            self.lg.info('------>>>| {}...'.format(tmp_goods_id))
            spec_value_list = []
            for key, value in item.items():
                try:
                    if isinstance(int(key), int):
                        spec_value_list.append(value)
                except ValueError:
                    pass
            spec_value_list = delete_list_null_str(spec_value_list)
            spec_value_list = [i.replace('|', '/') for i in spec_value_list]    # 避免原先的'|'影响
            spec_value = '|'.join(spec_value_list)
            _5.append({
                'sku_id': tmp_goods_id,
                'spec_value': spec_value,
                'data': self._get_one_goods_id_sku_info(goods_id=tmp_goods_id),
            })

        return _5

    def _get_price_info_list(self, data) -> list:
        '''
        获取每个规格的详细信息
        :return:
        '''
        _ = data.get('5', [])
        # pprint(_)
        price_info_list = []
        for item in _:
            spec_value = item.get('spec_value', '')
            # self.lg.info(spec_value)
            image = item.get('data', {}).get('image', '')
            img_url = 'https:' + image if image != '' else ''
            rest_number = ''    # 默认为空值

            # 能否被购买
            # is_purchase = item.get('data', {}).get('stock', {}).get('IsPurchase', 'false')    # 这个判断不准确，取消
            stock_state_name = item.get('data', {}).get('stock', {}).get('StockStateName', '采购中')
            # self.lg.info(is_purchase)
            # if stock_state_name != '现货' \
            #         or not is_purchase:
            if stock_state_name != '现货':
                continue

            detail_price = item.get('data', {}).get('price', {}).get('p', '')   # 当前价
            normal_price = item.get('data', {}).get('price', {}).get('m', '')
            if detail_price == '':
                continue

            price_info_list.append({
                'unique_id': get_uuid3(spec_value),
                'spec_value': spec_value,
                'img_url': img_url,
                'rest_number': rest_number,
                'detail_price': detail_price,
                'normal_price': normal_price,
            })

        return price_info_list

    def _get_div_desc(self, data):
        _ = data.get('4', '')
        assert  _ != '', '获取到的div_desc为空值!'

        return _

    def _get_price_and_taobao_price(self, price_info_list, base_price_info):
        '''
        最高价和最低价处理  从已经获取到的规格对应价格中筛选最高价和最低价即可
        '''
        if price_info_list == []:
            detail_price = base_price_info.get('detail_price', '')
            price, taobao_price = detail_price, detail_price
        else:
            tmp_price_list = sorted([round(float(item.get('detail_price', '')), 2) for item in price_info_list])
            assert tmp_price_list != [], '获取最高价最低价时错误!' + self.error_record

            # self.lg.info(str(tmp_price_list))
            price = tmp_price_list[-1]
            taobao_price = tmp_price_list[0]

        return price, taobao_price

    def _get_is_delete(self, data):
        is_delete = data.get('is_delete', 1)

        return is_delete

    def _get_p_info(self, data):
        p_info = data.get('p_info', [])
        assert p_info != [], 'p_info为空list!'

        return p_info

    def _get_all_img_url(self, data):
        _ = data.get('1', {}).get('item', {}).get('image', [])
        assert _ != [], 'all_img_url为空list!'
        all_img_url = [{
            'img_url': 'https://img10.360buyimg.com/n1/s450x450_' + item,
        } for item in _]

        return all_img_url

    def _get_title(self, data) -> str:
        title = data.get('1', {}).get('item', {}).get('skuName', '')
        assert title != '', 'title为空值!'

        return self._wash_sensitive_info(data=title)

    def _get_sub_title(self, data) -> str:
        '''
        获取sub_title可为空
        :param data:
        :return:
        '''
        sub_title = data.get('2', {}).get('AdvertCount', {}).get('ad', '')
        sub_title = re.compile('<a.*?</a>').sub('', sub_title)

        return self._wash_sensitive_info(data=sub_title)

    def _get_pc_p_info(self, goods_id) -> list:
        '''
        获取pc html的p_info
        :param goods_id:
        :return:
        '''
        url = 'https://item.jd.com/{}.html'.format(goods_id)
        body = Requests.get_url_body(url=url, headers=self._get_pc_headers())
        # self.lg.info(str(body))
        li_list = Selector(text=body).css('div.p-parameter ul li ::text').extract() or []   # 尽可能多匹配
        # pprint(li_list)
        p_info = []
        for item in li_list:
            try:
                _ = item.split('：')
                before = _[0].replace('\xa0', '')
                end = _[1].replace('\xa0', '')
                assert before != '' and end.replace(' ', '') != ''
                p_info.append({
                    'p_name': before,
                    'p_value': end,
                })
            except (IndexError, AssertionError):
                # self.lg.error(exc_info=True)
                pass

        return p_info

    def _get_p_info_ori_data(self, goods_id) -> dict:
        '''
        获取p_info数据源
        :return:
        '''
        params = (
            ('callback', 'commParamCallBackA'),
            ('skuid', str(goods_id)),
            # ('t', '0.11230835598015143'),
        )
        url = 'https://wq.jd.com/commodity/itembranch/getspecification'
        headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_phone_ua(),
            'accept': '*/*',
            'authority': 'wq.jd.com',
        }
        # 有一些可能返回的是空的
        body = Requests.get_url_body(url=url, headers=headers, params=params)
        # self.lg.info(str(body))
        _ = {}
        try:
            _ = json_2_dict(re.compile('\((.*)\)').findall(body)[0]).get('data', {})
        except (IndexError, Exception):
            return _

        return _

    def _get_div_desc_oir_data(self, goods_id, description_id) -> str:
        '''
        获取div_desc数据源
        :return:
        '''
        url = 'https://wqsitem.jd.com/detail/{}_d{}_normal.html'.format(goods_id, description_id)
        body = Requests.get_url_body(url=url, headers=self._get_phone_headers())
        # self.lg.info(str(body))
        try:
            _ = json_2_dict(re.compile('\((.*)\)').findall(body)[0]).get('content', '')
            # self.lg.info(str(_))
            all = re.compile('background-image:url\((.*?)\)').findall(_)
            if all == []:
                all = re.compile('<img.*?src=\"(.*?)\".*?/>').findall(_)
        except IndexError:
            self.lg.error('获取div_desc时出错!')
            return ''

        # pprint(all)
        if all == []:
            self.lg.error('获取div_desc时出错!all为空list!')
            return ''

        tmp = ''
        for item in all:
            img_url = 'https:' + item if not item.startswith('http') else item
            tmp += '<img src="{}" style="height:auto;width:100%;"/>'.format(img_url)

        div_desc = '<div>' + tmp + '</div>'

        return div_desc

    def _wash_sensitive_info(self, data):
        '''
        清洗敏感信息
        :return:
        '''
        replace_str_list = [
            ('京东', '优秀网'),
            ('JD', '优秀网')
        ]
        add_sensitive_str_list = [
            'jd',
        ]
        return wash_sensitive_info(
            data=data,
            replace_str_list=replace_str_list,
            add_sensitive_str_list=add_sensitive_str_list,
        )

    def _data_error_init(self):
        '''
        错误初始化
        :return:
        '''
        self.result_data = {}

        return {}

    def _get_jd_type(self, is_jd_market, type):
        '''
        判断是否是京东商品类型
        '''
        # self.lg.info(str(data.get('isJdMarket')))
        if is_jd_market:  # False不是京东超市
            self.lg.info('该链接为京东超市')
            jd_type = 8  # 7为京东常规商品, 8表示京东超市, 9表示京东全球购, 10表示京东大药房
        elif type == 1:
            self.lg.info('该链接为京东全球购')
            jd_type = 9
        elif type == 2:
            self.lg.info('该链接为京东大药房')
            jd_type = 10
        else:
            jd_type = 7

        return jd_type

    def _get_shop_name(self, data):
        '''
        获取shop_name
        :param data:
        :return:
        '''
        shop_name = data.get('_2', {}).get('stock', {}).get('self_D', {}).get('vender', '')

        return self._wash_sensitive_info(data=shop_name)

    def _get_detail_name_list(self, data):
        '''
        获取detail_name_list
        :param data:
        :return:
        '''
        # new
        detail_name_list = []
        sale_prop = data.get('1', {}).get('item', {}).get('saleProp', {})
        sale_prop_seq = data.get('1', {}).get('item', {}).get('salePropSeq', {})
        # pprint(sale_prop)
        for key, value in sale_prop.items():
            img_here = 0
            if value == '' \
                    or sale_prop_seq.get(key, ['']) == ['']:
                continue

            if value == '颜色':
                img_here = 1

            detail_name_list.append({
                'spec_name': value,
                'img_here': img_here,
            })

        return detail_name_list

    def _get_one_goods_id_sku_info(self, goods_id) -> dict:
        '''
        获取一个规格的商品信息(包括价格，规格示例图)
        :return:
        '''
        params = (
            ('datatype', '1'),
            ('callback', 'skuInfoCBA'),
            ('cgi_source', 'mitem'),
            ('sku', str(goods_id)),
            # ('t', '0.5813500121860642'),
        )
        url = 'https://item.m.jd.com/item/mview2'
        body = Requests.get_url_body(url=url, headers=self._get_phone_headers(), params=params)
        # print(body)
        try:
            _ = json_2_dict(re.compile('\((.*)\)').findall(body)[0], default_res={})
        except IndexError:
            self.lg.error('获取goods_id: {}售价信息失败!返回空dict!')
            return {}

        # 清洗无用数据
        try:
            _['stock']['sr'] = []
            _['stock']['ir'] = []
            _['stock']['promiseYX'] = {}
            _['stock']['area'] = {}
            _['stock']['support'] = []
            _['stock']['self_D'] = {}
            _['addrInfo'] = {}
            _['bankpromo'] = {}
            _['item']['image'] = []
        except:
            pass
        # pprint(_)
        return _

    def _wash_div_desc(self, wdis):
        '''
        清洗div_desc
        :param wdis:
        :return:
        '''
        wdis = re.compile(r'&lt;').sub('<', wdis)  # self.driver.page_source转码成字符串时'<','>'都被替代成&gt;&lt;此外还有其他也类似被替换
        wdis = re.compile(r'&gt;').sub('>', wdis)
        wdis = re.compile(r'&amp;').sub('&', wdis)
        wdis = re.compile(r'&nbsp;').sub(' ', wdis)
        wdis = re.compile(r'\n').sub('', wdis)
        wdis = re.compile(r'src=\"https:').sub('src=\"', wdis)  # 先替换部分带有https的
        wdis = re.compile(r'src="').sub('src=\"https:', wdis)  # 再把所欲的换成https的

        wdis = re.compile(r'<html>|</html>').sub('', wdis)
        wdis = re.compile(r'<head.*?>.*?</head>').sub('', wdis)
        wdis = re.compile(r'<body>|</body>').sub('', wdis)

        return wdis

    def to_right_and_update_data(self, data, pipeline):
        '''
        实时更新数据
        :param data:
        :param pipeline:
        :return:
        '''
        site_id = self._from_jd_type_get_site_id_value(jd_type=data.get('jd_type'))
        tmp = _get_right_model_data(data=data, site_id=site_id)

        params = self.get_db_update_params(item=tmp)
        base_sql_str = jd_update_str_1
        if tmp['delete_time'] == '':
            sql_str = base_sql_str.format('shelf_time=%s', '')
        elif tmp['shelf_time'] == '':
            sql_str = base_sql_str.format('delete_time=%s', '')
        else:
            sql_str = base_sql_str.format('shelf_time=%s,', 'delete_time=%s')

        res = pipeline._update_table_2(sql_str=sql_str, params=params, logger=self.lg)

        return res

    def insert_into_jd_table(self, data, pipeline):
        site_id = self._from_jd_type_get_site_id_value(jd_type=data.get('jd_type'))
        if site_id == 0:
            self.lg.error('site_id获取异常, 请检查!')
            return False

        tmp = _get_right_model_data(data=data, site_id=site_id)

        self.lg.info('------>>>| 待存储的数据信息为:{0}'.format(tmp.get('goods_id')))

        pipeline.insert_into_jd_table(item=tmp)

        return True

    def old_jd_goods_insert_into_new_table(self, data, pipeline):
        '''
        老数据转到新表
        :param data:
        :param pipeline:
        :return:
        '''
        site_id = self._from_jd_type_get_site_id_value(jd_type=data.get('jd_type'))
        if site_id == 0:
            self.lg.error('site_id获取异常, 请检查!')
            return False

        tmp = _get_right_model_data(data=data, site_id=site_id)
        self.lg.info('------>>>| 待存储的数据信息为: {0}'.format(tmp.get('goods_id')))

        params = self._get_db_insert_params(item=tmp)
        if tmp.get('main_goods_id') is not None:
            sql_str = jd_insert_str_1

        else:
            sql_str = jd_insert_str_2

        result = pipeline._insert_into_table_2(sql_str=sql_str, params=params, logger=self.lg)

        return result

    def _get_db_insert_params(self, item):
        '''
        初始化存储参数
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

    def get_db_update_params(self, item):
        '''
        得到db待更新参数
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
            item['price'],
            item['taobao_price'],
            dumps(item['price_info'], ensure_ascii=False),
            dumps(item['detail_name_list'], ensure_ascii=False),
            dumps(item['price_info_list'], ensure_ascii=False),
            dumps(item['all_img_url'], ensure_ascii=False),
            dumps(item['p_info'], ensure_ascii=False),
            item['div_desc'],
            item['all_sell_count'],
            # item['delete_time'],
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

    def _from_jd_type_get_site_id_value(self, jd_type):
        '''
        根据jd_type来获取对应的site_id的值
        :param jd_type:
        :return: a int object
        '''
        # 采集的来源地
        if jd_type == 7:
            site_id = 7     # 采集来源地(京东)
        elif jd_type == 8:
            site_id = 8     # 采集来源地(京东超市)
        elif jd_type == 9:
            site_id = 9     # 采集来源地(京东全球购)
        elif jd_type == 10:
            site_id = 10    # 采集来源地(京东大药房)
        else:
            site_id = 0     # 表示错误

        return site_id

    def get_goods_id_from_url(self, jd_url):
        '''
        注意: 初始地址可以直接用这个[https://item.jd.com/xxxxx.html]因为jd会给你重定向到正确地址
        :param jd_url:
        :return:
        '''
        is_jd_url = re.compile(r'https://item.jd.com/.*?').findall(jd_url)
        if is_jd_url != []:
            goods_id = re.compile(r'https://item.jd.com/(.*?).html.*?').findall(jd_url)[0]
            self.lg.info('------>>>| 得到的京东商品id为:{0}'.format(goods_id))
            return [0, goods_id]            # 0表示京东常规商品, 包括京东超市, 京东精选
        else:
            is_jd_hk_url = re.compile(r'https://item.jd.hk/.*?').findall(jd_url)
            if is_jd_hk_url != []:
                goods_id = re.compile(r'https://item.jd.hk/(.*?).html.*?').findall(jd_url)[0]
                self.lg.info('------>>>| 得到的京东全球购商品id为:{0}'.format(goods_id))
                return [1, goods_id]        # 1表示京东全球购商品
            else:
                is_yiyao_jd_url = re.compile(r'https://item.yiyaojd.com/.*?').findall(jd_url)
                if is_yiyao_jd_url != []:
                    goods_id = re.compile(r'https://item.yiyaojd.com/(.*?).html.*?').findall(jd_url)[0]
                    self.lg.info('------>>>| 得到的京东大药房商品id为:{}'.format(goods_id))
                    return [2, goods_id]    # 2表示京东大药房
                else:
                    self.lg.info('京东商品url错误, 非正规的url, 请参照格式(https://item.jd.com/)或者(https://item.jd.hk/)开头的...')
                    return []

    def get_pc_no_watermark_picture(self, goods_id):
        '''
        获取pc端无水印示例图片
        :param goods_id: eg: [0, '111111']
        :return: {} 表示意外退出 | [] 表示获取pc无水印图片失败 | [{'img_url': 'xxxxx'}, ...] 表示success
        '''
        if goods_id == []:
            return {}
        elif goods_id[0] == 0:  # 京东常规商品，京东超市
            tmp_pc_url = 'https://item.jd.com/' + str(goods_id[1]) + '.html'
        elif goods_id[0] == 1:  # 京东全球购(税率无法计算忽略抓取)
            tmp_pc_url = 'https://item.jd.hk/' + str(goods_id[1]) + '.html'
        elif goods_id[0] == 2:  # 京东大药房
            tmp_pc_url = 'https://item.yiyaojd.com/' + str(goods_id[1]) + '.html'
        else:
            return {}

        # 常规requests被过滤重定向到jd主页, 直接用 自己写的phantomjs方法获取
        tmp_pc_body = self.driver.use_phantomjs_to_get_url_body(url=tmp_pc_url, css_selector='div#preview')  # 该css为示例图片
        # self.lg.info(str(tmp_pc_body))
        if tmp_pc_body == '':
            self.lg.info('#### 获取无水印示例图片失败! 导致原因: tmp_pc_body为空str!')
            all_img_url = []
        else:
            try:
                all_img_url = list(Selector(text=tmp_pc_body).css('div#spec-list ul.lh li img ::attr("src")').extract())
                # self.lg.info(str(all_img_url))
                if all_img_url != []:
                    all_img_url = ['https:' + item_img_url for item_img_url in all_img_url if re.compile(r'^http').findall(item_img_url) == []]
                    all_img_url = [re.compile(r'/n5.*?jfs/').sub('/n1/jfs/', item_img_url) for item_img_url in all_img_url]
                    all_img_url = [{
                        'img_url': item_img_url,
                    } for item_img_url in all_img_url]
                else:
                    all_img_url = []
            except Exception as e:
                self.lg.error('获取商品pc版无水印示例图片时出错: ', e)
                all_img_url = []

        return all_img_url

    def __del__(self):
        try:
            del self.driver
            del self.lg
        except:
            pass
        collect()

if __name__ == '__main__':
    jd = JdParse()
    while True:
        jd_url = input('请输入待爬取的京东商品地址: ')
        jd_url.strip('\n').strip(';')
        goods_id = jd.get_goods_id_from_url(jd_url)
        jd.get_goods_data(goods_id=goods_id)
        data = jd.deal_with_data(goods_id=goods_id)
        pprint(data)
