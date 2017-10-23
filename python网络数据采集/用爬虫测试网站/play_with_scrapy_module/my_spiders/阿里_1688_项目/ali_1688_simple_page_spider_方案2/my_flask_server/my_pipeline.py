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

from settings import HOST, USER, PASSWORD, DATABASE, PORT
# from .settings import HOST, USER, PASSWORD, DATABASE, PORT

class UserItemPipeline(object):
    """
    用户信息处理管道
    """
    def __init__(self):
        super(UserItemPipeline, self).__init__()
        self.conn = connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            port=PORT,
            charset='utf8'
        )

    def insert_into_table(self, item):
        try:
            cs = self.conn.cursor()

            params = item

            # print(params)
            # pymssql下的execute执行插入语句成功返回的值也是None, 所以不判断返回的行数
            cs.execute('insert into dbo.ali_spider_employee_table(username, passwd) values(%s, %s)', tuple(params))
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
        self.conn = connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            port=PORT,
            charset='utf8'
        )

    def insert_into_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['goods_id'],
                item['spider_url'],
                item['username'],
                item['deal_with_time'],
                item['company_name'],
                item['title'],
                item['link_name'],
                item['link_name_personal_url'],
                dumps(item['price_info'], ensure_ascii=False),        # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
                dumps(item['goods_name'], ensure_ascii=False),
                dumps(item['goods_info'], ensure_ascii=False),
                item['center_img_url'],
                dumps(item['all_img_url_info'], ensure_ascii=False),
                dumps(item['p_info'], ensure_ascii=False),
                item['property_info'],

                item['site_id'],
                item['is_delete'],
            ]

            # print(params)
            # ---->>> 注意要写对要插入数据的所有者,不然报错
            cs.execute('insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ShopName, GoodsName, LinkName, LinkNamePersonalUrl, PriceInfo, SKUName, SKUInfo, CenterImgUrl, ImageUrl, DetailInfo, PropertyInfo, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'.encode('utf-8'),
                       tuple(params))   # 注意必须是tuple类型
            self.conn.commit()
            cs.close()
            print('-' * 25 + '| ***该页面信息成功存入mysql中*** |')
            return True
        except Exception as e:
            cs.close()
            print('-' * 25 + '| 修改信息失败, 未能将该页面信息存入到mysql中 |')
            print('-------------------------| 错误如下: ', e)
            print('-------------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            return False

    def update_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['deal_with_time'],
                item['company_name'],
                item['title'],
                item['link_name'],
                item['link_name_personal_url'],
                dumps(item['price_info'], ensure_ascii=False),
                dumps(item['goods_name'], ensure_ascii=False),
                dumps(item['goods_info'], ensure_ascii=False),
                item['center_img_url'],
                dumps(item['all_img_url_info'], ensure_ascii=False),
                dumps(item['p_info'], ensure_ascii=False),
                item['property_info'],
                item['is_delete'],

                # item['username'],
                item['goods_id'],
            ]

            cs.execute('update dbo.GoodsInfoAutoGet set CreateTime = %s, ShopName=%s, GoodsName=%s, LinkName=%s, LinkNamePersonalUrl=%s, PriceInfo=%s, SKUName=%s, SKUInfo=%s, CenterImgUrl=%s, ImageUrl=%s, DetailInfo=%s, PropertyInfo=%s, IsDelete=%s where GoodsID = %s',
                       tuple(params))
            self.conn.commit()
            cs.close()
            print('=' * 20 + '| ***该页面信息成功存入mysql中*** |')
            return True
        except Exception as e:
            cs.close()
            print('-' * 20 + '| 修改信息失败, 未能将该页面信息存入到mysql中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是传入数据有误导致, 可以忽略 ... |')
            pass

    def select_all_goods_id(self):
        try:
            cs = self.conn.cursor()

            cs.execute('select GoodsID from dbo.GoodsInfoAutoGet')
            # self.conn.commit()

            result = cs.fetchall()
            # print(result)
            cs.close()
            return result
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            cs.close()
            return None



