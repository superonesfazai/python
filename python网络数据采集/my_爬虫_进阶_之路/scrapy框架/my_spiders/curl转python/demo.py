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
curl 'https://wenshu.court.gov.cn/List/ListContent' -H 'Cookie: _gscu_2116842793=38032346hapx8711; _gscbrs_2116842793=1; Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2=1538032347,1538033641,1538036233; Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2=1538036233; _gscs_2116842793=t38036233ti43gd11|pv:1; vjkl5=452b08fde99ff271a1601a11831f77c020f8e29d' -H 'Origin: https://wenshu.court.gov.cn' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: zh-CN,zh;q=0.9' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Referer: https://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2++%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6+%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'Param=%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B%3A%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6&Index=1&Page=5&Order=%E6%B3%95%E9%99%A2%E5%B1%82%E7%BA%A7&Direction=asc&vl5x=f83cc8fdec03895f73371c8d&number=%2Fwen&guid=32e2007b-0fe8-8bc0d5ed-938a16027a01' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)