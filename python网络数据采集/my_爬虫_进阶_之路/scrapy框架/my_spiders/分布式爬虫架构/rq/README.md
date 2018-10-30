# RQ
RQ（Redis Queue）是一个简单的Python库，用于排队作业并在后台与工作人员一起处理它们。它由Redis提供支持，旨在降低进入门槛。它可以轻松集成到您的Web堆栈中。

RQ要求Redis> = 2.7.0。

这个项目的灵感来自于Celery，Resque 和这个片段的优点，并且已经被创建为Celery或其他基于AMQP的排队实现的轻量级替代品。

使用RQ，您不必预先设置任何队列，也不必指定任何通道，交换，路由规则或诸如此类的东西。您可以将作业放到任何您想要的队列上。只要将作业排入尚不存在的队列，就会立即创建它。

RQ并没有采用先进的经纪人能够做消息路由给你。您可能会认为这是一个很棒的优势或障碍，取决于您正在解决的问题。

最后，它不会说便携式协议，因为它依赖于pickle 来序列化作业，因此它是一个仅限Python的系统。

## 安装
`pip3 install rq`

## 文档
[https://python-rq.org/docs/](https://python-rq.org/docs/)

## simple use
首先，运行Redis服务器。您可以使用现有的。要将作业放在队列中，您不必执行任何特殊操作，只需定义通常冗长或阻塞的功能
```python
import requests

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())
```
然后，创建一个RQ队列：
```python
from redis import Redis
from rq import Queue

q = Queue(connection=Redis())
```
并将函数调用排入队列：
```python
from my_module import count_words_at_url
result = q.enqueue(
             count_words_at_url, 'http://nvie.com')
```

## worker
要在后台开始执行入队函数调用，请从项目的目录中启动一个worker
```bash
$ rq worker
*** Listening for work on default
Got count_words_at_url('http://nvie.com') from default
Job result = 818
*** Listening for work on default
```
