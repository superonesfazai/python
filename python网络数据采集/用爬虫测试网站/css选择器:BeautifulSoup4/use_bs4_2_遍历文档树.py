# coding = utf-8

'''
@author = super_fazai
@File    : use_bs4_2_遍历文档树.py
@Time    : 2017/8/30 09:09
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

# .content
print(soup.head.contents)       # [<title>The Dormouse's story</title>]
print(soup.head.contents[0])    # 输出方式为list, 通过索引来获得其某一个元素  # [<title>The Dormouse's story</title>]

print('-' * 60)

# .children
print(soup.head.children)       #<listiterator object at 0x7f71457f5710>

for child in soup.body.children:
    print(child)

print('-' * 60)

# .descendants 属性可以对所有tag的子孙节点进行递归循环
for child in soup.descendants:
    print(child)

# 节点属性: .string属性
print(soup.head.string)         # The Dormouse's story
print(soup.title.string)        # The Dormouse's story

