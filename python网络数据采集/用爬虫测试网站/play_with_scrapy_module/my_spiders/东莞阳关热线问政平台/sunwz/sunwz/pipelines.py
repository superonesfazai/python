# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import codecs   # 文件处理类库, 可以指定编码格式
import json

class SunwzPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWriterPipeline(object):
    def __init__(self):
        # 创建一个只写文件, 指定文本编码格式为utf-8
        self.file_name = codecs.open('sunwz.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False)
        self.file_name.write(content)
        return item

    def spider_closed(self, spider):
        self.file.close()
