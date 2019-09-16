# coding:utf-8

'''
@author = super_fazai
@File    : zhe_800_pintuan_parse.py
@Time    : 2017/12/18 09:37
@connect : superonesfazai@gmail.com
'''

"""
折800常规拼团商品页面采集解析系统(官网地址:https://pina.m.zhe800.com)
由于pc版折800没有拼团的页面，只有手机版有，所以是基于手机版的页面采集
"""

import time
import gc

from settings import (
    PHANTOMJS_DRIVER_PATH,
    IP_POOL_TYPE,)

from sql_str_controller import (
    z8_insert_str_2,
    z8_update_str_3,)

from multiplex_code import (
    _z8_get_parent_dir,
    _get_right_model_data,
    contraband_name_check,
)

# from fzutils.spider.fz_phantomjs import BaseDriver
from fzutils.spider.async_always import *

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

class Zhe800PintuanParse(Crawler):
    def __init__(self):
        super(Zhe800PintuanParse, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
        )
        self._set_headers()
        self.result_data = {}
        self.num_retries = 3
        # self.driver = BaseDriver(executable_path=PHANTOMJS_DRIVER_PATH)

    def _set_headers(self):
        self.headers = get_random_headers(upgrade_insecure_requests=False,)
        self.headers.update({
            'accept-language': 'zh-CN,zh;q=0.8',
            'Host': 'pina.m.zhe800.com',
            # 'Cookie': 'api_uid=rBQh+FoXerAjQWaAEOcpAg==;',      # 分析发现需要这个cookie值
        })

    def get_goods_data(self, goods_id):
        '''
        模拟构造得到data的url
        :param goods_id:
        :return: data   类型dict
        '''
        if goods_id == '':
            return self._data_error_init()

        tmp_url = 'https://pina.m.zhe800.com/detail/detail.html?zid=' + str(goods_id)
        print('------>>>| 得到的商品手机版地址为: ', tmp_url)

        try:
            '''
            原先采用requests来模拟的，之前能用，但是数据多了请求多了sleep也不管用后面会获取不到信息
            '''
            body = Requests.get_url_body(
                url=tmp_url,
                headers=self.headers,
                proxy_type=PROXY_TYPE_HTTP,
                ip_pool_type=self.ip_pool_type,
                num_retries=self.num_retries,)
            assert body != ''
            # print(body)

            '''
            采用phantomjs
            '''
            # main_body = self.driver.use_phantomjs_to_get_url_body(url=tmp_url, css='div.title')
            # # print(main_body)
            # if main_body == '':
            #     print('获取到的main_body为空值, 此处跳过!')
            #     return self._data_error_init()

            # 不用这个了因为会影响到正常情况的商品
            try:
                if re.compile(r'很抱歉，您查看的页面木有了~').findall(body) != [] and (
                        len(body) < 660 and len(body) > 640):  # 单独处理商品页面不存在的情况
                    print('很抱歉，您查看的页面木有了~')
                    self.result_data = {}
                    return str(goods_id)
                else:
                    pass
            except:
                pass

            data = re.compile(r'window.prod_info = (.*?);seajs.use\(.*?\);</script>').findall(body)
            assert data != [], 'data为空!'
            data = json_2_dict(
                json_str=data[0],
                default_res={},)
            assert data != {}
            # pprint(data)
            # div_desc
            div_desc_body = self.get_div_desc_body(goods_id=goods_id)
            # print(div_desc_body)
            assert div_desc_body != '', '获取到的div_desc_body为空!'
            p_info = self.get_p_info_list(goods_id=goods_id)
            # pprint(p_info)
            assert p_info != []
            # 获取商品实时库存信息
            stock_info = self.get_stock_info_dict(goods_id=goods_id)
            assert stock_info != {}, '获取到的库存信息为{}!'
            # pprint(stock_info)
        except (IndexError, AssertionError, Exception) as e:
            print(e)
            return self._data_error_init()

        data['div_desc'] = div_desc_body
        data['p_info'] = p_info
        data['stock_info'] = stock_info

        if stock_info.get('pin_status', 2) == 3:
            print('##### 该拼团商品已经被抢光 ...')
            is_delete = 1
        else:
            is_delete = 0
        data['is_delete'] = is_delete
        data['parent_dir'] = _z8_get_parent_dir(goods_id)

        self.result_data = data
        # pprint(data)

        return data

    def deal_with_data(self):
        '''
        处理result_data, 返回需要的信息
        :return: 字典类型
        '''
        data = self.result_data
        if data != {}:
            try:
                shop_name = self._get_shop_name(data=data)
                title = self._get_title(data=data)
                sub_title = self._get_sub_title(data=data)
                detail_name_list = self._get_detail_name_list(data=data)
                price_info_list = self._get_price_info_list(
                    data=data,
                    detail_name_list=detail_name_list)
                price_info_list, price, taobao_price = self._get_price_and_tb_price(price_info_list=price_info_list, data=data)
                all_img_url = self._get_all_img_url(data=data)
                p_info = self._get_p_info(data=data)
                # 总销量(shop_sales字段)
                all_sell_count = self._get_all_sell_count(data=data)
                div_desc = self._get_div_desc(data=data)
                # 商品销售时间区间(sale_begin_time和sale_end_time字段)
                schedule = self._get_schedule(data=data)
                # pprint(schedule)

                is_delete = self._get_is_delete(data=data, schedule=schedule)
                # print(is_delete)
                parent_dir = data.get('parent_dir', '')
                if contraband_name_check(target_name=title):
                    print('违禁物品下架...')
                    is_delete = 1
                else:
                    pass
            except Exception as e:
                print('遇到错误:', e)
                return self._data_error_init()

            result = {
                'shop_name': shop_name,                 # 店铺名称
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
                'schedule': schedule,                   # 商品开卖时间和结束开卖时间
                'all_sell_count': all_sell_count,       # 商品总销售量
                'is_delete': is_delete,                  # 用于判断商品是否已经下架
                'parent_dir': parent_dir,
            }
            # pprint(result)
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

    def _get_shop_name(self, data):
        shop_name = data.get('sellerName', '')

        return shop_name

    def _get_title(self, data):
        title = data.get('title', '')

        return title

    def _get_sub_title(self, data):
        sub_title = data.get('desc', '')
        sub_title = re.compile(r'  ').sub('', sub_title)
        sub_title = re.compile(r'\n').sub('', sub_title)

        return sub_title

    def _get_detail_name_list(self, data):
        img_name = data.get('sku', {}).get('img_name', '')
        size_name = data.get('sku', {}).get('size_name', '')
        # pprint(img_name)
        # pprint(size_name)
        tmp_detail_name_list_1 = [{'spec_name': img_name, 'img_here': 1}] if img_name != '' else []
        tmp_detail_name_list_2 = [{'spec_name': size_name, 'img_here': 0}] if size_name != '' else []

        detail_name_list = tmp_detail_name_list_1 + tmp_detail_name_list_2

        return detail_name_list

    def _get_price_info_list(self, **kwargs):
        data = kwargs.get('data', {})
        detail_name_list = kwargs.get('detail_name_list', [])

        price_info_list = []
        if detail_name_list == []:
            print('## detail_name_list为空值 ##')
            pass

        else:
            sku_map = data.get('sku', {}).get('sku_map', {})
            # 每个规格的照片
            sku_img_list = [{item.get('pId', '') + '-' + item.get('vId', ''): item.get('vPicture', '')} for item in
                            data.get('sku', {}).get('img_list', [])]
            # pprint(sku_img_list)

            # 规格list
            tmp_sku_map = [value for value in sku_map.values()]
            # pprint(tmp_sku_map)

            # 每个规格的库存list
            sku_stock_info = data.get('stock_info', {}).get('product_sku', {}).get('sku_map', {})
            # pprint(sku_stock_info)

            for item in tmp_sku_map:
                tmp = {}
                sku_key = item.get('sku', '')

                # 处理得到每个规格对应的图片地址
                tmp_sku_key_1 = sku_key.split(':')[0]
                img_url = [list(item1.values())[0] for item1 in sku_img_list if tmp_sku_key_1 == list(item1.keys())[0]][0]
                # print(img_url)

                # 处理得到每个规格
                spec_value = item.get('sku_desc', '')  # 颜色-265咸菜:尺码-180
                spec_value = spec_value.split(':')  # ['颜色-265咸菜', '尺码-180']
                spec_value = [item2.split('-')[1] for item2 in spec_value]  # ['265咸菜', '180']
                spec_value = '|'.join(spec_value)  # '265咸菜|180'

                # 处理得到每个规格对应的库存值
                tmp_sku_key_2 = sku_key.split(':')
                tmp_sku_key_2 = [item3.split('-')[1] for item3 in tmp_sku_key_2]
                tmp_sku_key_2 = ':'.join(tmp_sku_key_2)  # 1011:1108
                # print(tmp_sku_key_2)
                rest_number = [sku_stock_info[key] for key in sku_stock_info if tmp_sku_key_2 == key][0]
                # print(rest_number)

                if rest_number > 0:
                    # 该规格库存大于0时再进行赋值否则跳过
                    tmp['spec_value'] = spec_value
                    tmp['pintuan_price'] = str(item.get('pinPrice', ''))
                    tmp['detail_price'] = str(item.get('curPrice', ''))
                    tmp['normal_price'] = ''
                    tmp['img_url'] = img_url
                    tmp['rest_number'] = rest_number
                    price_info_list.append(tmp)
                else:
                    pass

        return price_info_list

    def _get_price_and_tb_price(self, **kwargs):
        price_info_list = kwargs.get('price_info_list', [])
        data = kwargs.get('data', {})

        # 商品价格和淘宝价
        try:
            tmp_price_list = sorted([round(float(item.get('pintuan_price', '')), 2) for item in price_info_list])
            price = tmp_price_list[-1]  # 商品价格
            taobao_price = tmp_price_list[0]  # 淘宝价
        except:  # 单独处理无规格的商品
            print('此商品无规格!所以我给它单独处理')
            price_info_list = [{
                'spec_value': '',
                'detail_price': str(data.get('pin_price', '')),
                'normal_price': str(data.get('real_cur_price', '')),
                'img_url': '',
                'rest_number': 100
            }]
            # print(price_info_list)
            tmp_price_list = sorted([round(float(item.get('detail_price', '')), 2) for item in price_info_list])
            price = tmp_price_list[-1]  # 商品价格
            taobao_price = tmp_price_list[0]  # 淘宝价

        # print('最高价为: ', price)
        # print('最低价为: ', taobao_price)
        # print(len(price_info_list))
        # pprint(price_info_list)

        return (price_info_list, price, taobao_price)

    def _get_all_img_url(self, data):
        return [{'img_url': item} for item in data.get('shop_images', [])]

    def _get_p_info(self, data):
        return data.get('p_info', [])

    def _get_all_sell_count(self, data):
        return str(data.get('shop_sales', ''))

    def _get_div_desc(self, data):
        return data.get('div_desc', '')

    def _get_schedule(self, data):
        return [{
            'begin_time': data.get('sale_begin_time', ''),
            'end_time': data.get('sale_end_time', ''),
        }]

    def _get_is_delete(self, **kwargs):
        data = kwargs.get('data', {})
        schedule = kwargs.get('schedule', [])

        is_delete = data['is_delete']
        if schedule != []:
            if data.get('sale_end_time') is not None:
                end_time = data.get('sale_end_time')
                try:
                    end_time = int(str(time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S')))[0:10])
                    # print(end_time)
                except:
                    raise ValueError('end_time由str时间转换为时间戳时出错, 此处跳过!')

                if float(end_time) < time.time():
                    # 结束时间戳小于当前时间戳则表示已经删除无法购买
                    is_delete = 1
        else:
            pass

        return is_delete

    def _data_error_init(self):
        '''
        数据处理错误初始化
        :return:
        '''
        self.result_data = {}

        return {}

    def insert_into_zhe_800_pintuan_table(self, data, pipeline) -> bool:
        try:
            tmp = _get_right_model_data(data=data, site_id=17)  # 采集来源地(折800拼团商品)
        except:
            print('此处抓到的可能是折800拼团券所以跳过')
            return False

        print('------>>>| 待存储的数据信息为: {0}'.format(data.get('goods_id')))
        params = self._get_db_insert_pintuan_params(item=tmp)
        res = pipeline._insert_into_table(sql_str=z8_insert_str_2, params=params)

        return res

    def to_right_and_update_data(self, data, pipeline):
        try:
            tmp = _get_right_model_data(data=data, site_id=17)
        except:
            print('此处抓到的可能是折800拼团券所以跳过')
            return None
        print('------>>>| 待存储的数据信息为: {0}'.format(data.get('goods_id')))

        params = self._get_db_update_pintuan_params(item=tmp)
        pipeline._update_table(sql_str=z8_update_str_3, params=params)

    def _get_db_insert_pintuan_params(self, item):
        params = (
            item['goods_id'],
            item['goods_url'],
            item['username'],
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
            item['all_sell_count'],
            dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
            item['div_desc'],  # 存入到DetailInfo
            dumps(item['schedule'], ensure_ascii=False),
            item['pintuan_begin_time'],
            item['pintuan_end_time'],
            item['page'],

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
            dumps(item['detail_name_list'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
            dumps(item['price_info_list'], ensure_ascii=False),
            dumps(item['all_img_url'], ensure_ascii=False),
            item['all_sell_count'],
            dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
            item['div_desc'],  # 存入到DetailInfo
            dumps(item['schedule'], ensure_ascii=False),
            item['is_delete'],
            item['parent_dir'],

            item['goods_id'],
        )

        return params

    def get_div_desc_body(self, goods_id):
        '''
        得到div_desc的html页面
        :param goods_id:
        :return: str类型的data, 出错的情况下返回{}
        '''
        div_desc_url = 'https://pina.m.zhe800.com/nnc/product/detail_content.json?zid=' + str(goods_id)

        # 使用requests
        div_desc_body = Requests.get_url_body(url=div_desc_url, headers=self.headers, high_conceal=True, ip_pool_type=self.ip_pool_type)
        if div_desc_body == '':
            div_desc_body = '{}'

        # 使用phantomjs
        # div_desc_body = self.driver.use_phantomjs_to_get_url_body(url=div_desc_url)
        # # print(div_desc_body)
        # if div_desc_body == '':
        #     div_desc_body = '{}'
        # else:
        #     try:
        #         div_desc_body = re.compile(r'<body><pre .*?>(.*)</pre></body>').findall(div_desc_body)[0]
        #         div_desc_body = re.compile(r'&gt;').sub('>', div_desc_body)
        #         div_desc_body = re.compile(r'&lt;').sub('<', div_desc_body)
        #     except:
        #         div_desc_body = '{}'

        tmp_body = json_2_dict(json_str=div_desc_body).get('data', '')
        if tmp_body == '':
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值

        tmp_body = self._wash_div_desc(tmp_body=tmp_body)

        if tmp_body != '':
            tmp_body = '<div>' + tmp_body + '</div>'

        return tmp_body

    def get_p_info_list(self, goods_id):
        '''
        得到详情介绍信息
        :param goods_id:
        :return: 返回一个list
        '''
        p_info_url = 'https://pina.m.zhe800.com/cns/products/get_product_properties_list.json?productId=' + str(goods_id)
        p_info_body = Requests.get_url_body(url=p_info_url, headers=self.headers, high_conceal=True, ip_pool_type=self.ip_pool_type)
        if p_info_body == '':
            print('获取到的p_info_body为空值, 此处跳过!')
            p_info_body = '{}'

        tmp_p_info = json_2_dict(json_str=p_info_body).get('perportieslist', [])
        if tmp_p_info == []:
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值

        if tmp_p_info != []:
            p_info = [{
                'p_name': item.get('name', ''),
                'p_value': item.get('value'),
            } for item in tmp_p_info]
        else:
            p_info = tmp_p_info

        return p_info

    def get_stock_info_dict(self, goods_id):
        '''
        得到实时库存信息
        :param goods_id:
        :return: 返回dict类型
        '''
        stock_info_url = 'https://pina.m.zhe800.com/cns/products/' + str(goods_id) + '/realtime_info.json'
        stock_info_body = Requests.get_url_body(url=stock_info_url, headers=self.headers, high_conceal=True, ip_pool_type=self.ip_pool_type)
        if stock_info_body == '':
            print('获取到的stock_info_body为空值!')
            stock_info_body = '{}'

        tmp_stock_info = json_2_dict(json_str=stock_info_body).get('data', {})
        if tmp_stock_info == {}:
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值

        return tmp_stock_info

    def _wash_div_desc(self, tmp_body):
        # 清洗
        tmp_body = re.compile(r'<div class=\"by_deliver\">.*?</div></div>').sub('', tmp_body)
        tmp_body = re.compile(r'src=.*? />').sub('/>', tmp_body)
        tmp_body = re.compile(r'data-url=').sub('src=\"', tmp_body)
        tmp_body = re.compile(r' />').sub('\" style="height:auto;width:100%;"/>', tmp_body)

        return tmp_body

    def get_goods_id_from_url(self, zhe_800_pintuan_url):
        '''
        得到goods_id
        :param pinduoduo_url:
        :return: goods_id (类型str)
        '''
        is_zhe_800_pintuan_url = re.compile(r'https://pina.m.zhe800.com/detail/detail.html.*?').findall(zhe_800_pintuan_url)
        if is_zhe_800_pintuan_url != []:
            if re.compile(r'https://pina.m.zhe800.com/detail/detail.html\?.*?zid=ze(\d+).*?').findall(zhe_800_pintuan_url) != []:
                tmp_zhe_800_pintuan_url = 'ze' + re.compile(r'https://pina.m.zhe800.com/detail/detail.html\?.*?zid=ze(\d+).*?').findall(zhe_800_pintuan_url)[0]
                if tmp_zhe_800_pintuan_url != '':
                    goods_id = tmp_zhe_800_pintuan_url
                else:  # 只是为了在pycharm里面测试，可以不加
                    zhe_800_pintuan_url = re.compile(r';').sub('', tmp_zhe_800_pintuan_url)
                    goods_id = 'ze' + re.compile(r'https://pina.m.zhe800.com/detail/detail.html\?.*?zid=ze(\d+).*?').findall(zhe_800_pintuan_url)[0]
                print('------>>>| 得到的折800拼团商品id为:', goods_id)
                return goods_id
            else:
                pass
        else:
            print('折800拼团商品url错误, 非正规的url, 请参照格式(https://pina.m.zhe800.com/detail/detail.html)开头的...')
            return ''

    def __del__(self):
        # try:
        #     del self.driver
        # except:
        #     pass
        gc.collect()

if __name__ == '__main__':
    zhe_800_pintuan = Zhe800PintuanParse()
    while True:
        zhe_800_pintuan_url = input('请输入待爬取的折800拼团商品地址: ')
        zhe_800_pintuan_url.strip('\n').strip(';')
        goods_id = zhe_800_pintuan.get_goods_id_from_url(zhe_800_pintuan_url)
        zhe_800_pintuan.get_goods_data(goods_id=goods_id)
        data = zhe_800_pintuan.deal_with_data()
        pprint(data)
