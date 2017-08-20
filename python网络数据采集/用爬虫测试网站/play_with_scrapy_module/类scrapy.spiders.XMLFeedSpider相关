## scrapy.spiders.XMLFeedSpider类
XMLFeedSpider设计用于通过按特定节点名称循环来解析XML源。

迭代器可以选自：iternodes，xml，和html。我们推荐使用iternodes性能方面的原因迭代器，因为xml和html迭代器，以便分析它立刻生成整个DOM。但是，使用html错误的标记来解析XML时，迭代器可能很有用。

要设置迭代器和标签名称，您必须定义以下类属性：

#### iterator
一个定义要使用的迭代器的字符串。它可以是：
```html
'iternodes' - 基于正则表达式的快速迭代器
'html'- 使用的迭代器Selector。请记住，这使用DOM解析，并且必须加载内存中的所有DOM，这可能是大的Feed的问题
'xml'- 使用的迭代器Selector。请记住，这使用DOM解析，并且必须加载内存中的所有DOM，这可能是大的Feed的问题
```
它默认为：'iternodes'。
#### itertag
一个字符串，其中要重复的节点（或元素）的名称。示例：
```html
itertag  =  'product'
```
#### namespaces
一个(prefix, uri)元组列表，用于定义该文档中可用于使用此蜘蛛处理的命名空间。prefix 和 uri 将使用register_namespace()命名空间方法自动注册

然后，您可以在itertag 属性中指定具有命名空间的节点。
eg.
```python
class YourSpider(XMLFeedSpider):

    namespaces = [('n', 'http://www.sitemaps.org/schemas/sitemap/0.9')]
    itertag = 'n:url'
    # ...
```
除了这些新的属性，这个蜘蛛也有以下可重写的方法：
#### adapt_response（回应）
一种从蜘蛛中间件到达之后，在蜘蛛程序开始解析之前，它会收到响应。它可以用于在解析之前修改响应正文。此方法接收响应并返回响应（可能相同或相同）。

#### parse_node（响应，选择器）
对于与提供的标签名称（itertag）匹配的节点，将调用此方法。接收Selector每个节点的响应和一个 。覆盖此方法是强制性的。否则你的蜘蛛不会工作。此方法必须返回Item对象， Request对象或包含其中任何一个的迭代。

#### process_results（回应，结果）
对由蜘蛛返回的每个结果（项目或请求）调用此方法，并且将返回结果返回到框架核心之前执行所需的最后一次处理，例如设置项目ID。它收到结果列表和起始于这些结果的响应。它必须返回结果列表（项目或请求）

## XMLFeedSpider示例
这些蜘蛛很容易使用，我们来看一个例子：
```python
from scrapy.spiders import XMLFeedSpider
from myproject.items import TestItem

class MySpider(XMLFeedSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com/feed.xml']
    iterator = 'iternodes'  # This is actually unnecessary, since it's the default value
    itertag = 'item'

    def parse_node(self, response, node):
        self.logger.info('Hi, this is a <%s> node!: %s', self.itertag, ''.join(node.extract()))

        item = TestItem()
        item['id'] = node.xpath('@id').extract()
        item['name'] = node.xpath('name').extract()
        item['description'] = node.xpath('description').extract()
        return item
```
基本上我们做的是创建一个蜘蛛，从给定的start_urls下载一个feed，然后迭代每个item标签，打印出来，并存储一些随机数据Item