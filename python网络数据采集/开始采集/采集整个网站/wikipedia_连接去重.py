#coding:utf-8

'''
为了避免一个页面被采集两次,链接去重是非常重要的。在代码运行时,把已发现的所有
链接都放到一起,并保存在方便查询的列表里(下文示例指 Python 的集合 set 类型)。只
有“新”链接才会被采集,之后再从页面中搜索其他链接:
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
            for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
                if 'href' in link.attrs:
                    if link.attrs['href'] not in pages:
                        #我们遇到了新页面
                        newPage = link.attrs['href']
                        print(newPage)
                        pages.add(newPage)
                        getLinks(newPage)

# 一开始,用 get_links 处理一个空 URL,其实是维基百科的主页
getLinks("")

'''
只要遇到页面就查找所有以 /wiki/ 开头的链接
也不考虑链接是不是包含分号。(提示:词条链接不包含分号,而文档上传页
面、讨论页面之类的页面 URL 链接都包含分号。)
'''

'''
然后,遍历首页上每个链接,并检查是否已经在全局变量
集合 pages 里面了(已经采集的页面集合)。如果不在,就打印到屏幕上,并把链接加入
pages 集合,再用 get_links 递归地处理这个链接
'''
