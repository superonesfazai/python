#coding:utf-8

'''
为了有效地使用它们,在用爬虫的时候我们需要在页面上做些事情
让我们看看如何创建一个爬虫来收集页面标题、正文的第一个段落
以及编辑页面的链接(如果有的话)这些信息
'''

'''
*和往常一样,决定如何做好这些事情的第一步就是先观察网站上的一些页面,然后拟定一
个采集模式。通过观察几个维基百科页面,包括词条和非词条页面,比如隐私策略之类的
页面,就会得出下面的规则。
'''

'''
• 所有的标题(所有页面上,不论是词条页面、编辑历史页面还是其他页面)都是在
h1 → span 标签里,而且页面上只有一个 h1 标签。
• 前 面 提 到 过, 所 有 的 正 文 文 字 都 在 div#bodyContent 标 签 里。 但 是, 如 果 我 们 想 更
进一步获取第一段文字,可能用 div#mw-content-text → p 更好(只选择第一段的标
签)。这个规则对所有页面都适用,除了文件页面(例如,https://en.wikipedia.org/wiki/
File:Orbit_of_274301_Wikipedia.svg),页面不包含内容文字( content text )的部分内容。
• 编辑链接只出现在词条页面上。如果有编辑链接,都位于 li#ca-edit 标签的 li#ca-
edit → span → a 里面。
'''

from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import re

pages = set()
def getLinks(pageUrl):
    global pages
    try:
        html = urlopen('http://en.wikipedia.org'+pageUrl)
    except HTTPError as e:
        print('url is not found!')
    else:
        if html is None:
            print('url is None!')
        else:
            bsObj = BeautifulSoup(html)
            try:
                print(bsObj.h1.get_text())
                print(bsObj.find(id="mw-content-text").findAll("p")[0])
                print(bsObj.find(id="ca-edit").find("span").find("a").attrs['href'])
            except AttributeError:
                print("页面缺少一些属性!不过不用担心!")
            for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
                if 'href' in link.attrs:
                    if link.attrs['href'] not in pages:
                        # 我们遇到了新页面
                        newPage = link.attrs['href']
                        print("----------------\n" + newPage)
                        pages.add(newPage)
                        getLinks(newPage)

getLinks('')

# 这个 for 循环和原来的采集程序基本上是一样的(除了打印一条虚线来分离不同的页面内容之外)

'''
因为我们不可能确保每一页上都有所有类型的数据,所以每个打印语句都是按照数据在页
面上出现的可能性从高到低排列的。也就是说, <h1> 标题标签会出现在每一页上(只要能
识别,无论哪一页都有),所以我们首先试着获取它的数据。正文内容会出现在大多数页
面上(除了文件页面),因此是第二个获取的数据。“编辑”按钮只出现在标题和正文内容
都已经获取的页面上,但不是所有这类页面上都有,所以我们最后打印这类数据
'''