## celery 架构
![](./images/111.png)
Celery包含如下组件：

- Producer：调用了Celery提供的API、函数或者装饰器而产生任务并交给任务队列处理的都是任务生产者。
- Celery Beat：任务调度器，Beat进程会读取配置文件的内容，周期性地将配置中到期需要执行的任务发送给任务队列。
- Celery Worker：执行任务的消费者，通常会在多台服务器运行多个消费者来提高执行效率。
- Broker：消息代理，或者叫作消息中间件，接受任务生产者发送过来的任务消息，存进队列再按序分发给任务消费方（通常是消息队列或者数据库）。
- Result Backend：任务处理完后保存状态信息和结果，以供查询。Celery默认已支持Redis、RabbitMQ、MongoDB、Django ORM、SQLAlchemy等方式。

## Celery序列化
在客户端和消费者之间传输数据需要序列化和反序列化，Celery支持如下的序列化方案：

- pickle
    - pickle是Python标准库中的一个模块，支持Python内置的数据结构，但是它是Python的专有协议。从Celery3.2开始，由于安全性等原因Celery将拒绝pickle这个方案。
- json
    - json支持多种语言，可用于跨语言方案。
- yaml
    - yaml的表达能力更强，支持的数据类型比json多，但是Python客户端的性能不如JSON。
- msgpack
    - msgpack是一个二进制的类JSON的序列化方案，但是比JSON的数据结构更小、更快。

#### apply_async常用参数
- countdown：指定多少秒后执行任务
```python
task1.apply_async(args=(2, 3), countdown=5)    # 5 秒后执行任务
```
- eta (estimated time of arrival)：指定任务被调度的具体时间，参数类型是 datetime
```python
from datetime import datetime, timedelta

# 当前 UTC 时间再加 10 秒后执行任务
task1.multiply.apply_async(args=[3, 7], eta=datetime.utcnow() + timedelta(seconds=10))
```
- expires：任务过期时间，参数类型可以是 int，也可以是 datetime
```python
task1.multiply.apply_async(args=[3, 7], expires=10)    # 10 秒后过期
```
- calllback: 回调通过callback指定
```python
task1.apply_async(args=[admin_id], callback=on_success) # on_success是回调函数, 但是回调函数参数唯一，只为response, 访问方法: response.result
```
- queue: queue 指定队列名称，可以把不同任务分配到不同的队列
```python
task1.apply_async((2, 2), queue='lopri')
```
- 结果选项
```python
# 你可以使用以下ignore_result选项启用或禁用结果存储
result = add.apply_async(1, 2, ignore_result=True)
result.get() # -> None

# Do not ignore result (default)
result = add.apply_async(1, 2, ignore_result=False)
result.get() # -> 3
```

## 切记
异步, 不要在外部调用task的函数中sleep阻塞进程, 可在task内休眠

#### 任务状态
ready() 方法查看任务是否完成处理:
```python
>>> result.ready()
False
```
你可以等待任务完成，但这很少使用，因为它把异步调用变成了同步调用:
```python
>>> result.get(timeout=1)
8
```
倘若任务抛出了一个异常， get() 会重新抛出异常， 但你可以指定 propagate 参数来覆盖这一行为:
```python
>>> result.get(propagate=False)
```
如果任务抛出了一个异常，你也可以获取原始的回溯信息:
```python
>>> result.traceback
…
```
完整的结果对象参考见 celery.result 

## Supervisor
在生产环境中，我们通常会使用[Supervisor](http://supervisord.org/)来控制 Celery Worker 进程。

## 错误排查
错误1: Received unregistered task of type 
```bash
# 去查看该APP中的所有注册了的task.
$ celery -A proxy_tasks inspect registered
-> celery@afahostdeiMac.local: OK
    * proxy_tasks._get_kuaidaili_proxy
    * proxy_tasks._write_into_redis
    * proxy_tasks.check_proxy_status
```

## 优化建议
1. 忽略掉你不需要的任务结果

如果你不关心任务的执行结果，请确保ignore_result
是关闭的状态，因为存储结果将耗费时间并且占用资源。
```python
@app.task(ignore_result=True) 
def mytask():
     something()
```
另外，任务结果的设置还可以由task_ignore_result来指定为全局设置。
2. 避免创建同步的子任务

让一个任务等待另一个任务是十分低效的，如果并行工作池的资源耗尽了，还将造成任务死锁。

建议采用异步任务的方式，比如可以使用回调函数来实现。
- 不好的方式：
```python
@app.task 
def update_page_info(url):
    page = fetch_page.delay(url).get()
    info = parse_page.delay(url, page).get()
    store_page_info.delay(url, info)
@app.task 
def fetch_page(url):
    return myhttplib.get(url)
@app.task 
def parse_page(url, page):
    return myparser.parse_document(page)
@app.task 
def store_page_info(url, info):
    return PageInfo.objects.create(url, info)
```
- 好的方式：
```python
def update_page_info(url):
    # fetch_page -> parse_page -> store_page
    chain = fetch_page.s(url) | parse_page.s() | store_page_info.s(url)
    chain() 
@app.task() def fetch_page(url):
    return myhttplib.get(url)
@app.task() 
def parse_page(page):
    return myparser.parse_document(page)
@app.task(ignore_result=True)
def store_page_info(info, url):
    PageInfo.objects.create(url=url, info=info)
```
这里我将不同的任务通过签名[signature()](http://docs.celeryproject.org/en/master/reference/celery.html#celery.signature)连接起来，创建一个任务链。在[Canvas: Designing Work-flows](http://docs.celeryproject.org/en/master/getting-started/next-steps.html#designing-workflows)你可以看到关于任务链和其他强大的结构的使用方法。
默认的，celery不允许你运行同步任务，但在罕见的极端情况下你可能必须这么做。

【警告】不建议将子任务做成同步设计。
```python
@app.task 
def update_page_info(url):
    page = fetch_page.delay(url).get(disable_sync_subtasks=False)
    info = parse_page.delay(url, page).get(disable_sync_subtasks=False)
    store_page_info.delay(url, info)
@app.task 
def fetch_page(url):
    return myhttplib.get(url)
@app.task 
def parse_page(url, page):
    return myparser.parse_document(page)
@app.task 
def store_page_info(url, info):
    return PageInfo.objects.create(url, info)
```
3. 颗粒度
任务颗粒度是指每个子任务所需的计算量。总体上说，把大的问题拆分成很多个小的任务，比很少的几个长任务要好一点。因为采用小任务的方式，你可以并行执行很多小任务，并且这些小任务不会因为执行时间太长而阻塞了执行进程，使它无法运行其他正在等待的任务。

但是，执行任务是有开销的，比如需要发送一个消息、数据不在本地（译者注：需要到远端请求数据或将数据存储到远端）等。所以如果任务粒度被拆分的过细，这些开销很可能将使你得不偿失。

4. 数据位置
任务执行进程离数据越近越好。最好是在本地的内存里，最差的情况，可别是从另一个大陆传输过来啊。如果数据离你很远，你可以考虑在那个地方跑另一个任务执行进程。如果这都做不到，那就把常用的数据缓存起来，或者预先把一些常用数据读过来。
在任务执行器之间共享数据的最简单的办法，就是使用一个分布式缓存系统，例如memcached。

5. 状态
由于celery是一个分布式系统，你不知道任务在哪个进程、或者在什么机器上执行，你甚至不知道任务是否将及时被运行。

古老的异步名言告诉我们，“要靠每个任务来负责维护整个世界”，意思是说，在某个任务要执行的时候，这个世界可能看起来已经变化了，因此任务端要肩负起保证这个世界是他应有的样子的责任。例如，如果你有一个任务需要对一个搜索引擎进行重新索引，并且这个重新索引的过程需要最多5分钟来执行，那么必须由任务端来负责这个事情，而不是调用端。

假设以下的场景，你有一片文章，并且有一个任务是自动添加缩略语的扩写：
