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
curl 'http://www.mafengwo.cn/flight/rest/flightlist/?filter%5BdepartCity%5D=%E6%9D%AD%E5%B7%9E&filter%5BdepartCode%5D=HGH&filter%5BdestCity%5D=%E5%8C%97%E4%BA%AC&filter%5BdestCode%5D=BJS&filter%5BdepartDate%5D=2018-10-26&filter%5BdestDate%5D=&filter%5BotaId%5D=102' -H 'Cookie: PHPSESSID=36j3ivqmre5ktovi77sqaa26m4; mfw_uuid=5bd1767c-e073-605b-d996-4c5633701186; _r=google; _rp=a%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A18%3A%22www.google.com.hk%2F%22%3Bs%3A1%3A%22t%22%3Bi%3A1540454012%3B%7D; oad_n=a%3A5%3A%7Bs%3A5%3A%22refer%22%3Bs%3A25%3A%22https%3A%2F%2Fwww.google.com.hk%22%3Bs%3A2%3A%22hp%22%3Bs%3A17%3A%22www.google.com.hk%22%3Bs%3A3%3A%22oid%22%3Bi%3A1075%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222018-10-25+15%3A53%3A32%22%3B%7D; uva=s%3A156%3A%22a%3A4%3A%7Bs%3A13%3A%22host_pre_time%22%3Bs%3A10%3A%222018-10-25%22%3Bs%3A2%3A%22lt%22%3Bi%3A1540454015%3Bs%3A10%3A%22last_refer%22%3Bs%3A26%3A%22https%3A%2F%2Fwww.google.com.hk%2F%22%3Bs%3A5%3A%22rhost%22%3Bs%3A17%3A%22www.google.com.hk%22%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1540454015%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A17%3A%22www.google.com.hk%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5bd1767c-e073-605b-d996-4c5633701186; UM_distinctid=166aa36e6d0134a-05249b72868517-346c780e-1fa400-166aa36e6d168e; __mfwlv=1540461443; __mfwvn=2; all_ad=1; CNZZDATA30065558=cnzz_eid%3D69982733-1540451845-null%26ntime%3D1540457245; CNZZDATA1253221316=773198110-1540458503-http%253A%252F%252Fwww.mafengwo.cn%252F%7C1540458503; __mfwlt=1540461556' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://www.mafengwo.cn/flight/list?departCity=%E6%9D%AD%E5%B7%9E&departCode=HGH&destCity=%E5%8C%97%E4%BA%AC&destCode=BJS&type=oneWay&status=0&departDate=2018-10-26&destDate=' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)