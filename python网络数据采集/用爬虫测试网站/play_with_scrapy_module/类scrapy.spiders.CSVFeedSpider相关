## scrapy.spiders.CSVFeedSpider类
这个蜘蛛非常类似于XMLFeedSpider，除了它遍历行而不是节点。在每次迭代中调用的方法是parse_row()。

#### delimiter
CSV文件中每个字段分隔符的字符串默认为','（逗号）。

#### quotechar
CSV文件中每个字段的字符串带有字符串默认为'"'（引号）。

#### headers
CSV文件中的列名列表。

#### parse_row（响应，行）
使用CSV文件的每个提供（或检测到）标题的键接收响应和dict（表示每行）。这个蜘蛛也有机会超越adapt_response和process_results处理之前和之后的方法。
## CSVFeedSpider示例
我们来看一个类似于上一个例子的例子，但是使用 CSVFeedSpider：
```python
from scrapy.spiders import CSVFeedSpider
from myproject.items import TestItem

class MySpider(CSVFeedSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com/feed.csv']
    delimiter = ';'
    quotechar = "'"
    headers = ['id', 'name', 'description']

    def parse_row(self, response, row):
        self.logger.info('Hi, this is a row!: %r', row)

        item = TestItem()
        item['id'] = row['id']
        item['name'] = row['name']
        item['description'] = row['description']
        return item
```