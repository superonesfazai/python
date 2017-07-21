#coding: utf-8

from xml.dom import minidom

#不能用~,只能是具体的路径
#这就是进行所有工作的一行代码: minidom.parse 接收一个参数并返回 XML文档解析后的表示形式
xmldoc = minidom.parse('/home/afa/myFiles/codeDoc/PythonDoc/basic/xml处理/artifacts.xml')
print(type(xmldoc))
#print(xmldoc.toxml())      #打印整个xml
print(xmldoc.childNodes)
print(xmldoc.childNodes[0])
print(xmldoc._get_firstChild())

grammarNode = xmldoc._get_firstChild()
print(grammarNode.toxml())
print(grammarNode.childNodes)
print(grammarNode._get_lastChild())
#print(xmldoc._get_lastChild().toxml())     #打印最后一个字节点的xml

print()
print(grammarNode)
print(grammarNode.data)     #因为第一个节点的字节点为0,所以取它的下一个节点进行数据分析
refNode = grammarNode.childNodes
print(refNode)


#把文本挖出来
grammarNode = xmldoc.childNodes[1]
print(grammarNode)
repNode = grammarNode.childNodes[1]
print(repNode)
print(repNode.childNodes)
print()

pNode = repNode.childNodes[1]
print(pNode.toxml())
print(pNode._get_firstChild())

print()

print('下面是解析文本：')
#解析文本
from xml.dom import minidom

xmldoc = minidom.parse('/home/afa/myFiles/codeDoc/PythonDoc/basic/xml处理/artifacts.xml')
#每个元素都是可搜索的
title = xmldoc.getElementsByTagName('properties')[0].childNodes[1]
print('title:')
print(title)
#convertedtitle = title.encode('utf-8')
#print(convertedtitle)

print()
#xml属性
print('xml属性：')
replist = xmldoc.getElementsByTagName('properties')
print(replist[0].toxml())
print(replist[0].attributes)
print(replist[0].attributes.keys())
print(replist[0].attributes.values())
#访问单个属性, 通过'.name','.value'访问对应属性的key和value
print(replist[0].attributes['size'])
print(replist[0].childNodes[1].attributes['name'])
print(replist[0].childNodes[1].attributes['name'].value)
print(replist[0].childNodes[1].attributes['value'].name)
print(replist[0].childNodes[1].attributes['value'].value)

'''
(1) Attr 对象完整代表了单个 XML 元素的单个 XML 属性。属性的名称 (与你在bitref.attributes NamedNodeMap伪字典中寻找的对象同名) 保存在 a.name 中。
(2) 这个 XML 属性的真实文本值保存在 a.value 中。
'''

'''
Note: 属性没有顺序
类似于字典,一个 XML 元素的属性没有顺序。属性可以以某种顺序 偶然 列在
最初的 XML 文档中,而在 XML 文档解析为 Python 对象时, Attr 对象以某种顺
序 偶然 列出,这些顺序都是任意的,没有任何特别的含义。你应该总是使用
名称来访问单个属性,就像字典的键一样
'''