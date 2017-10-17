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
