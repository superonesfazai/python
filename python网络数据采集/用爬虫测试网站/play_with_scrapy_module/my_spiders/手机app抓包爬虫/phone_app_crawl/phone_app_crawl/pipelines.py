# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import scrapy
import os
from scrapy.utils.project import get_project_settings

class PhoneAppCrawlPipeline(object):
    def process_item(self, item, spider):
        return item

class ImagesPipeline(ImagesPipeline):
    # 获得自定义在settings里的元素
    IMAGES_STORE = get_project_settings().get('IMAGES_STORE')

    def get_media_requests(self, item, info):
        image_url = item['images_urls']
        yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        # 固定写法，获取图片路径, 同时判断这个路径是否正确, 如果正确, 就放到image_path里
        image_path = [x['path'] for ok, x in results if ok]

        os.rename(self.IMAGES_STORE + '/' + image_path[0], self.IMAGES_STORE + '/' + item['name'] + '.jpg')
        item['images_path'] = self.IMAGES_STORE + '/' + item['name']

        return item

    # get_media_requests的作用就是为每一个图片链接生成一个Request对象，这个方法的输出将作为item_completed的输入中的results，results是一个元组，每个元组包括(success, imageinfoorfailure)。如果success=true，imageinfoor_failure是一个字典，包括url/path/checksum三个key。


