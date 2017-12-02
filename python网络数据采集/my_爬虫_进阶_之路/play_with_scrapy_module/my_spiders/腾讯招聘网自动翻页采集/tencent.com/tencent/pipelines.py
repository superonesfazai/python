# coding = utf-8

'''
@author = super_fazai
@File    : pipeline.py
@Time    : 2017/9/1 21:15
@connect : superonesfazai@gmail.com
'''

import json

class TencentJsonPipeline(object):
    def __init__(self):
        self.file = open('tencent.json', 'wb')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False)
        self.file.write(content.encode('utf-8'))
        return item

    def close_spider(self, spider):
        self.file.close()