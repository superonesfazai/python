## scrapy.spider.CrawlSpider类
这是用于爬网常规网站的最常用的蜘蛛，因为它通过定义一组规则提供了一个方便的下列链接机制。它可能不是最适合您的特定网站或项目，但它对于几种情况来说足够通用，所以您可以从它开始，根据需要覆盖更多自定义功能，或仅实现自己的蜘蛛。

除了继承自Spider（您必须指定）的属性外，此类还支持一个新属性：

## LinkExtractors
```python
class scrapy.linkextractors.LinkExtractor
```
Link Extractors 的目的很简单: 提取链接｡

每个LinkExtractor有唯一的公共方法是 extract_links()，它接收一个 Response 对象，并返回一个 scrapy.link.Link 对象。

Link Extractors要实例化一次，并且 extract_links 方法会根据不同的 response 调用多次提取链接｡
```python
class scrapy.linkextractors.LinkExtractor(
    allow = (),
    deny = (),
    allow_domains = (),
    deny_domains = (),
    deny_extensions = None,
    restrict_xpaths = (),
    tags = ('a','area'),
    attrs = ('href'),
    canonicalize = True,
    unique = True,
    process_value = None
)
```
```html
主要参数：
    * allow：满足括号中“正则表达式”的值会被提取，如果为空，则全部匹配。
    
    * deny：与这个正则表达式(或正则表达式列表)不匹配的URL一定不提取。
    
    * allow_domains：会被提取的链接的domains。
    
    * deny_domains：一定不会被提取链接的domains。
    
    * restrict_xpaths：使用xpath表达式，和allow共同作用过滤链接
```


#### rules
在rules中包含一个（或多个）Rule对象的列表。每个都Rule对爬取网站的动作定义了特定操作。规则对象如下所述。如果多个规则匹配相同的链接，则将根据在此属性中定义的顺序使用第一个规则。

这个蜘蛛也暴露了一个可重写的方法：
#### parse_start_url(response)
start_urls响应调用此方法。它允许解析初始响应，并且必须返回 Item对象，Request 对象或包含其中任何一个的迭代

## Crawling rules
```python
class scrapy.spiders.Rule(
    link_extractor, 
    callback=None, 
    cb_kwargs=None, 
    follow=None, 
    process_links=None, 
    process_request=None)
```
```html
* link_extractor  是一个链接提取器对象，它定义了如何从每个爬网页面中提取链接。

* callback  从link_extractor中每获取到链接时，参数所指定的值作为回调函数，该回调函数接受一个response作为其第一个参数。此回调接收响应作为其第一个参数，并且必须返回包含Item和/或 Request对象（或其任何子类）的列表。
        注意:
            当编写爬网蜘蛛规则时，避免使用parse回调，因为CrawlSpider使用parse方法本身来实现其逻辑。因此，如果您覆盖该parse方法，爬网蜘蛛将无法工作
* cb_kwargs 是一个包含要传递给回调函数的关键字参数的dict。

* follow  是一个布尔值，它指定是否应该使用此规则提取的每个响应都遵循链接。如果callback是无follow默认值True，否则默认为False。

* process_links  指定该spider中哪个的函数将会被调用，从link_extractor中获取到链接列表时将会调用该函数。该方法主要用来过滤。

* process_request  指定该spider中哪个的函数将会被调用， 该规则提取到每个request时都会调用该函数。 (用来过滤request)
```
## CrawlSpider示例
```python
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = scrapy.Item()
        item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
        item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
        return item
```
这个蜘蛛将开始爬行example.com的主页，收集类别链接和项目链接，使用该parse_item方法解析后者。对于每个项目响应，将使用XPath从HTML中提取一些数据，并将Item填充它

## 爬取规则(Crawling rules)
继续用腾讯招聘为例，给出配合rule使用CrawlSpider的例子:

1. 首先运行
```shell
scrapy shell "http://hr.tencent.com/position.php?&start=0#a"
```
2. 导入LinkExtractor，创建LinkExtractor实例对象。：
```
from scrapy.linkextractors import LinkExtractor

page_lx = LinkExtractor(allow=('position.php?&start=\d+'))
```
```
allow : LinkExtractor对象最重要的参数之一，
        这是一个正则表达式，必须要匹配这个正则表达式(或正则表达式列表)的URL才会被提取，
        如果没有给出(或为空), 它会匹配所有的链接｡

deny : 用法同allow，只不过与这个正则表达式匹配的URL不会被提取)｡
        它的优先级高于 allow 的参数，如果没有给出(或None), 将不排除任何链接｡
```
3. 调用LinkExtractor实例的extract_links()方法查询匹配结果：
```
page_lx.extract_links(response)
```
4. 没有查到：
```
[]
```
5. 注意转义字符的问题，继续重新匹配：
```
page_lx = LinkExtractor(allow=('position\.php\?&start=\d+'))
# page_lx = LinkExtractor(allow = ('start=\d+'))

page_lx.extract_links(response)
```
![](https://i.loli.net/2019/09/24/ba1p8PmnZM9Y3gj.jpg)
## CrawlSpider 版本
那么，scrapy shell测试完成之后，修改以下代码
```python
# 提取匹配 'http://hr.tencent.com/position.php?&start=\d+'的链接
page_lx = LinkExtractor(allow = ('start=\d+'))

rules = [
    #提取匹配,并使用spider的parse方法进行分析;并跟进链接(没有callback意味着follow默认为True)
    Rule(page_lx, callback = 'parse', follow = True)
]
```
这么写对吗？

不对！千万记住 callback 千万不能写 parse，再次强调：由于CrawlSpider使用parse方法来实现其逻辑，如果覆盖了 parse方法，crawl spider将会运行失败。