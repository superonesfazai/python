# coding = utf-8

'''
@author = super_fazai
@File    : item_pipline_demo.py
@Time    : 2017/9/1 20:41
@connect : superonesfazai@gmail.com
'''

"""
编写item pipline很简单, item pipeline组件是一个独立的python类
其中process_item()方法必须实现
"""

class SomethingPipeline(object):
    def __init__(self):
        # 可选实现，做参数初始化等
        # doing something
        pass

    def process_item(self, item, spider):
        # item (Item 对象) – 被爬取的item
        # spider (Spider 对象) – 爬取该item的spider
        # 这个方法必须实现，每个item pipeline组件都需要调用该方法，
        # 这个方法必须返回一个 Item 对象，被丢弃的item将不会被之后的pipeline组件所处理。
        return item

    def open_spider(self, spider):
        # spider (Spider 对象) – 被开启的spider
        # 可选实现，当spider被开启时，这个方法被调用。
        pass

    def close_spider(self, spider):
        # spider (Spider 对象) – 被关闭的spider
        # 可选实现，当spider被关闭时，这个方法被调用
        pass

'''
* 启用一个Item Pipeline组件
    为了启用Item Pipeline组件，
    必须将它的类添加到 settings.py文件ITEM_PIPELINES 配置，

就像下面这个例子:
# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #'mySpider.pipelines.SomePipeline': 300,
    "mySpider.pipelines.ItcastJsonPipeline":300
}

分配给每个类的整型值，确定了他们运行的顺序，
item按数字从低到高的顺序，通过pipeline，
通常将这些数字定义在0-1000范围内(0-1000随意设置，数值越低，组件的优先级越高)
'''

'''
案例: item写入JSON文件
import json

class SomeWebNameJsonPipeline(object):
    def __init__(self):
        self.file = open('teacher.json', 'wb')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(content)
        return item

    def close_spider(self, spider):
        self.file.close()
'''