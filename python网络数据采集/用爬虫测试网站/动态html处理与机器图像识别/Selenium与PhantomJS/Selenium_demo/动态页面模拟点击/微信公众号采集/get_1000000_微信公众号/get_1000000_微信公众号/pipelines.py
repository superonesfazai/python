# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from redis import *
from MySQLdb import *

class Get1000000Pipeline(object):
    def __init__(self):
        super(Get1000000Pipeline, self).__init__()
        self.conn = connect(
            host='localhost',
            port=3306,
            db='python',
            user='root',
            passwd='lrf654321',
            # charset='utf-8',
        )

    def process_item(self, item, spider):
        tmp_sr = StrictRedis(host='127.0.0.1', port=6379, db=1)
        for item in list(item['em_weixinhao']):
            print(item)
            result = tmp_sr.get(item)
            if result is not None:
                print('正在写入文件中'.center(100, '*'))
                tmp_sr.set(item, 'True')
                self.insert_mysql(item)
            else:
                tmp = self.select_id_is_saved(item)
                if tmp:
                    self.insert_mysql(item)
                else:
                    print('========该公众号已经存在于mysql中, 插入失败!')

    def insert_mysql(self, item):
        try:
            cs1 = self.conn.cursor()

            count = cs1.execute('insert into gongzonghao(id) values(%s)', [item])
            self.conn.commit()
            cs1.close()

            if count is not None:
                print(item + '成功存入mysql')
            else:
                print('微信公众号已经存在于mysql中，插入失败!!')
        except Exception as e:
            print('========mysql错误为', e)

    def select_id_is_saved(self, item):
        try:
            cs = self.conn.cursor()

            cs.execute('select id from gongzonghao where id = \"%s\"', [item])

            result = cs.fetchone()

            cs.close()
            if result:
                print('========该公众号已经存在于mysql中, 插入失败!')
                return False
            else:
                return True
        except Exception as e:
            print('========mysql错误为', e)
            return False




