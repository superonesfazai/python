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
curl 'https://piaofang.maoyan.com/?ver=normal' -H 'authority: piaofang.maoyan.com' -H 'cache-control: max-age=0' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.9' -H 'cookie: _lxsdk_cuid=16642591771c8-0c7b42770a7c79-346a7809-1fa400-16642591772c8; __mta=48499097.1538711428133.1538711442416.1538718413212.3; _lxsdk=D78D54B0C85111E88CF261F13D453A3D36140E6C0657438DBE9D4F1BDFF21C75; __mta=48499097.1538711428133.1538718413212.1538794606047.4; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; _lxsdk_s=166474e4d91-671-c55-7b9%7C%7C12' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)