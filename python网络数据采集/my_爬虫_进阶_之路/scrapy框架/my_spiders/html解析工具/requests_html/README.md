# requests_html
该库旨在使解析HTML（例如，抓取Web）尽可能简单直观。

使用此库时，您会自动获得：

- 完整的JavaScript支持！
- CSS Selectors（又名jQuery风格，感谢PyQuery）。
- XPath Selectors，对于胆小的人来说。
- 模拟用户代理（如真实的Web浏览器）。
- 自动跟踪重定向。
- 连接池和cookie持久性。
- 请求体验您熟悉和喜爱，具有神奇的解析能力。

[docs](http://html.python-requests.org/)

## 安装
```bash
$ pip3 install requests-html
```

## JavaScript支持
让我们抓一些由JavaScript呈现的文本：
```bash
>>> r = session.get('http://python-requests.org/')
>>> r.html.render()

>>> r.html.search('Python 2 will retire in only {months} months!')['months']
'<time>25</time>'
```
请注意，第一次运行该render()方法时，它会将Chromium下载到您的主目录（例如~/.pyppeteer/）。这只发生过一次。

## 无请求时使用
```bash
>>> from requests_html import HTML
>>> doc = """<a href='https://httpbin.org'>"""

>>> html = HTML(html=doc)
>>> html.links
{'https://httpbin.org'}
```

## api文档

### 主类
class requests_html.HTML

### HTML会话
class requests_html.HTMLSession