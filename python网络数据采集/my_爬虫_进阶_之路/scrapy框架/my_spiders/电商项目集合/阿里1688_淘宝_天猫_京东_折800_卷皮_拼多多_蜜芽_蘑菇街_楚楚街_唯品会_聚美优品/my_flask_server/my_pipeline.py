# coding=utf-8

'''
@author = super_fazai
@File    : my_pipeline.py
@Time    : 2017/10/15 07:15
@connect : superonesfazai@gmail.com
'''

# from MySQLdb import *
from pymssql import *
from json import dumps
import gc
from sqlalchemy import create_engine
import datetime, calendar
import asyncio
from logging import INFO, ERROR

from settings import HOST, USER, PASSWORD, DATABASE, PORT
from settings import INIT_PASSWD
from settings import HOST_2, USER_2, PASSWORD_2, DATABASE_2, PORT_2
from settings import MY_SPIDER_LOGS_PATH
from my_logging import set_logger
from my_utils import get_shanghai_time

class UserItemPipeline(object):
    """
    用户信息处理管道
    """
    def __init__(self):
        super(UserItemPipeline, self).__init__()
        self.is_connect_success = True
        try:
            self.conn = connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DATABASE,
                port=PORT,
                charset='utf8'
            )
        except Exception as e:
            print('数据库连接失败!!')
            self.is_connect_success = False

    def insert_into_table(self, item):
        cs = self.conn.cursor()
        try:
            params = item

            # print(params)
            # pymssql下的execute执行插入语句成功返回的值也是None, 所以不判断返回的行数
            cs.execute('insert into dbo.ali_spider_employee_table(username, passwd, createtime, department, realnane) values(%s, %s, %s, %s, %s)', tuple(params))
            self.conn.commit()
            cs.close()
            print('-' * 60 + '| ***该用户信息成功存入mysql中*** |')
            return True
        except Exception as e:
            cs.close()
            print('-' * 60 + '| 修改信息失败, 未能将该评论信息存入到mysql中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            pass

    def select_all_info(self):
        cs = self.conn.cursor()
        try:
            cs.execute('select * from dbo.ali_spider_employee_table')
            result = list(cs.fetchall())
            self.conn.commit()

            if result != []:
                cs.close()
                # print(result)
                return result
            else:
                cs.close()
                return []
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            cs.close()
            return []

    def find_user_by_username(self, username):
        cs = self.conn.cursor()
        try:
            cs.execute('select * from dbo.ali_spider_employee_table where username=%s', tuple([username,]))
            result = list(cs.fetchone())
            self.conn.commit()

            if result != []:
                cs.close()
                # print(result)
                return result
            else:
                cs.close()
                return []
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            cs.close()
            return []

    def find_user_by_real_name(self, name):
        cs = self.conn.cursor()
        try:
            cs.execute('select * from dbo.ali_spider_employee_table where realnane=%s', tuple([name,]))
            result = list(cs.fetchall())
            self.conn.commit()

            if result != []:
                cs.close()
                # print(result)
                return result
            else:
                cs.close()
                return []
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            cs.close()
            return []

    def init_user_passwd(self, username):
        cs = self.conn.cursor()
        try:
            cs.execute('update dbo.ali_spider_employee_table set passwd=%s where username=%s', tuple([INIT_PASSWD, username]))

            cs.close()
            return True
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            cs.close()
            return False

    def delete_users(self, item):
        cs = self.conn.cursor()
        try:
            for i in item:
                cs.execute('delete from dbo.ali_spider_employee_table where username=%s', tuple([i]))

            cs.close()
            return True
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            cs.close()
            return False

    def select_is_had_username(self, username, passwd):
        try:
            cs = self.conn.cursor()

            params = [
                username,
                passwd,
            ]

            cs.execute('select username from dbo.ali_spider_employee_table where username = %s and passwd = %s', tuple(params))
            count = cs.fetchone()

            self.conn.commit()
            # print(type(cs.fetchone()))      # return  ->  <class 'NoneType'>
            # print(cs.fetchone())
            print(count)
            if count:
                cs.close()
                return True
            else:
                cs.close()
                return False
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            cs.close()
            return False

'''
class MyPageInfoSaveItemPipeline(object):
    """
    页面存储管道
    """
    def __init__(self):
        super(MyPageInfoSaveItemPipeline, self).__init__()
        self.conn = connect(
            host='localhost',
            port=3306,
            db='python',
            user='root',
            passwd='lrf654321',
            # charset='utf-8',
        )

    def insert_into_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['spider_url'],
                item['username'],
                item['deal_with_time'],
                item['title'],
                item['price'],
                item['trade_number'],
                item['color'],
                item['color_img_url'],
                item['size_info'],
                item['detail_price'],
                item['rest_number'],
                item['center_img_url'],
                item['all_img_url'],
            ]

            # print(params)
            count = cs.execute('insert into ali_spider_page_info_table(spider_url, username, deal_with_time, title, price, trade_number, color, color_img_url, size_info, detail_price, rest_number, center_img_url, all_img_url) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', params)
            self.conn.commit()

            print(count)
            cs.close()
            if count:
                print('-' * 60 + '| ***该页面信息成功存入mysql中*** |')
                return True
            else:
                print('-' * 60 + '| 修改信息失败, 未能将该页面信息存入到mysql中 ! |')
                return False
        except Exception as e:
            cs.close()
            print('-' * 60 + '| 修改信息失败, 未能将该页面信息存入到mysql中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def update_table(self, info):
        try:
            cs = self.conn.cursor()

            params = [
                info['deal_with_time'],
                info['title'],
                info['price'],
                info['trade_number'],
                info['color'],
                info['color_img_url'],
                info['size_info'],
                info['detail_price'],
                info['rest_number'],
                info['center_img_url'],
                info['all_img_url'],

                info['username'],
                info['spider_url'],
            ]

            count = cs.execute('update ali_spider_page_info_table set deal_with_time = %s, title = %s, price = %s, trade_number = %s, color = %s, color_img_url = %s, size_info = %s, detail_price = %s, rest_number = %s, center_img_url = %s, all_img_url = %s where username = %s and spider_url = %s', params)
            self.conn.commit()

            print(count)
            cs.close()
            if count:
                print('-' * 60 + '| ***该页面信息成功存入mysql中*** |')
                return True
            else:
                print('-' * 60 + '| 修改信息失败, 未能将该页面信息存入到mysql中 ! |')
                return False

        except Exception as e:
            cs.close()
            print('-' * 60 + '| 修改信息失败, 未能将该页面信息存入到mysql中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def select_is_had_username(self, spider_url, username):
        try:
            cs = self.conn.cursor()

            params = [
                spider_url,
                username,
            ]

            count = cs.execute('select username from ali_spider_employee_table where username = %s and passwd = %s', params)

            self.conn.commit()
            # print(type(cs.fetchone()))      # return  ->  <class 'NoneType'>
            # print(cs.fetchone())
            print(count)
            if count:
                cs.close()
                return True
            else:
                cs.close()
                return False
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            cs.close()
            return False
'''

class SqlServerMyPageInfoSaveItemPipeline(object):
    """
    页面存储管道
    """
    def __init__(self):
        super(SqlServerMyPageInfoSaveItemPipeline, self).__init__()
        self.is_connect_success = True
        try:
            self.conn = connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DATABASE,
                port=PORT,
                charset='utf8'
            )
        except Exception as e:
            print('数据库连接失败!!')
            self.is_connect_success = False

    def insert_into_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['goods_id'],
                item['spider_url'],
                item['username'],
                item['deal_with_time'],
                item['modfiy_time'],
                item['company_name'],
                item['title'],
                item['link_name'],
                item['price'],
                item['taobao_price'],
                dumps(item['price_info'], ensure_ascii=False),        # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['spec_name'], ensure_ascii=False),
                dumps(item['sku_map'], ensure_ascii=False),
                dumps(item['all_img_url_info'], ensure_ascii=False),
                item['detail_info'],                          # 存入到DetailInfo
                dumps(item['property_info'], ensure_ascii=False),      # 存入到PropertyInfo

                item['site_id'],
                item['is_delete'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, GoodsName, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, DetailInfo, PropertyInfo, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'),
                       tuple(params))   # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def update_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['modfiy_time'],
                item['company_name'],
                item['title'],
                item['link_name'],
                item['price'],
                item['taobao_price'],
                dumps(item['price_info'], ensure_ascii=False),
                dumps(item['spec_name'], ensure_ascii=False),
                dumps(item['sku_map'], ensure_ascii=False),
                dumps(item['all_img_url_info'], ensure_ascii=False),
                item['detail_info'],
                dumps(item['property_info'], ensure_ascii=False),
                dumps(item['my_shelf_and_down_time'], ensure_ascii=False),
                item['delete_time'],
                item['is_delete'],

                item['goods_id'],
            ]

            cs.execute('update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, GoodsName=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, DetailInfo=%s, PropertyInfo=%s, MyShelfAndDownTime=%s, delete_time=%s, IsDelete=%s where GoodsID = %s',
                       tuple(params))
            self.conn.commit()
            cs.close()
            print('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def old_ali_1688_goods_insert_into_new_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['goods_id'],
                item['spider_url'],
                item['username'],
                item['deal_with_time'],
                item['modfiy_time'],
                item['company_name'],
                item['title'],
                item['link_name'],
                item['price'],
                item['taobao_price'],
                dumps(item['price_info'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['spec_name'], ensure_ascii=False),
                dumps(item['sku_map'], ensure_ascii=False),
                dumps(item['all_img_url_info'], ensure_ascii=False),
                item['detail_info'],  # 存入到DetailInfo
                dumps(item['property_info'], ensure_ascii=False),  # 存入到PropertyInfo

                item['site_id'],
                item['is_delete'],
                item['main_goods_id'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute(
                'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, GoodsName, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, DetailInfo, PropertyInfo, SiteID, IsDelete, MainGoodsID) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode(
                    'utf-8'),
                tuple(params))  # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def insert_into_taobao_table(self, item, logger):
        try:
            cs = self.conn.cursor()

            params = [
                item['goods_id'],
                item['spider_url'],
                item['username'],
                item['deal_with_time'],
                item['modfiy_time'],
                item['shop_name'],
                item['account'],
                item['title'],
                item['sub_title'],
                item['link_name'],
                item['price'],
                item['taobao_price'],
                dumps(item['price_info'], ensure_ascii=False),
                dumps(item['detail_name_list'], ensure_ascii=False),    # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
                item['div_desc'],                          # 存入到DetailInfo
                item['month_sell_count'],

                item['site_id'],
                item['is_delete'],
            ]

            # logger.info(str(params))
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'),
                       tuple(params))   # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            logger.info('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except IntegrityError:
            logger.info('重复插入goods_id[%s], 此处跳过!' % item['goods_id'])
            return False

        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            logger.error('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 | 出错地址: ' + item['spider_url'])
            logger.exception(e)
            return False

    async def insert_into_taobao_tiantiantejia_table(self, item, logger):
        cs = self.conn.cursor()
        try:
            params = [
                item['goods_id'],
                item['goods_url'],
                item['deal_with_time'],
                item['modfiy_time'],
                item['shop_name'],
                item['account'],
                item['title'],
                item['sub_title'],
                item['price'],
                item['taobao_price'],
                dumps(item['detail_name_list'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
                item['div_desc'],  # 存入到DetailInfo
                item['month_sell_count'],
                dumps(item['schedule'], ensure_ascii=False),
                item['tejia_begin_time'],
                item['tejia_end_time'],
                item['block_id'],
                item['tag_id'],
                item['father_sort'],
                item['child_sort'],

                item['site_id'],
                item['is_delete'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.taobao_tiantiantejia(goods_id, goods_url, create_time, modfiy_time, shop_name, account, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, month_sell_count, schedule, tejia_begin_time, tejia_end_time, block_id, tag_id, father_sort, child_sort, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'), tuple(params))  # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            logger.info('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except IntegrityError:
            logger.info('###### 重复插入goods_id[%s]' % item['goods_id'])
            return False

        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            logger.error('修改信息失败, 未能将该页面信息存入到sqlserver中, 失败地址: ' + item['goods_url'])
            logger.exception(e)
            return False

    def update_taobao_table(self, item, logger):
        cs = self.conn.cursor()
        try:
            params = [
                item['modfiy_time'],
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
                item['month_sell_count'],
                dumps(item['my_shelf_and_down_time'], ensure_ascii=False),
                item['delete_time'],
                item['is_delete'],

                item['goods_id'],
            ]
            # print(item['month_sell_count'])

            cs.execute('update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, MyShelfAndDownTime=%s, delete_time=%s, IsDelete=%s where GoodsID=%s',
                       tuple(params))
            self.conn.commit()
            cs.close()
            logger.info('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            logger.info('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 | 出错goods_id: ' + item['goods_id'])
            logger.exception(e)
            return False

    async def update_taobao_tiantiantejia_table(self, item, logger):
        cs = self.conn.cursor()
        try:
            params = [
                item['modfiy_time'],
                item['shop_name'],
                item['account'],
                item['title'],
                item['sub_title'],
                item['price'],
                item['taobao_price'],
                dumps(item['detail_name_list'], ensure_ascii=False),
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                dumps(item['p_info'], ensure_ascii=False),
                item['div_desc'],
                item['month_sell_count'],
                # dumps(item['schedule'], ensure_ascii=False),
                # item['tejia_begin_time'],
                # item['tejia_end_time'],
                item['is_delete'],

                item['goods_id'],
            ]
            # logger.info(item['month_sell_count'])

            cs.execute('update dbo.taobao_tiantiantejia set modfiy_time = %s, shop_name=%s, account=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, month_sell_count=%s, is_delete=%s where goods_id=%s',
                tuple(params))
            self.conn.commit()
            cs.close()
            logger.info('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            logger.info('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 | 出错goods_id: ' + item['goods_id'])
            logger.exception(e)
            return False

    async def update_expired_goods_id_taobao_tiantiantejia_table(self, item, logger):
        cs = self.conn.cursor()
        try:
            params = [
                item['modfiy_time'],
                item['shop_name'],
                item['account'],
                item['title'],
                item['sub_title'],
                item['price'],
                item['taobao_price'],
                dumps(item['detail_name_list'], ensure_ascii=False),
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                dumps(item['p_info'], ensure_ascii=False),
                item['div_desc'],
                item['month_sell_count'],
                item['is_delete'],

                item['goods_id'],
            ]
            # print(item['month_sell_count'])

            cs.execute('update dbo.taobao_tiantiantejia set modfiy_time = %s, shop_name=%s, account=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, month_sell_count=%s, is_delete=%s where goods_id=%s',
                tuple(params))
            self.conn.commit()
            cs.close()
            logger.info('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            logger.error('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            logger.exception(e)
            return False

    def old_taobao_goods_insert_into_new_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['goods_id'],
                item['spider_url'],
                item['username'],
                item['deal_with_time'],
                item['modfiy_time'],
                item['shop_name'],
                item['account'],
                item['title'],
                item['sub_title'],
                item['link_name'],
                item['price'],
                item['taobao_price'],
                dumps(item['price_info'], ensure_ascii=False),
                dumps(item['detail_name_list'], ensure_ascii=False),    # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
                item['div_desc'],                          # 存入到DetailInfo
                item['month_sell_count'],

                item['site_id'],
                item['is_delete'],
                item['main_goods_id'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete, MainGoodsID) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'),
                       tuple(params))   # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            try:
                self.conn.close()
            except Exception:
                pass
            return False

    def insert_into_tmall_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['goods_id'],
                item['spider_url'],
                item['username'],
                item['deal_with_time'],
                item['modfiy_time'],
                item['shop_name'],
                item['account'],
                item['title'],
                item['sub_title'],
                item['link_name'],
                item['price'],
                item['taobao_price'],
                dumps(item['price_info'], ensure_ascii=False),
                dumps(item['detail_name_list'], ensure_ascii=False),    # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
                item['div_desc'],                          # 存入到DetailInfo
                item['month_sell_count'],

                item['site_id'],
                item['is_delete'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'),
                       tuple(params))   # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def update_tmall_table(self, item, logger):
        cs = self.conn.cursor()
        try:
            params = [
                item['modfiy_time'],
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
                item['month_sell_count'],
                dumps(item['my_shelf_and_down_time'], ensure_ascii=False),
                item['delete_time'],
                item['is_delete'],

                item['goods_id'],
            ]

            cs.execute('update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, MyShelfAndDownTime=%s, delete_time=%s, IsDelete=%s where GoodsID = %s',
                       tuple(params))
            self.conn.commit()
            cs.close()
            logger.info('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            logger.error('| 修改信息失败, 未能将该页面信息存入到sqlserver中 出错goods_id: %s|' % item['goods_id'])
            logger.exception(e)

            return False

    def update_tmall_goodsurl_by_site_id_6(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['goods_url'],

                item['goods_id'],
            ]

            cs.execute('update dbo.GoodsInfoAutoGet set GoodsUrl=%s where GoodsID = %s',
                       tuple(params))
            self.conn.commit()
            cs.close()
            print('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('| 修改信息失败, 未能将该页面信息存入到sqlserver中 出错goods_id: %s|' % item['goods_id'])
            print(e)

            return False

    def old_tmall_goods_insert_into_new_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['goods_id'],
                item['spider_url'],
                item['username'],
                item['deal_with_time'],
                item['modfiy_time'],
                item['shop_name'],
                item['account'],
                item['title'],
                item['sub_title'],
                item['link_name'],
                item['price'],
                item['taobao_price'],
                dumps(item['price_info'], ensure_ascii=False),
                dumps(item['detail_name_list'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
                item['div_desc'],  # 存入到DetailInfo
                item['month_sell_count'],

                item['site_id'],
                item['is_delete'],
                item['main_goods_id'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete, MainGoodsID) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'),
                tuple(params))  # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def insert_into_jd_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['goods_id'],
                item['spider_url'],
                item['username'],
                item['deal_with_time'],
                item['modfiy_time'],
                item['shop_name'],
                item['account'],
                item['title'],
                item['sub_title'],
                item['link_name'],
                item['price'],
                item['taobao_price'],
                dumps(item['price_info'], ensure_ascii=False),
                dumps(item['detail_name_list'], ensure_ascii=False),    # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
                item['div_desc'],                          # 存入到DetailInfo
                item['all_sell_count'],

                item['site_id'],
                item['is_delete'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'),
                       tuple(params))   # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def update_jd_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['modfiy_time'],
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
                item['all_sell_count'],
                dumps(item['my_shelf_and_down_time'], ensure_ascii=False),
                item['delete_time'],
                item['is_delete'],

                item['goods_id'],
            ]

            cs.execute('update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, MyShelfAndDownTime=%s, delete_time=%s, IsDelete=%s where GoodsID = %s',
                       tuple(params))
            self.conn.commit()
            cs.close()
            print('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def insert_into_zhe_800_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['goods_id'],
                item['spider_url'],
                item['username'],
                item['deal_with_time'],
                item['modfiy_time'],
                item['shop_name'],
                item['account'],
                item['title'],
                item['sub_title'],
                item['link_name'],
                item['price'],
                item['taobao_price'],
                dumps(item['price_info'], ensure_ascii=False),
                dumps(item['detail_name_list'], ensure_ascii=False),    # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
                item['div_desc'],                          # 存入到DetailInfo
                dumps(item['schedule'], ensure_ascii=False),

                item['site_id'],
                item['is_delete'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, Schedule, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'),
                       tuple(params))   # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def update_zhe_800_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['modfiy_time'],
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
                dumps(item['my_shelf_and_down_time'], ensure_ascii=False),
                item['delete_time'],
                item['is_delete'],
                dumps(item['schedule'], ensure_ascii=False),

                item['goods_id'],
            ]

            cs.execute('update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, MyShelfAndDownTime=%s, delete_time=%s, IsDelete=%s, Schedule=%s where GoodsID = %s',
                       tuple(params))
            self.conn.commit()
            cs.close()
            print('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def insert_into_zhe_800_xianshimiaosha_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['goods_id'],
                item['spider_url'],
                item['username'],
                item['deal_with_time'],
                item['modfiy_time'],
                item['shop_name'],
                item['title'],
                item['sub_title'],
                item['price'],
                item['taobao_price'],
                dumps(item['detail_name_list'], ensure_ascii=False),    # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
                item['div_desc'],                          # 存入到DetailInfo
                dumps(item['schedule'], ensure_ascii=False),
                dumps(item['stock_info'], ensure_ascii=False),
                dumps(item['miaosha_time'], ensure_ascii=False),
                item['miaosha_begin_time'],
                item['miaosha_end_time'],
                item['session_id'],

                item['site_id'],
                item['is_delete'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.zhe_800_xianshimiaosha(goods_id, goods_url, username, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_info, all_image_url, property_info, detail_info, schedule, stock_info, miaosha_time, miaosha_begin_time, miaosha_end_time, session_id, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'),
                       tuple(params))   # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def insert_into_zhe_800_pintuan_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['goods_id'],
                item['spider_url'],
                item['username'],
                item['deal_with_time'],
                item['modfiy_time'],
                item['shop_name'],
                item['title'],
                item['sub_title'],
                item['price'],
                item['taobao_price'],
                dumps(item['detail_name_list'], ensure_ascii=False),    # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                item['all_sell_count'],
                dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
                item['div_desc'],                          # 存入到DetailInfo
                dumps(item['schedule'], ensure_ascii=False),
                item['pintuan_begin_time'],
                item['pintuan_end_time'],
                item['page'],

                item['site_id'],
                item['is_delete'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.zhe_800_pintuan(goods_id, goods_url, username, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_info, all_image_url, all_sell_count, property_info, detail_info, schedule, miaosha_begin_time, miaosha_end_time, page, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'),
                       tuple(params))   # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def update_zhe_800_xianshimiaosha_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['modfiy_time'],
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
                item['goods_id'],
            ]

            cs.execute('update dbo.zhe_800_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, schedule=%s, stock_info=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s where goods_id = %s',
                       tuple(params))
            self.conn.commit()
            cs.close()
            print('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def update_zhe_800_pintuan_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['modfiy_time'],
                item['shop_name'],
                item['title'],
                item['sub_title'],
                item['price'],
                item['taobao_price'],
                dumps(item['detail_name_list'], ensure_ascii=False),    # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                item['all_sell_count'],
                dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
                item['div_desc'],                          # 存入到DetailInfo
                dumps(item['schedule'], ensure_ascii=False),
                item['is_delete'],

                item['goods_id']
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute(
                'update dbo.zhe_800_pintuan set modfiy_time=%s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, all_sell_count=%s, property_info=%s, detail_info=%s, schedule=%s, is_delete=%s where goods_id = %s',
                tuple(params))
            self.conn.commit()
            cs.close()
            print('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def insert_into_juanpi_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['goods_id'],
                item['spider_url'],
                item['username'],
                item['deal_with_time'],
                item['modfiy_time'],
                item['shop_name'],
                item['account'],
                item['title'],
                item['sub_title'],
                item['link_name'],
                item['price'],
                item['taobao_price'],
                dumps(item['price_info'], ensure_ascii=False),
                dumps(item['detail_name_list'], ensure_ascii=False),    # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
                item['div_desc'],                          # 存入到DetailInfo
                dumps(item['schedule'], ensure_ascii=False),

                item['site_id'],
                item['is_delete'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, Schedule, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'),
                       tuple(params))   # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def update_juanpi_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['modfiy_time'],
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
                dumps(item['my_shelf_and_down_time'], ensure_ascii=False),
                item['delete_time'],
                item['is_delete'],
                dumps(item['schedule'], ensure_ascii=False),

                item['goods_id'],
            ]

            cs.execute('update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, MyShelfAndDownTime=%s, delete_time=%s, IsDelete=%s, Schedule=%s where GoodsID = %s',
                       tuple(params))
            self.conn.commit()
            cs.close()
            print('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def insert_into_juanpi_xianshimiaosha_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['goods_id'],
                item['spider_url'],
                item['username'],
                item['deal_with_time'],
                item['modfiy_time'],
                item['shop_name'],
                item['title'],
                item['sub_title'],
                item['price'],
                item['taobao_price'],
                dumps(item['detail_name_list'], ensure_ascii=False),    # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
                item['div_desc'],                          # 存入到DetailInfo
                dumps(item['schedule'], ensure_ascii=False),
                dumps(item['stock_info'], ensure_ascii=False),
                dumps(item['miaosha_time'], ensure_ascii=False),
                item['miaosha_begin_time'],
                item['miaosha_end_time'],
                item['tab_id'],
                item['page'],

                item['site_id'],
                item['is_delete'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.juanpi_xianshimiaosha(goods_id, goods_url, username, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_info, all_image_url, property_info, detail_info, schedule, stock_info, miaosha_time, miaosha_begin_time, miaosha_end_time, tab_id, page, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'),
                       tuple(params))   # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def insert_into_juanpi_pintuan_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['goods_id'],
                item['spider_url'],
                item['username'],
                item['deal_with_time'],
                item['modfiy_time'],
                item['shop_name'],
                item['title'],
                item['sub_title'],
                item['price'],
                item['taobao_price'],
                dumps(item['detail_name_list'], ensure_ascii=False),    # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                item['all_sell_count'],
                dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
                item['div_desc'],                          # 存入到DetailInfo
                dumps(item['schedule'], ensure_ascii=False),
                item['pintuan_begin_time'],
                item['pintuan_end_time'],
                item['page'],

                item['site_id'],
                item['is_delete'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.juanpi_pintuan(goods_id, goods_url, username, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_info, all_image_url, all_sell_count, property_info, detail_info, schedule, miaosha_begin_time, miaosha_end_time, page, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'),
                       tuple(params))   # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def update_juanpi_xianshimiaosha_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['modfiy_time'],
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

                item['goods_id'],
            ]

            cs.execute('update dbo.juanpi_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, schedule=%s, stock_info=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s where goods_id = %s',
                       tuple(params))
            self.conn.commit()
            cs.close()
            print('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def update_juanpi_pintuan_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['modfiy_time'],
                item['shop_name'],
                item['title'],
                item['sub_title'],
                item['price'],
                item['taobao_price'],
                dumps(item['detail_name_list'], ensure_ascii=False),    # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                # item['all_sell_count'],
                dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
                item['div_desc'],                          # 存入到DetailInfo
                dumps(item['schedule'], ensure_ascii=False),
                item['is_delete'],

                item['goods_id']
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute(
                'update dbo.juanpi_pintuan set modfiy_time=%s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, schedule=%s, is_delete=%s where goods_id = %s',
                tuple(params))
            self.conn.commit()
            cs.close()
            print('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def insert_into_pinduoduo_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['goods_id'],
                item['spider_url'],
                item['username'],
                item['deal_with_time'],
                item['modfiy_time'],
                item['shop_name'],
                item['account'],
                item['title'],
                item['sub_title'],
                item['link_name'],
                item['price'],
                item['taobao_price'],
                dumps(item['price_info'], ensure_ascii=False),
                dumps(item['detail_name_list'], ensure_ascii=False),    # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
                item['div_desc'],                          # 存入到DetailInfo
                item['all_sell_count'],
                dumps(item['schedule'], ensure_ascii=False),

                item['site_id'],
                item['is_delete'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, Schedule, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'),
                       tuple(params))   # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def update_pinduoduo_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['modfiy_time'],
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
                item['all_sell_count'],
                dumps(item['my_shelf_and_down_time'], ensure_ascii=False),
                item['delete_time'],
                item['is_delete'],
                dumps(item['schedule'], ensure_ascii=False),

                item['goods_id'],
            ]

            cs.execute('update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, MyShelfAndDownTime=%s, delete_time=%s, IsDelete=%s, Schedule=%s where GoodsID = %s',
                       tuple(params))
            self.conn.commit()
            cs.close()
            print('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def insert_into_pinduoduo_xianshimiaosha_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['goods_id'],
                item['spider_url'],
                item['username'],
                item['deal_with_time'],
                item['modfiy_time'],
                item['shop_name'],
                item['title'],
                item['sub_title'],
                item['price'],
                item['taobao_price'],
                dumps(item['detail_name_list'], ensure_ascii=False),    # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
                item['div_desc'],                          # 存入到DetailInfo
                dumps(item['schedule'], ensure_ascii=False),
                dumps(item['stock_info'], ensure_ascii=False),
                dumps(item['miaosha_time'], ensure_ascii=False),
                item['miaosha_begin_time'],
                item['miaosha_end_time'],

                item['site_id'],
                item['is_delete'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.pinduoduo_xianshimiaosha(goods_id, goods_url, username, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_info, all_image_url, property_info, detail_info, schedule, stock_info, miaosha_time, miaosha_begin_time, miaosha_end_time, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'),
                       tuple(params))   # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def update_pinduoduo_xianshimiaosha_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['modfiy_time'],
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

                item['goods_id'],
            ]

            cs.execute('update dbo.pinduoduo_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, schedule=%s, stock_info=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s where goods_id = %s',
                       tuple(params))
            self.conn.commit()
            cs.close()
            print('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def insert_into_vip_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['goods_id'],
                item['spider_url'],
                item['username'],
                item['deal_with_time'],
                item['modfiy_time'],
                item['shop_name'],
                item['account'],
                item['title'],
                item['sub_title'],
                item['link_name'],
                item['price'],
                item['taobao_price'],
                dumps(item['price_info'], ensure_ascii=False),
                dumps(item['detail_name_list'], ensure_ascii=False),    # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
                item['div_desc'],                          # 存入到DetailInfo
                item['all_sell_count'],
                dumps(item['schedule'], ensure_ascii=False),

                item['site_id'],
                item['is_delete'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, Schedule, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'),
                       tuple(params))   # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def update_vip_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['modfiy_time'],
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
                item['all_sell_count'],
                dumps(item['my_shelf_and_down_time'], ensure_ascii=False),
                item['delete_time'],
                item['is_delete'],
                dumps(item['schedule'], ensure_ascii=False),

                item['goods_id'],
            ]

            cs.execute(
                'update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, MyShelfAndDownTime=%s, delete_time=%s, IsDelete=%s, Schedule=%s where GoodsID = %s',
                tuple(params))
            self.conn.commit()
            cs.close()
            print('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def insert_into_mia_xianshimiaosha_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['goods_id'],
                item['spider_url'],
                item['deal_with_time'],
                item['modfiy_time'],
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
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute(
                'insert into dbo.mia_xianshimiaosha(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, pid, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode(
                    'utf-8'),
                tuple(params))  # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def update_mia_xianshimiaosha_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['modfiy_time'],
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
            ]

            cs.execute(
                'update dbo.mia_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s where goods_id = %s',
                tuple(params))
            self.conn.commit()
            cs.close()
            print('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def insert_into_mia_pintuan_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['goods_id'],
                item['spider_url'],
                item['deal_with_time'],
                item['modfiy_time'],
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
                item['pid'],

                item['site_id'],
                item['is_delete'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute(
                'insert into dbo.mia_pintuan(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, all_sell_count, pid, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode(
                    'utf-8'),
                tuple(params))  # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def update_mia_pintuan_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['modfiy_time'],
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
            ]

            cs.execute(
                'update dbo.mia_pintuan set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s, all_sell_count=%s where goods_id = %s',
                tuple(params))
            self.conn.commit()
            cs.close()
            print('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def update_mia_pintuan_is_delete(self, goods_id):
        '''
        将该goods_id进行逻辑删除
        :param goods_id:
        :return:
        '''
        cs = self.conn.cursor()
        try:
            params = [
                goods_id,
            ]

            cs.execute(
                'update dbo.mia_pintuan set is_delete=1 where goods_id = %s',
                tuple(params))
            self.conn.commit()
            cs.close()
            print('| +++ 该商品状态已被逻辑is_delete = 1 +++ |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def insert_into_mogujie_xianshimiaosha_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['goods_id'],
                item['spider_url'],
                item['deal_with_time'],
                item['modfiy_time'],
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
                item['event_time'],

                item['site_id'],
                item['is_delete'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute(
                'insert into dbo.mogujie_xianshimiaosha(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, event_time, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode(
                    'utf-8'),
                tuple(params))  # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def update_mogujie_xianshimiaosha_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['modfiy_time'],
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
            ]

            cs.execute(
                'update dbo.mogujie_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s where goods_id = %s',
                tuple(params))
            self.conn.commit()
            cs.close()
            print('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def update_mogujie_miaosha_table_is_delete(self, goods_id):
        '''
        将该goods_id进行逻辑删除
        :param goods_id:
        :return:
        '''
        cs = self.conn.cursor()
        try:
            params = [
                goods_id,
            ]

            cs.execute(
                'update dbo.mogujie_xianshimiaosha set is_delete=1 where goods_id = %s',
                tuple(params))
            self.conn.commit()
            cs.close()
            print('| +++ 该商品状态已被逻辑is_delete = 1 +++ |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def insert_into_mogujie_pintuan_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['goods_id'],
                item['spider_url'],
                item['deal_with_time'],
                item['modfiy_time'],
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
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute(
                'insert into dbo.mogujie_pintuan(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, all_sell_count, fcid, page, sort, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'),
                tuple(params))  # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def update_mogujie_pintuan_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['modfiy_time'],
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
            ]

            cs.execute(
                'update dbo.mogujie_pintuan set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s, all_sell_count=%s where goods_id = %s',
                tuple(params))
            self.conn.commit()
            cs.close()
            print('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def update_mogujie_pintuan_table_2(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['modfiy_time'],
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
            ]

            cs.execute('update dbo.mogujie_pintuan set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s where goods_id = %s',
                tuple(params))
            self.conn.commit()
            cs.close()
            print('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def insert_into_chuchujie_xianshimiaosha_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['goods_id'],
                item['spider_url'],
                item['deal_with_time'],
                item['modfiy_time'],
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
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.chuchujie_xianshimiaosha(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, gender, page, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'), tuple(params))  # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def update_chuchujie_xianshimiaosha_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['modfiy_time'],
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
            ]

            cs.execute('update dbo.chuchujie_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s where goods_id = %s',
                tuple(params))
            self.conn.commit()
            cs.close()
            print('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def insert_into_jumeiyoupin_xianshimiaosha_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['goods_id'],
                item['spider_url'],
                item['deal_with_time'],
                item['modfiy_time'],
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
                item['page'],

                item['site_id'],
                item['is_delete'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.jumeiyoupin_xianshimiaosha(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, page, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'), tuple(params))  # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def update_jumeiyoupin_xianshimiaosha_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['modfiy_time'],
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
            ]

            cs.execute('update dbo.jumeiyoupin_xianshimiaosha set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s where goods_id = %s',
                tuple(params))
            self.conn.commit()
            cs.close()
            print('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def insert_into_jumeiyoupin_pintuan_table(self, item, logger):
        '''
        存入数据
        :param item: 待存数据
        :param logger: 日志对象
        :return:
        '''
        cs = self.conn.cursor()
        try:
            params = [
                item['goods_id'],
                item['spider_url'],
                item['deal_with_time'],
                item['modfiy_time'],
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
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.jumeiyoupin_pintuan(goods_id, goods_url, create_time, modfiy_time, shop_name, goods_name, sub_title, price, taobao_price, sku_name, sku_Info, all_image_url, property_info, detail_info, miaosha_time, miaosha_begin_time, miaosha_end_time, all_sell_count, page, sort, tab, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'), tuple(params))  # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            logger.info('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except IntegrityError:      # 单独捕捉重复插入, 不在error日志中打印
            logger.info('###### 重复插入goods_id[%s]' % str(item['goods_id']))
            return False

        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            logger.error('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |' + ' 出错地址: ' + item['spider_url'])
            logger.exception(e)
            return False

    def update_jumeiyoupin_pintuan_table(self, item, logger):
        cs = self.conn.cursor()
        try:
            params = [
                item['modfiy_time'],
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
            ]

            cs.execute('update dbo.jumeiyoupin_pintuan set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, miaosha_time=%s, miaosha_begin_time=%s, miaosha_end_time=%s, all_sell_count=%s where goods_id = %s', tuple(params))
            self.conn.commit()
            cs.close()
            logger.info('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            logger.error('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            logger.exception(e)
            return False

    def update_jumeiyoupin_pintuan_table_2(self, item, logger):
        cs = self.conn.cursor()
        try:
            params = [
                item['modfiy_time'],
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
            ]

            # print(params)
            cs.execute('update dbo.jumeiyoupin_pintuan set modfiy_time = %s, shop_name=%s, goods_name=%s, sub_title=%s, price=%s, taobao_price=%s, sku_name=%s, sku_Info=%s, all_image_url=%s, property_info=%s, detail_info=%s, is_delete=%s, all_sell_count=%s where goods_id = %s',
                tuple(params))
            self.conn.commit()
            cs.close()
            logger.info('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            logger.error('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            logger.exception(e)
            return False

    def select_ali_1688_all_goods_id(self):
        try:
            cs = self.conn.cursor()

            cs.execute('select GoodsID, IsDelete, MyShelfAndDownTime from dbo.GoodsInfoAutoGet where SiteID=2 order by ID desc')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def select_the_goods_id_is_in_ali_1688_table(self, goods_id):
        '''
        判断该goods_id是否已经存在于table中
        :param goods_id:
        :return:
        '''
        try:
            cs = self.conn.cursor()

            cs.execute('select GoodsID from dbo.GoodsInfoAutoGet where SiteID=2 and GoodsID=%s', tuple([goods_id]))
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def update_ali_1688_expired_goods_id_to_is_delete(self, goods_id):
        cs = self.conn.cursor()
        try:
            cs.execute('update dbo.GoodsInfoAutoGet set IsDelete=1 where GoodsID=%s', tuple([goods_id]))
            self.conn.commit()

            cs.close()
            return True
        except Exception as e:
            print('--------------------| 删除对应goods_id记录时报错：', e)
            try:
                cs.close()
            except Exception:
                pass

    def select_old_table_all_goods_id(self):
        try:
            cs = self.conn.cursor()

            cs.execute('select GoodsOutUrl, goods_id from db_k85u.dbo.goodsinfo where OutGoodsType<=13 and onoffshelf=1 and not exists (select maingoodsid from gather.dbo.GoodsInfoAutoGet c where c.maingoodsid=goodsinfo.goods_id)')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def select_taobao_all_goods_id(self):
        try:
            cs = self.conn.cursor()

            cs.execute('select GoodsID, IsDelete, MyShelfAndDownTime from dbo.GoodsInfoAutoGet where SiteID=1')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def select_taobao_tiantian_tejia_all_goods_id(self):
        cs = self.conn.cursor()
        result = []
        try:
            cs.execute('set lock_timeout 20000;')     # 设置客户端执行超时等待为20秒
            cs.execute('select goods_id, is_delete, tejia_end_time, block_id, tag_id from dbo.taobao_tiantiantejia where site_id=19')
            # self.conn.commit()

            # print('111')
            # index = 1
            # for row in cs:      # 这样处理能避免时间延迟的错而退出
            #     print(index)
            #     # print(list(row))
            #     result.append(list(row))
            #     index += 1

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result

        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None
            # return result

    async def delete_taobao_tiantiantejia_expired_goods_id(self, goods_id, logger):
        cs = self.conn.cursor()
        try:
            cs.execute('delete from dbo.taobao_tiantiantejia where goods_id=%s', tuple([goods_id]))
            self.conn.commit()

            cs.close()
            return True
        except Exception as e:
            logger.error('--------------------| 删除对应goods_id[%s]记录时报错!' % goods_id)
            logger.exception(e)
            try:
                cs.close()
            except Exception:
                pass
            return False

    def select_tmall_all_goods_id_url(self):
        try:
            cs = self.conn.cursor()

            cs.execute('select SiteID, GoodsID, IsDelete, MyShelfAndDownTime from dbo.GoodsInfoAutoGet where SiteID=3 or SiteID=4 or SiteID=6 order by ID desc')
            # cs.execute('select SiteID, GoodsID, IsDelete, MyShelfAndDownTime from dbo.GoodsInfoAutoGet where GoodsID=%s', ('12763890166',))

            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def select_tmall_all_goods_id_url_by_site_6(self):
        cs = self.conn.cursor()
        try:
            cs.execute('select GoodsID, SiteID, GoodsUrl from dbo.GoodsInfoAutoGet where SiteID=6 order by ID desc')

            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def select_jd_all_goods_id_url(self):
        try:
            cs = self.conn.cursor()

            cs.execute('select SiteID, GoodsID, IsDelete, MyShelfAndDownTime from dbo.GoodsInfoAutoGet where SiteID=7 or SiteID=8 or SiteID=9 or SiteID=10')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def select_zhe_800_all_goods_id(self):
        try:
            cs = self.conn.cursor()

            cs.execute('select GoodsID, IsDelete, MyShelfAndDownTime from dbo.GoodsInfoAutoGet where SiteID=11')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def select_zhe_800_xianshimiaosha_all_goods_id(self):
        try:
            cs = self.conn.cursor()

            cs.execute('select goods_id, miaosha_time, session_id from dbo.zhe_800_xianshimiaosha where site_id=14')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def delete_zhe_800_expired_goods_id(self, goods_id):
        try:
            cs = self.conn.cursor()

            cs.execute('delete from dbo.zhe_800_xianshimiaosha where goods_id=%s', tuple([goods_id]))
            self.conn.commit()

            cs.close()
            return True
        except Exception as e:
            print('--------------------| 删除对应goods_id记录时报错：', e)
            try:
                cs.close()
            except Exception:
                pass

    def select_zhe_800_pintuan_all_goods_id(self):
        try:
            cs = self.conn.cursor()

            cs.execute('select goods_id, is_delete from dbo.zhe_800_pintuan where site_id=17')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def delete_zhe_800_pintuan_expired_goods_id(self, goods_id):
        try:
            cs = self.conn.cursor()

            cs.execute('delete from dbo.zhe_800_pintuan where goods_id=%s', tuple([goods_id]))
            self.conn.commit()

            cs.close()
            return True
        except Exception as e:
            print('--------------------| 删除对应goods_id记录时报错：', e)
            try:
                cs.close()
            except Exception:
                pass

    def select_juanpi_all_goods_id(self):
        try:
            cs = self.conn.cursor()

            cs.execute('select GoodsID, IsDelete, MyShelfAndDownTime from dbo.GoodsInfoAutoGet where SiteID=12')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def select_juanpi_xianshimiaosha_all_goods_id(self):
        try:
            cs = self.conn.cursor()

            cs.execute('select goods_id, miaosha_time, tab_id, page from dbo.juanpi_xianshimiaosha where site_id=15')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def delete_juanpi_expired_goods_id(self, goods_id):
        try:
            cs = self.conn.cursor()

            cs.execute('delete from dbo.juanpi_xianshimiaosha where goods_id=%s', tuple([goods_id]))
            self.conn.commit()

            cs.close()
            return True
        except Exception as e:
            print('--------------------| 删除对应goods_id记录时报错：', e)
            try:
                cs.close()
            except Exception:
                pass

    def select_juanpi_pintuan_all_goods_id(self):
        try:
            cs = self.conn.cursor()

            cs.execute('select goods_id, schedule, is_delete from dbo.juanpi_pintuan where site_id=18')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def delete_juanpi_pintuan_expired_goods_id(self, goods_id):
        try:
            cs = self.conn.cursor()

            cs.execute('delete from dbo.juanpi_pintuan where goods_id=%s', tuple([goods_id]))
            self.conn.commit()

            cs.close()
            return True
        except Exception as e:
            print('--------------------| 删除对应goods_id记录时报错：', e)
            try:
                cs.close()
            except Exception:
                pass

    def select_pinduoduo_all_goods_id(self):
        cs = self.conn.cursor()
        try:
            cs.execute('select GoodsID, IsDelete, MyShelfAndDownTime from dbo.GoodsInfoAutoGet where SiteID=13')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def select_pinduoduo_xianshimiaosha_all_goods_id(self):
        try:
            cs = self.conn.cursor()

            cs.execute('select goods_id, miaosha_time from dbo.pinduoduo_xianshimiaosha where site_id=16')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def delete_pinduoduo_expired_goods_id(self, goods_id):
        cs = self.conn.cursor()
        try:
            cs.execute('delete from dbo.pinduoduo_xianshimiaosha where goods_id=%s', tuple([goods_id]))
            self.conn.commit()

            cs.close()
            return True
        except Exception as e:
            print('--------------------| 删除对应goods_id记录时报错：', e)
            try:
                cs.close()
            except Exception:
                pass

    def select_vip_all_goods_id(self):
        cs = self.conn.cursor()
        try:
            cs.execute('select GoodsID, IsDelete, MyShelfAndDownTime from dbo.GoodsInfoAutoGet where SiteID=25')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def select_mia_xianshimiaosha_all_goods_id(self):
        cs = self.conn.cursor()
        try:
            cs.execute('select goods_id, miaosha_time, pid from dbo.mia_xianshimiaosha where site_id=20')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def delete_mia_miaosha_expired_goods_id(self, goods_id):
        cs = self.conn.cursor()
        try:
            cs.execute('delete from dbo.mia_xianshimiaosha where goods_id=%s', tuple([goods_id]))
            self.conn.commit()

            cs.close()
            return True
        except Exception as e:
            print('--------------------| 删除对应goods_id记录时报错：', e)
            try:
                cs.close()
            except Exception:
                pass

    def select_mia_pintuan_all_goods_id(self):
        cs = self.conn.cursor()
        try:
            cs.execute('select goods_id, miaosha_time, pid from dbo.mia_pintuan where site_id=21')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def delete_mia_pintuan_expired_goods_id(self, goods_id):
        cs = self.conn.cursor()
        try:
            cs.execute('delete from dbo.mia_pintuan where goods_id=%s', tuple([goods_id]))
            self.conn.commit()

            cs.close()
            return True
        except Exception as e:
            print('--------------------| 删除对应goods_id记录时报错：', e)
            try:
                cs.close()
            except Exception:
                pass

    def select_mogujie_xianshimiaosha_all_goods_id(self):
        cs = self.conn.cursor()
        try:
            cs.execute('select goods_id, miaosha_time, event_time, goods_url from dbo.mogujie_xianshimiaosha where site_id=22')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def delete_mogujie_miaosha_expired_goods_id(self, goods_id):
        cs = self.conn.cursor()
        try:
            cs.execute('delete from dbo.mogujie_xianshimiaosha where goods_id=%s', tuple([goods_id]))
            self.conn.commit()

            cs.close()
            return True
        except Exception as e:
            print('--------------------| 删除对应goods_id记录时报错：', e)
            try:
                cs.close()
            except Exception:
                pass

    def select_mogujie_pintuan_all_goods_id(self):
        cs = self.conn.cursor()
        try:
            cs.execute('select goods_id, miaosha_time, fcid, page from dbo.mogujie_pintuan where site_id=23')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def delete_mogujie_pintuan_expired_goods_id(self, goods_id):
        cs = self.conn.cursor()
        try:
            cs.execute('delete from dbo.mogujie_pintuan where goods_id=%s', tuple([goods_id]))
            self.conn.commit()

            cs.close()
            return True
        except Exception as e:
            print('--------------------| 删除对应goods_id记录时报错：', e)
            try:
                cs.close()
            except Exception:
                pass

    def select_chuchujie_xianshimiaosha_all_goods_id(self):
        cs = self.conn.cursor()
        try:
            cs.execute('select goods_id, miaosha_time, gender, page, goods_url from dbo.chuchujie_xianshimiaosha where site_id=24')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def delete_chuchujie_miaosha_expired_goods_id(self, goods_id):
        cs = self.conn.cursor()
        try:
            cs.execute('delete from dbo.chuchujie_xianshimiaosha where goods_id=%s', tuple([goods_id]))
            self.conn.commit()

            cs.close()
            return True
        except Exception as e:
            print('--------------------| 删除对应goods_id记录时报错：', e)
            try:
                cs.close()
            except Exception:
                pass

    def select_jumeiyoupin_xianshimiaosha_all_goods_id(self):
        cs = self.conn.cursor()
        try:
            cs.execute('select goods_id, miaosha_time, page, goods_url from dbo.jumeiyoupin_xianshimiaosha where site_id=26')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    async def select_jumeiyoupin_pintuan_all_goods_id(self, logger):
        cs = self.conn.cursor()
        try:
            cs.execute('select goods_id, miaosha_time, tab, page, goods_url from dbo.jumeiyoupin_pintuan where site_id=27')
            # self.conn.commit()

            result = list(cs.fetchall())
            # print(result)
            cs.close()
            return result
        except Exception as e:
            logger.exception(e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def delete_jumeiyoupin_miaosha_expired_goods_id(self, goods_id):
        cs = self.conn.cursor()
        try:
            cs.execute('delete from dbo.jumeiyoupin_xianshimiaosha where goods_id=%s', (goods_id))
            self.conn.commit()

            cs.close()
            return True
        except Exception as e:
            print('--------------------| 删除对应goods_id记录时报错：', e)
            try:
                cs.close()
            except Exception:
                pass

    async def delete_jumeiyoupin_pintuan_expired_goods_id(self, goods_id, logger):
        cs = self.conn.cursor()
        try:
            cs.execute('delete from dbo.jumeiyoupin_pintuan where goods_id=%s', (goods_id))
            self.conn.commit()

            cs.close()
            return True
        except Exception as e:
            logger.error('--------------------| 删除对应goods_id记录时报错如下：')
            logger.exception(e)
            try:
                cs.close()
            except Exception:
                pass

    def select_all_goods_info_from_GoodsInfoAutoGet_table(self):
        cs = self.conn.cursor()
        try:
            cs.execute(r'select GoodsID, SiteID from dbo.GoodsInfoAutoGet where MainGoodsID!=%s and IsDelete=0', ('',))
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def insert_into_jd_youxuan_daren_recommend_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['nick_name'],
                item['head_url'],
                item['profile'],
                item['share_id'],
                item['article_url'],
                item['title'],
                item['comment_content'],
                dumps(item['share_img_url_list'], ensure_ascii=False),
                dumps(item['goods_id_list'], ensure_ascii=False),
                item['div_body'],
                item['create_time'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.jd_youxuan_daren_recommend(nick_name, head_url, profile, share_id, gather_url, title, comment_content, share_img_url_list, goods_id_list, div_body, create_time) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'),
                       tuple(params))   # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def select_jd_youxuan_daren_recommend_all_share_id(self):
        try:
            cs = self.conn.cursor()
            cs.execute('select share_id from dbo.jd_youxuan_daren_recommend')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def select_all_nick_name_from_sina_weibo(self):
        cs = self.conn.cursor()
        try:
            # cs.execute('set lock_timeout 10000;')
            cs.execute('select nick_name from dbo.sina_weibo')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return []

    def insert_into_sina_weibo_table(self, item):
        cs = self.conn.cursor()
        try:
            params = [
                item['nick_name'],
                item['sina_type'],
                item['head_img_url'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('set lock_timeout 1500;')     # 设置客户端执行超时等待为1.5秒
            cs.execute('insert into dbo.sina_weibo(nick_name, sina_type, head_img_url) values(%s, %s, %s)'.encode('utf-8'),
                       tuple(params))   # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 4 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            # print('-' * 4 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            # print('-------------------------| 错误如下: ', e)
            # print('---->>| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def __del__(self):
        try:
            self.conn.close()
        except Exception:
            pass
        gc.collect()

class CommentInfoSaveItemPipeline(object):
    """
    页面存储管道
    """
    def __init__(self, logger=None):
        super(CommentInfoSaveItemPipeline, self).__init__()
        self.is_connect_success = True
        try:
            self.conn = connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DATABASE,
                port=PORT,
                charset='utf8'
            )
        except Exception:
            print('数据库连接失败!!')
            self.is_connect_success = False

        self._set_logger(logger)
        self.msg = ''

    def _set_logger(self, logger):
        if logger is None:
            self.my_lg = set_logger(
                log_file_name=MY_SPIDER_LOGS_PATH + '/db/_/' + str(get_shanghai_time())[0:10] + '.txt',
                console_log_level=INFO,
                file_log_level=ERROR
            )
        else:
            self.my_lg = logger

    def insert_into_comment(self, item):
        cs = self.conn.cursor()
        _ = True
        try:
            params = (
                item['goods_id'],
                item['create_time'],
                item['modify_time'],
                dumps(item['_comment_list'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
            )

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.all_goods_comment(goods_id, create_time, modify_time, comment_info) values(%s, %s, %s, %s)'.encode('utf-8'), params)  # 注意必须是tuple类型
            self.conn.commit()
            self.my_lg.info('-' * 9 + '| ***该页面信息成功存入sqlserver中*** |')
        except Exception as e:
            self.my_lg.error('| 修改信息失败, 未能将该页面信息存入到sqlserver中 出错goods_id: %s|' % item.get('goods_id'))
            self.my_lg.exception(e)
            _ = False

        finally:
            try:
                cs.close()
            except Exception:
                pass
            return _

    def update_comment(self, item):
        cs = self.conn.cursor()
        try:
            params = (
                item['modify_time'],
                dumps(item['_comment_list'], ensure_ascii=False),

                item['goods_id'],
            )

            cs.execute('update dbo.all_goods_comment set modify_time=%s, comment_info=%s where goods_id=%s', params)
            self.conn.commit()
            cs.close()
            self.my_lg.info('=' * 9 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            self.my_lg.error('| 修改信息失败, 未能将该页面信息存入到sqlserver中, 出错goods_id: %s|' % item['goods_id'])
            self.my_lg.exception(e)
            pass

    def select_all_goods_id_from_all_goods_comment_table(self):
        cs = self.conn.cursor()
        try:
            cs.execute(r'select goods_id from dbo.all_goods_comment')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            self.my_lg.exception(e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def inner_select_goods_info(self):
        cs = self.conn.cursor()
        try:
            cs.execute(r'select goods_id, SiteID as site_id from dbo.GoodsInfoAutoGet as a, dbo.all_goods_comment as b where a.GoodsID=b.goods_id')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            self.my_lg.exception(e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def __del__(self):
        try:
            del self.my_lg
            del self.msg
            del self.conn
        except:
            pass
        gc.collect()

class SqlPools(object):
    def __init__(self):
        super(SqlPools, self).__init__()
        self.is_connect_success = True
        try:
            self.engine = create_engine('mssql+pymssql://%s:%s@%s:%d/%s' % (USER, PASSWORD, HOST, PORT, DATABASE), pool_recycle=3600)
            self.conn = self.engine.connect()
        except Exception as e:
            print('数据库连接失败!!')
            self.is_connect_success = False

    def update_taobao_table(self, item, logger):
        self.engine.begin()
        self.conn = self.engine.connect()
        try:
            params = [
                item['modfiy_time'],
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
                item['month_sell_count'],
                dumps(item['my_shelf_and_down_time'], ensure_ascii=False),
                item['delete_time'],
                item['is_delete'],

                item['goods_id'],
            ]

            self.conn.execute('update dbo.GoodsInfoAutoGet set ModfiyTime = %s, ShopName=%s, Account=%s, GoodsName=%s, SubTitle=%s, LinkName=%s, Price=%s, TaoBaoPrice=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, ImageUrl=%s, PropertyInfo=%s, DetailInfo=%s, SellCount=%s, MyShelfAndDownTime=%s, delete_time=%s, IsDelete=%s where GoodsID = %s',
                tuple(params))
            # self.engine.commit()
            logger.info('=' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            try: self.conn.close()
            except: pass
            return True

        except Exception as e:
            logger.error('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 | 出错goods_id: ' + item['goods_id'])
            logger.exception(e)
            try: self.conn.close()
            except: pass
            return False

    def insert_into_taobao_tiantiantejia_table(self, item):
        self.engine.begin()
        self.conn = self.engine.connect()
        try:
            params = [
                item['goods_id'],
                item['goods_url'],
                item['deal_with_time'],
                item['modfiy_time'],
                item['shop_name'],
                item['account'],
                item['title'],
                item['sub_title'],
                item['price'],
                item['taobao_price'],
                dumps(item['detail_name_list'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
                item['div_desc'],  # 存入到DetailInfo
                item['month_sell_count'],
                dumps(item['schedule'], ensure_ascii=False),
                item['tejia_begin_time'],
                item['tejia_end_time'],
                item['block_id'],
                item['tag_id'],
                item['father_sort'],
                item['child_sort'],

                item['site_id'],
                item['is_delete'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            self.conn.execute('insert into dbo.taobao_tiantiantejia(goods_id, goods_url, create_time, modfiy_time, shop_name, account, goods_name, sub_title, price, taobao_price, sku_name, sku_info, all_img_url, property_info, detail_info, month_sell_count, schedule, tejia_begin_time, tejia_end_time, block_id, tag_id, father_sort, child_sort, site_id, is_delete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'), tuple(params))  # 注意必须是tuple类型
            # self.conn.commit()
            print('-' * 20 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            pass
        finally:
            try:
                self.conn.close()
            except Exception:
                pass

    def old_taobao_goods_insert_into_new_table(self, item):
        self.engine.begin()
        self.conn = self.engine.connect()
        try:
            params = [
                item['goods_id'],
                item['spider_url'],
                item['username'],
                item['deal_with_time'],
                item['modfiy_time'],
                item['shop_name'],
                item['account'],
                item['title'],
                item['sub_title'],
                item['link_name'],
                item['price'],
                item['taobao_price'],
                dumps(item['price_info'], ensure_ascii=False),
                dumps(item['detail_name_list'], ensure_ascii=False),    # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['price_info_list'], ensure_ascii=False),
                dumps(item['all_img_url'], ensure_ascii=False),
                dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
                item['div_desc'],                          # 存入到DetailInfo
                item['month_sell_count'],

                item['site_id'],
                item['is_delete'],
                item['main_goods_id'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            self.conn.execute('insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete, MainGoodsID) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'),
                       tuple(params))   # 注意必须是tuple类型
            # self.conn.commit()
            # self.conn.close()
            print('-' * 25 + '| ***该页面信息成功存入sqlserver中*** |')
            return True
        except Exception as e:
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            pass
        finally:
            try:
                self.conn.close()
            except Exception:
                pass

    def select_taobao_all_goods_id(self):
        self.engine.begin()
        self.conn = self.engine.connect()
        try:
            result = list(self.conn.execute('select GoodsID, IsDelete, MyShelfAndDownTime from dbo.GoodsInfoAutoGet where SiteID=1 order by ID desc'))
            # self.conn.commit()
            self.conn.close()
            # print(result)
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            self.conn.close()
            return None

    def select_taobao_tiantian_tejia_all_goods_id(self):
        self.engine.begin()
        self.conn = self.engine.connect()
        try:
            result = list(self.conn.execute('select goods_id, is_delete, schedule, block_id, tag_id from dbo.taobao_tiantiantejia where site_id=19'))
            # self.conn.commit()

            # print(result)
            self.conn.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                self.conn.close()
            except Exception:
                pass
            return None

class OtherDb(object):
    def __int__(self):
        super(OtherDb, self).__init__()
        self.is_connect_success = True
        try:
            print('连接数据库成功!')

            self.conn = connect(
                host=HOST_2,
                user=USER_2,
                password=PASSWORD_2,
                database=DATABASE_2,
                port=PORT_2,
                charset='utf8'
            )
            print('连接数据库成功!')
        except Exception as e:
            print(e)
            print('数据库连接失败!!')
            self.is_connect_success = False

    def select_other_db_goods_id(self):
        try:
            cs = self.conn.cursor()

            cs.execute('select GoodsID from dbo.GoodsInfoAutoGet where SiteID=2')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def select_other_db_goods_url(self):
        try:
            cs = self.conn.cursor()

            cs.execute('select GoodsUrl from dbo.GoodsInfoAutoGet where SiteID=1')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

class DataAnalysisDbPipeline(object):
    """
    数据分析: 数据信息获取管道
    """
    def __init__(self):
        super(DataAnalysisDbPipeline, self).__init__()
        self.is_connect_success = True
        try:
            self.conn = connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                database='db_k85u',
                port=PORT,
                charset='utf8'
            )
        except Exception as e:
            print('数据库连接失败!!')
            self.is_connect_success = False

    def select_everyday_order_sell_count(self, year, month, day):
        '''
        筛选每月的每日订单量
        :param year:
        :param month:
        :param day:
        :return:
        '''
        cs = self.conn.cursor()
        wait_to_deal_with_time = datetime.datetime(year, month, day, 0, 0, 0)
        day_add_1 = datetime.datetime(year, month, day+1, 0, 0, 0)
        params = (wait_to_deal_with_time, day_add_1,)
        # print(params)
        try:
            cs.execute('select count(*) from dbo.OrderInfo where CreateTime>%s and CreateTime<%s', params)
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            try:
                cs.close()
            except Exception:
                pass
            return None

    def select_every_month_order_sell_count(self, year, month):
        '''
        筛选某月的每日订单量
        :param year:
        :param month:
        :return:
        '''
        cs = self.conn.cursor()
        month_range = calendar.monthrange(year, month)      # 获得一个月有多少天 return (3, 30)
        month_order_sell_count_by_day_list = []
        for day in range(1, month_range[1]):
            wait_to_deal_with_time = datetime.datetime(year, month, day, 0, 0, 0)
            day_add_1 = datetime.datetime(year, month, day+1, 0, 0, 0)
            params = (wait_to_deal_with_time, day_add_1,)
            # print(params)
            try:
                cs.execute('select count(*) from dbo.OrderInfo where CreateTime>%s and CreateTime<%s', params)
                # self.conn.commit()

                result = cs.fetchall()
                # print(result)
                # cs.close()
                month_order_sell_count_by_day_list.append([day, result[0][0]])
            except Exception as e:
                print('--------------------| 筛选level时报错：', e)
                try:cs.close()
                except Exception: pass
                return None

        try: cs.close()
        except: pass

        return month_order_sell_count_by_day_list

    def select_one_year_every_month_order_sell_count(self, year):
        '''
        某年每月订单数
        :param year:
        :return:
        '''
        cs = self.conn.cursor()
        year_order_sell_count_by_month_list = []
        for month in range(1, 13):
            wait_to_deal_with_time = datetime.datetime(year, month, 1, 0, 0, 0)
            if month == 12:
                month_add_1 = datetime.datetime(year+1, month, 1, 0, 0)
            else:
                month_add_1 = datetime.datetime(year, month+1, 1, 0, 0, 0)
            params = (wait_to_deal_with_time, month_add_1,)
            # print(params)
            try:
                cs.execute('select count(*) from dbo.OrderInfo where CreateTime>%s and CreateTime<%s', params)
                # self.conn.commit()

                result = cs.fetchall()
                # print(result)
                # cs.close()
                year_order_sell_count_by_month_list.append([month, result[0][0]])
            except Exception as e:
                print('--------------------| 筛选level时报错：', e)
                try:
                    cs.close()
                except Exception:
                    pass
                return None

        try:
            cs.close()
        except:
            pass

        return year_order_sell_count_by_month_list
