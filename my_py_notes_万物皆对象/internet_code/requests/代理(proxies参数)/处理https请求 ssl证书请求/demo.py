# coding = utf-8

'''
@author = super_fazai
@File    : demo.py
@Time    : 2017/8/29 08:39
@connect : superonesfazai@gmail.com
'''

"""
要想检查某个主机的ssl证书, 可以用verify参数(也可以不写)
"""

import requests

response = requests.get('https://www.baidu.com/', verify=True)

# 也可省略不写
# response = requests.get('https://www.baidu.com/')
print(response.text)

'''
如果SSL证书验证不通过，或者不信任服务器的安全证书，
则会报出SSLError，据说 12306 证书是自己做的
'''
import requests
response = requests.get("https://www.12306.cn/mormhweb/")
print(response.text)

'''
报错:
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='www.12306.cn', port=443): Max retries exceeded with url: /mormhweb/ (Caused by SSLError(SSLError("bad handshake: Error([('SSL routines', 'tls_process_server_certificate', 'certificate verify failed')],)",),))
'''

# 如果我们想跳过 12306 的证书验证，
# 把 verify 设置为 False 就可以正常请求了。
# r = requests.get("https://www.12306.cn/mormhweb/", verify = False)