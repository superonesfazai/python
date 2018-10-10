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
curl 'https://division-data.alicdn.com/simple/addr_3_001.js' -H 'Referer: https://item.taobao.com/item.htm?spm=a217f.8051907.312171.29.78ca3308tAk0sv&id=575480758937' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)