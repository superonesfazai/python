# coding = utf-8

'''
@author = super_fazai
@File    : use_bs4_2_get_tags.py
@Time    : 2017/8/29 20:28
@connect : superonesfazai@gmail.com
'''

"""
使用 Beautiful Soup 来获取 Tags
"""

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

print(soup.title)
print(soup.head)
print(soup.a)
print(soup.p)
print(type(soup.p))

'''对于 Tag，它有两个重要的属性，是 name 和 attrs'''
print(soup.name)        # [document] #soup 对象本身比较特殊，它的 name 即为 [document]

print(soup.head.name)   # head #对于其他内部标签，输出的值便为标签本身的名称

print(soup.p.attrs)     # {'class': ['title'], 'name': 'dromouse'}

# 在这里，我们把 p 标签的所有属性打印输出了出来，得到的类型是一个字典。

print(soup.p['class'])  # soup.p.get('class')   # ['title'] #还可以利用get方法，传入属性的名称，二者是等价的

soup.p['class'] = "newClass"
print(soup.p)           # 可以对这些属性和内容等等进行修改
# <p class="newClass" name="dromouse"><b>The Dormouse's story</b></p>

del soup.p['class']     # 还可以对这个属性进行删除
print(soup.p)           # <p name="dromouse"><b>The Dormouse's story</b></p>

'''对于 NavigableString, 通过.string获取标签内部的文字'''
print(soup.p.string)    # The Dormouse's story
print(type(soup.p.string))      # <class 'bs4.element.NavigableString'>

'''对于 BeautifulSoup 对象表示的是一个文档的内容, 这里获取它的类型，名称，以及属性来感受一下'''
print(type(soup.name))  # <type 'unicode'>

print(soup.name)        # [document]

print(soup.attrs)       # {}  # 文档本身的属性为空

'''对于 Comment 对象是一个特殊类型的 NavigableString 对象，其输出的内容不包括注释符号'''
print(soup.a)           # <a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>

print(soup.a.string)    # Elsie

print(type(soup.a.string))  # <class 'bs4.element.Comment'>


'''
我们可以利用 soup 加标签名轻松地获取这些标签的内容，
这些对象的类型是bs4.element.Tag。但是注意，
它查找的是在所有内容中的第一个符合要求的标签。
如果要查询所有的标签，后面会进行介绍。
'''

'''
测试结果:
<title>The Dormouse's story</title>
<head><title>The Dormouse's story</title></head>
<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<class 'bs4.element.Tag'>
[document]
head
{'class': ['title'], 'name': 'dromouse'}
['title']
<p class="newClass" name="dromouse"><b>The Dormouse's story</b></p>
<p name="dromouse"><b>The Dormouse's story</b></p>
The Dormouse's story
<class 'bs4.element.NavigableString'>
<class 'str'>
[document]
{}
<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>
 Elsie 
<class 'bs4.element.Comment'>
'''