# coding = utf-8

'''
@author = super_fazai
@File    : xpath_test.py
@Time    : 2017/8/29 17:59
@connect : superonesfazai@gmail.com
'''

"""
1. 获取所有li标签
"""
from lxml import etree

html = etree.parse('./hello.html')
print(type(html))   # 显示etree.parse返回的类型

result = html.xpath('//li')

print(result)
print(len(result))
print(type(result))
print(type(result[0]))

print('-' * 60)
"""
2. 继续获取<li> 标签的所有 class属性
"""
result = html.xpath('//li/@class')
print(result)

print('-' * 60)
"""
3. 继续获取<li>标签下hre 为 link1.html 的 <a> 标签
"""
result = html.xpath('//li/a[@href="link1.html"]')
print(result)

print('-' * 60)
"""
4. 获取<li> 标签下的所有 <span> 标签
"""
#result = html.xpath('//li/span')
#注意这么写是不对的：
#因为 / 是用来获取子元素的，而 <span> 并不是 <li> 的子元素，所以，要用双斜杠

result = html.xpath('//li//span')
print(result)

print('-' * 60)
"""
5. 获取 <li> 标签下的<a>标签里的所有 class
"""
result = html.xpath('//li/a//@class')
print(result)

print('-' * 60)
"""
6. 获取最后一个 <li> 的 <a> 的 href
"""
result = html.xpath('//li[last()]/a/@href')
# 谓语 [last()] 可以找到最后一个元素

print(result)

print('-' * 60)
"""
7. 获取倒数第二个元素的内容
"""
result = html.xpath('//li[last()-1]/a')

# text 方法可以获取元素内容
print(result[0].text)

print('-' * 60)
"""
8. 获取 class 值为 item-0 的标签名
"""
result = html.xpath('//*[@class="item-0"]')

# tag方法可以获取标签名
print(result[0].tag)


'''
测试结果:
<class 'lxml.etree._ElementTree'>
[<Element li at 0x102bb2188>, <Element li at 0x102bb21c8>, <Element li at 0x102bb2208>, <Element li at 0x102bb2248>, <Element li at 0x102bb2288>]
5
<class 'list'>
<class 'lxml.etree._Element'>
------------------------------------------------------------
['item-0', 'item-1', 'item-inactive', 'item-1', 'item-0']
------------------------------------------------------------
[<Element a at 0x102bb22c8>]
------------------------------------------------------------
[]
------------------------------------------------------------
[]
------------------------------------------------------------
['link5.html']
------------------------------------------------------------
fourth item
------------------------------------------------------------
li
'''