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
curl 'http://jandan.net/duan/page-104' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3' -H 'Referer: http://jandan.net/duan' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' -H 'Cookie: voted_comment_4196139=1; voted_comment_4196491=1; voted_comment_4196641=1; voted_comment_4197035=1; voted_comment_4196227=1; voted_comment_4196354=1; voted_comment_4196796=1; voted_comment_4196818=1; voted_comment_4196391=1; voted_comment_4196413=1' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)