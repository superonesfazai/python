# coding:utf-8

'''
@author = super_fazai
@File    : 身份认证_demo.py
@connect : superonesfazai@gmail.com
'''

from requests import get

# HTTP Basic Auth
resp1 = get('https://api.github.com/user', auth=('user', 'pass'))

# netrc 认证
'''
如果认证方法没有收到 auth 参数，Requests 将试图从用户的 netrc 文件中获取 URL 的 hostname 需要的认证身份。The netrc file overrides raw HTTP authentication headers set with headers=.
如果找到了 hostname 对应的身份，就会以 HTTP Basic Auth 的形式发送请求。
'''

# 摘要式身份认证
from requests.auth import HTTPDigestAuth

url = 'http://httpbin.org/digest-auth/auth/user/pass'
resp2 = get(url, auth=HTTPDigestAuth('user', 'pass'))
print(resp2.text)

# OAuth 1 认证
# OAuth允许用户提供一个令牌，而不是用户名和密码来访问他们存放在特定服务提供者的数据。每一个令牌授权一个特定的网站（例如，视频编辑网站)在特定的时段（例如，接下来的2小时内）内访问特定的资源（例如仅仅是某一相册中的视频）。这样，OAuth让用户可以授权第三方网站访问他们存储在另外服务提供者的某些特定信息，而非所有内容。
# requests-oauthlib 库可以让 Requests 用户简单地创建 OAuth 认证的请求
from requests_oauthlib import OAuth1Session

twitter = OAuth1Session(
    client_key='client_key',
    client_secret='client_secret',
    resource_owner_key='resource_owner_key',
    resource_owner_secret='resource_owner_secret')
url = 'https://api.twitter.com/1/account/settings.json'
resp3 = twitter.get(url)

# OAuth 2
# doc: https://oauth.net/getting-started/