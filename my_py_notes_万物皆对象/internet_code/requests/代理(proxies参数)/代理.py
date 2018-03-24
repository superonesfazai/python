# coding = utf-8

'''
@author = super_fazai
@File    : 代理.py
@Time    : 2017/8/28 20:03
@connect : superonesfazai@gmail.com
'''

'''
如果需要使用代理，你可以通过为任意请求方法提供 proxies 参数来配置单个请求
'''

import requests

# 根据协议类型，选择不同的代理
proxies = {
  "http": "http://12.34.56.79:9527",
  "https": "http://12.34.56.79:9527",
}

response = requests.get("http://www.baidu.com", proxies = proxies)
print(response.text)

# 也可以通过本地环境变量 HTTP_PROXY 和 HTTPS_PROXY 来配置代理：
# export HTTP_PROXY="http://12.34.56.79:9527"
# export HTTPS_PROXY="https://12.34.56.79:9527"
