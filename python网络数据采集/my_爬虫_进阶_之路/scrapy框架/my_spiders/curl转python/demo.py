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
curl 'http://m.01fy.cn/bj/rent/list_2_0_0_0-0_0_0-0_0_2_0_3_.html' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: http://m.01fy.cn/bj/rent/list_2_0_0_0-0_0_0-0_0_2_0_2_.html' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9' -H 'Cookie: Hm_lvt_dab72e550be0fa0f04610109fd49072a=1541141484,1541141660,1541141773,1541141787; FY_cityid=1; Hm_lpvt_dab72e550be0fa0f04610109fd49072a=1541144072' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)