# tenacity
python强大的通用重试库, 可用于def & async def, 简化了向任何事情添加重试行为的任务。

[github](https://github.com/jd/tenacity)

## 安装
`pip3 install tenacity`

## 功能
- 通用装饰器API
- 指定停止条件（即按尝试次数限制）
- 指定等待条件（即尝试之间的指数退避休眠）
- 自定义例外重试
- 自定义重试预期的返回结果
- 在协同程序上重试

## 示例

#### 基本重试
默认行为是永远重试，无需等待引发异常
```python
from tenacity import retry

@retry
def never_give_up_never_surrender():
    print("Retry forever ignoring Exceptions, don't wait between retries")
    raise Exception
```

#### 停止
- 在尝试n次后放弃重试
```python
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(7))
def stop_after_7_attempts():
    print("Stopping after 7 attempts")
    raise Exception
```
- 一直重试直到超时停止
```python
from tenacity import retry, stop_after_delay

@retry(stop=stop_after_delay(10))
def stop_after_10_s():
    print("Stopping after 10 seconds")
    raise Exception
```
- 使用'|'组合多个停止条件(常用)
```python
from tenacity import stop_after_delay, stop_after_attempt, retry

@retry(stop=(stop_after_delay(10) | stop_after_attempt(5)))
def stop_after_10_s_or_5_retries():
    print("Stopping after 10 seconds or 5 retries")
    raise Exception
```

#### 重试前等待
大多数事情都不希望尽可能快地进行轮询，所以让我们在重试之间等待2秒钟。
```python
from tenacity import retry, wait_fixed

@retry(wait=wait_fixed(2))
def wait_2_s():
    print("Wait 2 second between retries")
    raise Exception
```
有些东西表现得最好，注入了一点随机性。
```python
from tenacity import retry, wait_random

@retry(wait=wait_random(min=1, max=2))
def wait_random_1_to_2_s():
    print("Randomly wait 1 to 2 seconds between retries")
    raise Exception
```
然后，在重试分布式服务和其他远程端点时，很难超过指数退避。(指数等待)
```python
from tenacity import retry, wait_exponential

@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
def wait_exponential_1():
    print("Wait 2^x * 1 second between each retry starting with 4 seconds, then up to 10 seconds, then 10 seconds afterwards")
    raise Exception
```
然而，在重试分布式服务和其他远程端点时，同样难以击败固定等待和抖动（以帮助避免雷鸣般的群体）
```python
from tenacity import retry, wait_fixed, wait_random

@retry(wait=wait_fixed(3) + wait_random(0, 2))
def wait_fixed_jitter():
    print("Wait at least 3 seconds, and add up to 2 seconds of random delay")
    raise Exception
```
当多个进程争用共享资源时，指数级增加的抖动有助于最大限度地减少冲突。
```python
from tenacity import retry, wait_random_exponential

@retry(wait=wait_random_exponential(multiplier=1, max=60))
def wait_exponential_jitter():
    print("Randomly wait up to 2^x * 1 seconds between each retry until the range reaches 60 seconds, then randomly up to 60 seconds afterwards")
    raise Exception
```
有时需要建立一系列退避。
```python
from tenacity import retry, wait_fixed, wait_chain

@retry(wait=wait_chain(*[wait_fixed(3) for i in range(3)] +
                       [wait_fixed(7) for i in range(2)] +
                       [wait_fixed(9)]))
def wait_fixed_chained():
    print("Wait 3s for 3 attempts, 7s for the next 2 attempts and 9s for all attempts thereafter")
    raise Exception
```

#### 是否重试
- 我们有一些选项来处理引发特定或一般异常的重试
```python
from tenacity import retry, retry_if_exception_type

@retry(retry=retry_if_exception_type(IOError))
def might_io_error():
    print("Retry forever with no wait if an IOError occurs, raise any other errors")
    raise Exception
```
- 还可以使用函数的结果来改变重试的行为
```python
from tenacity import retry, retry_if_result

def is_none_p(value):
    """Return True if value is None"""
    return value is None

@retry(retry=retry_if_result(is_none_p))
def might_return_none():
    print("Retry with no wait if return value is None")
```
- 还可以结合几个条件(常用)
```python
from tenacity import retry, retry_if_result, retry_if_exception_type

def is_none_p(value):
    """Return True if value is None"""
    return value is None

@retry(retry=(retry_if_result(is_none_p) | retry_if_exception_type()))
def might_return_none():
    print("Retry forever ignoring Exceptions with no wait if return value is None")
```
还支持停止，等待等任意组合，以便您自由混合和匹配。

也可以通过提高TryAgain 异常随时显式重试：
```python
from tenacity import retry, TryAgain
@retry
def do_something():
    result = something_else()
    if result == 23:
       raise TryAgain
```

#### 错误处理
虽然“超时”重试的callables默认会引发RetryError，但如果需要，我们可以重新加载最后一次尝试的异常：
```python
from tenacity import retry, stop_after_attempt

@retry(reraise=True, stop=stop_after_attempt(3))
def raise_my_exception():
    raise MyException("Fail")

try:
    raise_my_exception()
except MyException:
    # timed out retrying
    pass
```

#### 重试之前和之后，以及记录(log)
在使用before回调函数调用函数的任何尝试之前，可以执行一个操作：
```python
import logging
from tenacity import retry, stop_after_attempt, before_log

logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(3), before=before_log(logger, logging.DEBUG))
def raise_my_exception():
    raise MyException("Fail")
```
本着同样的精神，可以在失败的呼叫之后执行
```python
import logging
from tenacity import retry, stop_after_attempt, after_log

logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(3), after=after_log(logger, logging.DEBUG))
def raise_my_exception():
    raise MyException("Fail")
```
也可以只记录要重试的故障。通常在等待间隔后重试，因此调用关键字参数 before_sleep：
```python
import logging
from tenacity import retry, stop_after_attempt, before_sleep_log

logger = logging.getLogger(__name__)
@retry(stop=stop_after_attempt(3),
       before_sleep=before_sleep_log(logger, logging.DEBUG))
def raise_my_exception():
    raise MyException("Fail")
```

#### 自定义回调
您还可以定义自己的回调。回调应该接受一个名为的参数retry_state，该参数包含有关当前重试调用的所有信息。

例如，您可以在所有重试失败后调用自定义回调函数，而不会引发异常（或者您可以重新加注或执行任何操作）
```python
from tenacity import retry, stop_after_attempt, retry_if_result

def return_last_value(retry_state):
    """return the result of the last call attempt"""
    return retry_state.outcome.result()

def is_false(value):
    """Return True if value is False"""
    return value is False

# will return False after trying 3 times to get a different result
@retry(stop=stop_after_attempt(3),
       retry_error_callback=return_last_value,
       retry=retry_if_result(is_false))
def eventually_return_false():
    return False
```

#### 在运行时更改参数
通过使用附加到包装函数的retry_with函数调用它时，可以根据需要更改重试装饰器的参数：
```python
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(3))
def raise_my_exception():
    raise MyException("Fail")

try:
    raise_my_exception.retry_with(stop=stop_after_attempt(4))()
except Exception:
    pass

print(raise_my_exception.retry.statistics)
```

#### 异步和重试
最后，retry也适用于asyncio和Tornado（> = 4.5）协同程序。睡眠也是异步完成的。
```python
from tenacity import retry

@retry
async def my_async_function(loop):
    await loop.getaddrinfo('8.8.8.8', 53)
```
```python
from tenacity import retry
import tornado

@retry
@tornado.gen.coroutine
def my_async_function(http_client, url):
    yield http_client.fetch(url)
```
您甚至可以通过传递正确的睡眠功能来使用替代事件循环，例如curio或Trio：
```python
from tenacity import retry

@retry(sleep=trio.sleep)
async def my_async_function(loop):
    await asks.get('https://example.org')
```
