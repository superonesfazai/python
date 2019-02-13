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
curl 'https://3g.made-in-china.com/product/2515000000-1.html' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' -H 'Cookie: pid=TEzLjIxNS4xNzkuMTM1MjAxOTAyMTMwOTMyMjQyNDQ4NzM5Mzk0MQM; sf_img=AM; __utmz=144487465.1550021545.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); cn_pd=zA1NzUzNDAyN; prodIds=; z18flag=1; cn_com=jUyNTg3NDIyN; session=niUPdFdJNLYdjN1WRnGTBMvEnFYMDWoGy7Oi%2BWnRp0QbkEeaP4Br1b3OjZV%2FVLOT; sid=niUPdFdJNLYdjN1WRnGTBMvEnFYMDWoGy7Oi%2BWnRp0QbkEeaP4Br1b3OjZV%2FVLOT; __utma=144487465.1573320121.1550021545.1550033368.1550042368.4; __utmc=144487465; __utmt=1; __utmb=144487465.1.10.1550042368' -H 'If-None-Match: W/"353e1-Lu2zX/pBemLF8alF9ftD5Mt4oDg"' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)