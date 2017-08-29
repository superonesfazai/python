# coding = utf-8

'''
@author = super_fazai
@File    : lxml_test.py
@Time    : 2017/8/29 17:46
@connect : superonesfazai@gmail.com
'''

"""
lxml 可以自动修正 html 代码，
例子里不仅补全了 li 标签，还添加了 body，html 标签。

下面 将字符串解析为html文档, 然后序列化为html文档
"""

from lxml import etree  # 使用 lxml 的 etree 库

text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a> # 注意，此处缺少一个 </li> 闭合标签
     </ul>
 </div>
'''

# 利用etree.HTML，将字符串解析为HTML文档
html = etree.HTML(text)

# 按字符串序列化HTML文档
result = etree.tostring(html)

print(result.decode())

'''
测试结果:
<html><body><div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a> # &#27880;&#24847;&#65292;&#27492;&#22788;&#32570;&#23569;&#19968;&#20010; </li> &#38381;&#21512;&#26631;&#31614;
     </ul>
 </div>
</body></html>
'''