#coding:utf-8
__author__ = 'super_fazai'

from scrapy.cmdline import execute

import sys
import os

#得到父目录
#print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#execute(['scrapy', 'crawl', 'baidu'])