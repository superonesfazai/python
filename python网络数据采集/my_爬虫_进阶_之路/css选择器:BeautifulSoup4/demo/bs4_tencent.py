# coding = utf-8

'''
@author = super_fazai
@File    : bs4_tencent.py
@Time    : 2017/8/30 10:40
@connect : superonesfazai@gmail.com
'''

"""
使用bs4，将招聘网页上的职位名称、职位类别、招聘人数、工作地点、发布时间，以及每个职位详情的点击链接存储出来
"""

from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import json
from pprint import pprint

def tencent():
    url = 'http://hr.tencent.com/'
    request = urllib.request.Request(url + 'position.php?&start=10#a')
    response = urllib.request.urlopen(request)
    result_html = response.read()

    output = open('tencent.json', 'w', encoding='utf-8')

    html = BeautifulSoup(result_html, 'lxml')

    # 创建css选择器
    result = html.select('tr[class="even"]')
    result2 = html.select('tr[class="odd"]')
    result += result2

    items = []
    for site in result:
        item = {}

        name = site.select('td a')[0].get_text()
        detailLink = site.select('td a')[0].attrs['href']
        catalog = site.select('td')[1].get_text()
        recruitNumber = site.select('td')[2].get_text()
        workLocation = site.select('td')[3].get_text()
        publishTime = site.select('td')[4].get_text()

        item['name'] = name
        item['detailLink'] = url + detailLink
        item['catalog'] = catalog
        item['recruitNumber'] = recruitNumber
        item['publishTime'] = publishTime

        items.append(item)

    # 禁用ascii编码，按utf-8编码
    line = json.dumps(items, ensure_ascii=False)

    output.write(line.encode('utf-8').decode())
    output.close()
    print('爬取完毕...')

if __name__ == "__main__":
    tencent()
    print('打印爬取结果'.center(60, '-'))
    file = open('./tencent.json', 'r', encoding='utf-8')
    tmp_json = json.load(file)
    pprint(tmp_json)
