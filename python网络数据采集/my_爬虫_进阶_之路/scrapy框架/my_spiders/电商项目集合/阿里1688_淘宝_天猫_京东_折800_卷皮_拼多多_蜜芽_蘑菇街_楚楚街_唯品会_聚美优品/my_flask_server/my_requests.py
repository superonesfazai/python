# coding:utf-8

'''
@author = super_fazai
@File    : my_requests.py
@Time    : 2017/3/22 10:13
@connect : superonesfazai@gmail.com
'''

import requests
from random import randint
from my_ip_pools import MyIpPools
import re, gc
from pprint import pprint

__all__ = [
    'MyRequests',
]

class MyRequests(object):
    def __init__(self):
        super().__init__()

    @classmethod
    def get_url_body(cls, url, headers:dict, params:dict=None, had_referer=False):
        '''
        根据url得到body
        :param tmp_url:
        :return: '' 表示出错退出 | body 类型str
        '''
        # 设置代理ip
        ip_object = MyIpPools()
        proxies = ip_object.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        proxy = proxies['http'][randint(0, len(proxies) - 1)]

        tmp_proxies = {
            'http': proxy,
        }
        # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))

        tmp_headers = headers
        tmp_headers['Host'] = re.compile(r'://(.*?)/').findall(url)[0]
        if had_referer:
            if re.compile(r'https').findall(url) != []:
                tmp_headers['Referer'] = 'https://' + tmp_headers['Host'] + '/'
            else:
                tmp_headers['Referer'] = 'http://' + tmp_headers['Host'] + '/'

        s = requests.session()
        try:
            if params is not None:
                response = s.get(url, headers=tmp_headers, params=params, proxies=tmp_proxies, timeout=12)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            else:
                response = s.get(url, headers=tmp_headers, proxies=tmp_proxies, timeout=12)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            body = response.content.decode('utf-8')

            body = re.compile('\t').sub('', body)
            body = re.compile('  ').sub('', body)
            body = re.compile('\r\n').sub('', body)
            body = re.compile('\n').sub('', body)
            # print(body)
        except Exception:
            print('requests.get()请求超时....')
            print('data为空!')
            body = ''

        return body

    def __del__(self):
        gc.collect()

def test():
    # 抓包: /vips-mobile/rest/
    url = 'https://mapi.appvipshop.com/vips-mobile/rest/product/app/detail/v4'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':	'gzip'
        'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Host': 'mapi.appvipshop.com',
        # 'Referer': 'http://s.h5.jumei.com/yiqituan/detail?item_id=ht180321p2453550t4&type=global_deal',
        'User-Agent': 'Spec/6.14.2 (iPhone; iOS 11.0; Scale/3.00)',
        'authorization':	'OAuth api_sign=314a873d27ac656938383c04454a9ab8635164b5'
    }

    params = {
        'api_key':	'34a65f18bae9439589ae5f889bc37075',
        'app_name':	'shop_iphone',
        'app_version':	'6.14.2',
        'client_type':	'iphone',
        'deeplink_cps':	'',
        'did':	'0.1.f7a27c9f9b803c693e30612199f4aa97.1bd8be',
        'fdc_area_id':	'103103101',
        'functions':	'sku_price,wh_transfer,ptype,shoeRecomm,sku_price,luxury_info,financeVip,brand_store_info,newBrandLogo,reduced_point_desc,hideOnlySize,ui_settings,atmospherePicture,haitaoFinanceVip',
        'haitao_description_fields':	'descri_image,beauty_descri_image,text,mobile_descri_image,mobile_prompt_image',
        'is_get_TUV':	'1',
        'is_get_credit_tips':	'0',
        'is_get_pms_tips':	'0',
        'is_multicolor':	'1',
        'mars_cid': 'ccff3274ca0dc3c52ab9d1fbde76aecd5db3a162',
        'mobile_channel': 'ng00010v:al80ssgp:37u8zn0w:ng00010p',
        'mobile_platform': '3',
        'other_cps': '',
        'page_id':	'page_te_commodity_category_1522483827457',
        'price_fields':	'vipshopPrice,saleSavePrice,specialPrice,salePriceTips,vipDiscount,priceIconURL,priceIconMsg',
        'productId':	'461818416',
        'province_id': '103103',
        'session_id':	'ccff3274ca0dc3c52ab9d1fbde76aecd5db3a162_shop_iphone_1522483800161',
        'skey': '917acdbd3ccdbbc962182fc7ea56e4f4',
        'source_app': 'iphone_1',
        'standby_id': 'ng00010v:al80ssgp:37u8zn0w:ng00010p',
        'supportMedicine':	'1',
        'supportReserved':	'0',
        'timestamp':	'1522483834',
        'user_id':	'283682746',
        'user_token': 'C337EC6808C1434599D5F85CBC3BE982546293A7',
        'warehouse': 'VIP_SH',
    }

    body = requests.get(url=url, headers=headers, params=params)
    print(body.content.decode('utf-8'))
    # body = MyRequests().get_url_body(url=url, headers=headers, params=params)
    # print(body)

test()
