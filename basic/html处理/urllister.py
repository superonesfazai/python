#!/usr/bin/python2.7
#coding:utf-8

from sgmllib import SGMLParser      #使用其它包得自己导入在其他python环境里

class URLLister(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.urls = []

    def start_a(self, attrs):       #只要找到一个 <a> 标记, start_a 就会由 SGMLParser 进行调用。这个标记可以包含一个 href 属性,或者包含其它的属性,如 name 或 title, attrs 参数是一个 tuple 的 list
        href = [v for k, v in attrs if k == 'href']
        if href:
            self.urls.extend(href)
