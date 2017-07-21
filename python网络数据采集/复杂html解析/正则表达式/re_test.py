#coding: utf-8

# 正则表达式可以作为 BeautifulSoup 语句的任意一个参数
# 让你的目标元素查找工作极具灵活性
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re

try:
    html = urlopen('http://www.pythonscraping.com/pages/page3.html')
except HTTPError as e:
    print('url is not found!')
else:
    if html is None:
        print('url is None!')
    else:
        bsObj = BeautifulSoup(html)

        # 注意观察网页上有几个商品图片——它们的源代码形式如下:
        # <img src="../img/gifts/img3.jpg">
        images = bsObj.findAll("img", {"src": re.compile("\.\.\/img\/gifts/img.*\.jpg")})
        for image in images:
            print(image["src"])