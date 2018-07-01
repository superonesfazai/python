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
