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
curl 'https://3g.163.com/touch/reconstruct/article/list/BBM54PGAwangning/10-10.html' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: zh-CN,zh;q=0.9' -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36' -H 'Accept: */*' -H 'Referer: https://3g.163.com/touch/news/' -H 'Cookie: mail_psc_fingerprint=26a7cc93b2b579f7a8a1851a10404970; __f_=1535513055077; _ntes_nnid=c0babdfe7fa473382a136cec679641e3,1535513055271; _ntes_nuid=c0babdfe7fa473382a136cec679641e3; _ga=GA1.2.1329854078.1536827208; vjuids=-7dff571f.16647003f74.0.0cfc84a971874; _ntes_newfund_recent_=110011; vjlast=1538789491.1539312336.13; ne_analysis_trace_id=1539423233042; s_n_f_l_n3=529b12adc23dceea1539423233045; NNSSPID=21da268713c040919303ddfa3dec7d5e; vinfo_n_f_l_n3=529b12adc23dceea.1.1.1538789490693.1538789619575.1539423239737' -H 'Connection: keep-alive' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)