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
curl 'http://www.youdict.com/ciku/id_0_0_0_0_0.html' -H 'Proxy-Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: http://www.youdict.com/ciku/id_0_0_0_0_2238.html' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9' -H 'Cookie: UM_distinctid=1683ab54d82470-0818269b0526ee-10326653-1fa400-1683ab54d835d9; CNZZDATA1254976343=1507356200-1547171394-null%7C1547171394; Hm_lvt_88704587328aa1eb2cae7909f17b3601=1547173187; Hm_lpvt_88704587328aa1eb2cae7909f17b3601=1547173266' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)