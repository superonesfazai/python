# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from MySQLdb import *

class SinaWeiboHomeInfoSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class HomeInfoPipeline(object):
    def __init__(self):
        super(HomeInfoPipeline, self).__init__()
        self.conn = connect(
            host='localhost',
            port=3306,
            db='python',
            user='root',
            passwd='lrf654321',
            # charset='utf-8',
        )

    def process_item(self, item, spider):
        if item is None:
            print('=' * 12 + '| 传入的Item为空! |')
            pass
        else:
            nick_name = item['nick_name']
            result = self.select_level_is_zero(nick_name)

            if result:
                print('=' * 12 + '| 准备存入mysql中 ...... |')
                self.insert_into_table(item)
            else:
                print('=' * 12 + '| 该微博号的信息已经存在, 插入失败！|')
                pass

    def insert_into_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['care_number'],
                item['fans_number'],
                item['weibo_number'],
                item['verify_type'],
                item['sina_level'],
                item['verify_desc'],
                item['personal_deal_info_url'],
                item['nick_name'],
            ]

            # print(params)
            count = cs.execute('update bozhu_user set care_number = %s, fans_number = %s, weibo_number = %s, verify_type = %s, sina_level = %s, verify_desc = %s, personal_deal_info_url = %s where nick_name = %s;', params)
            self.conn.commit()

            print(count)
            cs.close()
            if count:
                print('============| ***该博主主页信息成功存入mysql中*** |')
            else:
                print('=' * 12 + '| 修改信息失败, 未能将主页信息存入到mysql中 ! |')
        except Exception as e:
            cs.close()
            print('=' * 12 + '| 修改信息失败, 未能将主页信息存入到mysql中 |')
            print('============| 错误如下: ', e)
            pass

    def select_level_is_zero(self, nick_name):
        try:
            cs = self.conn.cursor()

            params = [
                nick_name,
            ]
            cs.execute('select sina_level from bozhu_user where nick_name = %s', params)
            self.conn.commit()
            cs.close()
            # print(type(cs.fetchone()))      # return  ->  <class 'NoneType'>
            if cs.fetchone():
                return False
            else:
                return True
        except Exception as e:
            print('============| 筛选level时报错：', e)
            cs.close()
            return False
