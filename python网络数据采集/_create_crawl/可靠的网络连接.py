#coding:utf-8

'''
让我们看看爬虫 import 语句后面的第一行代码,如何处理那里可能出现的异常:
html = urlopen("http://www.pythonscraping.com/pages/page1.html")
这行代码主要可能会发生两种异常:
• 网页在服务器上不存在(或者获取页面的时候出现错误)
• 服务器不存在
'''

'''
第一种异常发生时,程序会返回 HTTP 错误。HTTP 错误可能是“404 Page Not Found” “500
Internal Server Error”等。所有类似情形, urlopen 函数都会抛出“HTTPError”异常
我们可以用下面的方式处理这种异常
'''

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

try:
    html = urlopen('http://www.pythonscraping.com/pages/page1.html')
except HTTPError as e:
    print(e)
    # 返回空值,中断程序,或者执行另一个方案
else:
    # 如果服务器不存在(就是说链接 http://www.pythonscraping.com/ 打不开
    # 或者是 URL 链接写错了), urlopen 会返回一个 None 对象
    # 我们可以增加一个判断语句检测返回的 html 是不是 None
    if html is None:
        print('URL is not found')
    else:
        # 程序继续
        # 当然,即使网页已经从服务器成功获取,如果网页上的内容并非完全是我们期望的那样,仍然可能会出现异常
        # 每当你调用 BeautifulSoup 对象里的一个标签时,增加一个检查条件保证标签确实存在是很聪明的做法
        # 如果你想要调用的标签不存在,BeautifulSoup 就会返回 None 对象
        # 不过,如果再调用这个 None 对象下面的子标签,就会发生 AttributeError错误
        bsObj = BeautifulSoup(html.read())
        # 下面这行代码(nonExistentTag 是虚拟的标签,BeautifulSoup 对象里实际没有会返回一个 None 对象)
        # print(bs_obj.nonExistentTag)

        # 处理和检查这个对象是十分必要的,如果你不检查,直接调用这个None 对象的子标签,麻烦就来了
        # 如下所示
        # print(bs_obj.nonExistentTag.someTag)     #这时就会返回一个异常:AttributeError: 'NoneType' object has no attribute 'someTag'

        # 那么我们怎么才能避免这两种情形的异常呢?最简单的方式就是对两种情形进行检查
        # try:
        #     badContent = bs_obj.nonExistentTag.anotherTag
        # except AttributeError as e:
        #     print('Tag was not found')
        # else:
        #     if badContent == None:
        #         print('Tag was not found')
        #     else:
        #         print(badContent)
        pass

# 初看这些检查与错误处理的代码会觉得有点儿累赘,但是,我们可以重新简单组织一下代码
# 让它变得不那么难写(更重要的是,不那么难读)
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read())
        title = bsObj.body.h1
    except AttributeError as e:
        return None
    return title

title = getTitle('http://www.pythonscraping.com/pages/page1.html')
if title == None:
    print('Title could not be found')
else:
    print(title)
