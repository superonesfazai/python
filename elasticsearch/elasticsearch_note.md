# python 与 elasticsearch

## linux java env配置
```bash
$ sudo apt-get update
$ sudo apt-get install default-jdk
$ java -version
```

## 安装最新的elasticsearch
https://www.elastic.co/downloads/elasticsearch
```bash
# ubuntu
$ wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.3.2.zip
# 安装
$ unzip elasticsearch-6.3.2.zip
```

## 启动elasticsearch
- 不能以root启动, 否则报错
```bash
org.elasticsearch.bootstrap.StartupException: java.lang.RuntimeException: can not run elasticsearch as root
	at org.elasticsearch.bootstrap.Elasticsearch.init(Elasticsearch.java:140) ~[elasticsearch-6.3.2.jar:6.3.2]
	at org.elasticsearch.bootstrap.Elasticsearch.execute(Elasticsearch.java:127) ~[elasticsearch-6.3.2.jar:6.3.2]
	at org.elasticsearch.cli.EnvironmentAwareCommand.execute(EnvironmentAwareCommand.java:86) ~[elasticsearch-6.3.2.jar:6.3.2]
	at org.elasticsearch.cli.Command.mainWithoutErrorHandling(Command.java:124) ~[elasticsearch-cli-6.3.2.jar:6.3.2]
	at org.elasticsearch.cli.Command.main(Command.java:90) ~[elasticsearch-cli-6.3.2.jar:6.3.2]
	at org.elasticsearch.bootstrap.Elasticsearch.main(Elasticsearch.java:93) ~[elasticsearch-6.3.2.jar:6.3.2]
	at org.elasticsearch.bootstrap.Elasticsearch.main(Elasticsearch.java:86) ~[elasticsearch-6.3.2.jar:6.3.2]
Caused by: java.lang.RuntimeException: can not run elasticsearch as root
	at org.elasticsearch.bootstrap.Bootstrap.initializeNatives(Bootstrap.java:104) ~[elasticsearch-6.3.2.jar:6.3.2]
	at org.elasticsearch.bootstrap.Bootstrap.setup(Bootstrap.java:171) ~[elasticsearch-6.3.2.jar:6.3.2]
	at org.elasticsearch.bootstrap.Bootstrap.init(Bootstrap.java:326) ~[elasticsearch-6.3.2.jar:6.3.2]
	at org.elasticsearch.bootstrap.Elasticsearch.init(Elasticsearch.java:136) ~[elasticsearch-6.3.2.jar:6.3.2]
	... 6 more
```
- 新建用户来启动
```bash
# * 先挪动文件
# 运行下面命令将安装包移动到 /opt 目录，然后转到 opt 目录
$ mv elasticsearch-6.3.2.zip /opt && cd /opt
# 解压安装包,然后重命名为 elasticsearch
$ unzip elasticsearch-6.3.2.zip
$ mv elasticsearch-6.3.2 elasticsearch
```
```bash
# 创建elsearch用户组及elsearch用户
$ groupadd elsearch
$ useradd elsearch -g elsearch -p elasticsearch
# 更改elasticsearch文件夹及内部文件的所属用户及组为elsearch:elsearch
$ cd /opt && chown -R elsearch:elsearch elasticsearch

# 切换到elsearch用户再启动
$ su elsearch
$ cd elasticsearch/bin
$ ./elasticsearch
```
```bash
# ElasticSearch后端启动命令
./elasticsearch -d
```

## 测试是否成功启动
```bash
$ curl http://localhost:9200
```
这就意味着你现在已经启动并运行一个 Elasticsearch 节点了，你可以用它做实验了。 单个节点 可以作为一个运行中的 Elasticsearch 的实例。 而一个 集群 是一组拥有相同 cluster.name 的节点， 他们能一起工作并共享数据，还提供容错与可伸缩性。(当然，一个单独的节点也可以组成一个集群) 你可以在 elasticsearch.yml 配置文件中 修改 cluster.name ，该文件会在节点启动时加载 (这个重启服务后才会生效)。

## 与elasearch交互
- simple demo
```python
from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}
res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
print(res['result'])

res = es.get(index="test-index", doc_type='tweet', id=1)
print(res['_source'])

es.indices.refresh(index="test-index")

res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
```
- 典型搜索示例
```python
from elasticsearch import Elasticsearch
client = Elasticsearch()

response = client.search(
    index="my-index",
    body={
        "query": {
            "filtered": {
                "query": {
                    "bool": {
                        "must": [{"match": {"title": "python"}}],
                        "must_not": [{"match": {"description": "beta"}}]
                    }
                },
                "filter": {"term": {"category": "search"}}
            }
        },
        "aggs" : {
            "per_tag": {
                "terms": {"field": "tags"},
                "aggs": {
                    "max_lines": {"max": {"field": "lines"}}
                }
            }
        }
    }
)

for hit in response['hits']['hits']:
    print(hit['_score'], hit['_source']['title'])

for tag in response['aggregations']['per_tag']['buckets']:
    print(tag['key'], tag['max_lines']['value'])
```
- 使用Python DSL重写搜索示例：
    - Query按名称创建适当的对象（例如“match”）
    - 将查询组成复合bool查询
    - filtered自.filter()使用以来创建查询
    - 提供对响应数据的便捷访问
    - 到处都没有卷曲或方括号
```python
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

client = Elasticsearch()

s = Search(using=client, index="my-index") \
    .filter("term", category="search") \
    .query("match", title="python")   \
    .exclude("match", description="beta")

s.aggs.bucket('per_tag', 'terms', field='tags') \
    .metric('max_lines', 'max', field='lines')

response = s.execute()

for hit in response:
    print(hit.meta.score, hit.title)

for tag in response.aggregations.per_tag.buckets:
    print(tag.key, tag.max_lines.value)
```
- 持久性示例
    - 在此示例中，您可以看到：
        - 提供默认连接
        - 使用映射配置定义字段
        - 设置索引名称
        - 定义自定义方法
        - 重写内置.save()方法以挂钩持久性生命周期
        - 检索并将对象保存到Elasticsearch中
        - 访问底层客户端以获取其他API
```python
'''简单的Python类来表示博客系统中的文章'''
from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])

class Article(Document):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    body = Text(analyzer='snowball')
    tags = Keyword()
    published_from = Date()
    lines = Integer()

    class Index:
        name = 'blog'
        settings = {
            "number_of_shards": 2,
        }

    def save(self, ** kwargs):
        self.lines = len(self.body.split())
        return super(Article, self).save(** kwargs)

    def is_published(self):
        return datetime.now() >= self.published_from

# create the mappings in elasticsearch
Article.init()

# create and save and article
article = Article(meta={'id': 42}, title='Hello world!', tags=['test'])
article.body = ''' looong text '''
article.published_from = datetime.now()
article.save()

article = Article.get(id=42)
print(article.is_published())

# Display cluster health
print(connections.get_connection().cluster.health())
```
- 预先构建的分面搜索
    - 如果您已Document定义了自己的定义，则可以非常轻松地创建分面搜索类以简化搜索和过滤。
```python
from elasticsearch_dsl import FacetedSearch, TermsFacet, DateHistogramFacet

class BlogSearch(FacetedSearch):
    doc_types = [Article,]
    # fields that should be searched
    fields = ['tags', 'title', 'body']

    facets = {
        # use bucket aggregations to define facets
        'tags': TermsFacet(field='tags'),
        'publishing_frequency': DateHistogramFacet(field='published_from', interval='month')
    }

# empty search
bs = BlogSearch()
response = bs.execute()

for hit in response:
    print(hit.meta.score, hit.title)

for (tag, count, selected) in response.facets.tags:
    print(tag, ' (SELECTED):' if selected else ':', count)

for (month, count, selected) in response.facets.publishing_frequency:
    print(month.strftime('%B %Y'), ' (SELECTED):' if selected else ':', count)
```

## 完整python文档: http://elasticsearch-py.readthedocs.io/en/master/