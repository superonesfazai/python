# 高质量python代码

#### 三元运算符 "?:"
C?X:Y 等价于 X if C else Y

#### 利用assert来发现问题

#### 数值交换时不推荐使用中间变量  (测试发现下面speed更快)
```python
x, y = y, x
```

#### 充分利用Lazy evaluation的特性
Lazy evaluation常译为"延迟计算" 或 "惰性计算"，指仅仅在真正需求执行的时候才计算表达式的值

```
充分利用Lazy evaluation主要表现在下面两个方面:

1)避免不必要的计算, 带来性能上的提升
- 对于python中的条件表达式if x and y, 在x为false时y值将不进行计算
- 而对于if x or y, 当x的值为true时将直接返回不计算y的值
因此编程中充分利用这个特性

2)节省空间, 使得无线循环的数据结构变成可能
- python中最典型的使用延时计算的例子救赎生成器表达式, 它仅在每次需要计算时才通过yield产生需求元素
```

#### 不推荐用type做类型检查, 改用isinstance
```python
isinstance((2, 3), (str, list, tuple))  # 支持多种类型列表
# True
```

#### 警惕eval()的安全漏洞
"eval is evil" (eval是邪恶的), 这是一句广为人知的对eval的评价，它主要针对eval()的安全性
```
因此在实际应用过程中如果对象不是信任源, 应该尽量避免使用eval
在需要eval的地方用安全性更好的ast.literal_eval替代
```

#### 使用enumerate()获取序列迭代的索引和值

#### 分清==和is的适用场景

#### 构建合理的包成次来管理module
合理组织代码, 便于维护和使用

#### 优先使用absolute import来导入模块

#### i += 1不等于 ++i
```html
python解释器会将++i操作解释为+(+i), 其中+表示正数符号
eg: print(--2) # 2 负负得正 
```

#### 使用with自动关闭资源(上下文管理器)
with的神奇之处得益于一个叫做上下文管理器(context manager)的东西, 它用来创建一个运行时环境。
```
上下文管理器是这样一个对象: 
    它定义程序运行时需要建立的上下文, 处理程序的进入和退出, 实现上下文管理协议, 即在对象中定义__enter__()和__exit__()方法.
其中:
__enter__(): 进入运行时的上下文，返回运行时上下文相关对象, with语句会将这个值绑定到目标对象
__exit__(): 退出运行时的上下文, 定义在块执行(或终止)之后上下文管理器应该做什么。它可以处理异常, 清理现场或者处理with块语句执行完成后的需要处理的工作
```

#### 使用else子句简化循环(异常处理)
其他语言编程人员: 对于它无所不在的else往往感到非常惊讶
```html
在python中, 不仅分支里面有else语句，而且循环语句也有，甚至连异常处理也有
```

#### 遵循异常处理的几点基本规则
常用eg:
- try-except (一个或多个异常)
- try-except-else
- try-finally
- try-except-else-finally
```python
# 处理多个异常有如下语法
try:
    1
except (name1, name2):
    2
else:
    3
finally:
    4
```

#### 深入理解None, 正确判断对象是否为空

#### 格式化字符串尽量用.format方式而不是%

#### 警惕默认参数潜在的问题，慎用变长参数

#### 使用copy模块深拷贝对象

#### 使用Counter进行计数统计
```python
# 简单说就是统计某一项出现的次数
# 更优雅，更Pythonic的解决方法是使用collections.Counter
from collections import Counter
some_data = ['a', '2', 'a', '1', 'r']
print(Counter(some_data))   
# Counter({'a': 2, '2': 1, '1': 1, 'r': 1})
````

#### 深入掌握ConfigParser来读取配置文件(.conf)

####使用argparse代替optparse处理命令行参数
```
现阶段最好用的参数处理标准库是argparse，使optparse成为了一个被弃用的库
```

#### 使用pandas来处理大型的csv文件

#### 一般情况使用ElementTree解析XML
```python
import xml.etree.ElementTree as ET
tree = ET.ElementTree(file='test.xml')
root = tree.getroot()
print(root)
```

#### 使用traceback获取栈信息
```
面对异常开发人员最希望看到的往往是异常发生的现场信息
* traceback可以满足这个需求，它会完整输出完整的栈信息。
```
```python
import traceback
try:
    [][2]
except IndexError as e:
    print('xxxx')
    print(e)
    # 会输出异常发生时完整的栈信息, 包括调用顺序, 异常发生的语句, 错误类型等
    traceback.print_exc()
```

#### 使用logging记录日志信息

#### 使用Queue使多线程编程更安全

#### 利用模块实现单例模式
单例模式是最常使用的模式, 通过单例模式可以保证系统中一个类只有一个实例而且该实例易于被外界访问, 从而方便对实例个数的控制并节约系统资源
每当大家想要实现一个XxxManger类时，往往意味着这是一个单例

#### \__init__()不是构造方法(只是在类对象创建好后进行变量的初始化), \__new__()才是真正意义上的构造方法

#### 使用更安全的property设置类属性

#### 掌握metaclass(元类)

#### 熟悉python的对象协议
详情可google python协议与函数对应关系表

#### 熟悉python迭代器协议

#### 熟悉python的生成器, 使用生成器提高效率

#### 理解GIL的局限性

#### 使用multiprocessing克服GIL的缺陷

#### 对象管理与垃圾回收

#### 使用parse创建包

#### 将包发布到PyPI

#### 使用memory_profiler和objgraph剖析内存的使用

#### 努力降低算法的复杂度

#### 使用线程池提高效率

#### 使用C/C++模块扩展提高性能

#### 使用Cpython编写扩展模块