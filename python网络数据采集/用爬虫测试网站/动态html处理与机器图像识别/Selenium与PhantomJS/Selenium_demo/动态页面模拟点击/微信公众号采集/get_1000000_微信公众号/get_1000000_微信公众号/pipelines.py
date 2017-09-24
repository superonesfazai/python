# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from redis import *

class Get1000000Pipeline(object):
    def process_item(self, item, spider):
        print('正在写入文件中'.center(100, '*'))

        tmp_sr = StrictRedis(host='127.0.0.1', port=6379, db=0)
        for item in list(item['em_weixinhao']):
            print(item)
            result = tmp_sr.get(item)
            if result == None:
                tmp_sr.set(item, 'True')


