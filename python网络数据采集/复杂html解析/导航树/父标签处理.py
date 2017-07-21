#coding: utf-8

#偶尔在特殊情况下你也会用到BeautifulSoup 的父标签查找函数, parent 和 parents
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
        print(bsObj.find('img', {"src":"../img/gifts/img1.jpg"
                            }).parent.previous_sibling.get_text())
        # 这段代码会打印 ../img/gifts/img1.jpg 这个图片对应商品的价格(这个示例中价格是$15.00)

'''
这是如何实现的呢?下面的图形是我们正在处理的 HTML 页面的部分结构,用数字表示步
骤的话:
• <tr>
    — <td>
    — <td>
    — <td>(3)
        — "$15.00" (4)
    — <td>(2)
        — <img src="../img/gifts/img1.jpg"> (1)
(1) 选择图片标签 src="../img/gifts/img1.jpg" ;
(2) 选择图片标签的父标签(在示例中是 <td> 标签);
(3) 选择 <td> 标签的前一个兄弟标签 previous_sibling (在示例中是包含美元价格的 <td>
标签);
(4) 选择标签中的文字,“$15.00”。
'''