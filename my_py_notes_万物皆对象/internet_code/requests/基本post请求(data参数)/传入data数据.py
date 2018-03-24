# coding = utf-8

'''
@author = super_fazai
@File    : 传入data数据.py
@Time    : 2017/8/28 19:25
@connect : superonesfazai@gmail.com
'''

# 最基本的post方法
# response = requests.post("http://www.baidu.com/", data = data)

import requests

formdata = {
    "type":"AUTO",
    "i":"i love python",
    "doctype":"json",
    "xmlVersion":"1.8",
    "keyfrom":"fanyi.web",
    "ue":"UTF-8",
    "action":"FY_BY_ENTER",
    "typoResult":"true"
}

url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null"

headers={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

response = requests.post(url, data = formdata, headers = headers)

print(response.text)

# 如果是json文件可以直接显示
print(response.json())