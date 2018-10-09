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
curl 'https://m.toutiao.com/list/?tag=__all__&ac=wap&count=20&format=json_raw&as=A1B59B7B0C715AA&cp=5BBCD1857A0A6E1&max_behot_time=1539052864&_signature=LlHSKgAAdfSRJyPM71N2US5R0j&i=1539052864' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.9' -H 'user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36' -H 'accept: */*' -H 'referer: https://m.toutiao.com/' -H 'authority: m.toutiao.com' -H 'cookie: UM_distinctid=166567a132726-01fc6e064e2903-346a7809-1fa400-166567a1328919; tt_webid=6610165677918160398; csrftoken=ea2ace9007d12ac41e6304682fedc0d9; W2atIF=1; _ga=GA1.2.2005212523.1539052958; _gid=GA1.2.901934545.1539052958; _ba=BA0.2-20181009-51225-fsmfanFEfzTimrRPNVZ6; __tasessionId=c7nh7mahz1539052959998' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)