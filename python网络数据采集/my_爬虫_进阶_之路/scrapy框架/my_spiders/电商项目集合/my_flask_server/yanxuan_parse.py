# coding:utf-8

'''
@author = super_fazai
@File    : yanxuan_parse.py
@Time    : 2018/8/6 09:40
@connect : superonesfazai@gmail.com
'''

"""
网易严选m站抓取
"""

import gc
import re
from pprint import pprint
from logging import (
    INFO,
    ERROR,
)
from json import dumps
from settings import (
    PHANTOMJS_DRIVER_PATH,
    MY_SPIDER_LOGS_PATH,)

# from fzutils.spider.fz_requests import MyRequests
from fzutils.spider.fz_phantomjs import MyPhantomjs
from fzutils.common_utils import (
    json_2_dict,
    wash_sensitive_info,)
from fzutils.data.json_utils import nonstandard_json_str_handle
from fzutils.log_utils import set_logger
from fzutils.internet_utils import (
    get_random_phone_ua,
    _get_url_contain_params,)
from fzutils.cp_utils import _get_right_model_data
from fzutils.time_utils import (
    get_shanghai_time,
    datetime_to_timestamp,
    timestamp_to_regulartime,
    string_to_datetime,)
from fzutils.data.list_utils import unique_list_and_keep_original_order

class YanXuanParse(object):
    def __init__(self, logger=None):
        super(YanXuanParse, self).__init__()
        self.result_data = {}
        self._set_logger(logger)
        self._set_headers()
        self.my_phantomjs = MyPhantomjs(executable_path=PHANTOMJS_DRIVER_PATH, logger=self.my_lg)

    def _set_logger(self, logger):
        if logger is None:
            self.my_lg = set_logger(
                log_file_name=MY_SPIDER_LOGS_PATH + '/网易严选/_/' + str(get_shanghai_time())[0:10] + '.txt',
                console_log_level=INFO,
                file_log_level=ERROR
            )
        else:
            self.my_lg = logger

    def _set_headers(self):
        self.headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_phone_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

    def _get_goods_data(self, goods_id):
        '''
        得到需求数据
        :param goods_id:
        :return:
        '''
        if goods_id == '':
            self.my_lg.error('获取到的goods_id为空值!此处跳过!')
            return self._get_data_error_init()

        # 网易严选m站抓取
        url = 'http://m.you.163.com/item/detail'
        params = self._get_params(goods_id=goods_id)

        m_url = url + '?id={0}'.format(goods_id)
        self.my_lg.info('------>>>| 正在抓取严选地址为: {0}'.format(m_url))

        write_info = '出错goods_id:{0}, 出错地址: {1}'.format(goods_id, m_url)

        '''requests被无限转发'''
        # body = MyRequests.get_url_body(url=url, headers=self.headers, params=params)
        # self.my_lg.info(str(body))

        '''改用phantomjs'''
        body = self.my_phantomjs.use_phantomjs_to_get_url_body(url=_get_url_contain_params(url=url, params=params))
        if body == '':
            self.my_lg.error('获取到的body为空值!'+write_info)
            return self._get_data_error_init()

        try:
            body = re.compile('var jsonData=(.*?),policyList=').findall(body)[0]
        except IndexError:
            self.my_lg.error('获取body时索引异常!'+write_info, exc_info=True)
            return self._get_data_error_init()

        body = nonstandard_json_str_handle(json_str=body)
        # self.my_lg.info(str(body))
        _ = json_2_dict(
            json_str=body, logger=self.my_lg)
        # pprint(_)
        if _ == {}:
            self.my_lg.error('获取到的data为空dict!'+write_info)
            return self._get_data_error_init()

        _ = self._wash_data(_)
        data = {}
        try:
            data['title'] = self._wash_sensitive_info(self._get_title(data=_))
            data['sub_title'] = self._wash_sensitive_info(self._get_sub_title(data=_))
            data['shop_name'] = ''
            data['all_img_url'] = self._get_all_img_url(data=_)
            data['p_info'] = self._get_p_info(data=_)
            data['div_desc'] = self._get_div_desc(data=_)
            data['sell_time'] = self._get_sell_time(data=_)
            data['detail_name_list'] = self._get_detail_name_list(data=_.get('skuSpecList', []))
            data['price_info_list'] = self._get_price_info_list(data=_.get('skuList', []))
            data['price'], data['taobao_price'] = self._get_price_and_taobao_price(
                price_info_list=data['price_info_list']
            )
            if data['price'] == 0 or data['taobao_price'] == 0:     # 售罄商品处理
                data['is_delete'] = 1
            else:
                data['is_delete'] = self._get_is_delete(price_info_list=data['price_info_list'], data=data, other=_)

        except Exception:
            self.my_lg.error('遇到错误:', exc_info=True)
            self.my_lg.error(write_info)
            return self._get_data_error_init()

        if data != {}:
            self.result_data = data
            return data
        else:
            self.my_lg.info('data为空值')
            return self._get_data_error_init()

    def _deal_with_data(self):
        '''
        结构化数据
        :return:
        '''
        data = self.result_data
        if data != {}:
            # 店铺名称
            shop_name = data['shop_name']
            # 掌柜
            account = ''
            # 商品名称
            title = data['title']
            # 子标题
            sub_title = data['sub_title']

            # 商品标签属性名称
            detail_name_list = data['detail_name_list']

            # 要存储的每个标签对应规格的价格及其库存
            price_info_list = data['price_info_list']

            # 所有示例图片地址
            all_img_url = data['all_img_url']

            # 详细信息标签名对应属性
            p_info = data['p_info']
            # pprint(p_info)

            # div_desc
            div_desc = data['div_desc']

            is_delete = data['is_delete']

            # 上下架时间
            if data.get('sell_time', {}) != {}:
                schedule = [{
                    'begin_time': data.get('sell_time', {}).get('begin_time', ''),
                    'end_time': data.get('sell_time', {}).get('end_time', ''),
                }]
            else:
                schedule = []

            # 销售总量
            all_sell_count = ''

            # 商品价格和淘宝价
            price, taobao_price = data['price'], data['taobao_price']

            result = {
                'shop_name': shop_name,                 # 店铺名称
                'account': account,                     # 掌柜
                'title': title,                         # 商品名称
                'sub_title': sub_title,                 # 子标题
                'price': price,                         # 商品价格
                'taobao_price': taobao_price,           # 淘宝价
                # 'goods_stock': goods_stock,               # 商品库存
                'detail_name_list': detail_name_list,   # 商品标签属性名称
                # 'detail_value_list': detail_value_list,   # 商品标签属性对应的值
                'price_info_list': price_info_list,     # 要存储的每个标签对应规格的价格及其库存
                'all_img_url': all_img_url,             # 所有示例图片地址
                'p_info': p_info,                       # 详细信息标签名对应属性
                'div_desc': div_desc,                   # div_desc
                'schedule': schedule,                   # 商品特价销售时间段
                'all_sell_count': all_sell_count,       # 销售总量
                'is_delete': is_delete                  # 是否下架
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
            self.result_data = {}
            return result

        else:
            self.my_lg.error('待处理的data为空的dict, 该商品可能已经转移或者下架')

            return self._get_data_error_init()

    def to_right_and_update_data(self, data, pipeline):
        '''
        实时更新数据
        :param data:
        :param pipeline:
        :return:
        '''
        tmp = _get_right_model_data(data, site_id=30, logger=self.my_lg)

        params = self._get_db_update_params(item=tmp)
        base_sql_str = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, {0} {1} where GoodsID = %s'
        if tmp['delete_time'] == '':
            sql_str = base_sql_str.format('shelf_time=%s', '')
        elif tmp['shelf_time'] == '':
            sql_str = base_sql_str.format('delete_time=%s', '')
        else:
            sql_str = base_sql_str.format('shelf_time=%s,', 'delete_time=%s')

        pipeline._update_table_2(sql_str=sql_str, params=params, logger=self.my_lg)

    def _get_db_update_params(self, item):
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

    def _wash_sensitive_info(self, target_str):
        '''
        清洗敏感信息
        :param target_str:
        :return:
        '''
        add_sensitive_str_list = [
            '网易',
            '严选',
            '云音乐',
        ]
        target_str = wash_sensitive_info(data=target_str, replace_str_list=[], add_sensitive_str_list=add_sensitive_str_list)

        return target_str

    def _get_title(self, data):
        title = data.get('name', '')
        assert title != '', '获取到的name为空值!请检查!'

        return title

    def _get_sub_title(self, data):
        sub_title = data.get('simpleDesc', '')  # 可以为空

        return sub_title

    def _get_all_img_url(self, data):
        tmp = data.get('itemDetail', {})
        first_img_url = data.get('listPicUrl', '')
        assert tmp != {}, '获取到的all_img_url为空dict！'

        all_img_url = [{
            'img_url': first_img_url
        }] if first_img_url != '' else []
        for key, value in tmp.items():
            if re.compile('picUrl').findall(key) != []:
                all_img_url.append({
                    'img_url': value,
                })

        return all_img_url

    def _get_p_info(self, data):
        p_info = [{
            'p_name': item.get('attrName', ''),
            'p_value': self._wash_sensitive_info(item.get('attrValue', '')),
        } for item in data.get('attrList', [])]

        return p_info

    def _get_div_desc(self, data):
        div_desc = data.get('itemDetail', {}).get('detailHtml', '')
        assert div_desc != '', '获取到的div_desc为空值!请检查!'
        # self.my_lg.info(str(div_desc))

        div_desc = self._wash_div_desc(div_desc)
        # print(div_desc)

        return div_desc

    def _wash_div_desc(self, div_desc):
        '''
        清洗div_desc
        :param div_desc:
        :return:
        '''
        # 方案1: 过滤不充分
        # filter = '''
        # _src=\".*?\"|
        # http://yanxuan.nosdn.127.net/e5f0f6b40368d7e532ff6b3a6481e6ab.jpg|
        # http://yanxuan.nosdn.127.net/c56658fa7b0b8a38bdb9c292a68fb176.jpg
        # '''.replace('\n', '').replace(' ', '')
        #
        # div_desc = re.compile(filter).sub('', div_desc)
        #
        # # 因为前面的严选声明照片地址是hash值, 每次都变
        # # 所以所有div_desc统一洗去前4张
        # div_desc = re.compile('<img.*?/>').sub('', div_desc, count=4)

        # 方案2:
        img_list = unique_list_and_keep_original_order(re.compile('src=\"(.*?)\"').findall(div_desc))
        # pprint(img_list)
        _ = ''
        for item in img_list[3:-2:]:
            _ += '<p><img src="{0}" style=""/></p>'.format(item)
        div_desc = _

        return div_desc

    def _get_sell_time(self, data):
        '''
        得到上下架时间
        :param data:
        :return:
        '''
        try:
            left_time = data.get('gradientPrice', {}).get('leftTime', 0)
        except AttributeError:  # gradientPrice的值可能为''
            return {}

        if left_time == 0:
            return {}

        now_time_timestamp = datetime_to_timestamp(get_shanghai_time())
        sell_time = {
            'begin_time': timestamp_to_regulartime(now_time_timestamp),
            'end_time': timestamp_to_regulartime(now_time_timestamp + left_time),
        }

        return sell_time

    def _get_detail_name_list(self, data):
        detail_name_list = []
        for item in data:
            if item.get('name') is None:
                return []
            else:
                detail_name_list.append({
                    'spec_name': item.get('name')
                })

        return detail_name_list

    def _get_price_info_list(self, data):
        '''
        得到price_info_list
        :param data:
        :return:
        '''
        price_info_list = []
        # pprint(data)
        for item in data:
            itemSkuSpecValueList = item.get('itemSkuSpecValueList', [])
            # pprint(itemSkuSpecValueList)
            spec_value_list = [i.get('skuSpecValue', {}).get('value', '') for i in itemSkuSpecValueList]
            spec_value = '|'.join(spec_value_list)
            img_url = item.get('pic', '')    # 默认为空
            if item.get('promotionDesc', '') == '新人专享价':    # 新人专享价处理为原价
                detail_price = str(item.get('calcPrice', ''))
            else:
                detail_price = str(item.get('retailPrice', ''))          # 零售价
            normal_price = str(item.get('counterPrice', ''))         # 市场价
            account_limit_buy_count = 5
            rest_number = item.get('sellVolume', 0)        # 官方接口没有规格库存信息, 此处默认为20
            if rest_number == 0:
                continue

            price_info_list.append({
                'spec_value': spec_value,
                'img_url': img_url,
                'detail_price': detail_price,
                'normal_price': normal_price,
                'account_limit_buy_count': account_limit_buy_count,
                'rest_number': rest_number,
            })

        return price_info_list

    def _get_price_and_taobao_price(self, price_info_list):
        # pprint(price_info_list)
        if price_info_list == []:   # 售罄商品处理
            return 0, 0

        try:
            tmp_price_list = sorted([round(float(item.get('detail_price', '')), 2) for item in price_info_list])
            price = tmp_price_list[-1]  # 商品价格
            taobao_price = tmp_price_list[0]  # 淘宝价
        except IndexError:
            raise IndexError('获取price, taobao_price时索引异常!请检查!')

        return price, taobao_price

    def _get_is_delete(self, price_info_list, data, other):
        is_delete = 0
        all_rest_number = 0
        if price_info_list != []:
            for item in price_info_list:
                all_rest_number += item.get('rest_number', 0)
            if all_rest_number == 0:
                is_delete = 1
        else:
            is_delete = 1

        # 当官方下架时间< 当前时间戳 则商品已下架 is_delete = 1
        if data['sell_time'] != {}:
            end_time = datetime_to_timestamp(string_to_datetime(data.get('sell_time', {}).get('end_time', '')))
            if end_time < datetime_to_timestamp(get_shanghai_time()):
                self.my_lg.info('该商品已经过期下架...! 进行逻辑删除 is_delete=1')
                is_delete = 1
            # print(is_delete)

        if other.get('soldOut'):    # True or False
            is_delete = 1

        return is_delete

    def _get_data_error_init(self):
        '''
        获取或者失败处理
        :return:
        '''
        self.result_data = {}

        return {}

    def _get_params(self, goods_id):
        params = (
            ('id', goods_id),
        )

        return params

    def _wash_data(self, data):
        '''
        清洗无用数据
        :param data:
        :return:
        '''
        try:
            data['comments'] = []
            data['issueList'] = []
        except:
            pass

        return data

    def get_goods_id_from_url(self, yanxuan_url):
        '''
        得到goods_id
        :param yanxuan_url:
        :return: goods_id
        '''
        # http://you.163.com/item/detail?id=1130056&_stat_area=mod_1_item_1&_stat_id=1005000&_stat_referer=itemList
        is_yanxuan_url = re.compile(r'you.163.com/item/detail.*?').findall(yanxuan_url)
        if is_yanxuan_url != []:
            if re.compile(r'id=(\d+)').findall(yanxuan_url) != []:
                goods_id = re.compile(r'id=(\d+)').findall(yanxuan_url)[0]
                self.my_lg.info('------>>>| 得到的严选商品的goods_id为: {0}'.format(goods_id))
                return goods_id
        else:
            self.my_lg.info('网易严选商品url错误, 非正规的url, 请参照格式(https://you.163.com/item/detail)开头的...')
            return ''

    def __del__(self):
        try:
            del self.my_phantomjs
            del self.my_lg
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    yanxuan = YanXuanParse()
    while True:
        kaola_url = input('请输入待爬取的严选商品地址: ')
        kaola_url.strip('\n').strip(';')
        goods_id = yanxuan.get_goods_id_from_url(kaola_url)
        yanxuan._get_goods_data(goods_id=goods_id)
        data = yanxuan._deal_with_data()
        # pprint(data)