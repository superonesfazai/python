# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/10/11 14:24
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')
from my_requests import MyRequests

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://s.taobao.com/search?data-key=sort&data-value=sale-desc&ajax=true&_ksTS=1528171408340_395&callback=jsonp396&q=%E8%BF%9E%E8%A1%A3%E8%A3%99%E5%A4%8F&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306', headers=headers)

