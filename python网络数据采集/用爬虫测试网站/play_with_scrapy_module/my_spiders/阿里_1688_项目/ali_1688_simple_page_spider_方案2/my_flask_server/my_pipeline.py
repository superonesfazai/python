# coding:utf-8

'''
@author = super_fazai
@File    : my_pipeline.py
@Time    : 2017/10/15 07:15
@connect : superonesfazai@gmail.com
'''

from MySQLdb import *

class UserItemPipeline(object):
    """
    用户信息处理管道
    """
    def __init__(self):
        super(UserItemPipeline, self).__init__()
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

            params = item

            # print(params)
            count = cs.execute('insert into ali_spider_employee_table(username, passwd) values(%s, %s)', params)
            self.conn.commit()

            print(count)
            cs.close()
            if count:
                print('-' * 60 + '| ***该用户信息成功存入mysql中*** |')
                return True
            else:
                print('-' * 60 + '| 修改信息失败, 未能将该用户信息存入到mysql中 ! |')
                return False
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


