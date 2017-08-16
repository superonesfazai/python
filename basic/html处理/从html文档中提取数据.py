#!/usr/bin/python3.5
#coding: utf-8

#从 html 文档中提取数据的第一步是得到某个 HTML 文件系统

#urllib介绍
# #得到html
# import urllib
# #sock = urllib.urlopen('http://www.itcast.com')
# sock = open('itcast.html', 'r')     #在本地打开html文件的方法
# htmlSource = sock.read()
# sock.close()
# print(htmlSource)

#使用urllister.py

# import urllib, urllister
#
# usock = open('itcast.html', 'r')
# parser = urllister.URLLister()
# parser.feed(usock.read())       #调用定义在SGMLParser中的feed方法,将html内容放入分析器中
# usock.close()
# parser.close()      #一旦分析器被close,分析过程也就结束
# for url in parser.urls:   #parser.urls包含html文档中所有的链接url
#     print(url)

# 使用BaseHTMLProcessor
import BaseHTMLProcessor
sock = open('itcast.html', 'r')
parser = BaseHTMLProcessor.BaseHTMLParser()
tmp = parser.feed(sock.read())
print(parser.output())
# print(''.join(parser.output()))
sock.close()
parser.close()
