# coding:utf-8

'''
@author = super_fazai
@File    : mia_parse.py
@Time    : 2018/1/13 10:57
@connect : superonesfazai@gmail.com
'''

"""
蜜芽页面采集系统
"""

from settings import IP_POOL_TYPE
from sql_str_controller import (
    mia_insert_str_1,
    mia_update_str_1,
    mia_update_str_4,
)
from multiplex_code import (
    _mia_get_parent_dir,
    get_db_commom_goods_update_params,
)
from my_exceptions import MiaSkusIsNullListException

from multiplex_code import (
    _get_right_model_data,
    CONTRABAND_GOODS_KEY_TUPLE,
)
from fzutils.data.str_utils import target_str_contain_some_char_check
from fzutils.spider.async_always import *

class MiaParse(Crawler):
    def __init__(self, is_real_times_update_call=False):
        super(MiaParse, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
        )
        self._set_headers()
        self.result_data = {}
        self.is_real_times_update_call = is_real_times_update_call
        if self.is_real_times_update_call:
            self.proxy_type = PROXY_TYPE_HTTPS
            # 不可太大，否则server采集时慢
            self.req_num_retries = 5
        else:
            # 提高server首次采集成功率
            self.proxy_type = PROXY_TYPE_HTTP
            self.req_num_retries = 2

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'm.mia.com',
            'Referer': 'https://m.mia.com/',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    def get_goods_data(self, goods_id):
        '''
        模拟构造得到data的url
        :param goods_id:
        :return: data dict类型
        '''
        if goods_id == '':
            return self._data_error_init()
        else:
            data = {}
            # 常规商品手机地址
            goods_url = 'https://m.mia.com/item-' + str(goods_id) + '.html'
            # 常规商品pc地址
            # goods_url = 'https://www.mia.com/item-' + str(goods_id) + '.html'
            print('------>>>| 待抓取的地址为: ', goods_url)

            body = Requests.get_url_body(
                url=goods_url,
                headers=self.headers,
                ip_pool_type=self.ip_pool_type,
                proxy_type=self.proxy_type,
                num_retries=self.req_num_retries,)
            # print(body)
            if body == '':
                return self._data_error_init()

            # 判断是否跳转，并得到跳转url, 跳转url的body, 以及is_hk(用于判断是否是全球购的商品)
            body, sign_direct_url, is_hk = self.get_jump_to_url_and_is_hk(body=body)
            # print(body)
            try:
                self.main_info_dict = self._get_goods_main_info_dict(goods_id=goods_id)
                data['title'], data['sub_title'] = self.get_title_and_sub_title(body=body)
                # print(data['title'], data['sub_title'])
                all_img_url = self.get_all_img_url()
                # pprint(all_img_url)

                p_info = self._get_p_info()
                data['p_info'] = p_info
                # pprint(p_info)

                # 获取每个商品的div_desc
                div_desc = self.get_goods_div_desc()
                # print(div_desc)
                assert div_desc != '', '获取到的div_desc为空值! 请检查'
                data['div_desc'] = div_desc

                sku_info = self.get_tmp_sku_info(body, goods_id, sign_direct_url, is_hk)
                assert sku_info != [], 'sku_info为空list'

                '''
                获取每个规格对应价格跟规格以及其库存
                '''
                true_sku_info, i_s = self.get_true_sku_info(sku_info=sku_info, goods_id=goods_id)
                data['price_info_list'] = true_sku_info
                # pprint(true_sku_info)

                # 设置detail_name_list
                data['detail_name_list'] = self.get_detail_name_list(true_sku_info=true_sku_info)
                # print(detail_name_list)

                '''单独处理all_img_url为[]的情况'''
                if all_img_url == []:
                    all_img_url = [{'img_url': true_sku_info[0].get('img_url')}]
                data['all_img_url'] = all_img_url
                # pprint(all_img_url)

                '''
                单独处理得到goods_url
                '''
                if sign_direct_url != '':
                    goods_url = sign_direct_url

                data['goods_url'] = goods_url
                data['parent_dir'] = _mia_get_parent_dir(p_info=p_info)
                data['is_delete'] = self._get_is_delete(price_info_list=data['price_info_list'])

            except MiaSkusIsNullListException as e:
                print('获取到的mia skus为空list !!')
                return self._data_error_init()

            except Exception as e:
                print('遇到错误如下:', e)
                return self._data_error_init()

            if data != {}:
                # pprint(data)
                self.result_data = data
                return data

            else:
                print('data为空!')
                return self._data_error_init()

    def _get_goods_main_info_dict(self, goods_id) -> dict:
        '''
        获取新版的goods的主信息
        :param goods_id:
        :return:
        '''
        headers = self._get_phone_headers()
        _t = str(datetime_to_timestamp(get_shanghai_time())) + str(get_random_int_number(100, 999))
        params = (
            ('_', _t),
            ('callback', 'ms_success_jsonpCallback'),
        )
        url = 'https://p.mia.com/item/info/{}'.format(goods_id)
        err_msg = '获取新版goods main info时出错!'
        try:
            body = Requests.get_url_body(
                url=url,
                headers=headers,
                params=params,
                cookies=None,
                proxy_type=self.proxy_type,
                ip_pool_type=self.ip_pool_type,
                num_retries=self.req_num_retries,)
            # print(body)
            data = json_2_dict(
                json_str=re.compile('\((.*)\)').findall(body)[0],
                default_res={})
            # pprint(data)
            assert data != {}, err_msg
        except IndexError:
            raise AssertionError(err_msg)

        return data

    @staticmethod
    def _get_phone_headers():
        return {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'User-Agent': get_random_phone_ua(),
            'Accept': '*/*',
            # 'Referer': 'https://m.mia.com/item-2946764.html',
            'Connection': 'keep-alive',
        }

    def deal_with_data(self):
        '''
        处理得到规范的data数据
        :return: result 类型 dict
        '''
        data = self.result_data
        if data != {}:
            shop_name = ''
            account = ''
            title = data['title']
            sub_title = data['sub_title']

            # 商品价格和淘宝价
            try:
                tmp_price_list = sorted([round(float(item.get('detail_price', '')), 2) for item in data['price_info_list']])
                price = tmp_price_list[-1]
                taobao_price = tmp_price_list[0]
            except IndexError:
                return self._data_error_init()

            detail_name_list = data['detail_name_list']
            price_info_list = data['price_info_list']
            all_img_url = data['all_img_url']
            p_info = data['p_info']
            div_desc = data['div_desc']
            is_delete = data['is_delete']
            parent_dir = data['parent_dir']
            schedule = []
            if target_str_contain_some_char_check(
                    target_str=title,
                    check_char_obj=CONTRABAND_GOODS_KEY_TUPLE):
                print('违禁物品下架...')
                is_delete = 1
            else:
                pass

            result = {
                'goods_url': data['goods_url'],         # goods_url
                'shop_name': shop_name,                 # 店铺名称
                'account': account,                     # 掌柜
                'title': title,                         # 商品名称
                'sub_title': sub_title,                 # 子标题
                'price': price,                         # 商品价格
                'taobao_price': taobao_price,           # 淘宝价
                # 'goods_stock': goods_stock,            # 商品库存
                'detail_name_list': detail_name_list,   # 商品标签属性名称
                'price_info_list': price_info_list,     # 要存储的每个标签对应规格的价格及其库存
                'all_img_url': all_img_url,             # 所有示例图片地址
                'p_info': p_info,                       # 详细信息标签名对应属性
                'div_desc': div_desc,                   # div_desc
                'is_delete': is_delete,                 # 用于判断商品是否已经下架
                'schedule': schedule,
                'parent_dir': parent_dir,
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

    def _get_is_delete(self, price_info_list):
        '''
        是否下架
        :param price_info_list:
        :return:
        '''
        all_num = 0
        for i in price_info_list:
            all_num += i.get('rest_number', 0)

        is_delete = 0 if all_num != 0 else 1

        return is_delete

    def _to_right_and_update_data(self, data, pipeline):
        '''
        实时更新数据
        :param data:
        :param pipeline:
        :return:
        '''
        tmp = _get_right_model_data(data, site_id=31, logger=self.lg)
        params = get_db_commom_goods_update_params(item=tmp)
        base_sql_str = mia_update_str_4
        if tmp['delete_time'] == '':
            sql_str = base_sql_str.format('shelf_time=%s', '')
        elif tmp['shelf_time'] == '':
            sql_str = base_sql_str.format('delete_time=%s', '')
        else:
            sql_str = base_sql_str.format('shelf_time=%s,', 'delete_time=%s')

        res = pipeline._update_table(sql_str=sql_str, params=params)

        return res

    def _get_p_info(self, **kwargs) -> list:
        ori_p_dict = self.main_info_dict.get('property_list', {})
        p_info = []
        for key, value in ori_p_dict.items():
            p_info.append({
                'p_name': key,
                'p_value': value,
            })
        assert p_info != [], '获取到的tmp_p_info为空值, 请检查!'

        return p_info

    def _data_error_init(self):
        self.result_data = {}
        self.main_info_dict = {}

        return {}

    def _set_detail_price_to_miaosha_price(self, tmp):
        '''
        将detail_price设置为miaosha_price
        :param tmp:
        :return:
        '''
        # 将detail_price设置为秒杀价, 使其提前能购买
        price = tmp['price']                # Decimal
        taobao_price = tmp['taobao_price']  # Decimal
        price_info_list = tmp['price_info_list']
        for item in price_info_list:
            # if float(price) == float(item.get('detail_price')):   # 不对比, 直接设置 set detail_price = taobao_price
            if item.get('detail_price', '') != '':
                item['detail_price'] = str(float(taobao_price))

        tmp['price_info_list'] = price_info_list

        return tmp

    def insert_into_mia_xianshimiaosha_table(self, data, pipeline) -> bool:
        try:
            tmp = _get_right_model_data(data=data, site_id=20)  # 采集来源地(蜜芽秒杀商品)
        except:
            print('此处抓到的可能是蜜芽秒杀券所以跳过')
            return False

        tmp = self._set_detail_price_to_miaosha_price(tmp=tmp)
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_insert_miaosha_params(item=tmp)
        res = pipeline._insert_into_table(sql_str=mia_insert_str_1, params=params)

        return res

    def update_mia_xianshimiaosha_table(self, data, pipeline) -> (bool,):
        try:
            tmp = _get_right_model_data(data=data, site_id=20)
        except:
            print('此处抓到的可能是蜜芽秒杀券所以跳过')
            return False

        tmp = self._set_detail_price_to_miaosha_price(tmp=tmp)
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_update_miaosha_params(item=tmp)
        res = pipeline._update_table(sql_str=mia_update_str_1, params=params)

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
            item['pid'],
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
            dumps(item['miaosha_time'], ensure_ascii=False),
            item['miaosha_begin_time'],
            item['miaosha_end_time'],
            item['parent_dir'],

            item['goods_id'],
        )

        return params

    def get_jump_to_url_and_is_hk(self, body):
        '''
        得到跳转地址和is_hk
        :param body: 待解析的url的body
        :return: (body, sign_direct_url, is_hk) | 类型: str, str, boolean
        '''
        is_hk = False
        sign_direct_url = ''
        if re.compile(r'_sign_direct_url = ').findall(body) != []:  # 表明是跳转，一般会出现这种情况的是拼团商品
            # 出现跳转时
            try:
                sign_direct_url = re.compile("_sign_direct_url = \'(.*?)\'").findall(body)[0]
                print('*** 获取到跳转地址为: ', sign_direct_url)
            except IndexError:
                sign_direct_url = ''
                print('获取跳转的地址时出错!')

            if sign_direct_url != '':
                body = Requests.get_url_body(
                    url=sign_direct_url,
                    headers=self.headers,
                    ip_pool_type=self.ip_pool_type,
                    proxy_type=self.proxy_type,
                    num_retries=self.req_num_retries,)
                try:
                    _ = re.compile(r'://m.miyabaobei.hk/').findall(sign_direct_url)[0]
                    # 表示为全球购商品
                    print('*** 此商品为全球购商品!')
                    is_hk = True
                except IndexError:
                    pass
            else:
                pass
        else:
            pass

        return (body, sign_direct_url, is_hk)

    def get_title_and_sub_title(self, body):
        '''
        得到给与body的title, sub_title
        :param body:
        :return: title, sub_title
        '''
        # pprint(self.main_info_dict)
        try:
            title = re.compile('bfd_name: \"(.*?)\",').findall(body)[0]
        except IndexError:
            title = self.main_info_dict.get('brand_name', '') + self.main_info_dict.get('name', '')

        assert title != '', 'title不为空值!'
        # print(title)

        sub_title = self.main_info_dict.get('name_added', '')
        # print(sub_title)

        return (self._wash_sensitive_info(title), self._wash_sensitive_info(sub_title))

    def _wash_sensitive_info(self, target):
        replace_str_list = [
            ('蜜芽', '优秀网'),
            ('mia', 'yiuxiu'),
        ]

        return wash_sensitive_info(
            data=target,
            replace_str_list=replace_str_list,
            is_default_filter=True,)

    def get_all_img_url(self) -> list:
        '''
        得到all_img_url
        :return:
        '''
        _ = self.main_info_dict.get('top_pictures', [])
        assert _ != [], 'top_pictures为空list!'
        all_img_url = [{
            'img_url': item.get('local_url', '')
        } for item in _]
        assert all_img_url != [], 'all_img_url为空list!'

        return all_img_url

    def get_goods_div_desc(self):
        '''
        得到对应商品的div_desc
        :param body:
        :return: str or ''
        '''
        div_desc_img_list = self.main_info_dict.get('foot_pictures', [])
        assert div_desc_img_list != [], 'div_desc_img_list为空list'
        # r'<img src="{}" style="height:auto;width:100%;"/>'.format(item)
        div_desc = ''
        if len(div_desc_img_list) == 2:
            # 表示无div_desc, 为其默认的官方图
            return '<div></div>'

        for item in div_desc_img_list[:-2]: # 最后两张图不取
            img_url = item.get('local_url', '')
            if img_url != '':
                div_desc += r'<img src="{}" style="height:auto;width:100%;"/>'.format(img_url)

        if div_desc != '':
            div_desc = '<div>' + div_desc + '</div>'

        return div_desc

    def get_detail_name_list(self, true_sku_info):
        '''
        得到detail_name_list
        :param i_s:
        :param true_sku_info:
        :return:
        '''
        # pprint(true_sku_info)
        img_here = 0
        try:
            if true_sku_info[0].get('img_url', '') != '':
                img_here = 1
        except IndexError:
            pass

        detail_name_list = [{'spec_name': '可选', 'img_here': img_here}]
        try:
            spec_value = true_sku_info[0].get('spec_value', '')
            # print(spec_value)
            count = spec_value.count('|')    # 无: 值为-1
            # print(count)
            if count == 0:
                pass
            elif count == 1:
                detail_name_list.append({
                    'spec_name': '规格',
                    'img_here': 0,
                })
            elif count == 2:
                detail_name_list.append({
                    'spec_name': '规格',
                    'img_here': 0,
                })
                detail_name_list.append({
                    'spec_name': '套餐',
                    'img_here': 0,
                })
            else:
                raise AssertionError('detail_name_list未知规格属性!')
        except IndexError:
            return []

        return detail_name_list

    def get_tmp_sku_info(self, *param):
        '''
        获取每个规格的goods_id，跟规格名，以及img_url, 用于后面的处理
        :param param:
        :return: sku_info 类型：{} 空字典表示出错 | [{...}, {...}]
        '''
        body = param[0]
        goods_id = param[1]
        sign_direct_url = param[2]
        is_hk = param[3]

        # 颜色规格等
        # var sku_list_info =
        # pc版没有sku_list_info，只在phone的html界面中才有这个
        # tmp_sku_info = re.compile('var sku_list_info = (.*?);sku_list_info = ').findall(body)[0]
        # # print(tmp_sku_info)
        #
        # try:
        #     # 看起来像json但是实际不是就可以这样进行替换，再进行json转换
        #     tmp_sku_info = str(tmp_sku_info).strip("'<>() ").replace('\'', '\"')
        #
        #     tmp_sku_info = json_2_dict(
        #         json_str=tmp_sku_info,
        #         default_res={})
        #     assert tmp_sku_info != {}, 'tmp_sku_info不为空dict!'
        #     # print(tmp_sku_info)   # None
        # except Exception as e:
        #     print(e)
        #     return self._data_error_init()

        # tmp_sku_info = [{'goods_id': item.get('id'), 'color_name': item.get('code_color')} for item in tmp_sku_info.values()]
        # pprint(tmp_sku_info)

        # pprint(self.main_info_dict)
        skus = self.main_info_dict.get('sale_property', {}).get('skus', [])
        # 处理skus为空dict
        skus = [] if isinstance(skus, dict) and skus == {} else skus
        com = self._get_com()
        # pprint(skus)
        if skus == []:
            raise MiaSkusIsNullListException
        else:
            pass

        tmp_sku_info = []
        # 先处理skus中的多规格
        for item in skus:
            spec_value = ''
            for key, value in item.items():
                try:
                    int(key)
                    if spec_value == '':
                        spec_value += value
                    else:
                        spec_value += '|{}'.format(value)
                except Exception as e:
                    # print(e)
                    continue

            # 无com
            tmp_sku_info.append({
                'goods_id': str(item.get('item_id', '')),
                'color_name': spec_value,
            })
        # pprint(tmp_sku_info)

        # 再处理com中的多规格
        # pprint(com)
        if com != []:
            # 存储已有的规格
            tmp_spec_value_list = []
            tmp_sku_info2 = []
            for item in tmp_sku_info:
                for item2 in com:
                    # tmp_sku_info中的子元素, 即每次重置
                    spec_value = item.get('color_name', '')

                    item_amount = str(item2.get('item_amount', ''))
                    item_unit = str(item2.get('item_unit', ''))
                    item2_goods_id = str(item2.get('spu_id', ''))
                    # eg: 2罐
                    item2_spec_value = item_amount + item_unit
                    # print(item2_spec_value)
                    if item2_spec_value not in tmp_spec_value_list:
                        spec_value += '|{}'.format(item_amount + item_unit)
                        # print(spec_value)

                        tmp_sku_info2.append({
                            'goods_id': item2_goods_id,
                            'color_name': spec_value,
                        })
                        tmp_spec_value_list.append(item2_spec_value)
                    else:
                        break

            tmp_sku_info = tmp_sku_info2
        else:
            pass
        # pprint(tmp_sku_info)

        sku_info = []
        for item in tmp_sku_info:
            # todo 由于mia pc站已不提供, 都被跳转到m站
            if is_hk is True:
                # tmp_url = 'https://www.miyabaobei.hk/item-' + str(goods_id) + '.html'
                tmp_url = 'https://m.miyabaobei.hk/item-' + str(goods_id) + '.html'

            else:
                # tmp_url = 'https://www.mia.com/item-' + item.get('goods_id') + '.html'
                tmp_url = 'https://m.mia.com/item-' + item.get('goods_id') + '.html'

            # print(tmp_url)
            tmp_body = Requests.get_url_body(
                url=tmp_url,
                headers=self.headers,
                had_referer=True,
                ip_pool_type=self.ip_pool_type,
                proxy_type=self.proxy_type,
                num_retries=self.req_num_retries,)
            # print(tmp_body)

            # 下面是pc版的匹配图
            # if sign_direct_url != '':
            #     # 下面由于html不规范获取不到img_url，所以采用正则
            #     # img_url = Selector(text=body).css('div.big.rel img::attr("src")').extract_first()
            #     img_url = re.compile(r'<div class="big rel"><img src="(.*?)"width=').findall(tmp_body)[0]
            #     # print(img_url)
            # else:
            #     img_url = re.compile(r'normal_pic_src = "(.*?)"').findall(tmp_body)[0]

            # 改用m站, 获取首图
            img_url = re.compile(';var imgurl = \'(.*?)\' \|\|').findall(tmp_body)[0]

            sku_info.append({
                'goods_id': item.get('goods_id'),
                'color_name': item.get('color_name'),
                'img_url': img_url,
            })
            sleep(.1)
        # pprint(sku_info)

        return sku_info

    def _get_com(self) -> list:
        '''
        第三类规格获取
        :return:
        '''
        com = self.main_info_dict.get('com', [])
        if isinstance(com, dict):
            # 由于com可能为{}
            if com == {}:
                com = []
            else:
                raise AssertionError('未知异常, 请检查!')
        else:
            pass

        return com

    def _get_replenishment_status(self, goods_id) -> bool:
        """
        获取某goods_id是否为缺货状态!
        :param goods_id:
        :return: True 缺货状态
        """
        headers = self._get_pc_headers()
        data = dumps({
            'count': '1',
            # 'size': 'SINGLE',
            'id': goods_id,
        })
        url = 'https://www.mia.com/instant/cart/addToCart'
        body = Requests.get_url_body(
            method='post',
            url=url,
            headers=headers,
            data=data,
            proxy_type=self.proxy_type,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.req_num_retries,)
        # print(body)
        msg = json_2_dict(
            json_str=body,
            default_res={}).get('msg', '')
        # print("add to cart返回的msg: {}".format(msg))

        if msg == '商品正在努力上架中'\
                or msg == '错误的商品规格':
            return True
        else:
            return False

    @staticmethod
    def _get_pc_headers():
        return {
            'Origin': 'https://www.mia.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'User-Agent': get_random_pc_ua(),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }

    def get_true_sku_info(self, sku_info, goods_id):
        '''
        获取每个规格对应价格跟规格以及其库存
        :param sku_info:
        :return: {} 空字典表示出错 | (true_sku_info, i_s)
        '''
        skus = self.main_info_dict.get('sale_property', {}).get('skus', [])
        assert skus != [], 'skus不为空list!'
        # pprint(skus)
        goods_id_str = '-'.join([item.get('goods_id', '') for item in sku_info])

        # print(goods_id_str)
        tmp_url = 'https://p.mia.com/item/list/{}'.format(goods_id_str)
        # print(tmp_url)

        tmp_body = Requests.get_url_body(
            url=tmp_url,
            headers=self.headers,
            had_referer=True,
            ip_pool_type=self.ip_pool_type,
            proxy_type=self.proxy_type,
            num_retries=self.req_num_retries,)
        # print(tmp_body)

        tmp_data = json_2_dict(json_str=tmp_body, default_res={}).get('data', [])
        assert tmp_data != [], 'tmp_data不为空list!'
        # pprint(tmp_data)

        true_sku_info = []
        i_s = {}
        for item_1 in sku_info:
            for item_2 in tmp_data:
                if item_1.get('goods_id') == str(item_2.get('id', '')):
                    i_s = item_2.get('i_s', {})
                    # print(i_s)
                    for item_3 in i_s.keys():
                        tmp = {}
                        spec_value = item_1.get('color_name', '')

                        normal_price = str(item_2.get('mp'))
                        detail_price = str(item_2.get('sp'))
                        img_url = item_1.get('img_url')
                        rest_number = i_s.get(item_3)
                        if rest_number == 0:
                            pass
                        else:
                            tmp['spec_value'] = spec_value
                            tmp['normal_price'] = normal_price
                            tmp['detail_price'] = detail_price
                            tmp['img_url'] = img_url
                            tmp['rest_number'] = rest_number
                            true_sku_info.append(tmp)

        return (true_sku_info, i_s)

    def get_goods_id_from_url(self, mia_url):
        '''
        得到goods_id
        :param mia_url:
        :return: goods_id (类型str)
        '''
        mia_url = re.compile(r';').sub('', mia_url)
        is_mia_irl = re.compile(r'mia.com/item|miyabaobei.hk/item').findall(mia_url)
        if is_mia_irl != []:
            try:
                goods_id = re.compile(r'item-(\d+).html.*?').findall(mia_url)[0]
                print('------>>>| 得到的蜜芽商品的地址为:', goods_id)
                assert goods_id != '', 'goods_id为空值!'
            except (IndexError, AssertionError):
                return ''

            return goods_id
        else:
            print('蜜芽商品url错误, 非正规的url, 请参照格式(https://www.mia.com/item-)开头的...')
            return ''

    def __del__(self):
        collect()

if __name__ == '__main__':
    mia = MiaParse()
    while True:
        mia_url = input('请输入待爬取的蜜芽商品地址: ')
        mia_url.strip('\n').strip(';')
        goods_id = mia.get_goods_id_from_url(mia_url)
        mia.get_goods_data(goods_id=goods_id)
        data = mia.deal_with_data()
        pprint(data)