# coding = utf-8

'''
@author = super_fazai
@File    : use_bs4_css选择器.py
@connect : superonesfazai@gmail.com
'''

from bs4 import BeautifulSoup

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

# 创建 Beautiful Soup 对象
soup = BeautifulSoup(html, 'lxml')

# 1. 通过标签名查找
print(soup.select('title'))     # [<title>The Dormouse's story</title>]
print(soup.select('a'))
print(soup.select('b'))

# 2. 通过类名查找
print(soup.select('.sister'))

# 3.通过id名查找
print(soup.select('#link1'))

# 4. 组合查找
print(soup.select('p #link1'))
print(soup.select('head > title'))

# 5. 属性查找
print(soup.select('a[class="sister"]'))
print(soup.select('a[href="http://example.com/elsie"]'))
print(soup.select('p a[href="http://example.com/elsie"]'))

# 6. 获取内容
# 以上的 select 方法返回的结果都是列表形式，可以遍历形式输出，然后用 get_text() 方法来获取它的内容
print(type(soup.select('title')))
print(soup.select('title')[0].get_text())

for title in soup.select('title'):
    print(title.get_text())