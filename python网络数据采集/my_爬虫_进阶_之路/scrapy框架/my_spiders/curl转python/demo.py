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
curl 'https://www.wenshen520.com/s.php?k=%E5%8E%9F%E7%A8%BF%E5%9B%BE&p=2' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://www.wenshen520.com/s.php?k=%E5%8E%9F%E7%A8%BF%E5%9B%BE&p=1' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: zh-CN,zh;q=0.9' -H 'Cookie: UM_distinctid=165d6927080350-0b9aa8a7c9c5e6-34677908-1fa400-165d6927082653; mob=0; CNZZDATA1259966084=1946211302-1536900175-https%253A%252F%252Fwww.google.com%252F%7C1537843362; Hm_lvt_03eab7e8fa5fa9fe807305a416f8d263=1536903246,1537845233,1537845317; view=26228%2C26059%2C37331%2C; Hm_lpvt_03eab7e8fa5fa9fe807305a416f8d263=1537845458' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)