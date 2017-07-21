#coding:utf-8

# 如果你只想找出子标签,可以用 .children 标签
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

try:
    html = urlopen('http://www.pythonscraping.com/pages/page3.html')
except HTTPError as e:
    print('url is not found!')
else:
    if html is None:
        print('url is None!')
    else:
        bsObj = BeautifulSoup(html)
        for child in bsObj.find('table', {'id': 'giftList'}).children:
            print(child)

'''
这段代码会打印 giftList 表格中所有产品的数据行。如果你用 descendants() 函数而不是
children() 函数,那么就会有二十几个标签打印出来,包括 img 标签、 span 标签,以及每
个 td 标签。掌握子标签与后代标签的差别十分重要!
'''