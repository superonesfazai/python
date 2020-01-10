# coding:utf-8

'''
@author = super_fazai
@File    : jumeiyoupin_pintuan_parse.py
@Time    : 2018/3/24 09:33
@connect : superonesfazai@gmail.com
'''

"""
聚美优品拼团页面解析类
"""

from settings import (
    MY_SPIDER_LOGS_PATH,
    PHANTOMJS_DRIVER_PATH,
    IP_POOL_TYPE,)

from sql_str_controller import (
    jm_insert_str_2,
    jm_update_str_2,
    jm_update_str_3,)

from multiplex_code import (
    _get_right_model_data,
    CONTRABAND_GOODS_KEY_TUPLE,
)

from fzutils.data.str_utils import target_str_contain_some_char_check
from fzutils.spider.fz_aiohttp import AioHttp
from fzutils.spider.async_always import *

class JuMeiYouPinPinTuanParse(Crawler):
    def __init__(self, logger=None):
        super(JuMeiYouPinPinTuanParse, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            logger=logger,
            log_save_path=MY_SPIDER_LOGS_PATH + '/聚美优品/拼团/',
            
            is_use_driver=True,
            driver_executable_path=PHANTOMJS_DRIVER_PATH,
        )
        self._set_headers()
        self.result_data = {}
        self.msg = ''

    def _set_headers(self):
        self.headers = get_random_headers(
            upgrade_insecure_requests=False,
        )
        self.headers.update({
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Host': 's.h5.jumei.com',
            'Referer': 'https://s.h5.jumei.com/yiqituan/detail?item_id=ht180321p2453550t4&type=global_deal',
            'X-Requested-With': 'XMLHttpRequest',
        })

    async def get_goods_data(self, jumei_pintuan_url):
        '''
        异步模拟得到原始data
        :param goods_id:
        :return:
        '''
        goods_id = await self.get_goods_id_from_url(jumei_pintuan_url)
        if goods_id == []:
            return await self._data_error()

        '''
        原先采用requests被过滤无返回结果, 于是用AioHttp无奈速度过慢, 换用phantomjs
        '''
        # 拼团商品手机地址
        goods_url = 'https://s.h5.jumei.com/yiqituan/detail?item_id={0}&type={1}'.format(goods_id[0], goods_id[1])
        self.msg = '------>>>| 对应手机端地址为: ' + goods_url
        self.lg.info(self.msg)

        #** 获取ajaxDetail请求中的数据
        tmp_url = 'https://s.h5.jumei.com/yiqituan/ajaxDetail?item_id={0}&type={1}'.format(str(goods_id[0]), [goods_id[1]][0])
        # self.headers['Referer'] = goods_url
        # params = {
        #     'item_id': str(goods_id[0]),
        #     'type': [goods_id[1]][0],
        # }
        # body = await AioHttp.aio_get_url_body(url=tmp_url, headers=self.headers, params=params, timeout=JUMEIYOUPIN_PINTUAN_GOODS_TIMEOUT)
        # # 获取原始url的tmp_body
        # tmp_body = await AioHttp.aio_get_url_body(url=goods_url, headers=self.headers, timeout=JUMEIYOUPIN_PINTUAN_GOODS_TIMEOUT)
        # # print(tmp_body)

        '''
        换用phantomjs
        '''
        body = self.driver.get_url_body(
            url=tmp_url,
            timeout=25,)
        # print(body)
        try:
            body = re.compile('<pre .*?>(.*)</pre>').findall(body)[0]
            # print(body)
        except IndexError:
            body = ''
        tmp_body = self.driver.get_url_body(url=goods_url)
        # print(tmp_body)

        if body == '' or tmp_body == '':
            self.msg = '获取到的body为空str!' + ' 出错地址: ' + goods_url
            self.lg.error(self.msg)
            return await self._data_error()

        data = await self.json_2_dict(json_str=body)
        if data == {}:
            self.msg = '出错地址: ' + goods_url
            self.lg.error(self.msg)
            return await self._data_error()

        data = await self.wash_data(data=data)
        data = data.get('data', {})
        # pprint(data)
        try:
            data['title'] = await self._get_title(data=data)
            data['sub_title'] = await self._get_sub_title(data=data)
            data['shop_name'] = await self._get_shop_name(data=data)
            data['all_img_url'] = await self.get_all_img_url(data=data)
            data['p_info'] = await self.get_p_info(body=tmp_body)

            div_desc = await self.get_div_desc(body=tmp_body)
            div_desc = await AioHttp.wash_html(div_desc)
            # print(div_desc)
            data['div_desc'] = div_desc

            # 上下架时间(拼团列表数据接口里面有这里先不获取)
            detail_name_list = await self.get_detail_name_list(
                size_attr=data.get('buy_alone', {}).get('size_attr', []))
            data['detail_name_list'] = detail_name_list
            true_sku_info = await self.get_true_sku_info(
                buy_alone_size=data.get('buy_alone', {}).get('size', []),
                size=data.get('size', []),
                group_single_price=data.get('group_single_price', ''),
                detail_name_list_len=len(detail_name_list))
            data['price_info_list'] = true_sku_info
            data['is_delete'] = await self.get_is_delete(product_status=data.get('product_status', ''), true_sku_info=true_sku_info)
            data['all_sell_count'] = await self._get_all_sell_count(data)
            data['goods_url'] = goods_url
        except Exception as e:
            self.msg = '遇到错误如下: ' + str(e) + ' 出错地址: ' + goods_url
            self.lg.error(self.msg, exc_info=True)
            return await self._data_error()

        # pprint(data)
        self.result_data = data
        return data

    async def _get_all_sell_count(self, data):
        all_sell_count = data.get('buyer_number_text', '')
        if all_sell_count != '':
            all_sell_count = re.compile(r'(\d+\.?\d*)').findall(all_sell_count)[0]
            is_W = re.compile(r'万').findall(all_sell_count)
            if is_W != []:
                all_sell_count = str(int(float(all_sell_count) * 10000))
        else:
            all_sell_count = '0'

        return all_sell_count

    async def _get_shop_name(self, data):
        shop_name = ''
        if data.get('shop_info') != []:
            shop_name = data.get('shop_info', {}).get('store_title', '')

        return shop_name

    async def _get_sub_title(self, data):
        sub_title = ''
        if len(data.get('buy_alone', {})) != 1:
            sub_title = data.get('buy_alone', {}).get('name', '')
            sub_title = re.compile(r'聚美').sub('', sub_title)

        return sub_title

    async def _get_title(self, data):
        title = data.get('share_info', [])[1].get('text', '')
        title = re.compile('聚美').sub('', title)
        assert title != '', '获取到的title为空值, 请检查!'

        return title

    async def deal_with_data(self, jumei_pintuan_url) -> dict:
        '''
        得到规范数据并处理
        :return:
        '''
        data = await self.get_goods_data(jumei_pintuan_url=jumei_pintuan_url)
        if data != {}:
            shop_name = data['shop_name']
            account = ''
            title = data['title']
            sub_title = data['sub_title']
            # 商品价格和淘宝价
            try:
                tmp_price_list = sorted([round(float(item.get('pintuan_price', '')), 2) for item in data['price_info_list']])
                price = tmp_price_list[-1]  # 商品价格
                taobao_price = tmp_price_list[0]  # 淘宝价
            except IndexError:
                self.msg = '获取price or taobao_price时出错请检查!' + ' 出错地址: ' + data['goods_url']
                self.lg.error(self.msg)
                return await self._data_error()

            detail_name_list = data['detail_name_list']
            price_info_list = data['price_info_list']
            all_img_url = data['all_img_url']
            p_info = data['p_info']
            div_desc = data['div_desc']
            is_delete = data['is_delete']
            if target_str_contain_some_char_check(
                    target_str=title,
                    check_char_obj=CONTRABAND_GOODS_KEY_TUPLE):
                self.lg.info('违禁物品下架...')
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
                'detail_name_list': detail_name_list,   # 商品标签属性名称
                'price_info_list': price_info_list,     # 要存储的每个标签对应规格的价格及其库存
                'all_img_url': all_img_url,             # 所有示例图片地址
                'p_info': p_info,                       # 详细信息标签名对应属性
                'div_desc': div_desc,                   # div_desc
                'all_sell_count': data['all_sell_count'], # 总销量
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
            try:
                self.msg = '待处理的data为空的dict, 该商品可能已经转移或者下架' + ' 出错地址: ' + data['goods_url']
                self.lg.error(self.msg)
            except KeyError:
                pass
            return {}

    async def _data_error(self):
        self.result_data = {}

        return {}

    async def insert_into_jumeiyoupin_pintuan_table(self, data, pipeline, logger) -> bool:
        '''
        存储数据
        :param data:
        :param pipeline:
        :param logger
        :return:
        '''
        try:
            tmp = _get_right_model_data(data=data, site_id=27, logger=self.lg)  # 采集来源地(聚美优品拼团商品)
        except:
            self.lg.error('此处抓到的可能是聚美优品拼团券所以跳过')
            return False
        self.msg = '------>>>| 待存储的数据信息为: |' + str(tmp.get('goods_id'))
        logger.info(self.msg)

        params = await self._get_db_insert_pintuan_params(item=tmp)
        try:
            pipeline._insert_into_table_2(sql_str=jm_insert_str_2, params=params, logger=logger)
            return True
        except Exception as e:
            logger.exception(e)
            return False

    async def update_jumeiyoupin_pintuan_table(self, data, pipeline, logger) -> bool:
        '''
        异步更新数据
        :param data:
        :param pipeline:
        :param logger:
        :return:
        '''
        try:
            tmp = _get_right_model_data(data=data, site_id=27, logger=self.lg)
        except:
            self.lg.error('此处抓到的可能是聚美优品拼团券所以跳过')
            return False
        # print('------>>> | 待存储的数据信息为: |', tmp)
        self.msg = '------>>>| 待存储的数据信息为: |' + str(tmp.get('goods_id'))
        logger.info(self.msg)

        params = await self._get_db_update_pintuan_params(item=tmp)
        try:
            pipeline._update_table_2(sql_str=jm_update_str_2, params=params, logger=logger)
            return True
        except Exception as e:
            logger.exception(e)
            return False

    async def update_jumeiyoupin_pintuan_table_2(self, data, pipeline, logger) -> bool:
        '''
        异步更新数据
        :param data:
        :param pipeline:
        :param logger:
        :return:
        '''
        try:
            tmp = _get_right_model_data(data=data, site_id=27, logger=self.lg)
        except:
            self.lg.error('此处抓到的可能是聚美优品拼团券所以跳过')
            return False
        # print('------>>> | 待存储的数据信息为: |', tmp)
        logger.info('------>>>| 待存储的数据信息为: ' + str(tmp.get('goods_id')))

        params = await self._get_db_update_pintuan_params_2(item=tmp)
        # pprint(params)
        try:
            result = pipeline._update_table_2(sql_str=jm_update_str_3, params=params, logger=logger)
            return result
        except Exception as e:
            logger.exception(e)
            return False

    async def _get_db_insert_pintuan_params(self, item) -> tuple:
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
            item['page'],
            item['sort'],
            item['tab'],

            item['site_id'],
            item['is_delete'],
        )

        return params

    async def _get_db_update_pintuan_params(self, item):
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

    async def _get_db_update_pintuan_params_2(self, item):
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
            item['all_sell_count'],

            item['goods_id'],
        )

        return params

    async def get_all_img_url(self, data):
        '''
        得到all_img_url
        :param data:
        :return:
        '''
        if len(data.get('buy_alone', {})) == 1:
            all_img_url = data.get('share_info', [])[1].get('image_url_set', {}).get('url', {}).get('800', '')
            if all_img_url == '':
                self.lg.error('all_img_url获取失败!')
                raise Exception
        else:
            all_img_url = data.get('buy_alone', {}).get('image_url_set', {}).get('single', {}).get('800', '')

        all_img_url = [{
            'img_url': all_img_url,
        }]

        return all_img_url

    async def get_p_info(self, body):
        '''
        得到p_info
        :param body:
        :return:
        '''
        p_info = []
        for item in list(Selector(text=body).css('ul.detail_arg li').extract()):
            p_name = str(Selector(text=item).css('span.arg_title::text').extract_first())
            p_value = str(Selector(text=item).css('span.arg_content::text').extract_first())
            p_info.append({
                'p_name': p_name,
                'p_value': p_value,
            })

        return p_info

    async def get_div_desc(self, body):
        '''
        获取div_desc
        :param body:
        :return:
        '''
        try:
            div_desc = str(Selector(text=body).css('section#detailImg').extract_first() or '')
        except:
            self.lg.error('获取到的div_desc出错,请检查!')
            raise Exception

        assert div_desc != ''
        div_desc = re.compile(r'src="http://p0.jmstatic.com/templates/jumei/images/baoxian_pop.jpg"').sub('', div_desc)

        return '<div>' + div_desc + '</div>'

    async def get_detail_name_list(self, size_attr):
        '''
        获取detail_name_list
        :param size_attr:
        :return:
        '''
        # pprint(size_attr)
        detail_name_list = []
        for item in size_attr:
            detail_name_list.append({
                'spec_name': item.get('title', ''),
                'img_here': 1 if int(item.get('show_sku_img')) == 1 else 0,  # show_sku_img原始数据为 '1' or '0'
            })

        if size_attr == []:
            # print('获取detail_name_list失败!')
            detail_name_list = [{
                'spec_name': '规格',
                'img_here': 0,
            }]

        return detail_name_list

    async def get_true_sku_info(self, **kwargs):
        '''
        获取每个规格对应价格跟库存
        :param kwargs:
        :return:
        '''
        buy_alone_size = kwargs.get('buy_alone_size')
        size = kwargs.get('size')
        detail_name_list_len = kwargs.get('detail_name_list_len', 0)
        try:
            # 单独购买价格
            group_single_price = re.compile(r'(\d+)').findall(kwargs.get('group_single_price'))[0]
        except IndexError:
            group_single_price = ''
        if size == []:
            self.lg.error('size为空[]')
            raise Exception

        # pprint(buy_alone_size)
        # pprint(size)
        if buy_alone_size == []:
            alone_size = []
        else:
            alone_size = [{
                # 'spec_value': item.get('name', '').replace(',', '|'),
                'spec_value': item.get('name', '').replace(',', '|') if detail_name_list_len > 1 else item.get('name', ''),
                'alone_price': item.get('jumei_price', '')
            } for item in buy_alone_size]

        true_sku_info = [{
            # 原先官方单规格无','分割
            # 'spec_value': item.get('name', '').replace(',', '|'),
            # 现增加单规格判断处理
            'spec_value': item.get('name', '').replace(',', '|') if detail_name_list_len > 1 else item.get('name', ''),
            'pintuan_price': item.get('jumei_price', ''),
            'detail_price': item.get('market_price', ''),
            'normal_price': '',
            'img_url': item.get('img', ''),
            'rest_number': int(item.get('stock', '0')),
        } for item in size]

        if alone_size != []:
            for item_1 in alone_size:
                for item_2 in true_sku_info:
                    if item_1.get('spec_value') == item_2.get('spec_value'):
                        item_2['detail_price'] = item_1['alone_price']

        else:
            # 拿单独购买价来设置detail_price
            for item in true_sku_info:      # alone_size为空，表示: 单独无法购买 可能出现小于拼团价的情况 eg: http://s.h5.jumei.com/yiqituan/detail?item_id=df1803156441482p3810742&type=jumei_pop&selltype=coutuanlist&selllabel=coutuan_home
                # item['detail_price'] = '单价模式无法购买'
                item['detail_price'] = group_single_price

            # # todo 为了避免cp显示异常
            # raise AssertionError('单价模式无法购买不进行采集该商品!')

        return true_sku_info

    async def get_is_delete(self, **kwargs):
        '''
        获取商品上下架状态
        :param params:
        :return:
        '''
        is_delete = 0
        product_status = kwargs.get('product_status', '')
        true_sku_info = kwargs.get('true_sku_info')

        all_stock = 0
        for item in true_sku_info:
            all_stock += item.get('rest_number', 0)
        if all_stock == 0: is_delete = 1            # 总库存为0
        if product_status == 'end': is_delete = 1   # 商品状态为end

        return is_delete

    async def wash_data(self, data):
        '''
        清洗数据
        :param data:
        :return:
        '''
        try:
            del data['data']['address_list']
            del data['data']['default_address']
            del data['data']['fen_qi']
            del data['data']['icon_tag']
            del data['data']['price_detail']
            del data['data']['recommend_data']
            del data['data']['recommend_group']
            # del data['data']['share_info']
            del data['data']['wechat_switches']
        except Exception:
            pass

        return data

    async def json_2_dict(self, json_str):
        '''
        异步json_2_dict
        :param json_str:
        :return: {} | {...}
        '''
        return json_2_dict(json_str=json_str, logger=self.lg)

    async def get_goods_id_from_url(self, jumei_url) -> list:
        '''
        得到goods_id
        :param jumei_url:
        :return: goods_id 类型list eg: [] 表示非法url | ['xxxx', 'type=yyyy']
        '''
        jumei_url = re.compile(r'http://').sub(r'https://', jumei_url)
        jumei_url = re.compile(r';').sub('', jumei_url)
        is_jumei_url = re.compile(r'https://s.h5.jumei.com/yiqituan/detail').findall(jumei_url)
        if is_jumei_url != []:
            if re.compile('$&').findall(jumei_url) == []:   # 先加个&再做re筛选
                jumei_url += '&'

            if re.compile(r'item_id=(\w+)&{1,}.*?').findall(jumei_url) != []:
                goods_id = re.compile(r'item_id=(\w+)&{1,}.*').findall(jumei_url)[0]
                try:
                    type = re.compile(r'&type=(.*?)&{1,}.*').findall(jumei_url)[0]
                except IndexError:
                    self.msg = '获取url的type时出错, 请检查!' + ' 出错地址: ' + jumei_url
                    self.lg.error(self.msg)
                    return []
                self.msg = '------>>>| 得到的聚美商品id为: ' + goods_id + ' type为: ' + type
                self.lg.info(self.msg)

                return [goods_id, type]
            else:
                self.msg = '获取goods_id时出错, 请检查!' + '出错地址:' + jumei_url
                self.lg.error(self.msg)
                return []

        else:
            self.msg = '聚美优品商品url错误, 非正规的url, 请参照格式(https://s.h5.jumei.com/yiqituan/detail)开头的...' + ' 出错地址: ' + jumei_url
            self.lg.error(self.msg)
            return []

    def __del__(self):
        try:
            del self.driver
            del self.lg
            del self.msg
        except:
            pass
        collect()

if __name__ == '__main__':
    jumei_pintuan = JuMeiYouPinPinTuanParse()
    while True:
        try:
            jumei_url = input('请输入待爬取的聚美优品商品地址: ')
            jumei_url.strip('\n').strip(';')
            loop = get_event_loop()
            result = loop.run_until_complete(jumei_pintuan.deal_with_data(jumei_url))
            pprint(result)
        except KeyboardInterrupt:
            print('\nKeyboardInterrupt')
            try: loop.close()
            except NameError: pass

