# coding:utf-8

'''
@author = super_fazai
@File    : jd_parse.py
@Time    : 2017/11/9 10:41
@connect : superonesfazai@gmail.com
'''

"""
可对应爬取 京东常规商品(7)，京东超市(8)，京东生鲜，京东秒杀('miaosha'字段)，京东闪购, 京东大药房(在本地测试通过, 服务器data为空)
"""

from settings import (
    PHANTOMJS_DRIVER_PATH,
    CHROME_DRIVER_PATH,
    MY_SPIDER_LOGS_PATH,
    IP_POOL_TYPE,)

import re
from time import sleep
import gc
from pprint import pprint
from json import dumps
from scrapy.selector import Selector
from logging import (
    INFO,
    ERROR,)

from sql_str_controller import (
    jd_update_str_1,
    jd_insert_str_1,
    jd_insert_str_2,)

from fzutils.cp_utils import _get_right_model_data
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import Requests
from fzutils.spider.fz_phantomjs import BaseDriver
from fzutils.common_utils import json_2_dict
from fzutils.log_utils import set_logger
from fzutils.time_utils import get_shanghai_time

class JdParse(object):
    def __init__(self, logger=None):
        self._set_headers()
        self._set_pc_headers()
        self.result_data = {}
        self._set_logger(logger)
        self.driver = BaseDriver(executable_path=PHANTOMJS_DRIVER_PATH, logger=self.my_lg, ip_pool_type=IP_POOL_TYPE)

    def _set_logger(self, logger):
        if logger is None:
            self.my_lg = set_logger(
                log_file_name=MY_SPIDER_LOGS_PATH + '/jd/_/' + str(get_shanghai_time())[0:10] + '.txt',
                console_log_level=INFO,
                file_log_level=ERROR
            )
        else:
            self.my_lg = logger

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'jd.com;jd.hk',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    def _set_pc_headers(self):
        # pc头, 只识别小写
        self.pc_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'connection': 'keep-alive',
            'user-agent': get_random_pc_ua(),
        }

    def get_goods_data(self, goods_id):
        '''
        模拟构造得到data的url
        :param goods_id:
        :return: data   类型dict
        '''
        if goods_id == []:
            self.my_lg.error('goods_id为空list')
            return self._data_error_init()

        if isinstance(self._get_need_url(goods_id=goods_id), dict):     # 即返回{}
            return self._data_error_init()

        self.error_record = '出错goods_id:{0}'.format(goods_id[1])

        phone_url, tmp_url, comment_url = self._get_need_url(goods_id=goods_id)
        self.my_lg.info('------>>>| 得到的移动端地址为: {0}'.format(phone_url))

        # self.my_lg.info(str(tmp_url))
        if goods_id[0] == 1:    # ** 注意: 先预加载让driver获取到sid **
            # 研究分析发现京东全球购，大药房商品访问需要cookies中的sid值
            self.driver.use_phantomjs_to_get_url_body(url='https://mitem.jd.hk/cart/cartNum.json')
        elif goods_id[0] == 2:
            # 研究分析发现京东全球购，大药房商品访问需要cookies中的sid值
            self.driver.use_phantomjs_to_get_url_body(url='https://m.yiyaojd.com/cart/cartNum.json')

        # 得到总销售量
        comment_body = self.driver.use_phantomjs_to_get_url_body(url=comment_url)
        if comment_body == '':  # 网络问题或者ip切换出错
            return self._data_error_init()

        comment_body = self._wash_url_body(body=comment_body)
        # self.my_lg.info(str(comment_body))
        comment_body_1 = re.compile(r'<pre.*?>(.*)</pre>').findall(comment_body)
        if comment_body_1 != []:
            comment_data = comment_body_1[0]
            comment_data = json_2_dict(json_str=comment_data)
            # pprint(comment_data)
            all_sell_count = comment_data.get('wareDetailComment', {}).get('allCnt', '0')

        else:
            self.my_lg.error('获取到的comment的销售量data为空!'+self.error_record)
            return self._data_error_init()

        body = self.driver.use_phantomjs_to_get_url_body(url=tmp_url)
        if body == '':
            return self._data_error_init()

        body = self._wash_url_body(body=body)
        # self.my_lg.info(str(body))

        body_1 = re.compile(r'<pre.*?>(.*)</pre>').findall(body)

        ## ** 起初是拿phantomjs来进行url请求的，本来想着用requests来优化，但是改动有点大，就先暂时不改动 **
        # body_1 = Requests.get_url_body(url=tmp_url, headers=self.headers)
        # if body_1 == '':
        #     body_1 = []
        # else:
        # # self.my_lg.info(str(body_1[0]))

        if body_1 != []:
            data = body_1[0]
            data = json_2_dict(json_str=data)
            if data == {}:
                self.my_lg.error(r'此处直接返回data为{}'+self.error_record)
                return self._data_error_init()

            # pprint(data)
            wdis = data.get('wdis', '') # 图文描述
            data = data.get('ware', {})
            try:
                data.pop('wdisHtml')
                data.get('wi', {})['afterServiceList'] = []
            except Exception:
                pass

            # 处理'wi' 'code'
            if data.get('wi') is not None:
                # 用于获取p_info
                code = data.get('wi', {}).get('code', '')
                # self.my_lg.info('wi,code的为: {}'.format(code))
                if code != '':
                    code = json_2_dict(json_str=code)
                    try:
                        data.get('wi', {})['code'] = code
                    except Exception as e:  # 对应p_info解析错误的, 换方法解析
                        self.my_lg.info('wi中的code对应json解析错误, 为:', e)
                        code = data.get('wi', {}).get('wareQD', '')
                        data.get('wi', {})['code'] = code
            else:
                data['wi'] = {'code': []}

            # 处理wdis
            data['wdis'] = wdis

            # 商品总销售量
            data['all_sell_count'] = all_sell_count

            if data != {}:
                self.result_data = data
                # pprint(data)
                return data
            else:
                self.my_lg.error('获取到的data的key值ware为空!'+self.error_record)
                return self._data_error_init()

        else:
            self.my_lg.error('获取到的data为空!'+self.error_record)
            return self._data_error_init()

    def deal_with_data(self, goods_id):
        '''
        处理result_data, 返回需要的信息
        :return: 字典类型
        '''
        data = self.result_data
        if data != {}:
            shop_name = self._get_shop_name(data=data)
            account = ''
            title = data.get('wname', '')
            sub_title = ''
            detail_name_list = self._get_detail_name_list(data=data)

            '''
            要存储的每个标签对应规格的价格及其库存(京东无库存抓取, 只有对应规格商品是否可买)
            '''
            price_info_list = self.get_price_info_list(goods_id, detail_name_list, data)
            # pprint(price_info_list)

            # 获取is_delete, price, taobao_price
            _ = self._get_price_and_taobao_price_and_is_delete(
                detail_name_list=detail_name_list,
                price_info_list=price_info_list,
                goods_id=goods_id)
            if _ == [0, '', '']:    # 异常退出
                return self._data_error_init()
            else:
                is_delete, price, taobao_price = _
            # self.my_lg.info('最高价: {0}, 最低价: {1}'.format(price, taobao_price))

            # 所有示例图片地址
            '''
            新增: 由于手机版获取到的jd示例图片数据有京东的水印，所以单独先通过pc端来获取图片，pc获取失败就用phone端的
            '''
            all_img_url = self.get_pc_no_watermark_picture(goods_id=goods_id)
            if all_img_url == {}:   # 意外退出
                return self._data_error_init()

            if all_img_url == []:   # 获取pc端失败, 即获取phone示例图
                if data.get('images') is not None:
                    all_img_url = [{
                        'img_url': item.get('bigpath')
                    } for item in data.get('images')]
                else:
                    all_img_url = []
            else:
                pass
            # pprint(all_img_url)

            p_info = self.get_p_info(data=data)
            # pprint(p_info)      # 爬取是手机端的所以没有第一行的，就是手机端的规格
            div_desc = self.get_right_div_desc(data=data)
            # self.my_lg.info(str(div_desc))
            jd_type = self._get_jd_type(is_jd_market=data.get('isJdMarket'), type=goods_id[0])
            # self.my_lg.info('jd_type为: {0}'.format(jd_type))

            # 商品总销售量
            all_sell_count = str(data.get('all_sell_count', '0'))
            if is_delete == 1:
                self.my_lg.info('**** 该商品已下架...')

            result = {
                'shop_name': shop_name,                 # 店铺名称
                'account': account,                     # 掌柜
                'title': title,                         # 商品名称
                'sub_title': sub_title,                 # 子标题
                'price': price,                         # 商品价格
                'taobao_price': taobao_price,           # 淘宝价
                # 'goods_stock': goods_stock,             # 商品库存
                'detail_name_list': detail_name_list,   # 商品标签属性名称
                # 'detail_value_list': detail_value_list, # 商品标签属性对应的值
                'price_info_list': price_info_list,     # 要存储的每个标签对应规格的价格及其库存(京东隐藏库存无法爬取，只能能买或不能买)
                'all_img_url': all_img_url,             # 所有示例图片地址
                'p_info': p_info,                       # 详细信息标签名对应属性
                # 'pc_div_url': pc_div_url,               # pc端描述地址
                'div_desc': div_desc,                   # div_desc
                'is_delete': is_delete,                 # 是否下架判断
                'jd_type': jd_type,                     # 京东类型，(京东常规商品为7,京东超市为8)
                'all_sell_count': all_sell_count,       # 商品总销售量
            }
            # pprint(result)
            # self.my_lg.info(str(result))
            # wait_to_send_data = {
            #     'reason': 'success',
            #     'data': result,
            #     'code': 1
            # }
            # json_data = json.dumps(wait_to_send_data, ensure_ascii=False)
            # self.my_lg.info(str(json_data))
            gc.collect()
            return result

        else:
            self.my_lg.info('待处理的data为空的dict'+self.error_record)
            return {}

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
        # self.my_lg.info(str(data.get('isJdMarket')))
        if is_jd_market:  # False不是京东超市
            self.my_lg.info('该链接为京东超市')
            jd_type = 8  # 7为京东常规商品, 8表示京东超市, 9表示京东全球购, 10表示京东大药房
        elif type == 1:
            self.my_lg.info('该链接为京东全球购')
            jd_type = 9
        elif type == 2:
            self.my_lg.info('该链接为京东大药房')
            jd_type = 10
        else:
            jd_type = 7

        return jd_type

    def _get_price_and_taobao_price_and_is_delete(self, **kwargs):
        '''
        获取is_delete, price, taobao_price
        :return: [0, '', ''] 表示异常退出 | [x, xx, xx] 表示成功
        '''
        detail_name_list = kwargs.get('detail_name_list', [])
        price_info_list = kwargs.get('price_info_list', [])
        goods_id = kwargs.get('goods_id', [])
        # 是否下架判断
        is_delete = 0

        # 商品价格
        '''
        最高价和最低价处理  从已经获取到的规格对应价格中筛选最高价和最低价即可
        '''
        if detail_name_list == []:  # 说明没有规格，所有价格只能根据当前的goods_id来获取
            if self.from_ware_id_get_price_info(ware_id=goods_id)[0] == '暂无报价':
                is_delete = 1  # 说明已经下架
                price, taobao_price = (0, 0,)
            else:
                try:
                    # self.my_lg.info(str(self.from_ware_id_get_price_info(ware_id=goods_id)[0]))
                    price = round(float(self.from_ware_id_get_price_info(ware_id=goods_id)[0]), 2)
                    taobao_price = price
                except TypeError:
                    is_delete = 1  # 说明该商品暂无报价
                    price, taobao_price = (0, 0,)
        else:
            try:
                tmp_price_list = sorted([round(float(item.get('detail_price', '')), 2) for item in price_info_list])
            except ValueError:
                self.my_lg.error('tmp_price_list的ValueError，此处设置为跳过' + self.error_record)
                return [0, '', '']

            # self.my_lg.info(str(tmp_price_list))
            if tmp_price_list != []:
                price = tmp_price_list[-1]
                taobao_price = tmp_price_list[0]
            else:
                self.my_lg.error('获取最高价最低价时错误' + self.error_record)
                return [0, '', '']

        return [is_delete, price, taobao_price]

    def _get_need_url(self, goods_id):
        '''
        获取需求的url
        :param goods_id:
        :return:
        '''
        phone_url = ''
        tmp_url = ''
        comment_url = ''
        if goods_id[0] == 0:  # 表示为京东常规商品
            phone_url = 'https://item.m.jd.com/ware/view.action?wareId=' + str(goods_id[1])
            # 用于得到常规信息
            tmp_url = 'https://item.m.jd.com/ware/detail.json?wareId=' + str(goods_id[1])
            comment_url = 'https://item.m.jd.com/ware/getDetailCommentList.json?wareId=' + str(goods_id[1])

        elif goods_id[0] == 1:  # 表示为京东全球购商品 (此处由于进口关税无法计算先不处理京东全球购)
            phone_url = 'https://mitem.jd.hk/ware/view.action?wareId=' + str(goods_id[1])
            tmp_url = 'https://mitem.jd.hk/ware/detail.json?wareId=' + str(goods_id[1])
            comment_url = 'https://mitem.jd.hk/ware/getDetailCommentList.json?wareId=' + str(goods_id[1])

            self.my_lg.info('此商品为京东全球购商品，由于进口关税无法计算，先不处理京东全球购')
            return {}

        elif goods_id[0] == 2:  # 表示京东大药房商品
            phone_url = 'https://m.yiyaojd.com/ware/view.action?wareId=' + str(goods_id[1])
            tmp_url = 'https://m.yiyaojd.com/ware/detail.json?wareId=' + str(goods_id[1])
            comment_url = 'https://m.yiyaojd.com/ware/getDetailCommentList.json?wareId=' + str(goods_id[1])

        return phone_url, tmp_url, comment_url

    def from_ware_id_get_price_info(self, ware_id):
        '''
        得到价格信息，由于过滤了requests所以用phantomjs
        '''
        price_url = ''
        if ware_id[0] == 0:    # 表示为京东常规商品
            price_url = 'https://item.m.jd.com/ware/getSpecInfo.json?wareId=' + str(ware_id[1])

        elif ware_id[0] == 1:  # 表示为京东全球购商品
            price_url = 'https://mitem.jd.hk/ware/getSpecInfo.json?wareId=' + str(ware_id[1])

        elif ware_id[0] == 2:  # 表示京东大药房商品
            price_url = 'https://m.yiyaojd.com/ware/getSpecInfo.json?wareId=' + str(ware_id[1])

        # self.my_lg.info(str(price_url))
        price_body = self.driver.use_phantomjs_to_get_url_body(url=price_url)

        price_body_1 = re.compile(r'<pre.*?>(.*)</pre>').findall(price_body)
        if price_body_1 != []:
            price_data = json_2_dict(json_str=price_body_1[0])
            try:
                price_data.pop('defaultAddress')
                price_data.pop('commonConfigJson')
            except Exception: pass
            try: price_data.pop('newYanBaoInfo')
            except Exception: pass

            # 处理newYanBaoInfo
            new_yan_bao_info = price_data.get('newYanBaoInfo')
            if new_yan_bao_info is not None:
                new_yan_bao_info = json_2_dict(json_str=new_yan_bao_info)
                price_data['newYanBaoInfo'] = new_yan_bao_info

            # 处理allColorSet
            all_color_set = price_data.get('allColorSet')
            if all_color_set is not None:
                all_color_set = json_2_dict(json_str=all_color_set)
                price_data['allColorSet'] = all_color_set

            # 处理allSpecSet
            all_spec_set = price_data.get('allSpecSet')
            if all_spec_set is not None:
                all_spec_set = json_2_dict(json_str=all_spec_set)
                price_data['allSpecSet'] = all_spec_set

            # 处理allSizeSet
            all_size_set = price_data.get('allSizeSet')
            if all_size_set is not None:
                all_size_set = json_2_dict(json_str=all_size_set)
                price_data['allSizeSet'] = all_size_set

            # pprint(price_data)
            if price_data.get('wareMainImageUrl') is not None:
                main_image_url = price_data.get('wareMainImageUrl')
            else:
                main_image_url = ''

            return [
                price_data.get('warePrice', ''),    # 价格
                main_image_url,                     # 主图地址
            ]

        else:
            # self.my_lg.error('获取到的price_data为空!')
            return []

    def _get_shop_name(self, data):
        '''
        获取shop_name
        :param data:
        :return:
        '''
        return data.get('shopInfo', {}).get('shop', {}).get('name', '') \
            if data.get('shopInfo', {}).get('shop') is not None \
            else ''

    def _get_detail_name_list(self, data):
        '''
        获取detail_name_list
        :param data:
        :return:
        '''
        detail_name_list = []
        color_size_title = data.get('skuColorSize', {}).get('colorSizeTitle', {})
        # pprint(data.get('skuColorSize', {}))
        # pprint(color_size_title)
        if color_size_title != {}:
            for key, value in color_size_title.items():
                img_here = 0
                if key == 'colorName':
                    if value is not None:
                        if value != '':         # 不为空则说明有图
                            img_here = 1

                detail_name_list.append({
                    'spec_name': value,
                    'img_here': img_here,
                })

        return detail_name_list

    def get_price_info_list(self, *params):
        '''
        得到规范的price_info_list
        :param *params:
        :return:
        '''
        goods_id = params[0]
        detail_name_list = params[1]
        data = params[2]
        # tmp_price_info_list = data.get('skuColorSize', {}).get('colorSize')
        # pprint(tmp_price_info_list)

        price_info_list = []
        if detail_name_list != []:  # 有规格
            tmp_price_info_list = data.get('skuColorSize', {}).get('colorSize')
            # pprint(tmp_price_info_list)
            if tmp_price_info_list is not None:
                for item in tmp_price_info_list:
                    tmp = {}
                    tmp_spec_value = []
                    if item.get('color') != '*':
                        tmp_spec_value.append(item.get('color'))

                    if item.get('size') != '*':
                        tmp_spec_value.append(item.get('size'))

                    if item.get('spec') != '*':
                        tmp_spec_value.append(item.get('spec'))

                    tmp_spec_value = '|'.join(tmp_spec_value)  # 具体规格
                    # self.my_lg.info(str(tmp_spec_value))

                    sku_id = item.get('skuId')
                    # 对每个sku_id就行一次请求，来获得对应sku_id的价格数据
                    if goods_id[0] == 0:
                        sku_id = [0, sku_id]
                    elif goods_id[0] == 1:
                        sku_id = [1, sku_id]
                    elif goods_id[0] == 2:
                        sku_id = [2, sku_id]
                    ware_price_and_main_img_url_list = self.from_ware_id_get_price_info(ware_id=sku_id)

                    tmp['spec_value'] = tmp_spec_value
                    if ware_price_and_main_img_url_list != []:
                        tmp['detail_price'] = ware_price_and_main_img_url_list[0]
                        tmp['img'] = ware_price_and_main_img_url_list[1]
                    else:
                        tmp['detail_price'] = ''
                        tmp['img'] = ''

                    tmp['rest_number'] = ''
                    if tmp.get('detail_price') is None:     # detail_price为None的跳过!
                        continue

                    price_info_list.append(tmp)
                    # pprint(price_info_list)

        return price_info_list

    def get_right_div_desc(self, data):
        '''
        得到处理后的div_desc
        :param data:
        :return:
        '''
        wdis = ''
        # 特殊处理script动态生成的
        if data.get('popWareDetailWebViewMap') is not None:
            if data.get('popWareDetailWebViewMap').get('cssContent') is not None:
                wdis = data.get('popWareDetailWebViewMap', {}).get('cssContent', '')
                wdis = self._wash_div_desc(wdis=wdis)

        wdis = wdis + data.get('wdis', '')  # 如果获取到script就与wdis重组
        div_desc = self._wash_div_desc(wdis=wdis)

        return div_desc

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

    def get_p_info(self, data):
        '''
        得到p_info
        :param data:
        :return: list
        '''
        tmp_p_info = data.get('wi', {}).get('code')
        # pprint(tmp_p_info)
        p_info = []
        if tmp_p_info is not None:
            if isinstance(tmp_p_info, str):
                p_info = [{'p_name': '规格和包装', 'p_value': tmp_p_info}]
            elif isinstance(tmp_p_info, list):
                for item in tmp_p_info:
                    tmp = {}
                    tmp['p_name'] = list(item.keys())[0]
                    tmp_p_value = list(item.values())[0]
                    tmp_p_value_2 = []
                    if isinstance(tmp_p_value, list):
                        for i in tmp_p_value:
                            tmp_2 = {}
                            tmp_2['name'] = list(i.keys())[0]
                            tmp_2['value'] = list(i.values())[0]
                            tmp_p_value_2.append(tmp_2)
                        tmp['p_value'] = tmp_p_value_2
                    else:
                        tmp['p_value'] = tmp_p_value

                    p_info.append(tmp)
            else:
                pass

        return p_info

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

        res = pipeline._update_table_2(sql_str=sql_str, params=params, logger=self.my_lg)

        return res

    def insert_into_jd_table(self, data, pipeline):
        site_id = self._from_jd_type_get_site_id_value(jd_type=data.get('jd_type'))
        if site_id == 0:
            self.my_lg.error('site_id获取异常, 请检查!')
            return False

        tmp = _get_right_model_data(data=data, site_id=site_id)

        self.my_lg.info('------>>>| 待存储的数据信息为:{0}'.format(tmp.get('goods_id')))

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
            self.my_lg.error('site_id获取异常, 请检查!')
            return False

        tmp = _get_right_model_data(data=data, site_id=site_id)
        self.my_lg.info('------>>>| 待存储的数据信息为: {0}'.format(tmp.get('goods_id')))

        params = self._get_db_insert_params(item=tmp)
        if tmp.get('main_goods_id') is not None:
            sql_str = jd_insert_str_1

        else:
            sql_str = jd_insert_str_2

        result = pipeline._insert_into_table_2(sql_str=sql_str, params=params, logger=self.my_lg)

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
            # item['price'],
            # item['taobao_price'],
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

    def _wash_url_body(self, body):
        '''
        清洗body
        :param body:
        :return:
        '''
        body = re.compile('\n|\t|  ').sub('', body)

        return body

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
            self.my_lg.info('------>>>| 得到的京东商品id为:{0}'.format(goods_id))
            return [0, goods_id]            # 0表示京东常规商品, 包括京东超市, 京东精选
        else:
            is_jd_hk_url = re.compile(r'https://item.jd.hk/.*?').findall(jd_url)
            if is_jd_hk_url != []:
                goods_id = re.compile(r'https://item.jd.hk/(.*?).html.*?').findall(jd_url)[0]
                self.my_lg.info('------>>>| 得到的京东全球购商品id为:{0}'.format(goods_id))
                return [1, goods_id]        # 1表示京东全球购商品
            else:
                is_yiyao_jd_url = re.compile(r'https://item.yiyaojd.com/.*?').findall(jd_url)
                if is_yiyao_jd_url != []:
                    goods_id = re.compile(r'https://item.yiyaojd.com/(.*?).html.*?').findall(jd_url)[0]
                    self.my_lg.info('------>>>| 得到的京东大药房商品id为:{}'.format(goods_id))
                    return [2, goods_id]    # 2表示京东大药房
                else:
                    self.my_lg.info('京东商品url错误, 非正规的url, 请参照格式(https://item.jd.com/)或者(https://item.jd.hk/)开头的...')
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
        # tmp_pc_body = Requests.get_url_body(url=tmp_pc_url, headers=self.pc_headers)
        tmp_pc_body = self.driver.use_phantomjs_to_get_url_body(url=tmp_pc_url, css_selector='div#spec-list ul.lh li img')  # 该css为示例图片
        # self.my_lg.info(str(tmp_pc_body))
        if tmp_pc_body == '':
            self.my_lg.info('#### 获取该商品的无水印示例图片失败! 导致原因: tmp_pc_body为空str!')
            all_img_url = []
        else:
            try:
                all_img_url = list(Selector(text=tmp_pc_body).css('div#spec-list ul.lh li img::attr("src")').extract())
                if all_img_url != []:
                    all_img_url = ['https:' + item_img_url for item_img_url in all_img_url if re.compile(r'^http').findall(item_img_url) == []]
                    all_img_url = [re.compile(r'/n5.*?jfs/').sub('/n1/jfs/', item_img_url) for item_img_url in all_img_url]
                    all_img_url = [{
                        'img_url': item_img_url,
                    } for item_img_url in all_img_url]
                else:
                    all_img_url = []
            except Exception as e:
                self.my_lg.error('获取商品pc版无水印示例图片时出错: ', e)
                all_img_url = []

        return all_img_url

    def __del__(self):
        try:
            del self.driver
            del self.my_lg
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    jd = JdParse()
    while True:
        jd_url = input('请输入待爬取的京东商品地址: ')
        jd_url.strip('\n').strip(';')
        goods_id = jd.get_goods_id_from_url(jd_url)
        jd.get_goods_data(goods_id=goods_id)
        data = jd.deal_with_data(goods_id=goods_id)
        pprint(data)
        