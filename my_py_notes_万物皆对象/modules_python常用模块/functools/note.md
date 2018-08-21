# functools模块
这个模块提供了3个有趣的函数，这里介绍下其用法。

首先是partial函数，它可以重新绑定函数的可选参数，生成一个callable的partial对象：
```python
>>> int('10') # 实际上等同于int('10', base=10)和int('10', 10)
10
>>> int('10', 2) # 实际上是int('10', base=2)的缩写
2
>>> from functools import partial
>>> int2 = partial(int, 2) # 这里我没写base，结果就出错了
>>> int2('10')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: an integer is required
>>> int2 = partial(int, base=2) # 把base参数绑定在int2这个函数里
>>> int2('10') # 现在缺省参数base被设为2了
2
>>> int2('10', 3) # 没加base，结果又出错了
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: keyword parameter 'base' was given by position and by name
>>> int2('10', base=3)
3
>>> type(int2)
<type 'functools.partial'>
```
从中可以看出，唯一要注意的是可选参数必须写出参数名。

接着是update_wrapper函数，它可以把被封装函数的__name__、__module__、__doc__和 __dict__都复制到封装函数去：
```python
def thisIsliving(fun):
  def living(*args, **kw):
    return fun(*args, **kw) + '活着就是吃嘛。'
  return living

@thisIsliving
def whatIsLiving():
  "什么是活着"
  return '对啊，怎样才算活着呢？'

print whatIsLiving()
print whatIsLiving.__doc__

print

from functools import update_wrapper
def thisIsliving(fun):
  def living(*args, **kw):
    return fun(*args, **kw) + '活着就是吃嘛。'
  return update_wrapper(living, fun)

@thisIsliving
def whatIsLiving():
  "什么是活着"
  return '对啊，怎样才算活着呢？'

print whatIsLiving()
print whatIsLiving.__doc__
```
结果：
```text
对啊，怎样才算活着呢？活着就是吃嘛。
None

对啊，怎样才算活着呢？活着就是吃嘛。
什么是活着
```
不过也没多大用处，毕竟只是少写了4行赋值语句而已。

最后是wraps函数，它将update_wrapper也封装了进来：
```python
#-*- coding: gbk -*-

from functools import wraps

def thisIsliving(fun):
  @wraps(fun)
  def living(*args, **kw):
    return fun(*args, **kw) + '活着就是吃嘛。'
  return living

@thisIsliving
def whatIsLiving():
  "什么是活着"
  return '对啊，怎样才算活着呢？'

print whatIsLiving()
print whatIsLiving.__doc__
```
结果还是一样的：
```text
对啊，怎样才算活着呢？活着就是吃嘛。
什么是活着
```