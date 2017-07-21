#coding: utf-8

'''
“获取页面上所有外链”这样的小函数是不错的做法,以后可以方便地修
改代码以满足另一个采集任务的需求。例如,如果我们的目标是采集一个网站所有的外
链,并且记录每一个外链,我们可以增加下面的函数
'''

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

from . import flexible_implement_different_crawlers

# import sys
# sys.path.append(r'flexible_implement_different_crawlers.py')

# 收集网站上发现的所有外链列表
all_ext_links = set()
all_int_links = set()

def get_all_external_links(site_url):
    try:
        html = urlopen(site_url)
    except HTTPError as e:
        print('url is not found!')
    else:
        if html is None:
            print('html is None!')
        else:
            bs_obj = BeautifulSoup(html)
            internal_links = flexible_implement_different_crawlers.get_internal_links(bs_obj, flexible_implement_different_crawlers.split_address(site_url)[0])
            external_links = flexible_implement_different_crawlers.get_external_links(bs_obj, flexible_implement_different_crawlers.split_address(site_url)[0])
            for link in external_links:
                if link not in all_ext_links:
                    all_ext_links.add(link)
                    print(link)
            for link in internal_links:
                if link not in all_int_links:
                    print("即将获取链接的URL是: " + link)
                    all_int_links.add(link)
                    get_all_external_links(link)

if __name__ == '__main__':
    get_all_external_links("http://oreilly.com")