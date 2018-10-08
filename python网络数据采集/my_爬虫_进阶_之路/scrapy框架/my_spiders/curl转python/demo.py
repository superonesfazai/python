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
curl 'https://club.autohome.com.cn/bbs/thread/1f05b4da4448439b/76044817-1.html' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://blog.csdn.net/xing851483876/article/details/82928607' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: zh-CN,zh;q=0.9' -H 'Cookie: __ah_uuid=3002DDA0-29B4-4DD2-832F-0FF763C3C31F; fvlid=1538984728528tvE1Uc4Bot; sessionip=113.215.181.156; sessionid=DE2BFA55-FEDE-4541-9638-258DB35E1B7D%7C%7C2018-10-08+15%3A45%3A31.208%7C%7Cblog.csdn.net; sessionvid=52E00162-E422-4D8F-8470-A4C7824D4981; area=330105; ahpau=1; ahpvno=2; ref=blog.csdn.net%7C0%7C0%7C0%7C2018-10-08+15%3A45%3A51.025%7C2018-10-08+15%3A45%3A31.208; ahrlid=1538984746495VqaxDIUKTv-1538984982222; autoac=6ABF38E1C1CBFA1F0180A033CE3A23BA' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)