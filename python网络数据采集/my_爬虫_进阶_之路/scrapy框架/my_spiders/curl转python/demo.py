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
curl 'https://sm.ms/api/upload?ssl=true' -H 'origin: null' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.9' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36' -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundaryq1Upc5nUDceFzzye' -H 'accept: */*' -H 'authority: sm.ms' -H 'cookie: cid=rBWawlulu8VQRSE3CE8hAg==; PHPSESSID=t8iem1udqma07dqscd1tdeu1vo' --data-binary $'------WebKitFormBoundaryq1Upc5nUDceFzzye\r\nContent-Disposition: form-data; name="smfile"; filename="\u5c4f\u5e55\u5feb\u7167 2018-09-22 \u4e0a\u53489.36.03.png"\r\nContent-Type: image/png\r\n\r\n\r\n------WebKitFormBoundaryq1Upc5nUDceFzzye\r\nContent-Disposition: form-data; name="smfile"; filename="\u5c4f\u5e55\u5feb\u7167 2018-09-22 \u4e0a\u53489.36.03.png"\r\nContent-Type: image/png\r\n\r\n\r\n------WebKitFormBoundaryq1Upc5nUDceFzzye--\r\n' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)