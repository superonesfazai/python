# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@connect : superonesfazai@gmail.com
'''

"""
curl命令 转成原生的python requests代码
"""

from fzutils.curl_utils import curl_cmd_2_py_code

curl_cmd = r'''
curl 'https://developers.whatismybrowser.com/useragents/explore/hardware_type_specific/mobile/1' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://developers.whatismybrowser.com/useragents/explore/hardware_type_specific/mobile/7' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' -H 'Cookie: _ga=GA1.2.1958769124.1548731051; _gid=GA1.2.967608832.1548731051' -H 'If-Modified-Since: Sat, 26 Jan 2019 21:19:54 GMT' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)