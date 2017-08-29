# coding = utf-8

'''
@author = super_fazai
@File    : 获取一个有登录信息的Cookie模拟登陆.py
@Time    : 2017/8/28 12:56
@connect : superonesfazai@gmail.com
'''

import urllib.request

# 1. 构建一个已经登录过的用户的headers信息
headers = {
    "Host":"www.renren.com",
    "Connection":"keep-alive",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",

    # 便于终端阅读，表示不支持压缩文件
    # Accept-Encoding: gzip, deflate, sdch,

    # 重点：这个Cookie是保存了密码无需重复登录的用户的Cookie，这个Cookie里记录了用户名，密码(通常经过RAS加密)
    "Cookie": "anonymid=ixrna3fysufnwv; depovince=GW; _r01_=1; JSESSIONID=abcmaDhEdqIlM7riy5iMv; jebe_key=f6fb270b-d06d-42e6-8b53-e67c3156aa7e%7Cc13c37f53bca9e1e7132d4b58ce00fa3%7C1484060607478%7C1%7C1484060607173; jebecookies=26fb58d1-cbe7-4fc3-a4ad-592233d1b42e|||||; ick_login=1f2b895d-34c7-4a1d-afb7-d84666fad409; _de=BF09EE3A28DED52E6B65F6A4705D973F1383380866D39FF5; p=99e54330ba9f910b02e6b08058f780479; ap=327550029; first_login_flag=1; ln_uact=mr_mao_hacker@163.com; ln_hurl=http://hdn.xnimg.cn/photos/hdn521/20140529/1055/h_main_9A3Z_e0c300019f6a195a.jpg; t=214ca9a28f70ca6aa0801404dda4f6789; societyguester=214ca9a28f70ca6aa0801404dda4f6789; id=327550029; xnsid=745033c5; ver=7.0; loginfrom=syshome"
}

# 2. 构建Request对象
request = urllib.request.Request('http://www.renren.com/', headers=headers)

# 3. 根据报头信息直接访问renren主页
response = urllib.request.urlopen(request)
print(response.read().decode())

'''
但是这样做太过复杂，我们先需要在浏览器登录账户，并且设置保存密码，并且通过抓包才能获取这个Cookie，那有么有更简单方便的方法呢？
'''

# headers = {
#     'Host': 'stackoverflow.com/questions/28906859/module-has-no-attribute-urlencode',
#     'Connection': 'keep-alive',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'accept-language': 'zh-CN,zh;q=0.8',
#     'cookie': 'prov=13b52c2f-43ce-9552-d8b7-7511d4e4910f; __qca=P0-1888046488-1501904700480; acct=t=Tpc%2fdrYBEroLuXA4pVu3yzuvDnKhLVQL&s=3Y4FuNZbabosLvCNJ%2fFZ%2fR2QnS5NBwFr; _ga=GA1.2.934182817.1501904699; _gid=GA1.2.316366978.1503838312',
# }
#
# request = urllib.request.Request('https://stackoverflow.com/questions/28906859/module-has-no-attribute-urlencode', headers=headers)
# response = urllib.request.urlopen(request)
# print(response.read().decode())