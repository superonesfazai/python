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
curl 'http://hz.huoniuniu.com/shop/72391' -H 'Proxy-Connection: keep-alive' -H 'Cache-Control: max-age=0' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: http://hz.huoniuniu.com/goods?q=%E7%9F%AD%E8%A2%96&sourcePage=/' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' -H 'Cookie: userid=1551668600281; UM_distinctid=1692cabc7b112c-0e83543c8627c5-36607102-1fa400-1692cabc7b2639; CXSESSID=c8aa374d12ac246f8157df4a2b0420ea; CNZZDATA1271156135=722508653-1551232650-null%7C1551666551; userid=1551668600281; dom_id=7; CNZZDATA1255714250=2144904728-1551230956-null%7C1551669625' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)