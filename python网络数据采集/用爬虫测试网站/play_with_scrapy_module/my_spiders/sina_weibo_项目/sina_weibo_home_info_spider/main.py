# coding:utf-8

'''
@author = super_fazai
@File    : main.py
@Time    : 2017/9/26 14:37
@connect : superonesfazai@gmail.com
'''

from scrapy import cmdline

# cmdline.execute("scrapy crawl user_home_info_spider".split())

cmdline.execute("scrapy crawl user_home_info_spider --nolog".split())

