# coding:utf-8

'''
@author = super_fazai
@File    : mogujie_parse.py
@connect : superonesfazai@gmail.com
'''

"""
蘑菇街页面解析
"""

import sys
sys.path.append('..')

from decimal import Decimal
from settings import IP_POOL_TYPE
from sql_str_controller import (
    mg_insert_str_2,
    mg_update_str_3,
    mg_update_str_4,)

from fzutils.cp_utils import _get_right_model_data
from fzutils.spider.async_always import *

class MoGuJieParse(Crawler):
    def __init__(self):
        super(MoGuJieParse, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
        )
        self._set_headers()
        self.result_data = {}

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'm.mogujie.com',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    def get_goods_data(self, goods_id):
        '''
        模拟构造得到data的url
        :param goods_id: 常规商品goods_id
        :return:
        '''
        """
        方案1: 原先采用调用api的方法, 无奈分析js源码未找到sign是如何md5加密，从而暂时无法实现通过api调用参数 (pass)
        """
        # """     # 这些是构造参数
        # mw-appkey:100028
        # mw-t:1517037701053
        # mw-uuid:956bf265-90a4-45b0-bfa8-31040782f99e
        # mw-ttid:NMMain@mgj_h5_1.0
        # mw-sign:ef29b1801c79d63907f3589c68e4cd4c
        # data:{"iid":"1lnrc42","template":"1-2-detail_normal-1.0.0","appPlat":"m","noPintuan":false}
        # callback:mwpCb2
        # _:1517037701056
        # """
        # print('------>>>| 对应的手机端地址为: ', 'https://h5.mogujie.com/detail-normal/index.html?itemId=' + goods_id)
        #
        # appkey = '100028'
        # t = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位
        #
        # uuid = '956bf265-90a4-45b0-bfa8-31040782f99e'
        # ttid = 'NMMain@mgj_h5_1.0'
        # sign = ''
        #
        # '''
        # 下面是构造params
        # '''
        # params_data_2 = {
        #     'iid': goods_id,
        #     'template': '1-2-detail_normal-1.0.0',
        #     'appPlat': 'm',
        #     'noPintuan': 'false',
        # }
        #
        # params = {
        #     'data': json.dumps(params_data_2),
        # }
        #
        # tmp_url = 'https://api.mogujie.com/h5/http.detail.api/1/?mw-appkey={}&mw-t={}&mw-uuid={}&mw-ttid={}&mw-sign={}&callback=mwpCb2'.format(
        #     appkey, t, uuid, ttid, sign
        # )
        #
        # # 设置代理ip
        # ip_object = MyIpPools()
        # self.proxies = ip_object.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        # self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]
        #
        # tmp_proxies = {
        #     'http': self.proxy,
        # }
        # # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))
        #
        # try:
        #     response = requests.get(tmp_url, headers=self.headers, params=params, proxies=tmp_proxies, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
        #     last_url = re.compile(r'\+').sub('', response.url)  # 转换后得到正确的url请求地址
        #     # print(last_url)
        #     response = requests.get(last_url, headers=self.headers, proxies=tmp_proxies, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
        #     data = response.content.decode('utf-8')
        #     print(data)
        #     data = re.compile(r'mwpCb2\((.*)\)').findall(data)  # 贪婪匹配匹配所有
        #     # print(data)
        # except Exception:
        #     print('requests.get()请求超时....')
        #     print('data为空!')
        #     return self._data_error_init()

        """
        方案2: 通过页面源码来获取
        """
        if goods_id == '':
            return self._data_error_init()

        tmp_url = 'https://shop.mogujie.com/detail/' + str(goods_id)
        print('------>>>| 原pc地址为: ', tmp_url)
        data = {}
        body = Requests.get_url_body(url=tmp_url, headers=self.headers, had_referer=True, ip_pool_type=self.ip_pool_type)
        # print(body)
        if body == '':
            print('获取到的body为空str!')
            return self._data_error_init()

        try:
            goods_info = re.compile(r'var detailInfo = (.*?);</script>').findall(body)[0]
            # print(goods_info)

            item_info = re.compile(r'itemInfo:(.*?),priceRuleImg').findall(goods_info)[0]
            # print(item_info)

            sku_info = re.compile(r'skuInfo:(.*?),pinTuanInfo').findall(goods_info)[0]
            # print(sku_info)

            shop_info = re.compile(r'shopInfo:(.*?),skuInfo').findall(goods_info)[0]
            # print(shop_info)

            item_info =  json_2_dict(json_str=item_info)
            sku_info = json_2_dict(json_str=sku_info)
            shop_info = json_2_dict(json_str=shop_info)
            # pprint(item_info)
            # pprint(sku_info)
            # pprint(shop_info)

            data['title'] = self._get_title(item_info)
            data['sub_title'] = ''
            data['shop_name'] = self._get_shop_name(shop_info)
            data['all_img_url'] = self._get_all_img_url(item_info=item_info)
            data['p_info'], tmp_p_info_body = self._get_p_info(goods_id=goods_id)
            data['div_desc'] = self._get_div_desc(tmp_p_info_body=tmp_p_info_body)
            data['detail_name_list'] = self._get_detail_name_list(sku_info=sku_info)

            '''
            获取每个规格对应价格跟规格以及其库存
            '''
            price_info_list = self.get_price_info_list(sku_info=sku_info)
            if price_info_list == '':
                raise Exception
            else:
                # pprint(price_info_list)
                data['price_info_list'] = price_info_list

            # 商品价格和淘宝价
            try:
                tmp_price_list = sorted([round(float(item.get('detail_price', '')), 2) for item in data['price_info_list']])
                price = Decimal(tmp_price_list[-1]).__round__(2)          # 商品价格
                taobao_price = Decimal(tmp_price_list[0]).__round__(2)    # 淘宝价
                # print('商品的最高价: ', price, ' 最低价: ', taobao_price)
            except IndexError:
                print('获取price和taobao_price时出错! 请检查')
                raise Exception

            data['price'] = price
            data['taobao_price'] = taobao_price

        except Exception as e:
            print('遇到错误: ', e)
            return self._data_error_init()

        if data != {}:
            # pprint(data)
            self.result_data = data
            return data

        else:
            print('data为空!')
            return self._data_error_init()

    def deal_with_data(self):
        '''
        处理得到规范的data数据
        :return: result 类型 dict
        '''
        data = self.result_data
        if data != {}:
            shop_name = data['shop_name']
            account = ''
            title = data['title']
            sub_title = data['sub_title']
            price = data['price']  # 商品价格
            taobao_price = data['taobao_price']  # 淘宝价
            detail_name_list = data['detail_name_list']
            price_info_list = data['price_info_list']
            all_img_url = data['all_img_url']
            p_info = data['p_info']
            div_desc = data['div_desc']
            is_delete = 0

            result = {
                # 'goods_url': data['goods_url'],         # goods_url
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
            # pprint(result)
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

    def _get_detail_name_list(self, sku_info):
        # pprint(sku_info)
        detail_name_list = self.get_goods_detail_name_list(sku_info=sku_info)
        # print(detail_name_list)
        assert detail_name_list != '', '获取detail_name_list出错, 请检查!'

        return detail_name_list

    def _get_div_desc(self, tmp_p_info_body):
        div_desc = self.get_goods_div_desc(tmp_p_info_body=tmp_p_info_body)
        assert div_desc != '', '获取到的div_desc为空str, 请检查!'

        return div_desc

    def _get_p_info(self, goods_id):
        p_info_api_url = 'https://shop.mogujie.com/ajax/mgj.pc.detailinfo/v1?_ajax=1&itemId=' + str(goods_id)
        tmp_p_info_body = Requests.get_url_body(url=p_info_api_url, headers=self.headers, had_referer=True, ip_pool_type=self.ip_pool_type)
        # print(tmp_p_info_body)
        assert tmp_p_info_body != '', '获取到的tmp_p_info_body为空值, 请检查!'

        p_info = self.get_goods_p_info(tmp_p_info_body=tmp_p_info_body)

        return p_info, tmp_p_info_body

    def _get_title(self, item_info):
        title = item_info.get('title', '')
        assert title != '', 'title为空!'

        return title

    def _get_shop_name(self, shop_info):
        return shop_info.get('name', '')

    def _get_all_img_url(self, item_info):
        return [{
            'img_url': item,
        } for item in item_info.get('topImages', [])]

    def _data_error_init(self):
        self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值

        return {}

    def insert_into_mogujie_pintuan_table(self, data, pipeline) -> bool:
        try:
            tmp = _get_right_model_data(data=data, site_id=23)
        except:
            print('此处抓到的可能是蜜芽拼团券所以跳过')
            return False

        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))
        params = self._get_db_insert_pintuan_params(item=tmp)
        _r = pipeline._insert_into_table(sql_str=mg_insert_str_2, params=params)

        return _r

    def update_mogujie_pintuan_table(self, data, pipeline):
        try:
            tmp = _get_right_model_data(data=data, site_id=23)
        except:
            print('此处抓到的可能是蜜芽拼团券所以跳过')
            return None
        # print('------>>> | 待存储的数据信息为: |', tmp)
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_update_pintuan_params(item=tmp)
        pipeline._update_table(sql_str=mg_update_str_3, params=params)

    def update_mogujie_pintuan_table_2(self, data, pipeline):
        try:
            tmp = _get_right_model_data(data=data, site_id=23)
        except:
            print('此处抓到的可能是蜜芽拼团券所以跳过')
            return None
        # print('------>>> | 待存储的数据信息为: |', tmp)
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_update_pintuan_params_2(item=tmp)
        pipeline._update_table(sql_str=mg_update_str_4, params=params)

    def _get_db_insert_pintuan_params(self, item):
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
            dumps(item['pintuan_time'], ensure_ascii=False),
            item['pintuan_begin_time'],
            item['pintuan_end_time'],
            item['all_sell_count'],
            item['fcid'],
            item['page'],
            item['sort'],

            item['site_id'],
            item['is_delete'],
        )

        return params

    def _get_db_update_pintuan_params(self, item):
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
            dumps(item['pintuan_time'], ensure_ascii=False),
            item['pintuan_begin_time'],
            item['pintuan_end_time'],
            item['all_sell_count'],

            item['goods_id'],
        )

        return params

    def _get_db_update_pintuan_params_2(self, item):
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

            item['goods_id'],
        )

        return params

    def get_price_info_list(self, sku_info):
        '''
        得到商品每个规格的价格库存及对应img_url
        :param sku_info:
        :return: '' 表示出错 or [] 表示规格为空 or [{}, ...] 正常
        '''
        try:
            skus = sku_info.get('skus', [])
            # pprint(skus)
            if skus == []:
                print('skus为空! 每个规格的价格为空!')
                return []

            price_info_list = []
            for item in skus:
                tmp = {}
                size = item.get('size', '')
                style = item.get('style', '')

                if size == '':
                    spec_value = style

                elif style == '':
                    spec_value = size

                else:
                    spec_value = style + '|' + size

                normal_price = Decimal(item.get('price', 0) / 100).__round__(2).__str__()
                detail_price = Decimal(item.get('nowprice', 0) / 100).__round__(2).__str__()
                img_url = item.get('img', '')
                rest_number = item.get('stock', 0)
                if rest_number == 0:
                    pass
                else:
                    tmp['spec_value'] = spec_value
                    tmp['normal_price'] = normal_price
                    tmp['detail_price'] = detail_price
                    tmp['img_url'] = img_url
                    tmp['rest_number'] = rest_number
                    price_info_list.append(tmp)

        except Exception as e:
            print('获取price_info_list时遇到错误: ', e)
            return ''

        return price_info_list

    def get_goods_detail_name_list(self, sku_info):
        '''
        得到sku_info
        :param sku_info:
        :return: '' or [] or [{}, {}, ...]
        '''
        detail_name_list = []
        try:
            props = sku_info.get('props', [])
            # pprint(props)
            if props == []:
                print('### detail_name_list为空值 ###')
                return []

            skus = sku_info.get('skus', [])
            img_here = 0
            try:
                img = skus[0].get('img', '')
                if img != '':
                    img_here = 1
            except IndexError:
                pass

            for item in props:
                label = item.get('label', '').replace(':', '')
                if label != '':
                    if img_here == 1:
                        try:
                            if item.get('list', [])[0].get('type', '') == 'style':
                                detail_name_list.append({
                                    'spec_name': label,
                                    'img_here': 1,
                                })
                        except IndexError:
                            detail_name_list.append({
                                'spec_name': label,
                                'img_here': 0,
                            })
                        img_here = 0    # 记录后置0
                    else:
                        detail_name_list.append({
                            'spec_name': label,
                            'img_here': 0,
                        })
                else:
                    pass

        except Exception as e:
            print('遇到错误: ', e)
            return ''

        return detail_name_list

    def get_goods_p_info(self, tmp_p_info_body):
        '''
        得到p_info
        :param tmp_p_info_body:
        :return: [] or [{}, {}, ....]
        '''
        tmp_p_info_data = json_2_dict(json_str=tmp_p_info_body)
        if tmp_p_info_data == {}:
            return []

        p_info = [{
            'p_name': item.get('key', ''),
            'p_value': item.get('value', ''),
        } for item in tmp_p_info_data.get('data', {}).get('itemParams', {}).get('info', {}).get('set', [])]

        return p_info

    def get_goods_div_desc(self, tmp_p_info_body):
        '''
        得到div_desc
        :param body:
        :return: '' or str
        '''
        def _get_div_images_list(target):
            div_images_list = []
            for item in target:
                if re.compile('http').findall(item) == []:
                    item = 'http:' + item
                div_images_list.append(item)

            return div_images_list

        tmp_p_info_data = json_2_dict(json_str=tmp_p_info_body)
        if tmp_p_info_data == {}:
            return ''

        div_images_list = _get_div_images_list(target=tmp_p_info_data.get('data', {}).get('detailInfos', {}).get('detailImage', [])[0].get('list', []))
        if div_images_list == []:
            # print('div_images_list为空list, 出错请检查!')
            # 可能在[1] 这个里面再进行处理
            div_images_list = _get_div_images_list(target=tmp_p_info_data.get('data', {}).get('detailInfos', {}).get('detailImage', [])[1].get('list', []))
            if div_images_list == []:
                print('div_images_list为空list, 出错请检查!')
                return ''
            else:
                tmp_div_desc = ''
                for item in div_images_list:
                    tmp = r'<img src="{}" style="height:auto;width:100%;"/>'.format(item)
                    tmp_div_desc += tmp
                div_desc = '<div>' + tmp_div_desc + '</div>'

        else:
            tmp_div_desc = ''
            for item in div_images_list:
                tmp = r'<img src="{}" style="height:auto;width:100%;"/>'.format(item)
                tmp_div_desc += tmp
            div_desc = '<div>' + tmp_div_desc + '</div>'

        return div_desc

    def get_goods_id_from_url(self, mogujie_url) -> str:
        mogujie_url = re.compile(r'http://').sub('https://', mogujie_url)
        is_mogujie_url = re.compile(r'https://shop.mogujie.com/detail/.*?').findall(mogujie_url)
        if is_mogujie_url != []:
            # 常规商品的地址处理
            if re.compile(r'https://shop.mogujie.com/detail/(.*?)\?.*?').findall(mogujie_url) != []:
                tmp_mogujie_url = re.compile('https://shop.mogujie.com/detail/(.*?)\?.*?').findall(mogujie_url)[0]
                if tmp_mogujie_url != '':
                    goods_id = tmp_mogujie_url
                else:
                    mogujie_url = re.compile(r';').sub('', mogujie_url)
                    goods_id = re.compile(r'https://shop.mogujie.com/detail/(.*?)\?.*').findall(mogujie_url)[0]

            else:   # 直接跟goods_id的地址(往往是自己构造的)
                mogujie_url = re.compile(r';').sub('', mogujie_url)
                goods_id = re.compile('https://shop.mogujie.com/detail/(.*)').findall(mogujie_url)[0]
            print('------>>>| 得到的蘑菇街商品id为:', goods_id)
            return goods_id

        else:
            print('蘑菇街商品url错误, 非正规的url, 请参照格式(https://shop.mogujie.com/detail/)开头的...')
            return ''

    def __del__(self):
        collect()

if __name__ == '__main__':
    mogujie = MoGuJieParse()
    while True:
        mogujie_url = input('请输入待爬取的蘑菇街商品地址: ')
        mogujie_url.strip('\n').strip(';')
        goods_id = mogujie.get_goods_id_from_url(mogujie_url)
        mogujie.get_goods_data(goods_id=goods_id)
        data = mogujie.deal_with_data()
        pprint(data)


