# coding:utf-8

'''
@author = super_fazai
@File    : 获取整站所有外链.py
@Time    : 2018/4/4 11:21
@connect : superonesfazai@gmail.com
'''

from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random

from fzutils.spider.fz_requests import MyRequests

headers = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'cache-control': 'max-age=0',
    'authority': 'analytics.snssdk.com',
    'cookie': 'tt_webid=6539865412716709389; _ba=BA0.2-20180402-5199e-464gM6Uwvw2j9GXI6sKx; _ga=GA1.2.1308585107.1522681076; _gid=GA1.2.1598657356.1522681076',
    'referer': 'https://www.iesdouyin.com/',
    'Accept-Encoding': 'identity;q=1, *;q=0',
    'Range': 'bytes=3899392-',
}

pages = set()
random.seed(datetime.datetime.now())

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

# 获取页面所有内链的列表
def getInternalLinks(bsObj, includeUrl):
    includeUrl = urlparse(includeUrl).scheme + "://" + urlparse(includeUrl).netloc
    internalLinks = []
    # 找出所有以“/”开头的链接
    for link in bsObj.findAll("a", href=re.compile("^(/|.*" + includeUrl + ")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if (link.attrs['href'].startswith("/")):
                    internalLinks.append(includeUrl + link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])
    return internalLinks

# 获取页面所有外链的列表
def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    # 找出所有以“http”或者“www”开头且不包含当前URL的链接
    for link in bsObj.findAll("a", href=re.compile("^(http|www)((?!" + excludeUrl + ").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])

    return externalLinks

def getRandomExternalLink(startingPage):
    html = MyRequests.get_url_body(url=startingPage, headers=headers)
    bsObj = BeautifulSoup(html, "html.parser")
    externalLinks = getExternalLinks(bsObj, urlparse(startingPage).netloc)
    if len(externalLinks) == 0:
        print("没有外部链接，准备遍历整个网站")
        domain = urlparse(startingPage).scheme + "://" + urlparse(startingPage).netloc
        internalLinks = getInternalLinks(bsObj, domain)
        return getRandomExternalLink(internalLinks[random.randint(0, len(internalLinks) - 1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks) - 1)]

def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print("随机外链是: " + externalLink)
    followExternalOnly(externalLink)

# 收集网站上发现的所有外链列表
allExtLinks = set()
allIntLinks = set()

def getAllExternalLinks(siteUrl):
    domain = urlparse(siteUrl).scheme + "://" + urlparse(siteUrl).netloc
    html = MyRequests.get_url_body(url=siteUrl, headers=headers)
    bsObj = BeautifulSoup(html, 'lxml')
    internalLinks = getInternalLinks(bsObj, domain)
    externalLinks = getExternalLinks(bsObj, domain)

    f = open('result.txt', 'w')
    # 收集外链
    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            # print(link)
            f.writelines(link + '\n')
            print("即将获取的外部链接的URL是：" + link)
            # 收集内链
    for link in internalLinks:
        if link not in allIntLinks:
            print("即将获取内部链接的URL是：" + link)
            allIntLinks.add(link)
            getAllExternalLinks(link)
            f.writelines(link + '\n')

            # followExternalOnly("http://bbs.3s001.com/forum-36-1.html")

# allIntLinks.add("http://bbs.3s001.com/forum-36-1.html")
url = input('请输入待抓取的整站url: ').replace(';', '')
getAllExternalLinks(url)

