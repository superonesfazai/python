#coding: utf-8

'''
我们需要让这段程序更像下面的形式。
• 一个函数 get_links ,可以用维基百科词条 /wiki/< 词条名称 > 形式的 URL 链接作为参数,
然后以同样的形式返回一个列表,里面包含所有的词条 URL 链接。
• 一个主函数,以某个起始词条为参数调用 get_links ,再从返回的 URL 列表里随机选择
一个词条链接,再调用 get_links ,直到我们主动停止,或者在新的页面上没有词条链接
了,程序才停止运行
'''

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import random
import datetime

# 程序首先做的是用系统当前时间生成一个随机数生成器
# 这样可以保证在每次程序运行的时候,维基百科词条的选择都是一个全新的随机路径
# Python 的伪随机数(pseudorandom number)生成器用的是梅森旋转(Mersenne Twister)算法
random.seed(datetime.datetime.now())
def getLinks(articleUrl):
    try:
        html = urlopen('http://en.wikipedia.org'+articleUrl)
    except HTTPError as e:
        print('url is not found!')
    else:
        if html is None:
            print('url is None!')
        else:
            bsObj = BeautifulSoup(html)
            return bsObj.find('div', {'id':'bodyContent'}).findAll("a",
                        href=re.compile("^(/wiki/)((?!:).)*$"))

links = getLinks('/wiki/kevin_Bacon')
while len(links) > 0:
    newArticle = links[random.randint(0, len(links)-1)].attrs['href']
    print(newArticle)
    links = getLinks(newArticle)

