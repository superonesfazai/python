## 通用蜘蛛
Scrapy带有一些有用的通用蜘蛛，您可以使用它来对蜘蛛进行子类化。

他们的目标是为几个常见的刮取案例提供方便的功能，例如基于某些规则的站点上的所有链接，从Sitemaps抓取，或解析XML / CSV Feed。

对于以下蜘蛛中使用的示例，我们假设您有一个TestItem在myproject.items模块中声明的项目：
```python
import scrapy

class TestItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
```