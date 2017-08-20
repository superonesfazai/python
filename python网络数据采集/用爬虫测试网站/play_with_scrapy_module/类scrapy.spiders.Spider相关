## scrapy.spiders.Spider类
这是最简单的蜘蛛，每个蜘蛛必须继承的蜘蛛（包括与Scrapy捆绑在一起的蜘蛛，以及您自己编写的蜘蛛）。

它不提供任何特殊功能。它只提供一个默认start_requests()实现，它从start_urlsspider属性发送请求，并parse 为每个结果响应调用spider的方法
#### name
一个字符串，用于定义此蜘蛛的名称。蜘蛛名称是如何通过Scrapy找到（并实例化的），因此它必须是唯一的。

但是，没有什么可以阻止您实例化同一个蜘蛛的多个实例。这是最重要的蜘蛛属性，它是必需的。

如果蜘蛛爬取了一个域，通常的做法是在域名之后命名蜘蛛，有或没有TLD。所以，例如，爬网的蜘蛛mywebsite.com通常会被调用 mywebsite

注意：
```
在Python 2中，这只能是ASCII
```
#### allowed_domains
可选的包含该蜘蛛允许爬网的域的字符串列表。

如果OffsiteMiddleware启用了不符合此列表（或其子域）中指定的域名的URL的请求 。

让我们说你的目标网址是https://www.example.com/1.html，然后添加'example.com'到列表中
####  start_urls
当没有指定特定URL时，蜘蛛将开始抓取的网址列表。那么下载的第一页就是这些列表。

随后的URL将从包含在起始URL中的数据连续生成
#### custom_settings
运行此蜘蛛时将从项目宽配置中覆盖的设置字典。

由于在实例化之前更新了设置，因此必须将其定义为类属性
#### settings
运行这个蜘蛛的配置。这是一个 Settings实例
#### logger
使用Spider创建的Python记录器name。您可以使用它通过它发送日志消息，如从Spiders记录中所述 。
#### from_crawler（crawler，* args，** kwargs ）
这是Scrapy用来创建你的蜘蛛的类方法。

您可能不需要直接覆盖它，因为默认实现作为方法的代理__init__()，使用给定的参数args和命名参数kwargs进行调用。

尽管如此，该方法 可以在新实例中设置crawler和settings属性，以便稍后在蜘蛛代码中进行访问。
```angularhtml
参数：	
crawler（Crawler实例） - 蜘蛛将被绑定到的爬行器
args（list） - 传递给__init__()方法的参数
kwargs（dict） - 传递给__init__()方法的关键字参数
```
#### start_requests（）
此方法必须返回一个可迭代的第一个请求抓取此蜘蛛。当蜘蛛开始爬取时，它被Scrapy调用。Scrapy只称之为一次，因此可以安全地实施 start_requests()为生成器

为每个url默认实现 Request(url, dont_filter=True), 然后生成start_urls
```
如果要更改用于开始抓取域的请求，则这是要覆盖的方法。
```
例如，如果您需要首先使用POST请求登录，则可以执行以下操作：
```python
class MySpider(scrapy.Spider):
    name = 'myspider'

    def start_requests(self):
        return [scrapy.FormRequest("http://www.example.com/login",
                                   formdata={'user': 'john', 'pass': 'secret'},
                                   callback=self.logged_in)]

    def logged_in(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        pass
```
#### parse（回应）
这是Scrapy使用的默认回调，用于处理下载的响应，当它们的请求没有指定回调时。

该parse方法负责处理响应并返回爬取的数据和/或更多URL。其他请求回调与Spider该类具有相同的要求。

此方法以及任何其他请求回调 必须返回一个可迭代的Request和/或一个或多个Item对象
```html
参数：
    response（Response） - 对解析的响应
```
#### log（message [，level，component ] ）
通过Spider发送日志消息的包装器logger，保持向后兼容。
#### closed（原因）
当蜘蛛关闭时调用。该方法为信号的signals.connect()提供了一个快捷方式spider_closed

我们来看一个例子：
```python
import scrapy

class MySpider(scrapy.Spider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = [
        'http://www.example.com/1.html',
        'http://www.example.com/2.html',
        'http://www.example.com/3.html',
    ]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
```
#### 从单个callback中返回多个请求和items
```python
import scrapy

class MySpider(scrapy.Spider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = [
        'http://www.example.com/1.html',
        'http://www.example.com/2.html',
        'http://www.example.com/3.html',
    ]

    def parse(self, response):
        for h3 in response.xpath('//h3').extract():
            yield {"title": h3}

        for url in response.xpath('//a/@href').extract():
            yield scrapy.Request(url, callback=self.parse)
```
#### 代替start_urls你能直接使用start_requests(), 你能使用items来得到更多的结构化数据
```python
import scrapy
from myproject.items import MyItem

class MySpider(scrapy.Spider):
    name = 'example.com'
    allowed_domains = ['example.com']

    def start_requests(self):
        yield scrapy.Request('http://www.example.com/1.html', self.parse)
        yield scrapy.Request('http://www.example.com/2.html', self.parse)
        yield scrapy.Request('http://www.example.com/3.html', self.parse)

    def parse(self, response):
        for h3 in response.xpath('//h3').extract():
            yield MyItem(title=h3)

        for url in response.xpath('//a/@href').extract():
            yield scrapy.Request(url, callback=self.parse)
```
## spider论证
蜘蛛可以接收修改行为的参数。Spider参数的一些常见用途是定义起始URL或限制爬网到站点的某些部分，但可以用于配置蜘蛛的任何功能

Spider参数通过crawl使用该-a选项的命令 传递。例如：
```shell
scrapy crawl myspider -a category=electronics
```
Spider可以以__init__方式访问参数：
```python
import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'

    def __init__(self, category=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.example.com/categories/%s' % category]
        # ...
```
默认的__init__方法将采用任何蜘蛛参数并将其复制到蜘蛛作为属性。上面的例子也可以写成如下：
```python
import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'

    def start_requests(self):
        yield scrapy.Request('http://www.example.com/categories/%s' % self.category)
```
请记住，spider参数只是字符串。蜘蛛不会自己做任何解析。如果要从命令行设置start_urls属性，则必须使用ast.literal_eval 或json.loads 等将其自身解析为列表 ，
然后将其设置为属性。否则，您将引发一个start_urls字符串（一个很常见的python陷阱）的迭代，导致每个字符被视为一个单独的URL。

一个有效的用例是设置由HttpAuthMiddleware 以下用户使用的用户代理所使用的http身份验证凭据UserAgentMiddleware：
```shell
scrapy crawl myspider -a http_user=myuser -a http_pass=mypassword -a user_agent=mybot
```
Spider参数也可以通过Scrapyd  schedule.jsonAPI 传递。