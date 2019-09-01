# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from MySQLdb import *
from pymssql import *

class SinaWeiboProjectPipeline(object):
    def process_item(self, item, spider):
        return item

class BoZhuUserPipeline(object):
    def __init__(self):
        super(BoZhuUserPipeline, self).__init__()
        self.conn = connect(
            host='localhost',       # 主机地址
            port=3306,              # readme.md
            db='python',            # 数据库
            user='root',            # 用户
            passwd='lrf654321',     # 密码
            # charset='utf-8',
        )

    def process_item(self, item, spider):
        if item == '':
            print('============| 页面上的item获取完毕，没有新值 |')
            pass
        else:
            nick_name = item['nick_name']
            result = self.select_nick_name_is_saved(nick_name)

            if result:
                print('============| 该nick_name已经存在于mysql中, 存入数据失败!(select 时查到同一nick_name存在) |')
                pass
            else:
                print('============| 准备存入mysql........ |')
                self.insert_into_mysql(item)

    def insert_into_mysql(self, item):
        try:
            params = [
                item['nick_name'],
                item['sina_type'],
                item['nick_name_url'],
            ]
            cs1 = self.conn.cursor()
            count = cs1.execute('insert into bozhu_user(nick_name, sina_type, nick_name_url) values(%s, %s, %s)', params)
            self.conn.commit()
            cs1.close()

            if count is not None:
                print('============| ***该博主号成功存入mysql中*** |')
            else:
                print('微信公众号已经存在于mysql中，插入失败!!(insert 时发现重复插入)')
        except Exception as e:
            cs1.close()
            print('========插入mysql时错误为', e)
            pass


    def select_nick_name_is_saved(self, item):
        try:
            cs = self.conn.cursor()

            cs.execute('select nick_name from bozhu_user where nick_name = %s', [item])
            self.conn.commit()
            result = cs.fetchone()

            cs.close()
            if result:
                return True
            else:
                return False
        except Exception as e:
            print('========筛选mysql时错误为', e)
            cs.close()
            return True
