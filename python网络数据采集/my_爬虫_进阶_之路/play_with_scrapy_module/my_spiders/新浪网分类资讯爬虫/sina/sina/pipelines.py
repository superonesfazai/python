# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals

class SinaPipeline(object):
    def process_item(self, item, spider):
        son_urls = item['son_urls']

        # 文件名为子链接url中间部分，并将 / 替换为 _，保存为 .txt格式
        file_name = son_urls[7:-6].replace('/','_')
        file_name += ".txt"

        fp = open(item['sub_file_name']+'/'+file_name, 'w', encoding='utf-8')
        fp.write(item['content'])
        fp.close()

        return item
