#coding:utf-8

'''
如果你仔细观察那些指向词条页面(不是指向其他内容页面)的链接
会发现它们都有三个共同点:
• 它们都在 id 是 bodyContent 的 div 标签里
• URL 链接不包含分号
• URL 链接都以 /wiki/ 开头
我们可以利用这些规则稍微调整一下代码来获取词条链接:
'''

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re

try:
    html = urlopen('http://en.wikipedia.org/wiki/Kevin_Bacon')
except HTTPError as e:
    print('url is not found!')
else:
    if html is None:
        print('url is None!')
    else:
        bsObj = BeautifulSoup(html)
        for link in bsObj.find('div', {'id': 'bodyContent'}).findAll('a',
                                href=re.compile('^(/wiki/)((?!:).)*$')):
            if 'href' in link.attrs:
                print(link.attrs['href'])

'''
如果你运行代码,就会看到维基百科上凯文 ·贝肯词条里所有指向其他词条的链接。
当然,写程序来找出这个静态的维基百科词条里所有的词条链接很有趣,不过没什么实际
用处。
'''
