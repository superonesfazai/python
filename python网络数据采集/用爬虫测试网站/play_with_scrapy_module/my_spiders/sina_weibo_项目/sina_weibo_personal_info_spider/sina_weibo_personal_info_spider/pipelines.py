# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from MySQLdb import *

class SinaWeiboPersonalInfoSpiderPipeline(object):
    def __init__(self):
        super(SinaWeiboPersonalInfoSpiderPipeline, self).__init__()
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
            print('-' * 60 + '| 传入的Item为空! |')
            pass
        else:
            nick_name = item['nick_name']
            result = self.select_is_had_nick_name(nick_name)

            if result:
                print('-' * 60 + '| 准备存入mysql中 ...... |')
                self.insert_into_table(item)
            else:
                print('-' * 60 + '| 该微博号的信息已经存在, 插入失败！|')
                pass

    def insert_into_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['nick_name'],
                item['true_name'],
                item['live_place'],
                item['sex'],
                item['love_man_or_woman'],
                item['feeling'],
                item['birthday'],
                item['blood_type'],
                item['blog_url'],
                item['simple_desc'],
                item['individuality_url'],
                item['register_time'],
                item['_email'],
                item['qq'],
                item['msn'],
                item['company'],
                item['edu'],
                item['_label'],

                item['medal_info'],
                item['sina_level'],
                item['sina_level_exp'],
                item['vip_icon'],
                item['vip_group_speed'],
                item['vip_group_value'],
                item['credit_value'],
            ]

            # print(params)
            count = cs.execute('insert into personal_deal_info(nick_name, true_name, live_place, sex, love_man_or_woman, feeling, birthday, blood_type, blog_url, simple_desc, individuality_url, register_time, _email, qq, msn, company, edu, _label, medal_info, sina_level, sina_level_exp, vip_icon, vip_group_speed, vip_group_value, credit_value) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', params)
            self.conn.commit()

            print('受影响行数: ' + str(count))
            cs.close()
            if count:
                print('-' * 60 + '| ***该博主主页信息成功存入mysql中*** |')
            else:
                print('-' * 60 + '| 插入信息失败, 未能将主页信息存入到mysql中 ! |')
        except Exception as e:
            cs.close()
            print('-' * 60 + '| 插入信息失败, 未能将主页信息存入到mysql中 |')
            print('--------------------| 错误如下: ', e.args[0])
            pass

    def select_is_had_nick_name(self, nick_name):
        try:
            cs = self.conn.cursor()

            params = [
                nick_name,
            ]

            cs.execute('select nick_name from personal_deal_info where nick_name = %s', params)
            self.conn.commit()
            cs.close()
            # print(type(cs.fetchone()))      # return  ->  <class 'NoneType'>
            if cs.fetchone():
                return False
            else:
                return True
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            cs.close()
            return False


class SinaWeiboCompanyDealInfoSpiderPipeline(object):
    def __init__(self):
        super(SinaWeiboCompanyDealInfoSpiderPipeline, self).__init__()
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
            print('-' * 60 + '| 传入的Item为空! |')
            pass
        else:
            nick_name = item['nick_name']
            result = self.select_is_had_nick_name(nick_name)

            if result:
                print('-' * 60 + '| 准备存入mysql中 ...... |')
                self.insert_into_table(item)
            else:
                print('-' * 60 + '| 该微博号的信息已经存在, 插入失败！|')
                pass

    def insert_into_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['nick_name'],

                item['simple_desc'],
                item['company_contact_name'],
                item['company_phone'],
                item['friend_url'],

                item['medal_info'],
                item['sina_level'],
                item['sina_level_exp'],
                item['vip_icon'],
                item['vip_group_speed'],
                item['vip_group_value'],
            ]

            # print(params)
            count = cs.execute(
                'insert into company_deal_info(nick_name, simple_desc, company_contact_name, company_phone, friend_url, medal_info, sina_level, sina_level_exp, vip_icon, vip_group_speed, vip_group_value) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                params)
            self.conn.commit()

            print(count)
            cs.close()
            if count:
                print('-' * 60 + '| ***该博主主页信息成功存入mysql中*** |')
            else:
                print('-' * 60 + '| 修改信息失败, 未能将主页信息存入到mysql中 ! |')
        except Exception as e:
            cs.close()
            print('-' * 60 + '| 修改信息失败, 未能将主页信息存入到mysql中 |')
            print('--------------------| 错误如下: ', e)
            pass

    def select_is_had_nick_name(self, nick_name):
        try:
            cs = self.conn.cursor()

            params = [
                nick_name,
            ]

            cs.execute('select nick_name from company_deal_info where nick_name = %s', params)
            self.conn.commit()
            cs.close()
            # print(type(cs.fetchone()))      # return  ->  <class 'NoneType'>
            if cs.fetchone():
                return False
            else:
                return True
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
            cs.close()
            return False



