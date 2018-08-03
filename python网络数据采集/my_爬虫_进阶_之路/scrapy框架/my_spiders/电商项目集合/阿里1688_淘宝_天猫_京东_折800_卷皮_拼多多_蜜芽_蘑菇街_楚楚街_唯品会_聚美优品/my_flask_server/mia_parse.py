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

import json
from pprint import pprint
from decimal import Decimal
from time import sleep
import re
import gc
from scrapy import Selector
from json import dumps

from fzutils.cp_utils import _get_right_model_data
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests
from fzutils.common_utils import json_2_dict

class MiaParse(object):
    def __init__(self):
        self._set_headers()
        self.result_data = {}

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
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            return {}
        else:
            data = {}
            # 常规商品手机地址
            goods_url = 'https://m.mia.com/item-' + str(goods_id) + '.html'
            # 常规商品pc地址
            # goods_url = 'https://www.mia.com/item-' + str(goods_id) + '.html'
            print('------>>>| 待抓取的地址为: ', goods_url)

            body = MyRequests.get_url_body(url=goods_url, headers=self.headers, had_referer=True)
            # print(body)

            if body == '':
                self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                return {}

            # 判断是否跳转，并得到跳转url, 跳转url的body, 以及is_hk(用于判断是否是全球购的商品)
            body, sign_direct_url, is_hk = self.get_jump_to_url_and_is_hk(body=body)

            try:
                # title, sub_title
                data['title'], data['sub_title'] = self.get_title_and_sub_title(body=body)

                # 获取所有示例图片
                all_img_url = self.get_all_img_url(goods_id=goods_id, is_hk=is_hk)
                if all_img_url == '':
                    self.result_data = {}
                    return {}

                '''
                获取p_info
                '''
                tmp_p_info = Selector(text=body).css('div.showblock div p').extract_first()

                if tmp_p_info == '':
                    print('获取到的tmp_p_info为空值, 请检查!')
                    self.result_data = {}
                    return {}
                else:
                    tmp_p_info = re.compile('<p>|</p>').sub('', tmp_p_info)
                    tmp_p_info = re.compile(r'<!--思源品牌，隐藏品牌-->').sub('', tmp_p_info)
                    p_info = [{'p_name': item.split('：')[0], 'p_value': item.split('：')[1]} for item in tmp_p_info.split('<br>') if item != '']

                # pprint(p_info)
                data['p_info'] = p_info

                # 获取每个商品的div_desc
                div_desc = self.get_goods_div_desc(body=body)

                if div_desc == '':
                    print('获取到的div_desc为空值! 请检查')
                    self.result_data = {}
                    return {}
                data['div_desc'] = div_desc

                '''
                获取每个规格的goods_id，跟规格名，以及img_url, 用于后面的处理
                '''
                sku_info = self.get_tmp_sku_info(body, goods_id, sign_direct_url, is_hk)
                if sku_info == {}:
                    return {}

                '''
                由于这个拿到的都是小图，分辨率相当低，所以采用获取每个goods_id的phone端地址来获取每个规格的高清规格图
                '''
                # # print(Selector(text=body).css('dd.color_list li').extract())
                # for item in Selector(text=body).css('dd.color_list li').extract():
                #     # print(item)
                #     try:
                #         # 该颜色的商品的goods_id
                #         color_goods_id = Selector(text=item).css('a::attr("href")').extract_first()
                #         # 该颜色的名字
                #         color_name = Selector(text=item).css('a::attr("title")').extract_first()
                #         # 该颜色的img_url
                #         color_goods_img_url = Selector(text=item).css('img::attr("src")').extract_first()
                #
                #         color_goods_id = re.compile('(\d+)').findall(color_goods_id)[0]
                #     except IndexError:      # 表示该li为这个tmp_url的地址 (单独处理goods_id)
                #         color_goods_id = goods_id
                #         color_name = Selector(text=item).css('a::attr("title")').extract_first()
                #         color_goods_img_url = Selector(text=item).css('img::attr("src")').extract_first()
                #     print(color_goods_id, ' ', color_name, ' ', color_goods_img_url)

                '''
                获取每个规格对应价格跟规格以及其库存
                '''
                if self.get_true_sku_info(sku_info=sku_info) == {}:     # 表示出错退出
                    self.result_data = {}
                    return {}
                else:                                                   # 成功获取
                    true_sku_info, i_s = self.get_true_sku_info(sku_info=sku_info)
                    data['price_info_list'] = true_sku_info
                # pprint(true_sku_info)

                # 设置detail_name_list
                data['detail_name_list'] = self.get_detail_name_list(i_s=i_s)
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

            except Exception as e:
                print('遇到错误如下: ', e)
                self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                return {}

            if data != {}:
                # pprint(data)
                self.result_data = data
                return data

            else:
                print('data为空!')
                self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
                return {}

    def deal_with_data(self):
        '''
        处理得到规范的data数据
        :return: result 类型 dict
        '''
        data = self.result_data
        if data != {}:
            # 店铺名称
            shop_name = ''

            # 掌柜
            account = ''

            # 商品名称
            title = data['title']

            # 子标题
            sub_title = data['sub_title']

            # 商品价格和淘宝价
            try:
                tmp_price_list = sorted([round(float(item.get('detail_price', '')), 2) for item in data['price_info_list']])
                price = Decimal(tmp_price_list[-1]).__round__(2)  # 商品价格
                taobao_price = Decimal(tmp_price_list[0]).__round__(2)  # 淘宝价
            except IndexError:
                self.result_data = {}
                return {}

            # 商品标签属性名称
            detail_name_list = data['detail_name_list']

            # 要存储的每个标签对应规格的价格及其库存
            price_info_list = data['price_info_list']

            # 所有示例图片地址
            all_img_url = data['all_img_url']

            # 详细信息标签名对应属性
            p_info = data['p_info']

            # div_desc
            div_desc = data['div_desc']

            # 用于判断商品是否已经下架
            is_delete = 0

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

    def insert_into_mia_xianshimiaosha_table(self, data, pipeline):
        try:
            tmp = _get_right_model_data(data=data, site_id=20)  # 采集来源地(蜜芽秒杀商品)
        except:
            print('此处抓到的可能是蜜芽秒杀券所以跳过')
            return None
        # print('------>>> | 待存储的数据信息为: |', tmp)
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_insert_miaosha_params(item=tmp)
        sql_str = 'insert into dbo.mia_xianshimiaosha(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, pid, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        pipeline._insert_into_table(sql_str=sql_str, params=params)

    def update_mia_xianshimiaosha_table(self, data, pipeline):
        try:
            tmp = _get_right_model_data(data=data, site_id=20)
        except:
            print('此处抓到的可能是蜜芽秒杀券所以跳过')
            return None
        # print('------>>> | 待存储的数据信息为: |', tmp)
        print('------>>>| 待存储的数据信息为: |', tmp.get('goods_id'))

        params = self._get_db_update_miaosha_params(item=tmp)
        sql_str = r'update dbo.mia_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s where goods_id = %s'
        pipeline._update_table(sql_str=sql_str, params=params)

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

            item['goods_id'],
        )

        return params

    def get_jump_to_url_and_is_hk(self, body):
        '''
        得到跳转地址和is_hk
        :param body: 待解析的url的body
        :return: (body, sign_direct_url, is_hk) | 类型: str, str, boolean
        '''
        if re.compile(r'_sign_direct_url = ').findall(body) != []:  # 表明是跳转，一般会出现这种情况的是拼团商品
            # 出现跳转时
            try:
                sign_direct_url = re.compile(r"_sign_direct_url = '(.*?)';").findall(body)[0]
                print('*** 获取到跳转地址为: ', sign_direct_url)
            except IndexError:
                sign_direct_url = ''
                print('获取跳转的地址时出错!')

            body = MyRequests.get_url_body(url=sign_direct_url, headers=self.headers, had_referer=True)

            if re.compile(r'://m.miyabaobei.hk/').findall(sign_direct_url) != []:
                # 表示为全球购商品
                print('*** 此商品为全球购商品!')
                is_hk = True
            else:
                is_hk = False

        else:
            is_hk = False
            sign_direct_url = ''

        return (body, sign_direct_url, is_hk)

    def get_title_and_sub_title(self, body):
        '''
        得到给与body的title, sub_title
        :param body:
        :return: title, sub_title
        '''
        # title
        # var google_tag_params =
        base_info = re.compile(r'var google_tag_params = (.*?);// ]]></script>').findall(body)[0]
        base_info = re.compile(r'//BFD商品页参数开始').sub('', base_info)
        # print(base_info)
        title = re.compile(r'bfd_name : "(.*?)"').findall(base_info)[0]
        # print(title)

        # 子标题
        try:
            sub_title = Selector(text=body).css('div.titleout div::text').extract_first()

            if sub_title is None:
                sub_title = Selector(text=body).css('div.descInfo::text').extract_first()

                if sub_title is None:
                    sub_title = ''
        except:
            sub_title = ''
        # print(sub_title)

        return (title, sub_title)

    def get_all_img_url(self, goods_id, is_hk):
        '''
        得到all_img_url
        :param goods_id:
        :param is_hk:
        :return:
        '''
        if is_hk is True:  # 全球购
            tmp_url_2 = 'https://www.miyabaobei.hk/item-' + str(goods_id) + '.html'
        else:
            tmp_url_2 = 'https://www.mia.com/item-' + str(goods_id) + '.html'

        tmp_body_2 = MyRequests.get_url_body(url=tmp_url_2, headers=self.headers, had_referer=True)
        # print(Selector(text=tmp_body_2).css('div.small').extract())

        if tmp_body_2 == '':
            print('请求tmp_body_2为空值, 此处先跳过!')
            return ''

        all_img_url = []
        for item in Selector(text=tmp_body_2).css('div.small img').extract():
            # print(item)
            tmp_img_url = Selector(text=item).css('img::attr("src")').extract_first()
            all_img_url.append({'img_url': tmp_img_url})

        return all_img_url

    def get_goods_div_desc(self, body):
        '''
        得到对应商品的div_desc
        :param body:
        :return: str or ''
        '''
        # 获取div_desc
        div_desc = Selector(text=body).css('div.showblock div.xq').extract_first()

        div_desc = re.compile('<!--香港仓特定下展图开始-->|<!--香港仓特定下展图结束-->').sub('', div_desc)
        div_desc = re.compile(r' src=".*?"').sub(' ', div_desc)
        div_desc = re.compile(r'data-src="').sub('src=\"', div_desc)
        # print(div_desc)

        return div_desc

    def get_detail_name_list(self, i_s):
        '''
        得到detail_name_list
        :param i_s:
        :return:
        '''
        if len(i_s) == 1 or len(i_s) == 0:
            detail_name_list = [{'spec_name': '可选'}]
        else:
            detail_name_list = [{'spec_name': '可选'}, {'spec_name': '规格'}]

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
        tmp_sku_info = re.compile('var sku_list_info = (.*?);sku_list_info = ').findall(body)[0]
        # print(tmp_sku_info)

        try:
            # 看起来像json但是实际不是就可以这样进行替换，再进行json转换
            tmp_sku_info = str(tmp_sku_info).strip("'<>() ").replace('\'', '\"')

            tmp_sku_info = json.loads(tmp_sku_info)
            # print(tmp_sku_info)
        except Exception as e:
            print('json.loads遇到错误如下: ', e)
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            return {}

        tmp_sku_info = [{'goods_id': item.get('id'), 'color_name': item.get('code_color')} for item in tmp_sku_info.values()]
        # pprint(tmp_sku_info)

        sku_info = []
        for item in tmp_sku_info:
            if is_hk is True:
                tmp_url = 'https://www.miyabaobei.hk/item-' + str(goods_id) + '.html'
            else:
                tmp_url = 'https://www.mia.com/item-' + item.get('goods_id') + '.html'

            tmp_body = MyRequests.get_url_body(url=tmp_url, headers=self.headers, had_referer=True)
            # print(tmp_body)

            if sign_direct_url != '':
                # 下面由于html不规范获取不到img_url，所以采用正则
                # img_url = Selector(text=body).css('div.big.rel img::attr("src")').extract_first()
                img_url = re.compile(r'<div class="big rel"><img src="(.*?)"width=').findall(tmp_body)[0]
                # print(img_url)
            else:
                img_url = re.compile(r'normal_pic_src = "(.*?)"').findall(tmp_body)[0]

            sku_info.append({
                'goods_id': item.get('goods_id'),
                'color_name': item.get('color_name'),
                'img_url': img_url,
            })
            sleep(.1)
            # pprint(sku_info)

        return sku_info

    def get_true_sku_info(self, sku_info):
        '''
        获取每个规格对应价格跟规格以及其库存
        :param sku_info:
        :return: {} 空字典表示出错 | (true_sku_info, i_s)
        '''
        goods_id_str = '-'.join([item.get('goods_id') for item in sku_info])
        # print(goods_id_str)
        tmp_url = 'https://p.mia.com/item/list/' + goods_id_str
        # print(tmp_url)

        tmp_body = MyRequests.get_url_body(url=tmp_url, headers=self.headers, had_referer=True)
        # print(tmp_body)

        tmp_data = json_2_dict(json_str=tmp_body).get('data', [])
        if tmp_data == []:
            self.result_data = {}
            return {}

        true_sku_info = []
        i_s = {}
        for item_1 in sku_info:
            for item_2 in tmp_data:
                if item_1.get('goods_id') == str(item_2.get('id', '')):
                    i_s = item_2.get('i_s', {})
                    # print(i_s)
                    for item_3 in i_s.keys():
                        tmp = {}
                        if item_3 == 'SINGLE':
                            spec_value = item_1.get('color_name')
                        else:
                            spec_value = item_1.get('color_name') + '|' + item_3
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
        is_mia_irl = re.compile(r'https://www.mia.com/item-.*?.html.*?').findall(mia_url)
        if is_mia_irl != []:
            if re.compile(r'https://www.mia.com/item-(\d+).html.*?').findall(mia_url) != []:
                tmp_mia_url = re.compile(r'https://www.mia.com/item-(\d+).html.*?').findall(mia_url)[0]
                if tmp_mia_url != '':
                    goods_id = tmp_mia_url
                else:   # 只是为了在pycharm运行时不跳到chrome，其实else完全可以不要的
                    mia_url = re.compile(r';').sub('', mia_url)
                    goods_id = re.compile(r'https://www.mia.com/item-(\d+).html.*?').findall(mia_url)[0]
                print('------>>>| 得到的蜜芽商品的地址为:', goods_id)
                return goods_id
        else:
            print('蜜芽商品url错误, 非正规的url, 请参照格式(https://www.mia.com/item-)开头的...')
            return ''

    def __del__(self):
        gc.collect()

if __name__ == '__main__':
    mia = MiaParse()
    while True:
        mia_url = input('请输入待爬取的蜜芽商品地址: ')
        mia_url.strip('\n').strip(';')
        goods_id = mia.get_goods_id_from_url(mia_url)
        data = mia.get_goods_data(goods_id=goods_id)
        mia.deal_with_data()