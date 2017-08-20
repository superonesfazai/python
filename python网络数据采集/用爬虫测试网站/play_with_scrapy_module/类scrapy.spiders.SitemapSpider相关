## scrapy.spiders.SitemapSpider类
SitemapSpider允许您通过使用Sitemaps发现URL来抓取 站点。

它支持嵌套的站点地图并从robots.txt发现站点地图URL 。
#### sitemap_urls
指向要抓取其网址的站点地图的网址列表。

您也可以指向robots.txt，并将其解析为从其中提取站点地图网址。
#### sitemap_rules
一个元组的列表，其中：(regex, callback)
```
* regex是一个正则表达式，用于匹配从站点地图提取的网址。 regex可以是一个str或一个编译的正则表达式对象。
* 回调是用于处理与正则表达式匹配的网址的回调。callback可以是字符串（指示蜘蛛方法的名称）或可调用。
```
例如：
```html
sitemap_rules  =  [（'/ product /' ， 'parse_product' ）]
```
规则按顺序应用，仅匹配的第一个将被使用。

如果省略此属性，则将在parse回调中处理在Sitemap中发现的所有网址。

#### sitemap_follow
应遵循的sitemap的正则表达式列表。这仅适用于使用指向其他站点地图文件的Sitemap索引文件的网站。

默认情况下，所有的Sitemaps都遵循。

#### sitemap_alternate_links
指定是否url应遵循一个替代链接。这些是同一个网站在同一个网站内传递的另一种语言的链接url。

例如：
```html
< url > 
    < loc > http ：// example 。com / </ loc > 
    < xhtml ：link  rel = “alternate”  hreflang = “de”  href = “http://example.com/de” /> 
</ url >
```
使用sitemap_alternate_linksset，这将检索两个URL。随着 sitemap_alternate_links禁用，只http://example.com/将被检索。

默认为sitemap_alternate_links禁用。
## SitemapSpider示例
最简单的例子：处理通过使用parse回调通过站点地图发现的所有URL ：
```python
from scrapy.spiders import SitemapSpider

class MySpider(SitemapSpider):
    sitemap_urls = ['http://www.example.com/sitemap.xml']

    def parse(self, response):
        pass # ... scrape item here ...
```
处理一些url与某些回调和其他url与不同的回调：
```python
from scrapy.spiders import SitemapSpider

class MySpider(SitemapSpider):
    sitemap_urls = ['http://www.example.com/sitemap.xml']
    sitemap_rules = [
        ('/product/', 'parse_product'),
        ('/category/', 'parse_category'),
    ]

    def parse_product(self, response):
        pass # ... scrape product ...

    def parse_category(self, response):
        pass # ... scrape category ...
```
关注robots.txt文件中定义的站点地图，并且仅跟踪其URL包含的站点地图/sitemap_shop：
```python
from scrapy.spiders import SitemapSpider

class MySpider(SitemapSpider):
    sitemap_urls = ['http://www.example.com/robots.txt']
    sitemap_rules = [
        ('/shop/', 'parse_shop'),
    ]
    sitemap_follow = ['/sitemap_shops']

    def parse_shop(self, response):
        pass # ... scrape shop here ...
```
将SitemapSpider与其他网址来源组合：
```python
from scrapy.spiders import SitemapSpider

class MySpider(SitemapSpider):
    sitemap_urls = ['http://www.example.com/robots.txt']
    sitemap_rules = [
        ('/shop/', 'parse_shop'),
    ]

    other_urls = ['http://www.example.com/about']

    def start_requests(self):
        requests = list(super(MySpider, self).start_requests())
        requests += [scrapy.Request(x, self.parse_other) for x in self.other_urls]
        return requests

    def parse_shop(self, response):
        pass # ... scrape shop here ...

    def parse_other(self, response):
        pass # ... scrape other here ...
```
