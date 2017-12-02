# coding:utf-8

'''
@author = super_fazai
@File    : my_pipelines.py
@Time    : 2017/10/4 15:23
@connect : superonesfazai@gmail.com
'''
from MySQLdb import *

class MySinaWeiboReviewsItemPipeline(object):
    def __init__(self):
        super(MySinaWeiboReviewsItemPipeline, self).__init__()
        self.conn = connect(
            host='localhost',
            port=3306,
            db='python',
            user='root',
            passwd='lrf654321',
            # charset='utf-8',
        )

    def process_item(self, item):
        if item is None:
            print('-' * 60 + '| 传入的Item为空! |')
            pass
        else:
            review_id = item['review_id']
            result = self.select_is_had_nick_name(review_id)

            if result:
                print('-' * 60 + '| 准备存入mysql中 ...... |')
                self.insert_into_table(item)
            else:
                print('-' * 60 + '| 该评论信息已经存在, 插入失败！|')
                pass

    def insert_into_table(self, item):
        try:
            cs = self.conn.cursor()

            params = [
                item['review_id'],
                item['wb_id'],
                item['username'],
                item['comment'],
                item['review_created_at'],
                item['is_reply_comment'],
                item['like_counts'],
                item['review_pics'],
                item['by_review_name'],
            ]

            # print(params)
            count = cs.execute(
                'insert into sina_review(review_id, wb_id, username, comment, review_created_at, is_reply_comment, like_counts, review_pics, by_review_name) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                params)
            self.conn.commit()

            print(count)
            cs.close()
            if count:
                print('-' * 60 + '| ***该评论信息成功存入mysql中*** |')
            else:
                print('-' * 60 + '| 修改信息失败, 未能将该评论信息存入到mysql中 ! |')
        except Exception as e:
            cs.close()
            print('-' * 60 + '| 修改信息失败, 未能将该评论信息存入到mysql中 |')
            print('--------------------| 错误如下: ', e)
            print('--------------------| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
            pass

    def select_is_had_nick_name(self, review_id):
        try:
            cs = self.conn.cursor()

            params = [
                review_id,
            ]

            cs.execute('select review_id from sina_review where review_id = %s', params)
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