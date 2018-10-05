# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

"""
curl命令 转成原生的python requests代码
"""

from fzutils.curl_utils import curl_cmd_2_py_code

curl_cmd = r'''
curl 'https://api-prod.wallstreetcn.com/apiv1/content/articles?category=global&limit=20&cursor=1538704276,1538664827&platform=wscn-platform' -H 'x-taotie-device-id: pcwscn-1655bf32-c6d4-92ef-6584-fc6d70501442' -H 'origin: https://wallstreetcn.com' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.9' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36' -H 'accept: application/json, text/plain, */*' -H 'referer: https://wallstreetcn.com/news/global?from=navbar' -H 'authority: api-prod.wallstreetcn.com' -H 'x-client-type: pc' -H 'x-ivanka-platform: wscn-platform' -H 'x-device-id: pcwscn-1655bf32-c6d4-92ef-6584-fc6d70501442' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)