# coding = utf-8

'''
@author = super_fazai
@File    : lxml_parse.py
@Time    : 2017/8/29 17:52
@connect : superonesfazai@gmail.com
'''

"""
文件读取
    除了直接读取字符串，lxml还支持从文件里读取内容
    
下面 利用 etree.parse() 方法来读取文件
"""

from lxml import etree

# 读取外部文件 hello.html
html = etree.parse('./hello.html')
result = etree.tostring(html, pretty_print=True)

print(result.decode())

'''
测试结果:
<!-- hello.html -->
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
'''