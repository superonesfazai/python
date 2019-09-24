现在随处可见 https 开头的网站，urllib2可以为 HTTPS 请求验证SSL证书，就像web浏览器一样，如果网站的SSL证书是经过CA认证的，则能够正常访问，如：https://www.baidu.com/等...

如果SSL证书验证不通过，或者操作系统不信任服务器的安全证书，比如浏览器在访问12306网站如：https://www.12306.cn/mormhweb/的时候，会警告用户证书不受信任。（据说 12306 网站证书是自己做的，没有通过CA认证）
![](https://i.loli.net/2019/09/24/YKUyWn3jZGzeOFh.jpg)

urllib2在访问的时候则会报出SSLError：
```python
import urllib.request

url = "https://www.12306.cn/mormhweb/"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

request = urllib.request.Request(url, headers = headers)

response = urllib.request.urlopen(request)

print(response.read())
```
运行结果：

urllib2.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:590)>

所以，如果以后遇到这种网站，我们需要单独处理SSL证书，让程序忽略SSL证书验证错误，即可正常访问。