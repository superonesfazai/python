#coding:utf-8

from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import datetime
import random
import re
import json

random.seed(datetime.datetime.now())

def get_links(article_url):
    html = urlopen("http://en.wikipedia.org" + article_url)
    bs_obj = BeautifulSoup(html)
    return bs_obj.find("div", {"id":"bodyContent"}).findAll("a",
                    href=re.compile("^(/wiki/)((?!:).)*$"))
def get_history_ips(page_url):
    # 编辑历史页面URL链接格式是:
    # http://en.wikipedia.org/w/index.php?title=Title_in_URL&action=history
    page_url = page_url.replace("/wiki/", "")
    history_url = "http://en.wikipedia.org/w/index.php?title=" \
                 + page_url + "&action=history"
    print("history url is: "+history_url)
    html = urlopen(history_url)
    bs_obj = BeautifulSoup(html)
    # 找出class属性是"mw-anonuserlink"的链接
    # 它们用IP地址代替用户名
    ip_addresses = bs_obj.findAll("a", {"class":"mw-anonuserlink"})
    address_list = set()
    for ip_address in ip_addresses:
        address_list.add(ip_address.get_text())
    return address_list

def get_country(ipAddress):
    try:
        response = urlopen("http://freegeoip.net/json/"
                        +ipAddress).read().decode('utf-8')
    except HTTPError:
        return None
    responseJson = json.loads(response)
    return responseJson.get("country_code")

links = get_links("/wiki/Python_(programming_language)")

while(len(links) > 0):
    for link in links:
        print("-------------------")
        history_ips = get_history_ips(link.attrs["href"])
        for history_ip in history_ips:
            country = get_country(history_ip)
            if country is not None:
                print(history_ip + 'is from' + country)
    new_link = links[random.randint(0, len(links) - 1)].attrs["href"]
    links = get_links(new_link)

'''
下面是部分输出结果:
-------------------
history url is: http://en.wikipedia.org/w/index.php?title=Programming_
paradigm&action=history
68.183.108.13 is from US
86.155.0.186 is from GB
188.55.200.254 is from SA
108.221.18.208 is from US
141.117.232.168 is from CA
76.105.209.39 is from US
182.184.123.106 is from PK
212.219.47.52 is from GB
72.27.184.57 is from JM
49.147.183.43 is from PH
209.197.41.132 is from US
174.66.150.151 is from US
'''