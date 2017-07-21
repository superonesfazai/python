#coding:utf-8

import os
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

#在python3中, urllib.request.urlretrieve 可以根据文件的 URL 下载文件

html = urlopen('http://www.pythonscraping.com')
bs_obj = BeautifulSoup(html)
image_location = bs_obj.find('a', {'id':'logo'}).find('img')['src']
urlretrieve(image_location, 'logo.jpg')
if urlretrieve(image_location, 'logo.jpg'):
    print('downloaded!')
