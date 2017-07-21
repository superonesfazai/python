#coding:utf-8

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

try:
    html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
except HTTPError as e:
    print('url is not found!')
else:
    if html is None:
        print('url is None!')
    else:
        bsObj = BeautifulSoup(html)
        # 现在,我们调用 bs_obj.findAll(tagName, tagAttributes) 可以获取页面中所有指定的标签,不再只是第一个了
        nameList = bsObj.findAll('span', {'class':'green'})
        for name in nameList:
            # .get_text() 会把你正在处理的 HTML 文档中所有的标签都清除
            # 然后返回一个只包含文字的字符串
            # 假如你正在处理一个包含许多超链接、段落和标签的大段源代码,那么 .get_text() 会把这些超链接、段落和标签都清除掉,只剩下一串不带标签的文字
            # 通常在你准备打印、存储和操作数据时,应该最后才使用 .get_text()
            # 一般情况下,你应该尽可能地保留 HTML 文档的标签结构
            print(name.get_text())  #通过get_text()来将标签中的内容分开显示

        # 文本参数 text 有点不同,它是用标签的文本内容去匹配,而不是用标签的属性
        nameList = bsObj.findAll(text="the prince")
        print(len(nameList))

        # 还有一个关键词参数 keyword ,可以让你选择那些具有指定属性的标签
        allText = bsObj.findAll(id="text")
        print(allText[0].get_text())

'''
BeautifulSoup 的 find() 和 findAll()
    BeautifulSoup 文档里两者的定义就是这样:
    findAll(tag, attributes, recursive, text, limit, keywords)
    find(tag, attributes, recursive, text, keywords)
        很可能你会发现,自己在 95% 的时间里都只需要使用前两个参数: tag 和 attributes 。但
        是,我们还是应该仔细地观察所有的参数
    tag: 标签参数(可传入一个或者多个标签组成list作为标签参数)
    attributes: 属性参数(是用一个 Python 字典封装一个标签的若干属性和对应的属性值)
        eg: .findAll("span", {"class":{"green", "red"}})
    recursive: 递归参数(是一个布尔变量)：
        你想抓取 HTML 文档标签结构里多少层的信息?如果
        recursive 设置为 True , findAll 就会根据你的要求去查找标签参数的所有子标签,以及子
        标签的子标签。如果 recursive 设置为 False , findAll 就只查找文档的一级标签。 findAll
        默认是支持递归查找的( recursive 默认值是 True );一般情况下这个参数不需要设置,除
        非你真正了解自己需要哪些信息,而且抓取速度非常重要,那时你可以设置递归参数
    text: 文本参数(它是用标签的文本内容去匹配,而不是用标签的属性)
        eg: nameList = bs_obj.findAll(text="the prince")
            print(len(nameList))
    limit: 范围限制参数(显然只用于 findAll 方法):
        find 其实等价于 findAll 的 limit 等于1 时的情形
        如果你只对网页中获取的前 x 项结果感兴趣,就可以设置它
        但是要注意,这个参数设置之后,获得的前几项结果是按照网页上的顺序排序的
        未必是你想要的那前几项
    keywords: 关键词参数,可以让你选择那些具有指定属性的标签
        eg: allText = bs_obj.findAll(id="text")
            print(allText[0].get_text())
        关键词参数的注意事项:
            是 BeautifulSoup 在技术上做的一个冗余功能。任何用关键词参数能够完成的任务,同样可以用本章后面将介绍的技术解决
            eg: bs_obj.findAll(id="text")   #两行代码的功能是完全一样的
                bs_obj.findAll("", {"id":"text"})
            另外,用 keyword 偶尔会出现问题,尤其是在用 class 属性查找标签的时候,
            因为 class 是 Python 中受保护的关键字。也就是说, class 是 Python 语言
            的保留字,在 Python 程序里是不能当作变量或参数名使用的
            假如你运行下面的代码,Python 就会因为你误用 class 保留字而产生一个语法错误
            bs_obj.findAll(class="green")
            你也可以用属性参数把 class 用引号包起来(让其正常运行):
            bs_obj.findAll("", {"class":"green"})
'''

'''
其他 BeautifulSoup 对象

• BeautifulSoup 对象
前面代码示例中的 bs_obj
• 标签 Tag 对象
BeautifulSoup 对象通过 find 和 findAll ,或者直接调用子标签获取的一列对象或单个
对象,就像:
bs_obj.div.h1
但是,这个库还有另外两种对象,虽然不常用,却应该了解一下。
• NavigableString 对象
用来表示标签里的文字,不是标签(有些函数可以操作和生成 NavigableString 对象,
而不是标签对象)。
• Comment 对象
用来查找 HTML 文档的注释标签, <!-- 像这样 -->
这四个对象是你用 BeautifulSoup 库时会遇到的所有对象
'''
