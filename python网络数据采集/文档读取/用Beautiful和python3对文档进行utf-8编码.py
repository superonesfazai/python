#coding:utf-8
from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen('http://en.wikipedia.org/wiki/Python_(programming_language)')
bs_obj = BeautifulSoup(html)
content = bs_obj.find('div', {'id': 'mw-content-text'}).get_text()
content = bytes(content, 'utf-8')
content = content.decode('utf-8')
