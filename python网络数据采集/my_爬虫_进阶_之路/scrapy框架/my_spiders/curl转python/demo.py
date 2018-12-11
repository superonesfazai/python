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
curl 'http://m.huangye88.com/gongsi/1003/detail.html' -H 'Proxy-Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9' -H 'Cookie: PHPSESSID=15444308692767-0eab192076809eff4fada9e7d1d77fb32de5fdc0; Hm_lvt_c8184fd80a083199b0e82cc431ab6740=1544430870; Hm_lvt_3e1ec27e48b8a2a5ab0b82204b4272cc=1544431067; websites=%E6%9D%AD%E5%B7%9E%E4%BC%81%E4%B8%9A%E5%90%8D%E5%BD%95%2B%7C%2B1544431839%2B%7C%2Bhttp%3A%2F%2Fwww.huangye88.com%2Fsearch.html%3Fkw%3D%25E6%259D%25AD%25E5%25B7%259E%25E4%25BC%2581%25E4%25B8%259A%25E5%2590%258D%25E5%25BD%2595%26type%3Dcompany%3A%2B%3A%E4%BC%81%E4%B8%9A%E5%90%8D%E5%BD%95%E5%A4%A7%E5%85%A8%2B%7C%2B1544441528%2B%7C%2Bhttp%3A%2F%2Fwww.huangye88.com%2Fsearch.html%3Fkw%3D%25E4%25BC%2581%25E4%25B8%259A%25E5%2590%258D%25E5%25BD%2595%25E5%25A4%25A7%25E5%2585%25A8%26type%3Dcompany%3A%2B%3A%E6%B5%99%E6%B1%9F%E6%9C%BA%E6%A2%B0%E4%BC%81%E4%B8%9A%E5%90%8D%E5%BD%95%2B%7C%2B1544441740%2B%7C%2Bhttp%3A%2F%2Fwww.huangye88.com%2Fsearch.html%3Fkw%3D%25E6%25B5%2599%25E6%25B1%259F%25E6%259C%25BA%25E6%25A2%25B0%25E4%25BC%2581%25E4%25B8%259A%25E5%2590%258D%25E5%25BD%2595%26type%3Dcompany; Hm_lpvt_c8184fd80a083199b0e82cc431ab6740=1544495303; Hm_lpvt_3e1ec27e48b8a2a5ab0b82204b4272cc=1544499888' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)