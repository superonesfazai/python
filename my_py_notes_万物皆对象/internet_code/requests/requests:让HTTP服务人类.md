# requests

虽然Python的标准库中 urllib2 模块已经包含了平常我们使用的大多数功能，但是它的 API 使用起来让人感觉不太好，而 Requests 自称 “HTTP for Humans”，说明使用更简洁方便。

```
Requests 唯一的一个非转基因的 Python HTTP 库，人类可以安全享用：）
```
Requests 继承了urllib2的所有特性。Requests支持HTTP连接保持和连接池，支持使用cookie保持会话，支持文件上传，支持自动确定响应内容的编码，支持国际化的 URL 和 POST 数据自动编码。

#### requests 的底层实现其实就是 urllib3
Requests的文档非常完备，中文文档也相当不错。Requests能完全满足当前网络的需求，支持Python 2.6—3.5，而且能在PyPy下完美运行。

[开源地址](https://github.com/kennethreitz/requests)
[中文文档API](http://docs.python-requests.org/zh_CN/latest/index.html)

```html
使用response.text 时，Requests 会基于 HTTP 响应的文本编码自动解码响应内容，大多数 Unicode 字符集都能被无缝地解码。

使用response.content 时，返回的是服务器响应数据的原始二进制字节流，可以用来保存图片等二进制文件。
```

## CA证书
请使用证书从包装[CERTIFI](https://certifiio.readthedocs.io/)。这允许用户在不更改请求版本的情况下更新其受信任的证书。

在2.16版之前，Requests捆绑了一组它信任的根CA，这些CA来自Mozilla信任库。证书仅针对每个请求版本更新一次。如果certifi未安装，则在使用显着较旧版本的请求时，会导致极其过时的证书捆绑包。

为安全起见，建议经常升级certifi！