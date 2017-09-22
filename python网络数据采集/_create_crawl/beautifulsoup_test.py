#coding:utf-8

from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/page1.html')

bsObj = BeautifulSoup(html.read())
print(bsObj.h1)

# 打印同样效果
# print(bs_obj.html.body.h1)
# print(bs_obj.body.h1)
# print(bs_obj.html.h1)