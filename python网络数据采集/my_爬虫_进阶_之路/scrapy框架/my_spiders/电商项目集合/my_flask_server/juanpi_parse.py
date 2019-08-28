# coding:utf-8

'''
@author = super_fazai
@File    : juanpi_parse.py
@Time    : 2017/11/17 17:26
@connect : superonesfazai@gmail.com
'''

"""
卷皮页面采集系统(别翻墙使用)
"""

import time
import gc

from settings import (
    PHANTOMJS_DRIVER_PATH,
    IP_POOL_TYPE,)
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from sql_str_controller import (
    jp_update_str_1,
    jp_update_str_2,
    jp_insert_str_1,
    jp_update_str_3,
    jp_insert_str_2,
    jp_update_str_4,
)

from multiplex_code import (
    _jp_get_parent_dir,
    _get_right_model_data,
)
from fzutils.spider.async_always import *

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

class JuanPiParse(Crawler):
    def __init__(self):
        super(JuanPiParse, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
            is_use_driver=True,
            driver_executable_path=PHANTOMJS_DRIVER_PATH,
        )
        self.result_data = {}

    def get_goods_data(self, goods_id):
        '''
        模拟构造得到data的url
        :param goods_id:
        :return: data   类型dict
        '''
        if goods_id == '':
            return self._data_error_init()
        else:
            tmp_url = 'https://web.juanpi.com/pintuan/shop/' + str(goods_id)
            print('------>>>| 得到的商品手机版的地址为: ', tmp_url)

            """
            2.采用phantomjs来处理，记住使用前别翻墙
            """
            body = self.driver.get_url_body(
                url=tmp_url,
                # 该css为手机端标题块
                # css_selector='div.sc-kgoBCf.bTQvTk',
                timeout=28,)
            # print(body)
            if re.compile(r'<span id="t-index">页面丢失ing</span>').findall(body) != []:    # 页面为空处理
                _ = SqlServerMyPageInfoSaveItemPipeline()
                if _.is_connect_success:
                    _._update_table(sql_str=jp_update_str_1, params=(goods_id,))
                    try: del _
                    except: pass
                    print('@@@ 逻辑删除该商品[{0}] is_delete = 1'.format(goods_id))
                    return self._data_error_init()

            if body == '':
                print('获取到的body为空str!请检查!')
                return self._data_error_init()

            data = re.compile(r'__PRELOADED_STATE__ = (.*);</script> <style ').findall(body)  # 贪婪匹配匹配所有

            # 得到skudata
            # 卷皮原先的skudata请求地址1(官方放弃)
            # skudata_url = 'https://webservice.juanpi.com/api/getOtherInfo?goods_id=' + str(goods_id)
            # 现在卷皮skudata请求地址2
            skudata_url = 'https://webservice.juanpi.com/api/getMemberAboutInfo?goods_id=' + str(goods_id)

            headers = get_random_headers(upgrade_insecure_requests=False,)
            headers.update({
                'Host': 'webservice.juanpi.com'
            })
            skudata_body = Requests.get_url_body(
                url=skudata_url,
                headers=headers,
                ip_pool_type=self.ip_pool_type,)
            if skudata_body == '':
                print('获取到的skudata_body为空str!请检查!')
                return self._data_error_init()
            skudata = re.compile(r'(.*)').findall(skudata_body)  # 贪婪匹配匹配所有

            if skudata != []:
                skudata = json_2_dict(json_str=skudata[0]).get('skudata', {})
                if skudata == {}:
                    return self._data_error_init()
                # pprint(skudata)

                try:
                    if skudata.get('info') is not None:
                        pass    # 说明得到正确的skudata
                    else:       # 否则跳出
                        print('skudata中info的key为None, 返回空dict')
                        return self._data_error_init()

                except AttributeError as e:
                    print('遇到错误如下(先跳过!): ', e)
                    return self._data_error_init()

            else:
                print('skudata为空!')
                return self._data_error_init()

            if data != []:
                main_data = json_2_dict(json_str=data[0])
                if main_data == {}:
                    return self._data_error_init()

                if main_data.get('detail') is not None:
                    main_data = self._wash_main_data(main_data.get('detail', {}))

                    main_data['skudata'] = skudata
                    main_data['goods_id'] = goods_id
                    main_data['parent_dir'] = _jp_get_parent_dir(phantomjs=self.driver, goods_id=goods_id)
                    self.result_data = main_data
                    # pprint(main_data)

                    return main_data

                else:
                    print('data中detail的key为None, 返回空dict')
                    return self._data_error_init()
            else:
                print('data为空!')
                return self._data_error_init()

    def deal_with_data(self):
        '''
        解析data数据,得到需要的东西
        :return: dict
        '''
        data = self.result_data
        if data != {}:
            shop_name = self._get_shop_name(data=data)
            # 掌柜
            account = ''
            title = self._get_title(data=data)
            sub_title = ''
            detail_name_list = self._get_detail_name_list(data=data)
            # print(detail_name_list)

            '''单独处理下架的情况'''
            if isinstance(detail_name_list, str):
                if detail_name_list == 'is_delete=1':
                    print('该商品已下架...')
                    sql_str = jp_update_str_1
                    params = (self.result_data.get('goods_id', ''),)
                    _ = SqlServerMyPageInfoSaveItemPipeline()
                    result = _._update_table(sql_str=sql_str, params=params)
                    if result:
                        print('### 该商品已经is_delete=1 ###')
                    else:
                        print('is_delete=1标记失败!')

            if detail_name_list == {}:
                return self._data_error_init()

            price_info_list, price, taobao_price = self._get_price_info_list_and_price_and_taobao_price(data=data)
            all_img_url = self._get_all_img_url(data=data)
            p_info = self._get_p_info(data=data)
            div_desc = self._get_div_desc(data=data)
            # 商品销售时间段
            schedule = self._get_goods_schedule(data=data)
            # pprint(schedule)

            is_delete = self._get_is_delete(data=data, schedule=schedule)
            if price == 0 or taobao_price == 0:     # 没有获取到价格说明商品已经下架了
                is_delete = 1
            parent_dir = data.get('parent_dir', '')

            result = {
                'shop_name': shop_name,                 # 店铺名称
                'account': account,                     # 掌柜
                'title': title,                         # 商品名称
                'sub_title': sub_title,                 # 子标题
                'price': price,                         # 商品价格
                'taobao_price': taobao_price,           # 淘宝价
                # 'goods_stock': goods_stock,           # 商品库存
                'detail_name_list': detail_name_list,   # 商品标签属性名称
                # 'detail_value_list': detail_value_list, # 商品标签属性对应的值
                'price_info_list': price_info_list,     # 要存储的每个标签对应规格的价格及其库存
                'all_img_url': all_img_url,             # 所有示例图片地址
                'p_info': p_info,                       # 详细信息标签名对应属性
                'div_desc': div_desc,                   # div_desc
                'is_delete': is_delete,                 # 是否下架判断
                'schedule': schedule,                   # 商品销售时间段
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
            gc.collect()
            return result

        else:
            print('待处理的data为空的dict')
            return {}

    def _data_error_init(self):
        self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值

        return {}

    def _get_title(self, data):
        title = data.get('baseInfo', {}).get('title', '')

        return title

    def _get_all_img_url(self, data):
        return [{'img_url': item} for item in data.get('goodImages')]

    def to_right_and_update_data(self, data, pipeline):
        tmp = _get_right_model_data(data=data, site_id=12)
        params = self._get_db_update_params(item=tmp)
        base_sql_str = jp_update_str_2
        if tmp['delete_time'] == '':
            sql_str = base_sql_str.format('shelf_time=%s', '')
        elif tmp['shelf_time'] == '':
            sql_str = base_sql_str.format('delete_time=%s', '')
        else:
            sql_str = base_sql_str.format('shelf_time=%s,', 'delete_time=%s')

        pipeline._update_table(sql_str=sql_str, params=params)

    def insert_into_juanpi_xianshimiaosha_table(self, data, pipeline) -> bool:
        tmp = _get_right_model_data(data=data, site_id=15)
        print('------>>> | 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_insert_miaosha_params(item=tmp)
        res = pipeline._insert_into_table(sql_str=jp_insert_str_1, params=params)

        return res

    def to_update_juanpi_xianshimiaosha_table(self, data, pipeline):
        tmp = _get_right_model_data(data=data, site_id=15)
        # print('------>>> | 待存储的数据信息为: |', tmp)
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_update_miaosha_params(item=tmp)
        res = pipeline._update_table(sql_str=jp_update_str_3, params=params)

        return res

    def insert_into_juanpi_pintuan_table(self, data, pipeline) -> bool:
        try:
            tmp = _get_right_model_data(data=data, site_id=18)
        except:
            print('此处抓到的可能是卷皮拼团券所以跳过')
            return False

        print('------>>> | 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_insert_pintuan_params(item=tmp)
        _r = pipeline._insert_into_table(sql_str=jp_insert_str_2, params=params)

        return _r

    def to_right_and_update_pintuan_data(self, data, pipeline):
        try:
            tmp = _get_right_model_data(data=data, site_id=18)
        except:
            print('此处抓到的可能是卷皮拼团券所以跳过')
            return None
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_update_pintuan_params(item=tmp)
        pipeline._update_table(sql_str=jp_update_str_4, params=params)

    def _get_shop_name(self, data):
        '''
        获取shop_name
        :param data:
        :return:
        '''
        if data.get('brand_info') is not None:
            shop_name = data.get('brand_info', {}).get('title', '')
        else:
            shop_name = data.get('schedule_info', {}).get('brand_title', '')

        return shop_name

    def _get_detail_name_list(self, data):
        '''
        获取detail_name_list
        :param data:
        :return: {} 表示出错 | [] 非空正常
        '''
        sku = data.get('skudata', {}).get('sku', [])
        # pprint(sku)
        detail_name_list = []
        if sku != []:
            try:
                if sku[0].get('av_fvalue', '') != '':
                    fav_name = data.get('skudata', {}).get('info', {}).get('fav_name', '')
                    detail_name_list.append({
                        'spec_name': fav_name,
                        'img_here': 0,
                    })
            except IndexError:
                print('IndexError错误，此处跳过!')
                # print(sku)
                if isinstance(sku, str):    # 单独处理下架的
                    if sku == '':
                        return 'is_delete=1'

                return {}

            if sku[0].get('av_zvalue', '') != '':
                zav_name = data.get('skudata', {}).get('info', {}).get('zav_name', '')
                detail_name_list.append({
                    'spec_name': zav_name,
                    'img_here': 1,
                })

        return detail_name_list

    def _get_price_info_list_and_price_and_taobao_price(self, data):
        '''
        获取price_info_list, price, taobao_price
        :param data:
        :return: a tuple
        '''
        sku = data.get('skudata', {}).get('sku', [])  # 分析得到sku肯定不为[]
        # pprint(sku)
        price_info_list = []
        if len(sku) == 1 and sku[0].get('av_fvalue', '') == '' and sku[0].get('av_zvalue') == '':  # 没有规格的默认只有一个{}
            # price最高价, taobao_price最低价
            price = round(float(sku[0].get('cprice')), 2)
            taobao_price = price

        else:  # 有规格的
            # 通过'stock'='1'来判断是否有库存, ='0'表示无库存
            # '由于卷皮不给返回库存值, 所以 'stock_tips'='库存紧张', 我就设置剩余库存为10, 如果'stock_tips'='', 就默认设置库存量为50
            # print('777')
            for item in sku:
                tmp = {}
                tmp_1 = []
                if item.get('av_fvalue', '') == '':
                    pass
                else:
                    tmp_1.append(item.get('av_fvalue'))

                if item.get('av_zvalue', '') == '':
                    pass
                else:
                    tmp_1.append(item.get('av_zvalue'))
                tmp_1 = '|'.join(tmp_1)

                if item.get('av_origin_zpic', '') != '':
                    tmp['img_url'] = item.get('av_origin_zpic', '')
                else:
                    tmp['img_url'] = ''

                if item.get('cprice', '') != '':
                    tmp['pintuan_price'] = item.get('cprice')
                    tmp['detail_price'] = item.get('sprice', '')
                    tmp['normal_price'] = item.get('price')
                else:
                    tmp['pintuan_price'] = item.get('price')
                    if item.get('sprice', '') != '':
                        tmp['detail_price'] = item.get('sprice', '')
                    else:
                        tmp['detail_price'] = item.get('price')
                    tmp['normal_price'] = item.get('price')

                if item.get('stock') == '0':  # 跳过
                    rest_number = '0'
                else:  # 即'stock'='1'
                    rest_number = '50'

                    if item.get('stock_tips', '') != '' and item.get('stock_tips', '') == '库存紧张':
                        # 库存紧张的时候设置下
                        rest_number = '10'

                    tmp['spec_value'] = tmp_1
                    tmp['rest_number'] = rest_number
                    price_info_list.append(tmp)

            # 得到有规格时的最高价和最低价
            tmp_price_list = sorted([round(float(item.get('pintuan_price', '')), 2) for item in price_info_list])
            # print(tmp_price_list)
            if tmp_price_list == []:
                price = 0
                taobao_price = 0
            else:
                price = tmp_price_list[-1]  # 商品价格
                taobao_price = tmp_price_list[0]  # 淘宝价

        # print('最高价为: ', price)
        # print('最低价为: ', taobao_price)
        # pprint(price_info_list)

        return price_info_list, price, taobao_price

    def _get_p_info(self, data):
        '''
        获取p_info
        :param data:
        :return:
        '''
        p_info = []
        attr = data.get('goodsDetail', {}).get('attr', [])
        # print(attr)
        if attr != []:
            # item是str时跳过
            p_info = [{'p_name': item.get('st_key'), 'p_value': item.get('st_value')} for item in attr if isinstance(item, dict)]
            for item in p_info:
                if item.get('p_name') == '运费':
                    # 过滤掉颜色的html代码
                    item['p_value'] = '全国包邮(偏远地区除外)'

                # 过滤清洗
                tmp_p_value = item.get('p_value', '')
                tmp_p_value = re.compile(r'\xa0').sub(' ', tmp_p_value)  # 替换为一个空格
                item['p_value'] = tmp_p_value

        return p_info

    def _get_div_desc(self, data):
        '''
        获取div_desc
        :param data:
        :return:
        '''
        div_images_list = data.get('goodsDetail', {}).get('images', [])
        tmp_div_desc = ''
        for item in div_images_list:
            tmp = r'<img src="{}" style="height:auto;width:100%;"/>'.format(item)
            tmp_div_desc += tmp

        return '<div>' + tmp_div_desc + '</div>'

    def _get_goods_schedule(self, data):
        '''
        获取商品销售时间段
        :param data:
        :return:
        '''
        # print(data.get('skudata', {}).get('info', {}))
        # print(data.get('skudata', {}))
        begin_time = data.get('skudata', {}).get('info', {}).get('start_time')  # 取这个时间段才是正确的销售时间, 之前baseInfo是虚假的
        end_time = data.get('skudata', {}).get('info', {}).get('end_time')
        if begin_time is None or end_time is None:
            schedule = []
        else:
            schedule = [{
                'begin_time': timestamp_to_regulartime(begin_time),
                'end_time': timestamp_to_regulartime(end_time),
            }]

        return schedule

    def _get_is_delete(self, data, schedule):
        '''
        得到商品的上下架状态
        :param data:
        :param schedule:
        :return:
        '''
        end_time = data.get('skudata', {}).get('info', {}).get('end_time')
        is_delete = 0
        # 是否下架判断
        # 结束时间戳小于当前时间戳则表示已经删除无法购买, 另外每个规格卖光也不显示is_delete=1(在上面已经判断, 这个就跟销售时间段没关系了)
        if schedule != []:
            if data.get('baseInfo', {}).get('end_time') is not None:
                '''
                先判断如果baseInfo中的end_time=='0'表示已经下架
                '''
                # base_info_end_time = data.get('baseInfo', {}).get('end_time')
                # self.my_lg.info(base_info_end_time)
                # if base_info_end_time == '0':
                #     is_delete = 1
                pass

            if float(end_time) < time.time():
                '''
                再判断日期过期的
                '''
                is_delete = 1

        '''
        卷皮-新增下架判断:
        time: 2018-5-12 
        '''
        if data.get('skudata', {}).get('info', {}).get('gstatus', '1') == '2':
            # 'gstatus'在售状态为'1'
            is_delete = 1

        return is_delete

    def _wash_main_data(self, main_data):
        '''
        清洗main_data
        :param main_data:
        :return:
        '''
        # 处理commitments
        try:
            main_data['commitments'] = ''
            main_data.get('discount', {})['coupon'] = ''
            main_data.get('discount', {})['coupon_index'] = ''
            main_data.get('discount', {})['vip_info'] = ''
            main_data['topbanner'] = ''
        except:
            pass
        try:
            main_data.get('brand_info')['sub_goods'] = ''
        except:
            pass

        return main_data

    def _get_db_update_params(self, item):
        '''
        得到待更新的db数据
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
            item['is_delete'],
            dumps(item['schedule'], ensure_ascii=False),
            item['is_price_change'],
            dumps(item['price_change_info'], ensure_ascii=False),
            item['sku_info_trans_time'],
            item['parent_dir'],
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

    def _get_db_insert_miaosha_params(self, item):
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
            dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
            item['div_desc'],  # 存入到DetailInfo
            dumps(item['schedule'], ensure_ascii=False),
            dumps(item['stock_info'], ensure_ascii=False),
            dumps(item['miaosha_time'], ensure_ascii=False),
            item['miaosha_begin_time'],
            item['miaosha_end_time'],
            item['tab_id'],
            item['page'],
            item['site_id'],
            item['is_delete'],
            item['parent_dir'],
        )

        return params

    def _get_db_update_miaosha_params(self, item):
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
            dumps(item['stock_info'], ensure_ascii=False),
            dumps(item['miaosha_time'], ensure_ascii=False),
            item['miaosha_begin_time'],
            item['miaosha_end_time'],
            item['parent_dir'],

            item['goods_id'],
        )

        return params

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
            item['parent_dir'],


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
            # item['all_sell_count'],
            dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
            item['div_desc'],  # 存入到DetailInfo
            dumps(item['schedule'], ensure_ascii=False),
            item['is_delete'],
            item['parent_dir'],

            item['goods_id']
        )

        return params

    def get_goods_id_from_url(self, juanpi_url):
        '''
        得到goods_id
        :param juanpi_url:
        :return: goods_id (类型str)
        '''
        is_juanpi_url = re.compile(r'http://shop.juanpi.com/deal/.*?').findall(juanpi_url)
        if is_juanpi_url != []:
            if re.compile(r'http://shop.juanpi.com/deal/(\d+).*?').findall(juanpi_url) != []:
                tmp_juanpi_url = re.compile(r'http://shop.juanpi.com/deal/(\d+).*?').findall(juanpi_url)[0]
                if tmp_juanpi_url != '':
                    goods_id = tmp_juanpi_url
                else:   # 只是为了在pycharm运行时不跳到chrome，其实else完全可以不要的
                    juanpi_url = re.compile(r';').sub('', juanpi_url)
                    goods_id = re.compile(r'http://shop.juanpi.com/deal/(\d+).*?').findall(juanpi_url)[0]
                print('------>>>| 得到的卷皮商品的地址为:', goods_id)
                return goods_id

        else:
            print('卷皮商品url错误, 非正规的url, 请参照格式(http://shop.juanpi.com/deal/)开头的...')
            return ''

    def __del__(self):
        try:
            del self.driver
            del self.result_data
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    juanpi = JuanPiParse()
    while True:
        juanpi_url = input('请输入待爬取的卷皮商品地址: ')
        juanpi_url.strip('\n').strip(';')
        goods_id = juanpi.get_goods_id_from_url(juanpi_url)
        juanpi.get_goods_data(goods_id=goods_id)
        data = juanpi.deal_with_data()
        # pprint(data)