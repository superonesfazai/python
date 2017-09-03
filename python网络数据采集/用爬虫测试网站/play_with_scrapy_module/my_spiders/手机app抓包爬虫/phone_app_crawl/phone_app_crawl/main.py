# coding = utf-8

'''
@author = super_fazai
@File    : main.py.py
@Time    : 2017/9/2 21:17
@connect : superonesfazai@gmail.com
'''

# 在根目录下新建main.py文件, 用于调试
from scrapy import cmdline

cmdline.execute('scrapy crawl douyu'.split())