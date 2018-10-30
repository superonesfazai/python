# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@connect : superonesfazai@gmail.com
'''

from newspaper import Article

# url = 'http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/'
# url = 'http://hao.jobbole.com/python-goose/'
url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1540268075&ver=1199&signature=9s8yg0BRca0W4Yjs00UP6xnlpMkGPBfHLPfZutCt5I1WRKFlCOMOKtc07DsES8UOpq27IlISj954*t1eZn7ZlBSFoGfkG7qhC0fiwNr-z6EdvEGhQXGuH3Y3JXS9JkJJ&new=1'
article = Article(url=url)
article.download()
# print(article.html)
article.parse()
print(article.authors)
print(article.publish_date)
print(article.text)
print(article.top_image)
print(article.movies)
try:
    article.nlp()
    print(article.keywords)
    print(article.summary)
except Exception as e:
    print(e)

