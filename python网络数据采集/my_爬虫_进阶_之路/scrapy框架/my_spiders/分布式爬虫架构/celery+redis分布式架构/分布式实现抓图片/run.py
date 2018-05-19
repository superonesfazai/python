# coding:utf-8

'''
@author = super_fazai
@File    : run.py
@Time    : 2018/5/19 17:58
@connect : superonesfazai@gmail.com
'''

"""
内置调用函数, 运行在redis服务器
"""

from spider import (
    get_page_url,
    get_url,
    get_img,
)
import requests
import threading

x = 0

def run(url):
    '''
    #run函数
    :param url:
    :return:
    '''
    html = requests.get(url[0]).text
    # print(html)
    url_list = get_url.delay(html).get()
    for url in url_list:
        url = 'http://umei.cc' + url
        print(url)
        img_html = requests.get(url).text
        img_list = get_img.delay(img_html).get()
        for img_url in img_list:
            print(img_url)
            # urllib.urlretrieve(img_url,'/test/%s.jpg' % x)
            # global x
            # x += 1

def main():
    page_urls = get_page_url.delay().get()
    url_group = []
    j = 0
    for i in range(0, len(page_urls)):
        if (j + 1) % 2 == 0:
            url_group.append(page_urls[i])
            t = threading.Thread(target=run,args=(url_group,))
            t.start()
            t.join(1)
            url_group = []

        else:
            url_group.append(page_urls[i])
        j = j + 1

if __name__ == '__main__':
    main()