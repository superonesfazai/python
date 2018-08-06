# coding:utf-8

'''
@author = super_fazai
@File    : kaola_parse.py
@Time    : 2018/7/27 14:18
@connect : superonesfazai@gmail.com
'''

"""
网易考拉pc站抓取, m站p_info信息不全(不采用)
"""

import re
import gc
from logging import (
    INFO,
    ERROR,
)
from pprint import pprint
from json import dumps

from settings import (
    PHANTOMJS_DRIVER_PATH,
    MY_SPIDER_LOGS_PATH,)

from fzutils.cp_utils import _get_right_model_data
from fzutils.spider.fz_requests import MyRequests
# from fzutils.spider.fz_phantomjs import MyPhantomjs
from fzutils.common_utils import (
    json_2_dict,
    get_random_int_number,)
from fzutils.internet_utils import (
    get_random_phone_ua,
    get_random_pc_ua,)
from fzutils.log_utils import set_logger
from fzutils.time_utils import (
    get_shanghai_time,
    datetime_to_timestamp,
    timestamp_to_regulartime,
    string_to_datetime,
)

class KaoLaParse(object):
    def __init__(self, logger=None):
        super(KaoLaParse, self).__init__()
        self.result_data = {}
        self._set_logger(logger)
        self._set_headers()

    def _set_headers(self):
        self.headers = {
            # 'cookie': 'davisit=2; usertrack=O2+g2Ftatitk7YwIAwY2Ag==; _ntes_nnid=7732365205c88dc47486ad1208406e7e,1532671534874; _ga=GA1.2.960357080.1532671535; _gid=GA1.2.1543960295.1532671535; JSESSIONID-WKL-8IO=JpPe0U2ISOSX%2B7b86uwx%2FDCCROKOxwv%2B9vh7Yj%2BBTVVOOIQXHVnSAe19xxMrURx2OK5Q6PV1E%2FSR5UOnm%5C0U2i1RDD3ur5uh%2F7lHemHDcbf90BrkXSqTqZySf%2F%5CWgGSu81cjbESgntQrE%2FYJU89hyhg%5CtPZ6jYgVrxw3yil6BxlEonas%3A1532757935029; _klhtxd_=31; kaola_user_key=47cca4d0-57c9-41ca-ae67-2172c4a81500; KAOLA_NEW_USER_COOKIE=yes; __da_ntes_utma=2525167.1705273738.1532671535.1532671535.1532671535.1; davisit=1; __da_ntes_utmb=2525167.1.10.1532671535; __da_ntes_utmz=2525167.1532671535.1.1.utmcsr%3D(direct)%7Cutmccn%3D(direct)%7Cutmcmd%3D(none); __da_ntes_utmfc=utmcsr%3D(direct)%7Cutmccn%3D(direct)%7Cutmcmd%3D(none); _jzqa=1.658432386831847000.1532671536.1532671536.1532671536.1; _jzqc=1; _jzqx=1.1532671536.1532671536.1.jzqsr=google%2Ecom|jzqct=/.-; _jzqckmp=1; WM_TID=BuJzWuW25WT9h9YnJbNPwKuHb0%2FJdiEw; __kaola_usertrack=20180727140634933960; _da_ntes_uid=20180727140634933960; NTES_KAOLA_ADDRESS_CONTROL=330000|330100|330102|1; _jzqb=1.8.10.1532671536.1; NTES_KAOLA_RV=1472242_1532671698324_0|27979_1532671614705_0; _gat=1',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_phone_ua(),
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            # 'referer': 'https://m-goods.kaola.com/product/27979.html?ri=navigation&from=page1&zn=result&zp=page1-5&position=5&istext=0&srId=7891cc6632688f65bdcb4f04e150950c&isMarketPriceShow=true&hcAntiCheatSwitch=0&anstipamActiCheatSwitch=1&anstipamActiCheatToken=de3223456456fa2e3324354u4567lt&anstipamActiCheatValidate=anstipam_acti_default_validate',
            'authority': 'm-goods.kaola.com',
            'x-requested-with': 'XMLHttpRequest',
        }

    def _set_logger(self, logger):
        if logger is None:
            self.my_lg = set_logger(
                log_file_name=MY_SPIDER_LOGS_PATH + '/网易考拉/_/' + str(get_shanghai_time())[0:10] + '.txt',
                console_log_level=INFO,
                file_log_level=ERROR
            )
        else:
            self.my_lg = logger

    def _get_pc_sku_info_headers(self):
        return {
            # 'cookie': "davisit=133; usertrack=O2+g2Ftatitk7YwIAwY2Ag==; _ntes_nnid=7732365205c88dc47486ad1208406e7e,1532671534874; _ga=GA1.2.960357080.1532671535; _gid=GA1.2.1543960295.1532671535; _klhtxd_=31; kaola_user_key=47cca4d0-57c9-41ca-ae67-2172c4a81500; __da_ntes_utma=2525167.1705273738.1532671535.1532671535.1532671535.1; davisit=1; __da_ntes_utmz=2525167.1532671535.1.1.utmcsr%3D(direct)%7Cutmccn%3D(direct)%7Cutmcmd%3D(none); __da_ntes_utmfc=utmcsr%3D(direct)%7Cutmccn%3D(direct)%7Cutmcmd%3D(none); _jzqc=1; WM_TID=BuJzWuW25WT9h9YnJbNPwKuHb0%2FJdiEw; __kaola_usertrack=20180727140634933960; _da_ntes_uid=20180727140634933960; _ga=GA1.3.960357080.1532671535; KAOLA_NEW_USER_COOKIE=no; _gid=GA1.3.1543960295.1532671535; _kaola_user_beta_traffic=11900565161; NETEASE_WDA_UID=\"ojk_rue0z670a55c0640959dc5053c7bab711ceab3@wx.163.com#|#1494121379042\"; S_INFO=1533005764|0|##|ojk_rue0z670a55c0640959dc5053c7bab711ceab3@wx.163.com; P_INFO=ojk_rue0z670a55c0640959dc5053c7bab711ceab3@wx.163.com|1533005764|0|kaola|00&99|null#0|null|kaola|ojk_rue0z670a55c0640959dc5053c7bab711ceab3@wx.163.com; NTES_OSESS=yYsn9MHD7G6TaLObUuWLbAz1ON8RoRfBZWUrWt7ORjAoWWhz6L9pI2UdlONyjpcbXvEjUTUQ3xmiHvJRReaDb2QTGF3XbGkuwkwoFcQ3ao1h4vbxvjk_SepopEgeUc_Pf6ZCSGQMSqhvzBLCfajZ37DH0_ECJb0bZn3alkCujGl95Ahlw5L7emqExM3GFwnw5u_ukogIaAhvj9NVmayKH8Y.wDj6Bz9Wy6ny48S4TB859; _ntes_nuid=c199afa0a5f0b5a2869b8cf66c6be415; _qzjc=1; davisit=2; NTES_KAOLA_ORDER_FLAG_NEW=-1533432028; JSESSIONID-WKL-8IO=zmtn3E1vXCr4M%5C%5Cmw7zWBwH%2B596vBzoqQRnzDgY%5CpIOn3DUZTp1LWf%5CsXXf7EI4o5D%2BDtY9BOeKcOlyxZ7yxrBmH9O6b7sRaNBgSWHLby224bWjd%5CnlVkUe9BWOsBfWviE5jcOr8Jf5iMngMw2SW9yM%2Fh7M1Wq6k0Sap6lzRgZAUeLx%2F%3A1533099535404; NTES_KAOLA_ADDRESS_CONTROL=330000|330100|330102|1; __da_ntes_utmb=2525167.1.10.1533086704; _jzqa=1.658432386831847000.1532671536.1533054637.1533086706.23; _jzqx=1.1532671536.1533086706.6.jzqsr=google%2Ecom|jzqct=/.jzqsr=kaola%2Ecom|jzqct=/; _jzqckmp=1; _qzja=1.171255260.1532671601817.1533008724580.1533086710431.1533086734453.1533086755814..0.0.28.9; _qzjb=1.1533086710431.4.0.0.0; _qzjto=4.1.0; _jzqb=1.9.10.1533086706.1; NTES_KAOLA_RV=16029_1533086756435_0|1917464_1533086735090_0|17992_1533086721244_0|27757_1533086711248_0|2066692_1533008725460_0|1453977_1533006382331_0|1351750_1533006337428_0|27979_1532939381249_0|2059765_1532939045569_0|2268339_1532938432179_0|2254882_1532938240407_0|2208483_1532930588764_0|1330333_1532918029707_0|1472242_1532671698324_0",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.9",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            'content-type': "application/x-www-form-urlencoded",
            'accept': "*/*",
            # 'referer': "https://goods.kaola.com/product/16029.html?ri=navigation&from=page1&zn=result&zp=page1-20&position=20&istext=0&srId=8ef2e561233225619e300ebc5782c129&isMarketPriceShow=true&hcAntiCheatSwitch=0&anstipamActiCheatSwitch=1&anstipamActiCheatToken=de3223456456fa2e3324354u4567lt&anstipamActiCheatValidate=anstipam_acti_default_validate",
            'authority': "goods.kaola.com",
            'x-requested-with': "XMLHttpRequest",
            'Cache-Control': "no-cache",
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

        # 网易考拉pc站抓取, m站p_info信息不全(不采用)
        # phone_body(requests设置代理一直302无限重定向, 于是phantomjs)
        # body = self.my_phantomjs.use_phantomjs_to_get_url_body(url=url)

        url = 'https://goods.kaola.com/product/{0}.html'.format(goods_id)
        self.my_lg.info('------>>>| 正在抓取考拉地址为: {0}'.format(url))

        body = self._get_pc_goods_body(url=url, goods_id=goods_id)
        # self.my_lg.info(body)
        if body == '':
            return self._get_data_error_init()

        # _ = self._get_right_body(body)    # phone端
        _ = self._get_pc_right_body(body)   # pc端
        # pprint(_)
        if _ == {}:
            self.my_lg.error('获取body时索引异常!出错goods_id为:{0}, 出错地址: {1}'.format(goods_id, url))
            return self._get_data_error_init()

        else:
            # TODO 获取m站的sku_info(但是没有税费)
            # sku_info_url = 'https://m-goods.kaola.com/product/getWapGoodsDetailDynamic.json'
            # params = self._get_params(goods_id=goods_id)
            # body = MyRequests.get_url_body(url=sku_info_url, headers=self.headers, params=params)

            # 获取pc站的sku_info
            sku_info_url = 'https://goods.kaola.com/product/getPcGoodsDetailDynamic.json'
            params = self._get_pc_sku_info_params(goods_id=goods_id)
            body = MyRequests.get_url_body(
                url=sku_info_url,
                headers=self._get_pc_sku_info_headers(),
                params=params)

            sku_info = json_2_dict(json_str=body, logger=self.my_lg).get('data')
            if sku_info is None:
                self.my_lg.error('获取到we的sku_info为None!出错goods_id: {0}, 出错地址: {1}'.format(goods_id, url))
            _['sku_info'] = sku_info
            # pprint(_)

        _ = self._wash_data(_)
        # pprint(_)

        data = {}
        try:
            # title, sub_title
            data['title'] = self._get_title(data=_)
            data['sub_title'] = ''
            data['shop_name'] = _.get('goodsInfoBase', {}).get('brandName', '')
            data['all_img_url'] = self._get_all_img_url(data=_)
            data['p_info'] = self._get_p_info(data=_)
            data['div_desc'] = self._get_div_desc(data=_)
            data['sell_time'] = self._get_sell_time(data=_.get('sku_info', {}))
            data['detail_name_list'] = self._get_detail_name_list(data=_.get('sku_info', {}).get('skuDetailList', []))
            # TODO 网易考拉官方有bug, 实际规格没货的商品, 前端还在卖, 估计是下单后再去订货, 库存0: 我这边就处理为下架
            # data['price_info_list'] = self._get_sku_info(data=_.get('sku_info', {}).get('skuDetailList', []))
            '''获取pc端的, 价格为算上税费的'''
            data['price_info_list'] = self._get_pc_sku_info(data=_.get('sku_info', {}).get('skuDetailList', []))

            data['price'], data['taobao_price'] = self._get_price_and_taobao_price(
                data=_.get('sku_info', {}).get('skuPrice', {}),
                price_info_list = data['price_info_list']
            )
            data['is_delete'] = self._get_is_delete(price_info_list=data['price_info_list'], data=data, other=_)

        except Exception:
            self.my_lg.error('遇到错误:', exc_info=True)
            self.my_lg.error('出错goods_id: {0}, 地址: {1}'.format(goods_id, url))
            return self._get_data_error_init()

        if data != {}:
            self.result_data = data
            return data
        else:
            self.my_lg.info('data为空值')
            return self._get_data_error_init()

    def _deal_with_data(self):
        '''
        处理得到需求data
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
                'shop_name': shop_name,                     # 店铺名称
                'account': account,                         # 掌柜
                'title': title,                             # 商品名称
                'sub_title': sub_title,                     # 子标题
                'price': price,                             # 商品价格
                'taobao_price': taobao_price,               # 淘宝价
                # 'goods_stock': goods_stock,               # 商品库存
                'detail_name_list': detail_name_list,       # 商品标签属性名称
                # 'detail_value_list': detail_value_list,   # 商品标签属性对应的值
                'price_info_list': price_info_list,         # 要存储的每个标签对应规格的价格及其库存
                'all_img_url': all_img_url,                 # 所有示例图片地址
                'p_info': p_info,                           # 详细信息标签名对应属性
                'div_desc': div_desc,                       # div_desc
                'schedule': schedule,                       # 商品特价销售时间段
                'all_sell_count': all_sell_count,           # 销售总量
                'is_delete': is_delete                      # 是否下架
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
        tmp = _get_right_model_data(data, site_id=29, logger=self.my_lg)

        params = self._get_db_update_params(item=tmp)
        if tmp['delete_time'] == '':
            sql_str = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, shelf_time=%s where GoodsID = %s'
        elif tmp['shelf_time'] == '':
            sql_str = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, delete_time=%s where GoodsID = %s'
        else:
            sql_str = 'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, IsDelete=%s, IsPriceChange=%s, PriceChangeInfo=%s, shelf_time=%s, delete_time=%s where GoodsID = %s'

        pipeline._update_table_2(sql_str=sql_str, params=params, logger=self.my_lg)

    def _get_db_update_params(self, item):
        '''
        得到db待更新的params
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

    def _get_pc_goods_body(self, url, goods_id):
        '''
        得到pc端商品的body
        :param goods_id:
        :return:
        '''
        headers = {
            'authority': 'goods.kaola.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_pc_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'cookie': 'davisit=39; usertrack=O2+g2Ftatitk7YwIAwY2Ag==; _ntes_nnid=7732365205c88dc47486ad1208406e7e,1532671534874; _ga=GA1.2.960357080.1532671535; _gid=GA1.2.1543960295.1532671535; _klhtxd_=31; kaola_user_key=47cca4d0-57c9-41ca-ae67-2172c4a81500; __da_ntes_utma=2525167.1705273738.1532671535.1532671535.1532671535.1; davisit=1; __da_ntes_utmz=2525167.1532671535.1.1.utmcsr%3D(direct)%7Cutmccn%3D(direct)%7Cutmcmd%3D(none); __da_ntes_utmfc=utmcsr%3D(direct)%7Cutmccn%3D(direct)%7Cutmcmd%3D(none); _jzqc=1; WM_TID=BuJzWuW25WT9h9YnJbNPwKuHb0%2FJdiEw; __kaola_usertrack=20180727140634933960; _da_ntes_uid=20180727140634933960; NTES_KAOLA_ADDRESS_CONTROL=330000|330100|330102|1; _qzjc=1; _ga=GA1.3.960357080.1532671535; KAOLA_NEW_USER_COOKIE=no; JSESSIONID-WKL-8IO=Ej0upUk4%2BoTwIaESuhWSdrP8LjGjGKPjy%5CzIHKVwWYJVzUbwkZTvIHZZ2oVgK9ZtzWBis36RUCxcfMMr793Xhr%2FSsY%2Br23bCIsjP%2F1bmz05eUdBpClLvMDOX%5CXC%5C4Chn2a6VZ%2FwA4VITIfWMWfpIO2CBt1YfXDpi0a7q2r6pvsE3SihO%3A1532930915344; _jzqckmp=1; _jzqx=1.1532671536.1532917914.2.jzqsr=google%2Ecom|jzqct=/.jzqsr=kaola%2Ecom|jzqct=/; _gid=GA1.3.1543960295.1532671535; _qzja=1.171255260.1532671601817.1532671601817.1532917917322.1532917929092.1532918028838..0.0.7.2; _qzjto=3.1.0; NTES_KAOLA_RV=1330333_1532918029707_0|27757_1532917929047_0|27979_1532672800324_0|1472242_1532671698324_0; _jzqa=1.658432386831847000.1532671536.1532917914.1532923346.10; __da_ntes_utmb=2525167.1.10.1532917929',
        }

        params = (
            ('ri', 'navigation'),
            ('from', 'page1'),
            ('zn', 'result'),
            ('zp', 'page1-0'),
            ('position', '0'),
            ('istext', '0'),
            # ('srId', '8bd1e06482b5730be802f6ce6f56dacf'),
            ('isMarketPriceShow', 'true'),
            ('hcAntiCheatSwitch', '0'),
            ('anstipamActiCheatSwitch', '1'),
            # ('anstipamActiCheatToken', 'de3223456456fa2e3324354u4567lt'),
            # ('anstipamActiCheatValidate', 'anstipam_acti_default_validate'),
        )

        body = MyRequests.get_url_body(url=url, headers=headers, params=params)
        # print(body)

        return body

    def _get_title(self, data):
        title = data.get('goodsInfoBase', {}).get('title', '')
        assert title != '', '获取到的title为空值!请检查!'

        return title

    def _get_all_img_url(self, data):
        '''
        得到all_img_url
        :param data:
        :return:
        '''
        # all_img_url
        all_img_url = data.get('goodsInfoBase', {}).get('webImageList', [])
        assert all_img_url != [], '获取到的all_img_url为空list!请检查!'
        all_img_url = [{
            'img_url': self._get_right_img_url(item.get('imageUrl', '')),
        } for item in all_img_url]
        # pprint(all_img_url)

        return all_img_url

    def _get_right_img_url(self, img_url):
        '''
        得到正确显示的地址
        :param img_url:
        :return:
        '''
        if img_url != '' and re.compile('\?').findall(img_url) == []:
            return img_url + '?imageView&thumbnail=800x0&quality=85'
        else:
            return img_url

    def _get_p_info(self, data):
        '''
        得到p_info
        :param data:
        :return:
        '''
        p_info = data.get('goodsDetailContent', {}).get('goodsPropertyList', [])
        assert p_info != [], '获取到的p_info为空list!请检查!'
        _ = []
        for item in p_info:
            tmp = {}
            tmp['p_name'] = item.get('propertyName', '')
            p_value_list = item.get('goodsPropertyValueList', [])
            p_value_str = ' '.join([str(i.get('propertyValue', '')) for i in p_value_list])
            tmp['p_value'] = p_value_str
            _.append(tmp)

        return _

    def _get_div_desc(self, data):
        '''
        获取div_desc
        :param data:
        :return:
        '''
        div_desc = data.get('goodsDetailContent', {}).get('detail', '')
        assert div_desc != '', '获取到的div_desc为空值!请检查!'

        div_desc = re.compile(r'&amp;').sub('&', div_desc)
        div_desc = div_desc.replace('\n', '').replace('<img src="//', '<img src="http://')

        # 清洗 考拉退货声明, 以及其他声明
        filter_str = '''
        http://haitao.nos.netease.com/08cb6647415e4295ac7d53a89d6ecfcb1529465797598jimkg2cd20256.jpg\?imageView&quality=98&crop=0_8000_960_500|
        http://haitao.nos.netease.com/08cb6647415e4295ac7d53a89d6ecfcb1529465797598jimkg2cd20256.jpg\?imageView&quality=98&crop=0_8500_960_500|
        http://haitao.nos.netease.com/08cb6647415e4295ac7d53a89d6ecfcb1529465797598jimkg2cd20256.jpg\?imageView&quality=98&crop=0_9000_960_444|
        http://haitao.nos.netease.com/e33ab27fd90748f9b522687325c457b81524635537108jgeomthv10334.jpg\?imageView&quality=98&crop=0_0_750_500|
        http://haitao.nos.netease.com/e33ab27fd90748f9b522687325c457b81524635537108jgeomthv10334.jpg\?imageView&quality=98&crop=0_500_750_150|
        <video .*?>.*?</video>|
        '''.replace(' ', '').replace('\n', '')
        div_desc = re.compile(filter_str).sub('', div_desc)
        div_desc = re.compile('<a.*?>').sub('<a>', div_desc)

        return div_desc

    def _get_sell_time(self, data):
        '''
        得到上下架时间点
        :param data:
        :return:
        '''
        if data.get('temaiActivityInfo') is None:
            return {}

        start_time = data.get('temaiActivityInfo', {}).get('startTime', 0)
        rest_time = data.get('temaiActivityInfo', {}).get('nowToEndMs', 0)
        if start_time == 0:
            return {}
        else:
            start_time = int(str(start_time)[:10])
            end_time = start_time + rest_time

            return {
                'begin_time': timestamp_to_regulartime(start_time),
                'end_time': timestamp_to_regulartime(end_time),
            }

    def _get_detail_name_list(self, data):
        '''
        得到detail_name_list
        :param data:
        :return:
        '''
        detail_name_list = []

        # 第一个就可以拿出需求信息
        sku_property_list = data[0].get('skuInfo', {}).get('skuPropertyList', [])
        if sku_property_list == []:     # 无detail_name_list
            return []
        else:
            for i in sku_property_list:
                detail_name_list.append({
                    'spec_name': i.get('propertyName', ''),
                })

        return detail_name_list

    def _get_pc_sku_info(self, data):
        '''
        得到pc端的sku_info(价格都为常规价格, 非新人价格)
        :param data:
        :return:
        '''
        # pprint(data)
        price_info_list = []
        if len(data) == 1:  # 没有规格的处理
            tax_amount = data[0].get('skuTaxInfoPc', {}).get('taxAmount')               # 税费
            current_price = data[0].get('skuPrice', {}).get('currentPrice', 999999)     # 当前价格, 999999表示出错了
            market_price = data[0].get('skuPrice', {}).get('marketPrice', 999999)      # 市场价
            if current_price == 999999 or market_price == 999999:
                raise ValueError('获取到的current_price或market_price错误!请检查!')

            detail_price = str(current_price + tax_amount) if tax_amount is not None else str(current_price)
            normal_price = str(market_price + tax_amount) if tax_amount is not None else str(market_price)
            price_info_list.append({
                'spec_value': '',
                'detail_price': detail_price,
                'normal_price': normal_price,
                'img_url': '',
                'account_limit_buy_count': 5,
                'rest_number': data[0].get('skuStore', {}).get('currentStore', 0)
            })
        else:
            for item in data:
                sku_property_list = item.get('skuInfo', {}).get('skuPropertyList', [])
                spec_value = '|'.join([i.get('propertyValue', '') for i in sku_property_list])
                img_url = ''
                for i in sku_property_list:
                    tmp_img_url = i.get('imageUrl', '')
                    if tmp_img_url != '':
                        img_url = tmp_img_url

                tax_amount = item.get('skuTaxInfoPc', {}).get('taxAmount')              # 税费
                current_price = item.get('skuPrice', {}).get('currentPrice', 999999)    # 当前价格, 999999 raise error
                market_price = item.get('skuPrice', {}).get('marketPrice', 999999)      # 市场价
                if current_price == 999999 or market_price == 999999:
                    raise ValueError('获取到的current_price或market_price错误!请检查!')

                detail_price = str(current_price + tax_amount) if tax_amount is not None else str(current_price)
                normal_price = str(market_price + tax_amount) if tax_amount is not None else str(market_price)
                # 每个账户限购数量
                # account_limit_buy_count = item.get('skuLimitBuyInfo', {}).get('accountLimitBuyCount', 5)  # 出现0，就采用下面默认值的方式
                account_limit_buy_count = 5  # 默认为5
                rest_number = item.get('skuStore', {}).get('currentStore', 0)

                price_info_list.append({
                    'spec_value': spec_value,
                    'img_url': self._get_right_img_url(img_url),
                    'detail_price': detail_price,
                    'normal_price': normal_price,
                    'account_limit_buy_count': account_limit_buy_count,
                    'rest_number': rest_number,
                })

        return price_info_list

    def _get_sku_info(self, data):
        '''
        得到sku_info(每个规格对应的库存, 价格, 图片等详细信息)
        :param data:
        :return:
        '''
        # pprint(data)
        price_info_list = []
        if len(data) == 1:          # 没有规格的处理
            price_info_list.append({
                'spec_value': '',
                'detail_price': str(data[0].get('skuPrice', {}).get('currentPrice', '')),
                'normal_price': str(data[0].get('skuPrice', {}).get('marketPrice', '')),
                'img_url': '',
                'account_limit_buy_count': 5,
                'rest_number': data[0].get('skuStore', {}).get('currentStore', 0)
            })
        else:
            for item in data:
                sku_property_list = item.get('skuInfo', {}).get('skuPropertyList', [])
                spec_value = '|'.join([i.get('propertyValue', '') for i in sku_property_list])
                img_url = ''
                for i in sku_property_list:
                    tmp_img_url = i.get('imageUrl', '')
                    if tmp_img_url != '':
                        img_url = tmp_img_url

                normal_price = str(item.get('skuPrice', {}).get('marketPrice', ''))
                detail_price = str(item.get('skuPrice', {}).get('currentPrice', ''))
                # 每个账户限购数量
                # account_limit_buy_count = item.get('skuLimitBuyInfo', {}).get('accountLimitBuyCount', 5)  # 出现0，就采用下面默认值的方式
                account_limit_buy_count = 5     # 默认为5
                rest_number = item.get('skuStore', {}).get('currentStore', 0)

                price_info_list.append({
                    'spec_value': spec_value,
                    'img_url': self._get_right_img_url(img_url),
                    'detail_price': detail_price,
                    'normal_price': normal_price,
                    'account_limit_buy_count': account_limit_buy_count,
                    'rest_number': rest_number,
                })

        return price_info_list

    def _get_is_delete(self, price_info_list, data, other):
        '''
        获取is_delete
        :param price_info_list:
        :param data:
        :return:
        '''
        is_delete = 0
        all_rest_number = 0
        if price_info_list != []:
            for item in price_info_list:
                all_rest_number += item.get('rest_number', 0)
            if all_rest_number == 0:
                is_delete = 1

        # 当官方下架时间< 当前时间戳 则商品已下架 is_delete = 1
        if data['sell_time'] != {}:
            end_time = datetime_to_timestamp(string_to_datetime(data.get('sell_time', {}).get('end_time', '')))
            if end_time < datetime_to_timestamp(get_shanghai_time()):
                self.my_lg.info('该商品已经过期下架...! 进行逻辑删除 is_delete=1')
                is_delete = 1
            # print(is_delete)

        if not other.get('sku_info', {}).get('goodsStoreStatus', True):
            is_delete = 1

        return is_delete

    def _get_price_and_taobao_price(self, data, price_info_list):
        '''
        获取taobao_price, price
        :param data:
        :param price_info_list:
        :return:
        '''
        # pprint(price_info_list)
        try:
            tmp_price_list = sorted([round(float(item.get('detail_price', '')), 2) for item in price_info_list])
            price = tmp_price_list[-1]  # 商品价格
            taobao_price = tmp_price_list[0]  # 淘宝价
        except IndexError:
            raise IndexError('获取price, taobao_price时索引异常!请检查!')

        return price, taobao_price

    def _get_pc_right_body(self, body):
        '''
        处理pc端得到需求数据
        :param body:
        :return:
        '''
        try:
            body = re.compile(r'window.__kaolaHeadData = (.*?);</script>').findall(body)[0]

            goodsInfoBase = re.compile(r'goodsInfoBase: (.*?), //基本').findall(body)[0]
            goodsDetailContent = re.compile(r'goodsDetailContent: (.*?), //图文详情').findall(body)[0]
            kaolaSuperMarket = re.compile(r'kaolaSuperMarket: (.*?), //needSelfTag').findall(body)[0]

            # self.my_lg.info(str(body))
        except IndexError:
            self.my_lg.error('遇到错误:', exc_info=True)
            return {}

        _ = {}
        _['goodsInfoBase'] = json_2_dict(json_str=goodsInfoBase, logger=self.my_lg)
        _['goodsDetailContent'] = json_2_dict(json_str=goodsDetailContent, logger=self.my_lg)
        _['kaolaSuperMarket'] = kaolaSuperMarket

        return _

    def _get_right_body(self, body):
        '''
        处理phone端得到需求数据
        :param body:
        :return:
        '''
        try:
            body_1 = re.compile(r'window.__Goods__ = (.*?),}</script>').findall(body)[0]
            body_1 += '}'
            # 尺码表
            sizeChartImgs = re.compile(r'sizeChartImgs: (.*?),//').findall(body[0])

            basicInfo = re.compile(r'basicInfo: (.*?),goodsNotice').findall(body_1)[0]
            skuPropertyList = re.compile(r'skuPropertyList: (.*?),specialGoodsDesc').findall(body_1)[0]
            kaolaSuperMarket = re.compile(r'kaolaSuperMarket: (.*?),colorSliderImgs').findall(body_1)[0]
            brandGoodsAmount = re.compile(r'brandGoodsAmount: (.*?),brandLogo').findall(body_1)[0]
            goodsDetailContent = re.compile(r'goodsDetailContent: (.*?),vipGoods').findall(body_1)[0]
            vipGoods = re.compile(r'vipGoods: (.*?),vipGoodsLogo').findall(body_1)[0]

            # self.my_lg.info(str(sizeChartImgs))
            # self.my_lg.info(str(body_1))
        except IndexError:
            self.my_lg.error('遇到错误:', exc_info=True)
            return {}

        _ = {}
        _['basicInfo'] = json_2_dict(json_str=basicInfo, logger=self.my_lg)
        _['skuPropertyList'] = json_2_dict(json_str=skuPropertyList, logger=self.my_lg)
        _['kaolaSuperMarket'] = kaolaSuperMarket
        _['brandGoodsAmount'] = brandGoodsAmount
        _['goodsDetailContent'] = json_2_dict(json_str=goodsDetailContent, logger=self.my_lg)
        _['vipGoods'] = vipGoods
        _['sizeChartImgs'] = sizeChartImgs
        # pprint(_)

        return _

    def _wash_data(self, data):
        '''
        清洗data
        :param data:
        :return:
        '''
        try:
            data['goodsDetailContent']['qualityGoodsResource'] = {}
            data['sku_info']['frontVipInfo']['vipRedStationingInfo'] = {}
            data['sku_info']['frontVipInfo']['vipSpanImageInfo'] = {}
            data['sku_info']['goodsDeclare']['contentList'] = []
            data['sku_info']['goodsDeclare']['title'] = []
            data['sku_info']['vipGoodsDiscountInfo'] = {}
        except:
            pass

        return data

    def _get_pc_sku_info_params(self, goods_id):
        '''
        获取pc端sku_info接口的params
        :param goods_id:
        :return:
        '''
        params = {
            # "provinceCode":"330000",
            # "cityCode":"330100",
            # "districtCode":"330102",
            "goodsId": goods_id,
            # "categoryId":"547",
            # "t":["1533086767674","1533086767674"]
        }

        return params

    def _get_params(self, goods_id):
        '''
        得到获取sku_info的params
        :param goods_id:
        :return:
        '''
        t = str(datetime_to_timestamp(get_shanghai_time())) + str(get_random_int_number(start_num=100, end_num=999))
        params = (
            ('t', t),
            ('goodsId', str(goods_id)),
            # ('provinceCode', '330000'),
            # ('cityCode', '330100'),
            # ('districtCode', '330102'),
        )

        return params

    def _get_data_error_init(self):
        '''
        获取或者失败处理
        :return:
        '''
        self.result_data = {}

        return {}

    def get_goods_id_from_url(self, kaola_url):
        '''
        得到goods_id
        :param kaola_url:
        :return: goods_id 
        '''
        kaola_url = kaola_url.replace('http://', 'https://').replace(';', '')

        # https://goods.kaola.com/product/27757.html?ri=navigation&from=page1&zn=result&zp=page1-0&position=0&istext=0&srId=8bd1e06482b5730be802f6ce6f56dacf&isMarketPriceShow=true&hcAntiCheatSwitch=0&anstipamActiCheatSwitch=1&anstipamActiCheatToken=de3223456456fa2e3324354u4567lt&anstipamActiCheatValidate=anstipam_acti_default_validate
        is_kaola_url = re.compile(r'https://goods.kaola.com/product/.*?').findall(kaola_url)
        if is_kaola_url != []:
            if re.compile(r'https://goods.kaola.com/product/(\d+).html.*').findall(kaola_url) != []:
                goods_id = re.compile(r'https://goods.kaola.com/product/(\d+).html.*').findall(kaola_url)[0]
                self.my_lg.info('------>>>| 得到的考拉商品的goods_id为: {0}'.format(goods_id))
                return goods_id
        else:
            self.my_lg.info('网易考拉商品url错误, 非正规的url, 请参照格式(https://goods.kaola.com/product/xxx.html)开头的...')
            return ''
    
    def __del__(self):
        try:
            del self.my_lg
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    kaola = KaoLaParse()
    while True:
        kaola_url = input('请输入待爬取的考拉商品地址: ')
        kaola_url.strip('\n').strip(';')
        goods_id = kaola.get_goods_id_from_url(kaola_url)
        kaola._get_goods_data(goods_id=goods_id)
        data = kaola._deal_with_data()
        # pprint(data)