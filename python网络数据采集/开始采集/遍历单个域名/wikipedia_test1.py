#coding:utf-8

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

try:
    html = urlopen('http://en.wikipedia.org/wiki/Kevin_Bacon')
except HTTPError as e:
    print('url is not found!')
else:
    if html is None:
        print('url is None!')
    else:
        bsObj = BeautifulSoup(html)
        for link in bsObj.findAll('a'):
            if 'href' in link.attrs:
                print(link.attrs['href'])


'''
如果你观察生成的一列链接,就会看到你想要的所有词条链接都在里面:“Apollo 13”
“Philadelphia”和“Primetime Emmy Award”,等等。但是,也有一些我们不需要的链接:
    //wikimediafoundation.org/wiki/Privacy_policy
    //en.wikipedia.org/wiki/Wikipedia:Contact_us
其实维基百科的每个页面都充满了侧边栏、页眉、页脚链接,以及连接到分类页面、对话
页面和其他不包含词条的页面的链接:
    /wiki/Category:Articles_with_unsourced_statements_from_April_2014
    /wiki/Talk:Kevin_Bacon
'''

'''
如果你仔细观察那些指向词条页面(不是指向其他内容页面)的链接
会发现它们都有三个共同点:
• 它们都在 id 是 bodyContent 的 div 标签里
• URL 链接不包含分号
• URL 链接都以 /wiki/ 开头
我们可以利用这些规则稍微调整一下代码来获取词条链接:
'''