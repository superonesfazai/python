#coding:utf-8

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
        # BeautifulSoup 的 next_siblings() 函数可以让收集表格数据成为简单的事情
        # 尤其是处理带标题行的表格
        for sibling in bsObj.find('table', {'id': 'giftList'}).tr.next_siblings:
            print(sibling)
        # 这段代码会打印产品列表里的所有行的产品,第一行表格标题除外
        # 为什么标题行被跳过了呢?有两个理由。
        # 首先,对象不能把自己作为兄弟标签。
        # 任何时候你获取一个标签的兄弟标签,都不会包含这个标签本身。其次,这个函数只调用后面的兄弟标签

        # 如果你很容易找到一组兄弟标签中的最后一个标签,那么previous_siblings 函数也会很有用
        # 当然,还有 next_sibling 和 previous_sibling 函数,与 next_siblings 和 previous_siblings
        # 的作用类似,只是它们返回的是单个标签,而不是一组标签