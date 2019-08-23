# coding:utf-8

'''
@author = super_fazai
@File    : chuchujie_9_9_parse.py
@Time    : 2018/2/23 10:36
@connect : superonesfazai@gmail.com
'''

"""
楚楚街9.9, 29.9, 49.9元商品页面解析系统
"""

from decimal import Decimal
import gc

from settings import (
    PHANTOMJS_DRIVER_PATH,
    IP_POOL_TYPE,)

from sql_str_controller import (
    cc_insert_str_1,
    cc_update_str_1,)

from multiplex_code import (
    _get_right_model_data,
)
from fzutils.spider.async_always import *

class ChuChuJie_9_9_Parse(Crawler):
    def __init__(self):
        super(ChuChuJie_9_9_Parse, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
            is_use_driver=True,
            driver_executable_path=PHANTOMJS_DRIVER_PATH)
        self.result_data = {}

    def get_goods_data(self, goods_id):
        '''
        模拟构造得到data的url
        :param goods_id:
        :return: data 类型dict
        '''
        if goods_id == '':
            return self._data_error()

        print('------>>>| 对应的手机端地址为: ', 'https://m.chuchujie.com/details/detail.html?id=' + goods_id)
        '''
        2. 改为解析pc端的商品页面数据
        '''
        tmp_url = 'http://wx.chuchujie.com/index.php?s=/WebProduct/product_detail/product_id/' + str(goods_id)

        # 开始常规requests有数据, 后面无数据, 改用phantomjs
        # headers = get_random_headers(user_agent_type=0,)
        # headers.update({
        #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #     'Host': 'api-product.chuchujie.com',
        #     'Origin': 'https://m.chuchujie.com',
        #     'Referer': 'https://m.chuchujie.com/details/detail.html?id=10016793335',
        # })
        # body = MyRequests.get_url_body(url=tmp_url, headers=self.headers, had_referer=True)
        
        body = self.driver.get_url_body(url=tmp_url)
        # print(body)
        if body == '':
            print('获取到的body为空str!')
            return self._data_error()

        data = {}
        try:
            data['title'] = Selector(text=body).css('div.zy_info_rt h3::text').extract_first() or ''
            assert data['title'] != '', 'title为空!'

            data['sub_title'] = ''
            data['shop_name'] = Selector(text=body).css('div.other.ft14.clearfix label b::text').extract_first() or ''
            data['all_img_url'] = self._get_all_img_url(body=body)
            data['p_info'] = []     # 由于获取的是pc端的对应没有p_info

            div_desc = Selector(text=body).css('div.s_two').extract_first() or ''
            assert div_desc != '', 'div_desc为空!请检查!'
            data['div_desc'] = div_desc

            detail_name_list = self._get_detail_name_list(body=body)
            data['detail_name_list'] = detail_name_list

            # 商品价格(原价)跟淘宝价格
            taobao_price = Selector(text=body).css('dl.detail p.price b::text').extract_first()
            price = Selector(text=body).css('dl.detail dd em.yjprice::text').extract_first()
            # print(taobao_price)
            # print(price)
            try:
                # 后面有'*' 是为了避免有价格为整数不是浮点类型的
                taobao_price = re.compile(r'(\d+\.{0,1}\d*)').findall(taobao_price)[0]
                price = re.compile(r'(\d+\.{0,1}\d*)').findall(price)[0]
            except IndexError:
                print('获取price失败,请检查!')
                raise IndexError

            assert taobao_price != '' or price != '', '获取到的taobao_price或者price为空值出错, 请检查!'

            taobao_price = Decimal(taobao_price).__round__(2)
            price = Decimal(price).__round__(2)
            # print('商品促销价为: ', taobao_price, ' 商品原价为: ', price)
            data['price'] = price
            data['taobao_price'] = taobao_price

            price_info_list = self.get_price_info_list(
                detail_name_list,
                body,
                price,
                taobao_price
            )
            # pprint(price_info_list)
            assert price_info_list != '', 'price_info_list为空值!'
            data['price_info_list'] = price_info_list
            data['is_delete'] = self._get_is_delete(body=body)

            self.result_data = data
            return data

        except Exception as e:
            print('遇到错误: ', e)
            return self._data_error()

    def deal_with_data(self) -> dict:
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
            is_delete = data['is_delete']

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
            return self._data_error()

    def _data_error(self) -> dict:
        self.result_data = {}

        return {}

    def _get_is_delete(self, body):
        is_delete = 0
        all_stock = int(Selector(text=body).css('dl.detail dd label em::text').extract_first())
        if all_stock == 0:
            is_delete = 1

        return is_delete

    def _get_all_img_url(self, body):
        return [{
            'img_url': item
        } for item in list(Selector(text=body).css('p.s_img label img::attr("src")').extract())]

    def _get_detail_name_list(self, body):
        detail_name_list = Selector(text=body).css('div.info-wd.bd-red dl.detail dt::text').extract()
        # pprint(detail_name_list)
        if len(detail_name_list) <= 1:
            detail_name_list = []
        else:
            detail_name_list = [{
                'spec_name': item,
                'img_here': 0,          # 楚楚街秒杀不显示图片
            } for item in detail_name_list[:-1]]

        return detail_name_list

    def insert_into_chuchujie_xianshimiaosha_table(self, data, pipeline) -> bool:
        try:
            tmp = _get_right_model_data(data=data, site_id=24)
        except:
            print('此处抓到的可能是楚楚街券所以跳过')
            return False

        # print('------>>> | 待存储的数据信息为: |', tmp)
        print('------>>>| 待存储的数据信息为: ', tmp.get('goods_id'))

        params = self._get_db_insert_miaosha_params(item=tmp)
        sql_str = cc_insert_str_1
        res = pipeline._insert_into_table(sql_str=sql_str, params=params)

        return res

    def update_chuchujie_xianshimiaosha_table(self, data, pipeline) -> bool:
        try:
            tmp = _get_right_model_data(data=data, site_id=24)
        except:
            print('此处抓到的可能是楚楚街券所以跳过')
            return False

        # print('------>>> | 待存储的数据信息为: |', tmp)
        print('------>>>| 待存储的数据信息为: ', tmp.get('goods_id'))

        params = self._get_db_update_miaosha_params(item=tmp)
        sql_str = cc_update_str_1
        res = pipeline._update_table(sql_str=sql_str, params=params)

        return res

    def _get_db_insert_miaosha_params(self, item):
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
            dumps(item['miaosha_time'], ensure_ascii=False),
            item['miaosha_begin_time'],
            item['miaosha_end_time'],
            item['gender'],
            item['page'],

            item['site_id'],
            item['is_delete'],
        )

        return params

    def _get_db_update_miaosha_params(self, item):
        params = (
            item['modify_time'],
            item['shop_name'],
            item['title'],
            # item['sub_title'],
            item['price'],
            item['taobao_price'],
            dumps(item['detail_name_list'], ensure_ascii=False),
            dumps(item['price_info_list'], ensure_ascii=False),
            dumps(item['all_img_url'], ensure_ascii=False),
            dumps(item['p_info'], ensure_ascii=False),
            item['div_desc'],
            item['is_delete'],
            # dumps(item['miaosha_time'], ensure_ascii=False),
            # item['miaosha_begin_time'],
            # item['miaosha_end_time'],

            item['goods_id'],
        )

        return params

    def get_price_info_list(self, *params):
        '''
        获取每个规格对应价格跟规格以及其库存
        :param params: 待传入的参数
        :return: '' 表示出错 | [] | [{}...]
        '''
        detail_name_list, body, price, taobao_price = params
        all_stock = int(Selector(text=body).css('dl.detail dd label em::text').extract_first())
        price_info_list = []
        if detail_name_list == []:
            pass

        elif len(detail_name_list) == 1:
            len_1_i_text_list = list(Selector(text=body).css('div.info-wd.bd-red dl.detail dd.tag i::text').extract())
            for item in len_1_i_text_list:
                tmp = {}
                spec_value = item

                if spec_value == '':
                    print('spec_value为空值, 请检查!')
                    price_info_list = ''
                    break
                    # raise Exception

                normal_price = str(price)
                detail_price = str(taobao_price)
                try:
                    rest_number = int(all_stock / len(len_1_i_text_list))   # 由于获取不到每个规格库存信息，所以先用总库存除以规格的数量
                except Exception:
                    print('rest_number获取失败, 请检查!')
                    raise Exception

                tmp['spec_value'] = spec_value
                tmp['normal_price'] = normal_price
                tmp['detail_price'] = detail_price
                tmp['img_url'] = ''  # 无图
                tmp['rest_number'] = rest_number
                price_info_list.append(tmp)

        else:  # detail_name_list > 1
            tmp_list = []       # 用来暂存规格
            for item in list(Selector(text=body).css('div.info-wd.bd-red dl.detail dd.tag').extract()):
                dd_i = tuple(Selector(text=item).css('i::text').extract())
                tmp_list.append(dd_i)

            # pprint(tmp_list)
            if len(tmp_list) == 2:
                # print('### detail_name_list ### 的len = 2')
                a, b = tmp_list

                for item_1 in a:
                    for item_2 in b:
                        tmp = {}
                        if item_1 == '' or item_2 == '':
                            print('spec_value为空值, 请检查!')
                            price_info_list = ''
                            break
                            # raise Exception
                        spec_value = str(item_1) + '|' + str(item_2)

                        normal_price = str(price)
                        detail_price = str(taobao_price)
                        rest_number = int(all_stock / (len(a) * len(b)))  # 由于获取不到每个规格库存信息，所以先用总库存除以规格的数量

                        tmp['spec_value'] = spec_value
                        tmp['normal_price'] = normal_price
                        tmp['detail_price'] = detail_price
                        tmp['img_url'] = ''  # 无图
                        tmp['rest_number'] = rest_number
                        price_info_list.append(tmp)

            elif len(tmp_list) == 3:
                print('### detail_name_list ### 的len >= 3')
                a, b, c = tmp_list

                for item_1 in a:
                    for item_2 in b:
                        for item_3 in c:
                            tmp = {}
                            if item_1 == '' or item_2 == '':
                                print('spec_value为空值, 请检查!')
                                price_info_list = ''
                                break
                                # raise Exception
                            spec_value = str(item_1) + '|' + str(item_2) + '|' + str(item_3)

                            normal_price = str(price)
                            detail_price = str(taobao_price)
                            rest_number = int(all_stock / (len(a) * len(b)))  # 由于获取不到每个规格库存信息，所以先用总库存除以规格的数量

                            tmp['spec_value'] = spec_value
                            tmp['normal_price'] = normal_price
                            tmp['detail_price'] = detail_price
                            tmp['img_url'] = ''  # 无图
                            tmp['rest_number'] = rest_number
                            price_info_list.append(tmp)

            else:
                print('### detail_name_list ### 的len >= 4, 出错!请检查!')
                raise Exception

        return price_info_list

    def get_goods_id_from_url(self, chuchujie_url):
        '''
        得到goods_id
        :param chuchujie_url:
        :return: str
        '''
        chuchujie_url = re.compile(r'http://').sub(r'https://', chuchujie_url)
        chuchujie_url = re.compile(r';').sub('', chuchujie_url)
        is_chuchujie_url = re.compile(r'https://wx.chuchujie.com/index.php').findall(chuchujie_url)
        if is_chuchujie_url != []:
            if re.compile(r'https://wx.chuchujie.com/index.php\?s=/WebProduct/product_detail/product_id/(\d+).*?').findall(chuchujie_url) != []:
                goods_id = re.compile(r'/product_id/(\d+).*?').findall(chuchujie_url)[0]
                # print(goods_id)
                print('------>>>| 得到的楚楚街商品id为:', goods_id)
                return goods_id
            else:
                print('获取goods_id时出错, 请检查!')
                return ''

        else:
            print('楚楚街商品url错误, 非正规的url, 请参照格式(https://wx.chuchujie.com/index.php?s=/WebProduct/product_detail/product_id/)开头的...')
            return ''

    def __del__(self):
        try:
            del self.driver
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    chuchujie_9_9 = ChuChuJie_9_9_Parse()
    while True:
        chuchujie_url = input('请输入待爬取的楚楚街商品地址: ')
        chuchujie_url.strip('\n').strip(';')
        goods_id = chuchujie_9_9.get_goods_id_from_url(chuchujie_url)
        data = chuchujie_9_9.get_goods_data(goods_id=goods_id)
        chuchujie_9_9.deal_with_data()
        # pprint(data)