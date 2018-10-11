# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

from newspaper import Article

# url = 'http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/'
url = 'http://hao.jobbole.com/python-goose/'
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

