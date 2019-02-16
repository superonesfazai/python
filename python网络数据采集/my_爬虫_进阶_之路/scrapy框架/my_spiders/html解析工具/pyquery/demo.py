# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

from lxml import etree
from pyquery import PyQuery as pq

# pq 参数可以直接传入 HTML 代码，doc 现在就相当于 jQuery 里面的 $ 符号

# 先用 lxml 的 etree 处理一下代码，这样如果你的 HTML 代码出现一些不完整或者疏漏，自动转化为完整清晰结构的 HTML代码
doc1 = pq(etree.fromstring(text='<html></html>'))

tmp_div = r'''
<div>
    <ul>
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
'''
doc2 = pq(etree.fromstring(text=tmp_div))
print(doc2.html())
print(type(doc2))       # <class 'pyquery.pyquery.PyQuery'>
li = doc2('li')
print(type(li))         # <class 'pyquery.pyquery.PyQuery'>
print(li.text())        # first item second item third item fourth item fifth item