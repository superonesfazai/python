# coding:utf-8

'''
@author = super_fazai
@File    : vip_parse.py
@Time    : 2018/3/5 09:47
@connect : superonesfazai@gmail.com
'''

"""
唯品会常规商品页面解析系统(也可采集预售商品)
"""

import time
from random import randint
import json
import requests
import re
from pprint import pprint
from decimal import Decimal
from time import sleep
import datetime
import re
import gc
import pytz
from scrapy import Selector

from settings import HEADERS
from my_ip_pools import MyIpPools
from my_requests import MyRequests

class VipParse(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'm.vip.com',
            'Referer': 'https://m.vip.com/product-0-432603261.html?goodsId=432603261',
            'User-Agent': HEADERS[randint(0, 34)],  # 随机一个请求头
        }
        self.result_data = {}

    def get_goods_data(self, goods_id):
        '''
        模拟构造得到data的url
        :param goods_id: 类型 list
        :return: data dict类型
        '''
        if goods_id == []:
            self.result_data = {}
            return {}
        else:
            data = {}
            # 常规商品手机地址
            goods_url = 'https://m.vip.com/product-0-' + str(goods_id[1]) + '.html'
            print('------>>>| 待抓取的地址为: ', goods_url)

            body = MyRequests.get_url_body(url=goods_url, headers=self.headers, had_referer=True)
            # print(body)

            if body == '':
                self.result_data = {}
                return {}

            else:
                try:
                    tmp_data = re.compile(r'var _WAP_PAGE_CACHE = (.*?);</script>').findall(body)[0]
                    # print(tmp_data)
                except IndexError:
                    print('re匹配不到关键数据, 请检查!')
                    self.result_data = {}
                    return {}

                try:
                    tmp_data = json.loads(tmp_data)
                    # pprint(tmp_data)
                except Exception:
                    print('json.loads转换tmp_data时出错, 请检查!')
                    tmp_data = {}

                if tmp_data == {}:
                    self.result_data = {}
                    return {}
                else:
                    tmp_data = self.wash_data(data=tmp_data)
                    # pprint(tmp_data)

                    if tmp_data == {}:
                        self.result_data = {}
                        return {}
                    else:
                        try:
                            # title, sub_title
                            data['title'] = tmp_data.get('productSize', {}).get('product', {}).get('product_name', '')
                            data['sub_title'] = ''

                            if data['title'] == '':
                                print('获取到的title为空值, 请检查!')
                                raise Exception

                            # shop_name
                            data['shop_name'] = tmp_data.get('productSize', {}).get('product', {}).get('brand_name', '')

                            # 获取所有示例图片
                            all_img_url = tmp_data.get('productDetailImg', {}).get('img_pre', [])
                            if all_img_url == []:
                                print('获取到的all_img_url为空[], 请检查!')
                                raise Exception
                            else:
                                all_img_url = [{
                                    'img_url': 'https:' + item.get('b_img', '')
                                } for item in all_img_url]
                            # pprint(all_img_url)
                            data['all_img_url'] = all_img_url

                            # 获取p_info
                            p_info = self.get_p_info(tmp_data=tmp_data)
                            if p_info == []:
                                raise Exception
                            # pprint(p_info)
                            data['p_info'] = p_info

                            # 获取每个商品的div_desc
                            div_desc = self.get_goods_div_desc(tmp_data=tmp_data.get('productDetailImg', {}).get('detailImages', []))
                            if div_desc == '':
                                print('获取到的div_desc为空值! 请检查')
                                raise Exception
                            data['div_desc'] = div_desc

                            '''
                            上下架时间
                            '''
                            data['sell_time'] = tmp_data.get('sell_time', {})
                            if int(data['sell_time'].get('begin_time')) > int(time.time()):
                                # *** 先根据上下架时间来判断是否为预售商品，如果是预售商品就按预售商品的method来去对应规格的价格
                                goods_id = [1, goods_id[1]]     # 设置成预售的商品goods_id格式

                            # 设置detail_name_list
                            detail_name_list = self.get_detail_name_list(tmp_data=tmp_data)
                            # print(detail_name_list)
                            data['detail_name_list'] = detail_name_list

                            '''
                            获取每个规格对应价格跟规格以及库存
                            '''
                            true_sku_info = self.get_true_sku_info(goods_id=goods_id, tmp_data=tmp_data)
                            # pprint(true_sku_info)
                            if true_sku_info == []:     # 也可能是 表示没有库存, 买完或者下架
                                print('获取到的sku_info为空值, 请检查!')
                                print('*** 注意可能是卖完了，库存为0 导致!! ***')
                                # raise Exception
                                data['price_info_list'] = true_sku_info
                            else:
                                data['price_info_list'] = true_sku_info

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

            '''
            用于判断商品是否已经下架
            '''
            is_delete = 0
            all_rest_number = 0
            for item in price_info_list:
                all_rest_number += item.get('rest_number', 0)
            if all_rest_number == 0:
                is_delete = 1
            # 当官方下架时间< int(time.time()) 则商品已下架 is_delete = 1
            if int(data.get('sell_time', {}).get('end_time', '')) < int(time.time()):
                print('该商品已经过期下架...! 进行逻辑删除 is_delete=1')
                is_delete = 1
            # print(is_delete)

            # 上下架时间
            schedule = [{
                'begin_time': self.timestamp_to_regulartime(int(data.get('sell_time', {}).get('begin_time', ''))),
                'end_time': self.timestamp_to_regulartime(int(data.get('sell_time', {}).get('end_time', ''))),
            }]

            # 销售总量
            all_sell_count = ''

            # 商品价格和淘宝价
            # pprint(data['price_info_list'])
            try:
                tmp_price_list = sorted([round(float(item.get('detail_price', '')), 2) for item in data['price_info_list']])
                price = tmp_price_list[-1]  # 商品价格
                taobao_price = tmp_price_list[0]  # 淘宝价
            except IndexError:
                print('获取price和taobao_price时出错, 请检查!')  # 商品下架时, detail_price为空str, 所以会IndexError报错
                print('@@@@@@ 此处对该商品进行逻辑删除! @@@@@@')
                self.result_data = {}
                price = 0.
                taobao_price = 0.
                is_delete = 1
                # return {}

            result = {
                'shop_name': shop_name,                 # 店铺名称
                'account': account,                     # 掌柜
                'title': title,                         # 商品名称
                'sub_title': sub_title,                 # 子标题
                'price': price,                         # 商品价格
                'taobao_price': taobao_price,           # 淘宝价
                # 'goods_stock': goods_stock,           # 商品库存
                'detail_name_list': detail_name_list,   # 商品标签属性名称
                # 'detail_value_list': detail_value_list,# 商品标签属性对应的值
                'price_info_list': price_info_list,     # 要存储的每个标签对应规格的价格及其库存
                'all_img_url': all_img_url,             # 所有示例图片地址
                'p_info': p_info,                       # 详细信息标签名对应属性
                'div_desc': div_desc,                   # div_desc
                'schedule': schedule,                   # 商品特价销售时间段
                'all_sell_count': all_sell_count,       # 销售总量
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
            self.result_data = {}
            return result

        else:
            print('待处理的data为空的dict, 该商品可能已经转移或者下架')
            self.result_data = {}
            return {}

    def to_right_and_update_data(self, data, pipeline):
        '''
        更新商品数据
        :param data:
        :param pipeline:
        :return:
        '''
        data_list = data
        tmp = {}
        tmp['goods_id'] = data_list['goods_id']  # 官方商品id

        '''
        时区处理，时间处理到上海时间
        '''
        tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
        now_time = datetime.datetime.now(tz)
        # 处理为精确到秒位，删除时区信息
        now_time = re.compile(r'\..*').sub('', str(now_time))
        # 将字符串类型转换为datetime类型
        now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')

        tmp['modfiy_time'] = now_time  # 修改时间

        tmp['shop_name'] = data_list['shop_name']  # 公司名称
        tmp['title'] = data_list['title']  # 商品名称
        tmp['sub_title'] = data_list['sub_title']  # 商品子标题
        tmp['link_name'] = ''  # 卖家姓名
        tmp['account'] = data_list['account']  # 掌柜名称

        # 设置最高价price， 最低价taobao_price
        tmp['price'] = Decimal(data_list['price']).__round__(2)
        tmp['taobao_price'] = Decimal(data_list['taobao_price']).__round__(2)
        tmp['price_info'] = []  # 价格信息

        tmp['detail_name_list'] = data_list['detail_name_list']  # 标签属性名称

        """
        得到sku_map
        """
        tmp['price_info_list'] = data_list.get('price_info_list')  # 每个规格对应价格及其库存

        tmp['all_img_url'] = data_list.get('all_img_url')  # 所有示例图片地址

        tmp['p_info'] = data_list.get('p_info')  # 详细信息
        tmp['div_desc'] = data_list.get('div_desc')  # 下方div

        tmp['schedule'] = data_list.get('schedule')

        # 采集的来源地
        # tmp['site_id'] = 25  # 采集来源地(唯品会常规商品)

        tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1
        tmp['my_shelf_and_down_time'] = data_list.get('my_shelf_and_down_time')
        tmp['delete_time'] = data_list.get('delete_time')
        tmp['all_sell_count'] = str(data_list.get('all_sell_count'))

        pipeline.update_vip_table(item=tmp)

    def get_detail_name_list(self, tmp_data):
        '''
        得到detail_name_list
        :param tmp_data:
        :return: Exception 表示异常退出 | [xx, ...] 表示success
        '''
        detail_name_list = []
        multiColor = tmp_data.get('multiColor', {})
        # pprint(multiColor)
        productSku = tmp_data.get('productSize', {}).get('productSku', [])

        if multiColor == {} or productSku == []:
            print('获取detail_name_list失败, 请检查!')
            raise Exception
        else:
            if multiColor.get('items') is None:
                pass
            elif multiColor.get('items', []).__len__() == 1:
                pass
            else:
                detail_name_list.append({'spec_name': multiColor.get('name', '')})

            other_spec_name = productSku.get('name', '')
            if other_spec_name == '':
                print('获取detail_name_list失败, 原因other_spec_name为空值, 请检查!')
                raise Exception

            detail_name_list.append({'spec_name': other_spec_name})

        return detail_name_list

    def get_true_sku_info(self, goods_id, tmp_data):
        '''
        得到每个规格对应的库存, 价格, 图片等详细信息
        :param tmp_data:
        :return:
        '''
        multiColor = tmp_data.get('multiColor', {})
        # sku_price = tmp_data.get('productSize', {}).get('product', {}).get('sku_price', [])
        ## ** 研究发现multiColor以及productSku中的type为1时，表示该商品规格库存为0
        productSku = tmp_data.get('productSize', {}).get('productSku', [])
        # tmp = {
        #     'multiColor': multiColor,
        #     # 'sku_price': sku_price,
        #     'productSku': productSku,
        # }
        # pprint(tmp)

        true_sku_info = []
        if multiColor == {} or productSku == {}:
            return []
        else:
            if multiColor.get('items') is None:
                color_ = None
            else:
                tmp_color_items = multiColor.get('items', [])
                color_ = []
                for item in tmp_color_items:
                    if item.get('type', 0) == 1:    # 该颜色无库存
                        continue
                    else:                           # 为0，表示有库存
                        # 先获取到有库存的对应规格, 是否有颜色属性后面再判断
                        color_.append({
                            'goods_id': item.get('product_id', ''),
                            'name': item.get('name', ''),
                            'img_url': 'https:' + item.get('icon', {}).get('imageUrl', '')
                        })

            if color_ == []:    # 没有规格 也可能是 # 表示没有库存, 买完或者下架
                print('获取到的color_为空[], 请检查!')
                return []
            else:
                if productSku.get('items') is None:
                    print('获取到的others_items为None')
                    return []

                else:
                    other_items = productSku.get('items', [])
                    other_ = []
                    for item in other_items:
                        if item.get('type', 0) == 1:    # 该规格无库存
                            continue
                        else:                           # 该规格有库存
                            detail_price = item.get('promotion_price', '')
                            # 还是选择所有商品都拿最优惠的价格
                            # if detail_price == '' or goods_id[0] == 1:      # 为空就改为获取vipshop_price字段
                            if detail_price == '':      # 为空就改为获取vipshop_price字段
                                detail_price = item.get('vipshop_price', '')
                            else:
                                pass
                            normal_price = item.get('market_price', '')
                            if normal_price == '':
                                normal_price = detail_price
                            other_.append({
                                'spec_value': item.get('sku_name', ''),
                                'detail_price': detail_price,
                                'normal_price': normal_price,
                                'img_url': '',      # 设置默认为空值
                                'rest_number': item.get('leavings', 0),  # 该规格的剩余库存量
                            })

                if color_ is None:
                    for item_2 in other_:
                        spec_value = item_2.get('spec_value', '')
                        item_2['spec_value'] = spec_value
                        item_2['img_url'] = ''
                        true_sku_info.append(item_2)

                elif len(color_) == 1:    # 颜色长度为1时，表示唯品会默认选择的属性，不需要将color_相关的值添加到spec_value里面
                    true_sku_info = other_

                else:
                    for item in color_:
                        if item.get('goods_id') == goods_id[1]:    # 表示为原先的那个goods_id
                            if item.get('name', '') == '无':     # 表示无颜色属性
                                pass
                            else:
                                for item_2 in other_:
                                    spec_value = item.get('name', '') + '|' + item_2.get('spec_value', '')
                                    item_2['spec_value'] = spec_value
                                    item_2['img_url'] = item.get('img_url', '')
                                    true_sku_info.append(item_2)

                        else:                                   # 表示是其他颜色对应的goods_id
                            '''
                            下面是获取该颜色对应goods_id的所有可售的规格价格信息
                            '''
                            goods_url = 'https://m.vip.com/product-0-' + str(item.get('goods_id', '')) + '.html'
                            tmp_data_2 = MyRequests.get_url_body(url=goods_url, headers=self.headers, had_referer=True)

                            # 先处理得到dict数据
                            if tmp_data_2 == '':
                                print('获取其他颜色规格的url的body时为空值')
                                return []
                            else:
                                try:
                                    tmp_data_2 = re.compile(r'var _WAP_PAGE_CACHE = (.*?);</script>').findall(tmp_data_2)[0]
                                    # print(tmp_data_2)
                                except IndexError:
                                    print('re匹配不到关键数据, 请检查!')
                                    return []

                                try:
                                    tmp_data_2 = json.loads(tmp_data_2)
                                    # pprint(tmp_data_2)
                                except Exception:
                                    print('json.loads转换tmp_data_2时出错, 请检查!')
                                    return []

                                productSku_2 = tmp_data_2.get('productSize', {}).get('productSku', [])
                                other_items_2 = productSku_2.get('items', [])
                                other_2 = []
                                for item_3 in other_items_2:
                                    if item_3.get('type', 0) == 1:  # 该规格无库存
                                        continue
                                    else:  # 该规格有库存
                                        detail_price = item_3.get('promotion_price', '')
                                        # 还是都拿最优惠的价格 不管限时2小时时间问题的折扣
                                        # if detail_price == '' or goods_id[0] == 1:  # 为空就改为获取vipshop_price字段
                                        if detail_price == '':  # 为空就改为获取vipshop_price字段
                                            detail_price = item_3.get('vipshop_price', '')
                                        normal_price = item_3.get('market_price', '')
                                        if normal_price == '':
                                            normal_price = detail_price
                                        other_2.append({
                                            'spec_value': item_3.get('sku_name', ''),
                                            'detail_price': detail_price,
                                            'normal_price': normal_price,
                                            'rest_number': item_3.get('leavings', 0),  # 设置默认的值
                                            'img_url': '',  # 设置默认为空值
                                        })

                                for item_4 in other_2:
                                    spec_value = item.get('name', '') + '|' + item_4.get('spec_value', '')
                                    item_4['spec_value'] = spec_value
                                    item_4['img_url'] = item.get('img_url', '')
                                    true_sku_info.append(item_4)

        return true_sku_info

    def get_goods_div_desc(self, tmp_data):
        '''
        得到div_desc
        :param tmp_data:
        :return: '' | 非空字符串
        '''
        tmp_div_desc = ''
        if tmp_data == []:
            print('获取到的div_desc的图片list为空[]')
            return ''
        else:
            for item in tmp_data:
                tmp = ''
                tmp_img_url = 'https:' + item.get('imageUrl', '')
                tmp = r'<img src="{}" style="height:auto;width:100%;"/>'.format(tmp_img_url)
                tmp_div_desc += tmp

            detail_data = '<div>' + tmp_div_desc + '</div>'

        return detail_data

    def wash_data(self, data):
        '''
        清洗数据
        :param data:
        :return: {} 表示获取上下架时间失败! | {xxx, xxx} 表示success
        '''
        try:
            begin_time = data.get('vtm', {}).get('product', {}).get('sell_time_from', '')
            end_time = data.get('vtm', {}).get('product', {}).get('sell_time_to', '')

            if begin_time != '' and end_time != '':
                data['sell_time'] = {
                    'begin_time': begin_time,
                    'end_time': end_time,
                }
                del data['vtm']

            else:
                print('获取该商品的上下架时间失败, 请检查!')
                return {}
        except Exception as e:
            print('获取上下架时间时遇到错误: ', e)
            return {}

        '''
        分开del, 避免都放在一块，一个del失败就跳出无法进行继续再往下的清洗
        '''
        try:
            del data['ShowComment']
        except:
            pass
        try:
            del data['flag']
        except:
            pass
        try:
            del data['addCart']
        except:
            pass
        try:
            del data['appDownload']
        except:
            pass
        try:
            del data['appWakeup']
        except:
            pass
        try:
            del data['cart']
        except:
            pass
        try:
            del data['browserHistory']
        except:
            pass
        try:
            del data['addCartGoods']
        except:
            pass
        try:
            del data['deliveryInfo']
        except:
            pass
        try:
            del data['footer']
        except:
            pass
        try:
            del data['footerToolbar']
        except:
            pass
        try:
            del data['functionEntry']
        except:
            pass
        try:
            del data['gift']
        except:
            pass
        try:
            del data['productExtra']
        except:
            pass
        try:
            del data['productLicense']
        except:
            pass
        try:
            del data['productPreheatCollect']
        except:
            pass
        try:
            del data['productSlide']
        except:
            pass
        try:
            del data['productTips']
        except:
            pass
        try:
            del data['refer']
        except:
            pass
        try:
            del data['serviceText']
        except:
            pass
        try:
            del data['wakeupBar']
        except:
            pass
        try:
            del data['weixinFollow']
        except:
            pass
        try:
            del data['wxShare']
        except:
            pass
        try:
            del data['independentAmount']
        except:
            pass
        try:
            del data['productPriceLine']    # 价格线，价格图，无用
        except:
            pass
        try:
            del data['recommendAddress']    # 当前定位的地址
        except:
            pass
        try:
            del data['share']
        except:
            pass
        try:
            del data['wxUserBehavior']
        except:
            pass
        try:
            for item in data['multiColor']['items']:
                del item['detailImages']     # 重复的detail_info的图片
                del item['previewImages']

        except Exception:
            pass
        try:
            del data['productSize']['product']['detailImages']
            del data['productSize']['product']['img_pre']
            del data['productSize']['product']['previewImages']
        except Exception:
            pass
        try:
            del data['productAttr']
        except:
            pass
        try:
            del data['productSize']['product']['brand_info']
        except:
            pass

        # print('清洗完毕')

        return data

    def get_p_info(self, tmp_data):
        '''
        得到p_info
        :param tmp_data:
        :return: [] 表示出错 | [xxx, ...] 表示success
        '''
        tmp_p_info = tmp_data.get('productSize', {}).get('product', {}).get('attrSpecProps', [])
        # pprint(tmp_p_info)
        # pprint(tmp_data.get('productSize', {}).get('product', {}))

        p_info = []
        brandStoreName = tmp_data.get('productSize', {}).get('product', {}).get('brandStoreName', '')
        if brandStoreName != '':
            p_info.append({'p_name': '品牌名称', 'p_value': brandStoreName})

        p_info.append({'p_name': '商品名称', 'p_value': tmp_data.get('productSize', {}).get('product', {}).get('product_name', '')})

        # 产地
        areaOutput = tmp_data.get('productSize', {}).get('product', {}).get('areaOutput', '')
        if areaOutput != '':
            p_info.append({'p_name': '产地', 'p_value': areaOutput})

        # 材质相关
        itemProperties = tmp_data.get('productSize', {}).get('product', {}).get('itemProperties', [])
        if itemProperties != []:
            for item in itemProperties:
                p_info.append({'p_name': item.get('name', ''), 'p_value': item.get('value', '')})

        # 洗涤说明相关
        itemDetailModules = tmp_data.get('productSize', {}).get('product', {}).get('itemDetailModules', [])
        if itemDetailModules != []:
            for item in itemDetailModules:
                p_info.append({'p_name': item.get('name', ''), 'p_value': item.get('value', '')})

        if tmp_p_info == []:
            # print('获取到的p_info为空[], 请检查!')
            return p_info

        for item in tmp_p_info:
            try:
                p_value = item.get('values', [])
                if p_value != [] and p_value.__len__() > 1:
                    p_value = [item_6.get('optionName', '') for item_6 in p_value]
                    p_value = ' '.join(p_value)

                elif p_value.__len__() == 1:
                    p_value = item.get('values', [])[0].get('optionName', '')

                else:
                    p_value = ''
                p_info.append({
                    'p_name': item.get('attributeName', ''),
                    'p_value': p_value
                })
            except IndexError:
                print('在解析p_info时索引出错, 请检查!')
                return []

        return p_info

    def timestamp_to_regulartime(self, timestamp):
        '''
        将时间戳转换成时间
        '''
        # 利用localtime()函数将时间戳转化成localtime的格式
        # 利用strftime()函数重新格式化时间

        # 转换成localtime
        time_local = time.localtime(timestamp)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

        return dt

    def get_goods_id_from_url(self, vip_url):
        '''
        得到goods_id
        :param vip_url:
        :return: goods_id (类型list)
        '''
        is_vip_url = re.compile(r'https://m.vip.com/product-(\d*)-.*?.html.*?').findall(vip_url)
        if is_vip_url != []:
            if re.compile(r'https://m.vip.com/product-.*?-(\d+).html.*?').findall(vip_url) != []:
                tmp_vip_url = re.compile(r'https://m.vip.com/product-.*?-(\d+).html.*?').findall(vip_url)[0]
                if tmp_vip_url != '':
                    goods_id = tmp_vip_url
                else:   # 只是为了在pycharm运行时不跳到chrome，其实else完全可以不要的
                    vip_url = re.compile(r';').sub('', vip_url)
                    goods_id = re.compile(r'https://m.vip.com/product-.*?-(\d+).html.*?').findall(vip_url)[0]
                print('------>>>| 得到的唯品会商品的goods_id为:', goods_id)
                return [0, goods_id]
        else:
            # 是否是预售商品
            is_vip_preheading = re.compile(r'https://m.vip.com/preheating-product-(\d+)-.*?.html.*?').findall(vip_url)
            if is_vip_preheading != []:
                if re.compile(r'https://m.vip.com/preheating-product-.*?-(\d+).html.*?').findall(vip_url) != []:
                    tmp_vip_url = re.compile(r'https://m.vip.com/preheating-product-.*?-(\d+).html.*?').findall(vip_url)[0]
                    if tmp_vip_url != '':
                        goods_id = tmp_vip_url
                    else:  # 只是为了在pycharm运行时不跳到chrome，其实else完全可以不要的
                        vip_url = re.compile(r';').sub('', vip_url)
                        goods_id = re.compile(r'https://m.vip.com/preheating-product-.*?-(\d+).html.*?').findall(vip_url)[0]
                    print('------>>>| 得到的唯品会 预售商品 的goods_id为:', goods_id)
                    return [1, goods_id]
            else:
                print('唯品会商品url错误, 非正规的url, 请参照格式(https://m.vip.com/product-0-xxxxxxx.html) or (https://m.vip.com/preheating-product-xxxx-xxxx.html)开头的...')
                return []

    def __del__(self):
        gc.collect()

if __name__ == '__main__':
    vip = VipParse()
    while True:
        vip_url = input('请输入待爬取的唯品会商品地址: ')
        vip_url.strip('\n').strip(';')
        goods_id = vip.get_goods_id_from_url(vip_url)
        data = vip.get_goods_data(goods_id=goods_id)
        vip.deal_with_data()