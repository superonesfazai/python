## 一目了然
Scrapy是用于抓取网站并提取结构化数据的应用程序框架，可用于广泛的有用应用程序，如数据挖掘，信息处理或历史存档

尽管Scrapy最初设计用于网页抓取，但它也可用于使用API​​（如Amazon Associates Web Services）或通用网页抓取工具提取数据
## 很好知道的事情
Scrapy是用纯Python编写的，并且取决于几个关键的Python包（以及其他）：
```
* lxml，一个高效的XML和HTML解析器
* parsel，一个写在lxml之上的HTML / XML数据提取库，
* w3lib是用于处理URL和网页编码的多用途帮助器
* twisted，异步网络框架
* cryptography和pyOpenSSL，以处理各种网络级的安全需求
```
## Scrapy的主要优点之一：请求被 异步排定和处理
```
这意味着Scrapy不需要等待完成和处理的请求，
它可以在此期间发送另一个请求或执行其他操作。
这也意味着即使某些请求失败或处理它时发生错误，
其他请求仍然可以继续进行
```
```
虽然这样，您可以进行非常快速的抓取（同时发送多个并发请求，以容错方式）
Scrapy还可以通过一些设置控制爬网的礼貌。
您可以在每个请求之间设置下载延迟，
限制每个域或每个IP的并发请求数量，
甚至使用自动调节扩展名来自动计算这些延迟
```
### 导出的数据格式
```
这是使用feed导出来生成JSON文件，
您可以轻松地更改导出格式（例如，XML或CSV）或存储后端（例如，FTP或Amazon S3）。
您还可以编写一个 项目管道以将项目存储在数据库中
```

## 还有什么？
您已经看到如何使用Scrapy从网站中提取和存储项目，但这只是表面。刮擦提供了许多强大的功能，可以使刮削更容易高效，如：
```
* 内置的支持，使用扩展的CSS选择器和XPath表达式从HTML / XML源中选择和提取数据，使用使用正则表达式提取的辅助方法。
* 一个交互的shell控制台(scrapy shell [url])用于尝试的CSS和XPath表达式抽取数据，非常有用的写作时或调试蜘蛛（IPython都知道）。
* 内置支持以多种格式生成Feed导出（JSON，CSV，XML），并将其存储在多个后端（FTP，S3，本地文件系统）
* 强大的编码支持和自动检测功能，用于处理国外，非标准和破解的编码声明。
* 强大的可扩展性支持，允许您使用信号和明确定义的API（中间件，扩展和 管道）插入自己的功能。
* 广泛的内置扩展和中间件处理：
    Cookie和会话处理
    HTTP功能，如压缩，身份验证，缓存
    用户代理欺骗
    robots.txt
    爬行深度限制
    和更多
* 一个Telnet控制台，用于挂接到您的Scrapy进程内运行的Python控制台，以便内部检查并调试您的爬虫
* 加上其他诸如可重复使用的蜘蛛之类的好处，可从Sitemaps和XML / CSV Feed中抓取网站，这是一种媒体管道，用于自动下载与抓取的项目相关联的图像（或任何其他媒体），缓存DNS解析器等等！
```

## create 一个scrapy项目
```
scrapy startproject tutorial[项目名]
```
这将创建一个tutorial包含以下内容的目录：
```
tutorial/
    scrapy.cfg            # 部署配置文件

    tutorial/             # project的Python模块
        __init__.py

        items.py          # 项目item定义文件

        pipelines.py      # 项目管道文件

        settings.py       # 项目设置文件

        spiders/          # 一个目录，你稍后会把你的爬虫放在这
            __init__.py
```
## XPath：简要介绍
XPath表达式非常强大，是Scrapy选择器的基础。实际上，CSS选择器被转换为XPath
```
>>> response.xpath('//title')
[<Selector xpath='//title' data='<title>Quotes to Scrape</title>'>]
>>> response.xpath('//title/text()').extract_first()
'Quotes to Scrape'
```

## css简单使用
假设要爬取http://quotes.toscrape.com中如下内容:
```angular2html
<div class="quote">
    <span class="text">“The world as we have created it is a process of our
    thinking. It cannot be changed without changing our thinking.”</span>
    <span>
        by <small class="author">Albert Einstein</small>
        <a href="/author/Albert-Einstein">(about)</a>
    </span>
    <div class="tags">
        Tags:
        <a class="tag" href="/tag/change/page/1/">change</a>
        <a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>
        <a class="tag" href="/tag/thinking/page/1/">thinking</a>
        <a class="tag" href="/tag/world/page/1/">world</a>
    </div>
</div>
```
```angular2html
1. $ scrapy shell 'http://quotes.toscrape.com'
2. >>> response.css('div .quote').extract()[0]
此外可以通过from pprint import pprint来美化打印
```
爬取具体内容
```angular2html
In [1]: pprint(response.css('div.quote span.text::text').extract()[0])
('“The world as we have created it is a process of our thinking. It cannot be '
 'changed without changing our thinking.”')
In [2]: pprint(response.css('div.quote span small.author::text').extract()[0])
'Albert Einstein'
In [3]: pprint(response.css('div.quote div.tags meta.keywords::attr(content)').extract()[0])
'change,deep-thoughts,thinking,world'
In [51]: pprint(response.css('ul.pager li.next a').extract()[0])
'<a href="/page/2/">Next <span aria-hidden="true">→</span></a>'
In [52]: pprint(response.css('ul.pager li.next a::attr(href)').extract()[0])
'/page/2/'
```

## 使用scrapy论证
您可以通过-a 在运行它们时使用该选项为您的蜘蛛提供命令行参数
```
scrapy crawl quotes -o quotes-humor.json -a tag=humor
```
__init__默认情况下，这些参数传递给Spider的方法并成为spider属性