# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs  #它与普通的open函数最大的区别就在于文件的编码,它可以让我们避免很多编码方面的繁杂工作
import json
import sys
import MySQLdb

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter  #这个包用来方便json导出成其他文件

#pipelines主要用来做数据存储的
class AtriclespiderPipeline(object):
    def process_item(self, item, spider):
        return item

#保存json的pipeline
class JsonWithEncodingPipeline(object):
    #自定义json文件的导出
    def __init__(self):   #初始化打开一个文件
        self.file = codecs.open('article.json', 'w', encoding='utf-8')  #所以此处用codecs来打开文件以及写入

    def process_item(self, item, spider):  #写入文件  #一般process_item都是处理的关键地方
        #下面这两行是python2用来避免报UnicodeDecodeError: 'ascii' codec can't decode 的错
        #而python3则不需要这两行
        reload(sys)
        sys.setdefaultencoding('utf-8')
        #得到字符串
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'   #ensure_ascii=False为了避免中文写入不正常
        self.file.write(lines)
        return item   #此处必须return item,因为pipeline还得处理下一个

    def spider_closed(self, spider):  #关闭文件
        self.file.close()

class JsonExporterPipeline(object):
    #调用scrapy提供的json exporter来导出json文件
    def __init__(self):  #初始化一下
        self.file = open('articleexporter.json', 'wb')  #'wb' 是以二进制的形式打开
        # 下面这两行是python2用来避免报UnicodeDecodeError: 'ascii' codec can't decode 的错
        # 而python3则不需要这两行
        reload(sys)
        sys.setdefaultencoding('utf-8')

        self.exporter = JsonItemExporter(self.file, ensure_ascii=False)  #python2中的写法
        #self.exporter = JsonItemExporter(self.file, encode('utf-8'), ensure_ascii=False)  #此处为python3的写法
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('host', 'user', 'password', 'dbname', charset = 'utf-8', use_unicode=True)
        self.cursor = self.cursor()  #执行数据库的具体操作是用cursor完成的

    def process_item(self, item, spider):
        insert_sql = '''
            insert into jobbole_article(title, create_date, url, url_object_id, front_image_url, front_image_path, praise_nums, comment_nums, fav_nums, tags, content)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        self.cursor.execute(insert_sql, item['title'], item['create_date'], item['url'], item['url_object_id'], item['front_image_url'], item['front_image_path'], item['praise_nums'], item['comment_nums'], item['fav_nums'], item['tags'], item['content'])

#自己定制一个图片处理的pipeline,用来处理封面图
class AtricleImagePipeline(ImagesPipeline):
    #重载这一个函数
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value['path']
        item['front_image_path'] = image_file_path  #用item的front_image_path属性保存image_file_path的值
        return item  #提交一个处理好的item
