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
curl 'http://www.cninfo.com.cn/new/disclosure?column=szse_latest&pageNum=3&pageSize=20' -X POST -H 'Cookie: JSESSIONID=6C8CBFFFB00FEA9A253A13DCDF4449B1; JSESSIONID=6C8CBFFFB00FEA9A253A13DCDF4449B1; _sp_ses.2141=*; _sp_id.2141=3c2647d6-c5c4-4e44-8f11-2ba4c3af382d.1539849334.1.1539850911.1539849334.5ba066ca-8315-430e-b3b1-e5fec73f47ed' -H 'Origin: http://www.cninfo.com.cn' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9' -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Content-Length: 0' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)