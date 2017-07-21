#coding: utf-8

# 灵活的实现不同类型的爬虫

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

# 获取页面所有内链的列表
def get_internal_links(bs_obj, include_url):
    internal_links = []
    # 找出所有以'/'开头的链接
    for link in bs_obj.findAll('a',
                               href=re.compile('^(/|.*"+include_url+")')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internal_links:
                internal_links.append(link.attrs['href'])
    return internal_links

# 获取页面所有外链的列表
def get_external_links(bs_obj, exclude_url):
    external_links = []
    # 找出所有以'http'或'www'开头且不包含当前的url链接
    for link in bs_obj.findAll('a',
                               href=re.compile('^(http|www)((?!"+exclude_url+").)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in external_links:
                external_links.append(link.attrs['href'])
    return external_links

def split_address(address):
    address_parts = address.replace('http://', '').split('/')
    return address_parts

def get_random_external_link(starting_page):
    try:
        html = urlopen(starting_page)
    except HTTPError as e:
        print('url is not found!')
    else:
        if html is None:
            print('url is None!')
        else:
            bs_obj = BeautifulSoup(html)
            external_links = get_external_links(bs_obj, split_address(starting_page)[0])
            if len(external_links) == 0:
                internal_links = get_internal_links(starting_page)
                #return get_next_external_link(internal_links[random.randint(0,
                                                #len(internal_links)-1)]))
            else:
                return external_links[random.randint(0, len(external_links)-1)]

def follow_external_only(starting_site):
    external_link = get_random_external_link('http://oreilly.com')
    print('随机外链是:' + external_link)
    follow_external_only(external_link)

if __name__ == '__main__':
    follow_external_only('http://oreilly.com')

'''
上面程序从http://oreilly.com开始
然后随机从一个外链跳到另一个外链
结果如下：
    随机外链是: http://igniteshow.com/
    随机外链是: http://feeds.feedburner.com/oreilly/news
    随机外链是: http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=q319
    随机外链是: http://makerfaire.com/
'''

#在以任何正式的目的运行代码之前,请确认你已经在可能出现问题的地方都放置了检查语句