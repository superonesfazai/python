# coding=utf-8

'''
@author = super_fazai
@File    : my_pipeline.py
@Time    : 2017/10/15 07:15
@connect : superonesfazai@gmail.com
'''

from pymssql import *
from json import dumps, loads
import gc
import sqlalchemy
from sqlalchemy import create_engine
import datetime, calendar
import asyncio
from logging import (
    INFO,
    ERROR,
)
from pprint import pprint

from settings import (
    HOST,
    USER,
    PASSWORD,
    DATABASE,
    PORT,
    HOST_2,
    USER_2,
    PASSWORD_2,
    DATABASE_2,
    PORT_2,
    MY_SPIDER_LOGS_PATH,
)

from fzutils.log_utils import set_logger
from fzutils.time_utils import get_shanghai_time
from fzutils.sql_utils import BaseSqlServer

class SqlServerMyPageInfoSaveItemPipeline(BaseSqlServer):
    """
    页面存储管道
    """
    def __init__(self, host=HOST, user=USER, passwd=PASSWORD, db=DATABASE, port=PORT):
        super(SqlServerMyPageInfoSaveItemPipeline, self).__init__(
            host=host,
            user=user,
            passwd=passwd,
            db=db,
            port=port)

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
            logger.info('-' * 9 + '| ***该页面信息成功存入sqlserver中*** ')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            logger.error('-' * 9 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            logger.exception(e)
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
            print('---------| ***该页面信息成功存入sqlserver中*** ')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            print('---------| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('---------| 错误如下: ', e)
            print('---------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

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
            print('-' * 4 + '| ***该页面信息成功存入sqlserver中*** ')
            return True
        except Exception as e:
            try:
                cs.close()
            except Exception:
                pass
            # print('-' * 4 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            # print('---------| 错误如下: ', e)
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

    def _insert_into_table(self, sql_str, params:tuple):
        cs = self.conn.cursor()
        _ = False
        try:
            # logger.info(str(params))
            cs.execute(sql_str.encode('utf-8'), params)   # 注意必须是tuple类型
            self.conn.commit()
            self.my_lg.info('-' * 9 + '| ***该页面信息成功存入sqlserver中*** ')
            _ = True
        except IntegrityError:
            self.my_lg.info('重复插入goods_id[%s], 此处跳过!' % params[0])

        except Exception as e:
            self.my_lg.error('| 修改信息失败, 未能将该页面信息存入到sqlserver中 | 出错goods_id: %s' % params[0])
            self.my_lg.exception(e)
        finally:
            try:
                cs.close()
            except Exception:
                pass
            return _

    def _update_table(self, sql_str, params:tuple):
        cs = self.conn.cursor()
        _ = False
        try:
            cs.execute(sql_str, params)

            self.conn.commit()
            self.my_lg.info('-' * 9 + '| ***该页面信息成功存入sqlserver中*** ')
            _ = True
        except Exception as e:
            self.my_lg.error('| 修改信息失败, 未能将该页面信息存入到sqlserver中 出错goods_id: %s|' % params[-1])
            self.my_lg.exception(e)

        finally:
            try:
                cs.close()
            except Exception:
                pass
            return _

    def _select_table(self, sql_str, params=None):
        cs = self.conn.cursor()
        result = None
        try:
            if params is not None:
                if isinstance(params, tuple) is False:
                    params = tuple(params)
                cs.execute(sql_str, params)
            else:
                cs.execute(sql_str)
            # self.conn.commit()

            result = cs.fetchall()
        except Exception as e:
            self.my_lg.exception(e)
        finally:
            try:
                cs.close()
            except Exception:
                pass
            return result

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

    def _select_table(self, sql_str, params=None):
        self.engine.begin()
        self.conn = self.engine.connect()
        result = None

        try:
            self.conn.execute('set lock_timeout 20000;')     # 设置客户端执行超时等待为20秒
            if params is not None:
                if not isinstance(params, tuple):
                    params = tuple(params)
                result = self.conn.execute(sql_str, params).fetchall()
            else:
                result = self.conn.execute(sql_str).fetchall()

        except Exception as e:
            print('---------| 筛选level时报错：', e)
        finally:
            try:
                self.conn.close()
            except Exception:
                pass
            return result

    def _update_table(self, sql_str, params:tuple, logger):
        self.engine.begin()
        self.conn = self.engine.connect()
        _ = False
        try:
            self.conn.execute(sql_str, params)

            # self.engine.commit()
            logger.info('-' * 9 + '| ***该页面信息成功存入sqlserver中*** ')
            _ = True

        except Exception as e:
            logger.error('| 修改信息失败, 未能将该页面信息存入到sqlserver中 | 出错goods_id: %s' % params[-1] )
            logger.exception(e)

        finally:
            try:
                self.conn.close()
            except:
                pass
            return _

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
            print('-' * 9 + '| ***该页面信息成功存入sqlserver中*** ')
            return True
        except Exception as e:
            print('-' * 9 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('---------| 错误如下: ', e)
            print('---------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
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
            print('---------| ***该页面信息成功存入sqlserver中*** ')
            return True
        except Exception as e:
            print('---------| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('---------| 错误如下: ', e)
            print('---------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
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
            result = list(self.conn.execute('select GoodsID, IsDelete, MyShelfAndDownTime, Price, TaoBaoPrice from dbo.GoodsInfoAutoGet where SiteID=1'))
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