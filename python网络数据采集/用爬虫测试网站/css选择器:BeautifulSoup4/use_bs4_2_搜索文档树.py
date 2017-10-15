# coding = utf-8

'''
@author = super_fazai
@File    : use_bs4_2_搜索文档树.py
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

# name参数--传字符串
print(soup.find_all('a'))

# name参数--传正则表达式
import re
for tag in soup.find_all(re.compile(r'^b')):
    print(tag.name)

# name参数--传list
print(soup.find_all(['a', 'b']))

# keyword参数
print(soup.find_all(id='link2'))

# text参数
print(soup.find_all(text='Elsie'))      # []
print(soup.find_all(text=["Tillie", "Elsie", "Lacie"]))     # ['Lacie', 'Tillie']
print(soup.find_all(text=re.compile("Dormouse")))   # ["The Dormouse's story", "The Dormouse's story"]