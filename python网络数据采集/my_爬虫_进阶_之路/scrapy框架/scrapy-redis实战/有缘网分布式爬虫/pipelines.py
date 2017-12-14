# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from datetime import datetime

class ExamplePipeline(object):
    def process_item(self, item, spider):
        # utcnow()  获取UTC时间
        item["crawled"] = datetime.utcnow()
        # 爬虫名
        item["spider"] = spider.name
        return item
