# JWT
json web token

以下几点特性会让你在程序中使用基于Token的身份验证
1. 无状态、可扩展
2. 支持移动设备
3. 跨程序调用
4. 安全

## 基于服务器验证方式暴露的一些问题
1. Seesion：每次认证用户发起请求时，服务器需要去创建一个记录来存储信息。当越来越多的用户发请求时，内存的开销也会不断增加。

2. 可扩展性：在服务端的内存中使用Seesion存储登录信息，伴随而来的是可扩展性问题。

3. CORS(跨域资源共享)：当我们需要让数据跨多台移动设备上使用时，跨域资源的共享会是一个让人头疼的问题。在使用Ajax抓取另一个域的资源，就可以会出现禁止请求的情况。

4. CSRF(跨站请求伪造)：用户在访问银行网站时，他们很容易受到跨站请求伪造的攻击，并且能够被利用其访问其他的网站。

在这些问题中，可扩展行是最突出的。因此我们有必要去寻求一种更有行之有效的方法。

## 基于Token的验证原理
基于Token的身份验证是无状态的，我们不将用户信息存在服务器或Session中。

这种概念解决了在服务端存储信息时的许多问题

　　NoSession意味着你的程序可以根据需要去增减机器，而不用去担心用户是否登录。

基于Token的身份验证的过程如下:
1. 用户通过用户名和密码发送请求。
2. 程序验证。
3. 程序返回一个签名的token 给客户端。
4. 客户端储存token,并且每次用于每次发送请求。
5. 服务端验证token并返回数据。

每一次请求都需要token。token应该在HTTP的头部发送从而保证了Http请求无状态。我们同样通过设置服务器属性Access-Control-Allow-Origin:* ，让服务器能接受到来自所有域的请求。需要主要的是，在ACAO头部标明(designating)*时，不得带有像HTTP认证，客户端SSL证书和cookies的证书。
 
当我们在程序中认证了信息并取得token之后，我们便能通过这个Token做许多的事情。

我们甚至能基于创建一个基于权限的token传给第三方应用程序，这些第三方程序能够获取到我们的数据（当然只有在我们允许的特定的token）

## Tokens的优势
无状态, 可扩展, 体积小传输速度快

在客户端存储的Tokens是无状态的，并且能够被扩展。基于这种无状态和不存储Session信息，负载负载均衡器能够将用户信息从一个服务传到其他服务器上。

如果我们将已验证的用户的信息保存在Session中，则每次请求都需要用户向已验证的服务器发送验证信息(称为Session亲和性)。用户量大时，可能会造成一些拥堵。

但是不要着急。使用tokens之后这些问题都迎刃而解，因为tokens自己hold住了用户的验证信息。

### 安全性
请求中发送token而不再是发送cookie能够防止CSRF(跨站请求伪造)。即使在客户端使用cookie存储token，cookie也仅仅是一个存储机制而不是用于认证。不将信息存储在Session中，让我们少了对session操作。 

token是有时效的，一段时间之后用户需要重新验证。我们也不一定需要等到token自动失效，token有撤回的操作，通过token revocataion可以使一个特定的token或是一组有相同认证的token无效。

### 可扩展性
Tokens能够创建与其它程序共享权限的程序。例如，能将一个随便的社交帐号和自己的大号(Fackbook或是Twitter)联系起来。当通过服务登录Twitter(我们将这个过程Buffer)时，我们可以将这些Buffer附到Twitter的数据流上(we are allowing Buffer to post to our Twitter stream)。

使用tokens时，可以提供可选的权限给第三方应用程序。当用户想让另一个应用程序访问它们的数据，我们可以通过建立自己的API，得出特殊权限的tokens。

### 多平台跨域
我们提前先来谈论一下CORS(跨域资源共享)，对应用程序和服务进行扩展的时候，需要介入各种各种的设备和应用程序。

支持跨域验证，可以应用于单点登录

只要用户有一个通过了验证的token，数据和资源就能够在任何域上被请求到。
```
Access-Control-Allow-Origin: * 
```

### 基于标准
它支持众多的语言。这意味在未来的使用中你可以真正的转换你的认证机制。

严格的结构化。它自身（在 payload 中）就包含了所有与用户相关的验证消息，如用户可访问路由、访问有效期等信息，服务器无需再去连接数据库验证信息的有效性，并且 payload 支持为你的应用而定制化。

## jwt 
eg: 
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
```
由 . 分为三段，通过解码可以得到：

### 1. 头部（Header）
```bash
// 包括类别（typ）、加密算法（alg）；
{
  "alg": "HS256",
  "typ": "JWT"
}
```
jwt的头部包含两部分信息：
- 声明类型，这里是jwt
- 声明加密的算法 通常直接使用 HMAC SHA256

然后将头部进行base64加密（该加密是可以对称解密的)，构成了第一部分。
```bash
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
```

### 2. 载荷（payload）
载荷就是存放有效信息的地方。这些有效信息包含三个部分：

- 标准中注册声明
- 公共的声名
- 私有的声明

#### 公共的声明 ：
公共的声明可以添加任何的信息，一般添加用户的相关信息或其他业务需要的必要信息.但不建议添加敏感信息，因为该部分在客户端可解密。

#### 私有的声明 ：
私有声明是提供者和消费者所共同定义的声明，一般不建议存放敏感信息，因为base64是对称解密的，意味着该部分信息可以归类为明文信息

eg:
```bash
// 包括需要传递的用户信息；
{ "iss": "Online JWT Builder", 
  "iat": 1416797419, 
  "exp": 1448333419, 
  "aud": "www.gusibi.com", 
  "sub": "uid", 
  "nickname": "goodspeed", 
  "username": "goodspeed", 
  "scopes": [ "admin", "user" ] 
}
```
- iss: 该JWT的签发者，是否使用是可选的；
- sub: 该JWT所面向的用户，是否使用是可选的；
- aud: 接收该JWT的一方，是否使用是可选的；
- exp(expires): 什么时候过期，这里是一个Unix时间戳，是否使用是可选的；
- iat(issued at): 在什么时候签发的(UNIX时间)，是否使用是可选的；

其他还有:
- nbf (Not Before)：如果当前时间在nbf里的时间之前，则Token不被接受；一般都会留一些余地，比如几分钟；，是否使用是可选的；
- jti: jwt的唯一身份标识，主要用来作为一次性token，从而回避重放攻击。

将上面的JSON对象进行base64编码可以得到下面的字符串。这个字符串我们将它称作JWT的Payload（载荷）。
```bash
eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE0MTY3OTc0MTksImV4cCI6MTQ0ODMzMzQxOSwiYXVkIjoid3d3Lmd1c2liaS5jb20iLCJzdWIiOiIwMTIzNDU2Nzg5Iiwibmlja25hbWUiOiJnb29kc3BlZWQiLCJ1c2VybmFtZSI6Imdvb2RzcGVlZCIsInNjb3BlcyI6WyJhZG1pbiIsInVzZXIiXX0
```
```bash
信息会暴露：由于这里用的是可逆的base64 编码，所以第二部分的数据实际上是明文的。我们应该避免在这里存放不能公开的隐私信息。
```
### 3. 签名（signature）
```bash
// 根据alg算法与私有秘钥进行加密得到的签名字串；
// 这一段是最重要的敏感信息，只能在服务端解密；
HMACSHA256(  
    base64UrlEncode(header) + "." +
    base64UrlEncode(payload),
    SECREATE_KEY
)
```
jwt的第三部分是一个签证信息，这个签证信息由三部分组成：

- header (base64后的)
- payload (base64后的)
- secret

将上面的两个编码后的字符串都用句号.连接在一起（头部在前），就形成了:
```bash
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJKb2huIFd1IEpXVCIsImlhdCI6MTQ0MTU5MzUwMiwiZXhwIjoxNDQxNTk0NzIyLCJhdWQiOiJ3d3cuZXhhbXBsZS5jb20iLCJzdWIiOiJqcm9ja2V0QGV4YW1wbGUuY29tIiwiZnJvbV91c2VyIjoiQiIsInRhcmdldF91c2VyIjoiQSJ9
```
最后，我们将上面拼接完的字符串用HS256算法进行加密。
在加密的时候，我们还需要提供一个密钥（secret）。
如果我们用 secret 作为密钥的话，那么就可以得到我们加密后的内容:
```bash
pq5IDv-yaktw6XEa5GEv07SzS9ehe6AcVSdTj0Ini4o
```
将这三部分用.连接成一个完整的字符串,构成了最终的jwt:

```bash
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE0MTY3OTc0MTksImV4cCI6MTQ0ODMzMzQxOSwiYXVkIjoid3d3Lmd1c2liaS5jb20iLCJzdWIiOiIwMTIzNDU2Nzg5Iiwibmlja25hbWUiOiJnb29kc3BlZWQiLCJ1c2VybmFtZSI6Imdvb2RzcGVlZCIsInNjb3BlcyI6WyJhZG1pbiIsInVzZXIiXX0.pq5IDv-yaktw6XEa5GEv07SzS9ehe6AcVSdTj0Ini4o
```
```bash
签名的目的：签名实际上是对头部以及载荷内容进行签名。
所以，如果有人对头部以及载荷的内容解码之后进行修改，再进行编码的话，那么新的头部和载荷的签名和之前的签名就将是不一样的。
而且，如果不知道服务器加密的时候用的密钥的话，得出来的签名也一定会是不一样的。
这样就能保证token不会被篡改。
```
token 生成好之后，接下来就可以用token来和服务器进行通讯了。

下图是client 使用 JWT 与server 交互过程:
![](../images/343693ff0be5b0f582096395c8574896.jpg)

这里在第三步我们得到 JWT 之后，需要将JWT存放在 client，之后的每次需要认证的请求都要把JWT发送过来。（请求时可以放到 header 的 Authorization ）

## python 使用JWT实践
```python
import jwt
import time

# 使用 sanic 作为restful api 框架 
def create_token(request):
    grant_type = request.json.get('grant_type')
    username = request.json['username']
    password = request.json['password']
    if grant_type == 'password':
        account = verify_password(username, password)
    elif grant_type == 'wxapp':
        account = verify_wxapp(username, password)
    if not account:
        return {}
        
    payload = {
        "iss": "gusibi.com",
         "iat": int(time.time()),
         "exp": int(time.time()) + 86400 * 7,
         "aud": "www.gusibi.com",
         "sub": account['_id'],
         "username": account['username'],
         "scopes": ['open']
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    return True, {'access_token': token, 'account_id': account['_id']}

def verify_bearer_token(token):
    #  如果在生成token的时候使用了aud参数，那么校验的时候也需要添加此参数
    payload = jwt.decode(token, 'secret', audience='www.gusibi.com', algorithms=['HS256'])
    if payload:
        return True, token
        
    return False, token
```
这里，我们可以使用 jwt 直接生成 token，不用手动base64加密和拼接。

## b64解码常遇到的问题
base64数据可能有多种方式被破坏

正如维基百科所说，删除填充（base64编码数据末尾的'='字符）是“无损”的

从理论的观点来看，不需要填充字符，因为可以从Base64数字的数量计算丢失的字节数。

因此，如果这对于你的base64数据来说真的是唯一“错误”，那么可以添加填充。我想出了这个能够解析WeasyPrint中的“数据”URL，其中一些是没有填充的base64：

```python
from base64 import b64decode
from fzutils.safe_utils import b64decode_plus

a = 'eyJVc2VySUQiOjI1OTE0NiwiVXNlclJvbGUiOjAsIkV4cGlyZURhdGUiOiIyMDE4LTExLTEyVDE3OjE4OjE4LjEwNTY1MzUrMDg6MDAifQ'
# print(b64decode(a))   # 报错: Error: Incorrect padding
print(b64decode_plus(a.encode()))
```