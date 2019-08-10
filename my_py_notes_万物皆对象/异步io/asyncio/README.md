# asyncio
该模块提供了使用协程编写单线程并发代码，通过套接字和其他资源复用I​​ / O访问，运行网络客户端和服务器以及其他相关原语的基础结构。

以下是包内容的更详细列表:
- 一个可插入的[事件循环](https://docs.python.org/3.6/library/asyncio-eventloop.html#asyncio-event-loop)，具有各种特定于系统的实现;
- [传输](https://docs.python.org/3.6/library/asyncio-protocol.html#asyncio-transport)和[协议](https://docs.python.org/3.6/library/asyncio-protocol.html#asyncio-protocol)抽象（类似于 [Twisted中的](https://twistedmatrix.com/trac/)那些）;
- 具体支持TCP，UDP，SSL，子进程管道，延迟调用等（有些可能与系统有关）;
- 一个[Future](https://docs.python.org/3.6/library/asyncio-task.html#asyncio.Future)模仿一个中类[concurrent.futures](https://docs.python.org/3.6/library/concurrent.futures.html#module-concurrent.futures) 模块，但适于与事件循环使用;
- 协同程序和任务基于（yield from[PEP 380](https://www.python.org/dev/peps/pep-0380/)），以顺序方式帮助编写并发代码;
- 取消对Futures和协同程序的支持;
- [同步原语](https://docs.python.org/3.6/library/asyncio-sync.html#asyncio-sync)，用于单个线程中的协同程序，模仿[threading](https://docs.python.org/3.6/library/threading.html#module-threading)模块中的协同程序;
- 一个接口，用于将工作传递给线程池，当你绝对必须使用一个阻塞I / O调用的库时。

异步编程比传统的“顺序”编程更复杂, 在开发期间[启用调试模式](https://docs.python.org/3.6/library/asyncio-dev.html#asyncio-debug-mode)以检测常见问题。

实际上，真正的asyncio比我们前几节中学到的要复杂得多，它还实现了零拷贝、公平调度、异常处理、任务状态管理等等使 Python 异步编程更完善的内容。

[零拷贝](https://blog.csdn.net/cnweike/article/details/48166121)

报错: RuntimeError: Cannot run the event loop while another loop is running

原因如下blog:

[asyncio与多线程/多进程那些事](https://zhuanlan.zhihu.com/p/38575715)

## 基本事件循环
[源码](https://github.com/python/cpython/tree/3.6/Lib/asyncio/events.py)

事件循环是由中央执行设备提供的asyncio。它提供多种设施，包括：
- 注册，执行和取消延迟呼叫（超时）。
- 为各种通信创建客户端和服务器传输。
- 启动子进程和相关传输以与外部程序进行通信。
- 将昂贵的函数调用委托给线程池。

类asyncio.BaseEventLoop

类asyncio.AbstractEventLoop
    事件循环的抽象基类。
这个类[不是线程安全的](https://docs.python.org/3.6/library/asyncio-dev.html#asyncio-multithreading)。

### 运行事件循环
- AbstractEventLoop.run_forever()
```
运行直到stop()被调用。
```

- AbstractEventLoop.run_until_complete(future)
```
运行直到Future完成。

如果参数是一个协程对象，它将被包装 ensure_future()

返回Future的结果，或者提出异常。
```
- AbstractEventLoop.is_running()

```
返回事件循环的运行状态。
```

- AbstractEventLoop.stop()
```bash
停止事件循环
```

- AbstractEventLoop.is_closed()
```bash
True如果事件循环已关闭，则返回。
```

- AbstractEventLoop.close()
```bash
关闭事件循环。循环不能运行。待处理的回调将丢失。

这会清除队列并关闭执行程序，但不会等待执行程序完成。

这是幂等的，不可逆转的。在此之后不应该调用其他方法。
```

- coroutine AbstractEventLoop.shutdown_asyncgens()
```bash
安排所有当前打开的异步生成器对象以通过aclose()调用关闭。
在调用此方法之后，只要迭代了新的异步生成器，事件循环就会发出警告。
应该用于可靠地完成所有计划的异步生成器。
```
```python
try:
    loop.run_forever()
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
```

### calls
大多数asyncio功能都不接受关键字。如果要将关键字传递给回调，请使用functools.partial()。

```python
loop.call_soon(functools.partial(print, "Hello", flush=True))
print("Hello", flush=True)
```
```bash
注意 functools.partial()比lambda函数更好，
因为 asyncio可以检查functools.partial()对象以在调试模式下显示参数，
而lambda函数的表示很差。
```
- AbstractEventLoop.call_soon（回调，* args ）
```bash
它作为FIFO队列运行，回调按照它们的注册顺序调用。每个回调将被调用一次。
asyncio.Handle返回一个实例，可用于取消回调。
使用functools.partial将关键字传递给回调。
```
- AbstractEventLoop.call_soon_threadsafe（回调，* args ）

### 延迟调用
事件循环有自己的内部时钟用于计算超时。使用哪个时钟取决于（特定于平台的）事件循环实现; 理想情况下，它是一个单调的时钟。这通常是一个不同的时钟time.time()。
```
注意: 超时（相对延迟或绝对时间）不应超过一天。
```
- AbstractEventLoop.call_later（延迟，回调，* args ）
```bash
安排在给定的延迟 秒（int或float）之后调用回调。
```

- AbstractEventLoop.call_at（何时，回调，* args ）
```bash
安排在给定的绝对时间戳（int或float）时调用 回调，使用相同的时间引用 。
AbstractEventLoop.time()
```
- AbstractEventLoop.time()
```bash
float根据事件循环的内部时钟，将当前时间作为值返回。
```

### Futures
- AbstractEventLoop.create_future()
```bash
创建一个asyncio.Future附加到循环的对象。

这是在asyncio中创建future的首选方法，因为事件循环实现可以提供Future类的替代实现（具有更好的性能或工具）。
```

### Tasks
查看Task对象的可用方法
`help(asyncio.Task)`

- AbstractEventLoop.create_task(coro)
```bash
安排协程对象的执行：将来包装它。返回一个Task对象。
```

- AbstractEventLoop.set_task_factory(factory)
```bash
设置将由其使用的任务工厂 AbstractEventLoop.create_task()

如果factory是None默认任务factory将被设置。

如果factory是可调用的，它应该具有签名匹配 ，其中循环将是对活动事件循环的引用，coro将是协同对象。callable必须返回兼容的对象。
```
- AbstractEventLoop.get_task_factory()
```bash
返回任务工厂，或者None如果正在使用默认工厂。
```

### 创建连接
[https://docs.python.org/3.6/library/asyncio-eventloop.html#creating-connections](https://docs.python.org/3.6/library/asyncio-eventloop.html#creating-connections)

### 创建监听连接
[https://docs.python.org/3.6/library/asyncio-eventloop.html#creating-listening-connections](https://docs.python.org/3.6/library/asyncio-eventloop.html#creating-listening-connections)


## 事件循环

### 时间循环函数
- asyncio.get_event_loop()
```bash
获取当前上下文的事件循环。

相当于召唤get_event_loop_policy().get_event_loop()
```
- asyncio.set_event_loop(loop)
```bash
将当前上下文的事件循环设置为循环。

相当于召唤get_event_loop_policy().set_event_loop(loop)
```
- asyncio.new_event_loop()
```bash
根据此策略的规则创建并返回一个新的事件循环对象。

相当于召唤get_event_loop_policy().new_event_loop()
```

### 访问全局循环策略
- asyncio.get_event_loop_policy()
```bash
获取当前的事件循环策略。
```
- asyncio.set_event_loop_policy(policy)
```bash
设置当前事件循环策略。如果政策是None，默认策略将被恢复。
```

### 自定义事件循环策略
要实现新的事件循环策略，建议您子类化具体的默认事件循环策略DefaultEventLoopPolicy 并覆盖要更改其行为的方法，例如：
```python
class MyEventLoopPolicy(asyncio.DefaultEventLoopPolicy):

    def get_event_loop(self):
        """Get the event loop.

        This may be None or an instance of EventLoop.
        """
        loop = super().get_event_loop()
        # Do something with loop ...
        return loop

asyncio.set_event_loop_policy(MyEventLoopPolicy())
```

## Tasks and coroutines(协程)

### 链协程
eg:
```python
import asyncio

async def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    await asyncio.sleep(1.0)
    return x + y

async def print_sum(x, y):
    result = await compute(x, y)
    print("%s + %s = %s" % (x, y, result))

loop = asyncio.get_event_loop()
loop.run_until_complete(print_sum(1, 2))
loop.close()
```
compute()被链接到print_sum()：print_sum()coroutine等到compute()完成才返回结果

### Future with run_forever()
```python
# 异步后增加一个常规函数回调
from asyncio import get_event_loop, sleep, Future, ensure_future

async def slow_operation(future):
    await sleep(1)
    future.set_result('Future is done!')

def got_result(future):
    print(future.result())
    loop.stop()

loop = get_event_loop()
future = Future()
ensure_future(slow_operation(future))
future.add_done_callback(got_result)
try:
    loop.run_forever()
finally:
    loop.close()
```

### Tasks
- class asyncio.Task（coro，*，loop = None ）
```bash
安排协程的执行：将来包装它。任务是一个子类Future。
```

### asyncio.wait(tasks) 与 async.gather(*task)的区别
- gather更加high-level高层， gather除了多任务外，还可以对任务进行分组。优先使用gather
- 两者都可以将多个任务封装成task注册到事件循环中，不同的是，前者可以接收一个task列表，后者可以接收多个task
- 注意，两者返回值是不一样的
    - asyncio.wait() 返回值是一个元组，(finished_task_set, pending_task_set)，即处于finish状态的task和处于pending状态的task的集合。task内封装了协程的运行状态，想要获取协程的结果，需要调用遍历并调用task的
    - async.gather() 返回值是一个列表，存放了协程函数的返回值
    
### asyncio.as_completed(tasks)
```python
for url in range(20):
        url = 'http://shop.projectsedu.com/goods/{}/'.format(url)
        tasks.append(asyncio.ensure_future(get_url(url)))     # tasks中放入的是future
    for task in asyncio.as_completed(tasks):    # 完成一个 print一个
        result = await task
        print(result)
```

## 协程通信
协程(Co-routine)，即是协作式的例程

它是非抢占式的多任务子例程的概括，可以允许有多个入口点在例程中确定的位置来控制程序的暂停与恢复执行。

例程是什么？编程语言定义的可被调用的代码段，为了完成某个特定功能而封装在一起的一系列指令。一般的编程语言都用称为函数或方法的代码结构来体现。

### queue
协程是单线程的，所以协程中完全可以使用全局变量实现queue来相互通信，但是如果想要 在queue中定义存放有限的最大数目。 我们需要使用 :
```python
from asyncio import Queue
queue = Queue(maxsize=3)   # queue的put和get需要用await
```

## 并发和多线程

## 传输
传输是由提供的类asyncio来抽象各种通信信道。您通常不会自己实例化运输; 相反，您将调用一个AbstractEventLoop方法来创建传输并尝试启动底层通信通道，并在成功时回拨您。

一旦建立了通信信道，传输总是与协议实例配对。然后，协议可以出于各种目的调用传输方法。

asyncio目前实现TCP，UDP，SSL和子流程管道的传输。运输方式可用的方法取决于运输方式。

传输类不是线程安全的。

## coroutine 协程
协程对象，指一个使用async关键字定义的函数，它的调用不会立即执行函数，而是会返回一个协程对象。协程对象需要注册到事件循环，由事件循环调用。

## event_loop 事件循环
程序开启一个无限的循环，程序员会把一些函数（协程）注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。

## future 对象
代表将来执行或没有执行的任务的结果。它和task上没有本质的区别

## task 任务
一个协程对象就是一个原生可以挂起的函数，任务则是对协程进一步封装，其中包含任务的各种状态。Task 对象是 Future 的子类，它将 coroutine 和 Future 联系在一起，将 coroutine 封装成一个 Future 对象。

## async/await 关键字
python3.5 用于定义协程的关键字，async定义一个协程，await用于挂起阻塞的异步调用接口。其作用在一定程度上类似于yield。