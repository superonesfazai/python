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
curl 'https://wenshu.court.gov.cn/ValiCode/GetCode' -H 'Cookie: _gscu_2116842793=38032346hapx8711; _gscbrs_2116842793=1; ASP.NET_SessionId=yj4ltfipmmoi5qnqquqf5lmp; VCode=c045d1eb-d6fe-4d92-bd9a-d71bf2c09a94; Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2=1538033641,1538036233,1538211271,1538213091; vjkl5=dd1e099ffa724ea01ed183705c1d676f0d808d56; Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2=1538213307; _gscs_2116842793=t38211017x4gnwo20|pv:5' -H 'Origin: https://wenshu.court.gov.cn' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: zh-CN,zh;q=0.9' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Referer: https://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2++%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6+%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'guid=982f8001-9e5f-b41af721-0a730b7bdc61' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)