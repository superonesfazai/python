#coding:utf-8

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random
import pymysql

'''
这里有几点需要注意:首先, charset='utf8' 要增加到连接字符串里。这是让连接 conn 把
所有发送到数据库的信息都当成 UTF-8 编码格式(当然,前提是数据库默认编码已经设置
成 UTF-8)
'''
conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock',
                        user='root', passwd='root654321', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE scraping")

random.seed(datetime.datetime.now())

def store(title, content):
    cur.execute("insert into pages (title, content) values (\"%s\",\
                \"%s\")", (title, content))
    cur.connection.commit()

def get_links(article_url):
    html = urlopen("http://en.wikipedia.org" + article_url)
    bs_obj = BeautifulSoup(html)
    title = bs_obj.find("h1").get_text()
    content = bs_obj.find("div", {"id":"mw-content-text"}).find("p").get_text()
    store(title, content)
    return bs_obj.find("div", {"id":"bodyContent"}).findAll("a",\
                        href = re.compile("^(/wiki/)((?!:).)*$"))

links = get_links("/wiki/Kevin_Bacon")
try:
    while len(links) > 0:
        newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
        print(newArticle)
        links = get_links(newArticle)
finally:
    cur.close()
    conn.close()
