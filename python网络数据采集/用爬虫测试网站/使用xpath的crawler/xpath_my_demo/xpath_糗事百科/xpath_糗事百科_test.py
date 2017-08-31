# coding = utf-8

'''
@author = super_fazai
@File    : xpath_糗事百科_test.py
@Time    : 2017/8/30 16:28
@connect : superonesfazai@gmail.com
'''

'''
url 为：http://www.qiushibaike.com/8hr/page/1

要求：
    使用requests获取页面信息，用XPath / re 做数据提取
    获取每个帖子里的用户头像链接、用户姓名、段子内容、点赞次数和评论次数
    保存到 json 文件内
'''

import requests
from lxml import etree
import json
from pprint import pprint

page = 1
url = 'http://www.qiushibaike.com/8hr/page/' + str(page)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.8'}

try:
    response = requests.get(url, headers=headers)
    resHtml = response.text

    html = etree.HTML(resHtml)
    result = html.xpath('//div[contains(@id,"qiushi_tag")]')
    print(result)
    items = []
    for site in result:
        item = {}

        img_url = site.xpath('./div/a/img/@src')[0]
        username = site.xpath('./div/a/@title')[0]
        # username = site.xpath('.//h2')[0].text
        content = site.xpath('.//div[@class="content"]/span')[0].text.strip()
        # 投票次数
        vote = site.xpath('.//i')[0].text
        # print site.xpath('.//*[@class="number"]')[0].text
        # 评论信息
        comments = site.xpath('.//i')[1].text

        item = {
            'img_url': img_url,
            'username': username,
            'content': content,
            'vote': vote,
            'comments': comments,
        }
        print(item)
        items.append(item)
        # print(img_url.decode(), username.decode(), content.decode(), vote, comments)
    json_obj = json.dumps(items, ensure_ascii=False)
    tmp_file = open('糗事百科.json', 'w', encoding='utf-8')
    tmp_file.write(json_obj.encode('utf-8').decode('utf-8'))
    # pprint(items)
except Exception as e:
    print(e)