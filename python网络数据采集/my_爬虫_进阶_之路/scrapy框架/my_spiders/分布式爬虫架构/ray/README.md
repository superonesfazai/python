# ray(推荐)
ray是一个灵活的高性能分布式执行框架(引擎)

Ray实现了一个动态任务图计算模型，它支持任务并行和actor编程模型。为了满足AI应用程序的性能要求，我们提出了一种体系结构，该体系结构使用分片存储系统和新型自下而上的分布式调度程序在逻辑上集中系统的控制状态。在我们的实验中，我们展示了亚毫秒的远程任务延迟和线性吞吐量扩展超过每秒180万个任务。

可以在单个机器上运行相同的代码以实现高效的多处理，并且可以在群集上使用它来进行大型计算。
- Ray如何异步执行任务以实现并行性。
- Ray如何使用对象ID来表示不可变的远程对象。

使用Ray时，涉及多个过程。
- 多个工作进程执行任务并将结果存储在对象库中。每个工人都是一个独立的过程。
- 每个节点一个对象存储将不可变对象存储在共享内存中，并允许工作人员以最少的复制和反序列化有效地共享同一节点上的对象。
- 每个节点一个本地调度程序将任务分配给同一节点上的工作程序。
- 一个全局调度本地调度接收任务，并将它们分配到其他地方调度。
- 甲驱动器是Python过程，所述用户控件。例如，如果用户正在运行脚本或使用Python shell，则驱动程序是运行脚本或shell的Python进程。驱动程序类似于工作程序，因为它可以将任务提交给其本地调度程序并从对象存储中获取对象，但不同之处在于本地调度程序不会将任务分配给要执行的驱动程序。
- 一个Redis的服务器维护大量系统状态。例如，它跟踪哪些对象存在于哪些机器和任务规范（但不是数据）上。它也可以直接查询以进行调试。

[github](https://github.com/ray-project/ray)

[doc](http://ray.readthedocs.io/en/latest/index.html)

## installation
```bash
$ pip3 install ray
```

## Actor模型
Actor模型是一个概念模型，用于处理并发计算。它定义了一系列系统组件应该如何动作和交互的通用规则

一个Actor指的是一个最基本的计算单元。它能接收一个消息并且基于其执行计算。

这个理念很像面向对象语言，一个对象接收一条消息（方法调用），然后根据接收的消息做事（调用了哪个方法）

Actors一大重要特征在于actors之间相互隔离，它们并不互相共享内存。这点区别于上述的对象。也就是说，一个actor能维持一个私有的状态，并且这个状态不可能被另一个actor所改变。

## 启动
```python
import ray

ray.init()
```

## 异步计算
Ray允许异步执行任意Python函数。
这是通过将Python函数指定为远程函数来完成的

## 远程功能
而调用返回并导致Python解释器阻塞直到计算完成，而调用 立即返回一个对象ID并创建一个任务。
该任务将由系统调度并异步执行（可能在不同的机器上）。当任务完成执行时，其返回值将存储在对象库中
```python
import ray

@ray.remote
def add2(a, b):
    return a + b

x_id = add2.remote(1, 2)
ray.get(x_id)  # 3
```
使用异步任务来并行化计算
```python
from time import sleep
import ray

def f1():
    sleep(1)

@ray.remote
def f2():
    sleep(1)

# The following takes ten seconds.
[f1() for _ in range(10)]

# The following takes one second (assuming the system has at least ten CPUs).
ray.get([f2.remote() for _ in range(10)])
```
提交任务和执行任务之间存在明显的区别。调用远程函数时，执行该函数的任务将提交给本地调度程序，并立即返回任务输出的对象ID。但是，在系统实际调度工作人员的任务之前，不会执行任务。任务执行不是懒惰的。系统将输入数据移动到任务，一旦其输入依赖性可用并且有足够的资源用于计算，任务将立即执行。

提交任务时，每个参数可以通过值或对象ID传入。例如，这些行具有相同的行为。
```python
add2.remote(1, 2)
add2.remote(1, ray.put(2))
add2.remote(ray.put(1), ray.put(2))
```
远程函数永远不会返回实际值，它们始终返回对象ID。

当实际执行远程函数时，它对Python对象进行操作。也就是说，如果使用任何对象ID调用远程函数，系统将从对象库中检索相应的对象。

请注意，远程函数可以返回多个对象ID。
```python
import ray

@ray.remote(num_return_vals=3)
def return_multiple():
    return 1, 2, 3

a_id, b_id, c_id = return_multiple.remote()
```

## 表达任务之间的依赖关系
可以通过将一个任务的对象ID输出作为参数传递给另一个任务来表达任务之间的依赖关系。例如，我们可以按如下方式启动三个任务，每个任务都取决于之前的任务。
```python
@ray.remote
def f(x):
    return x + 1

x = f.remote(0)
y = f.remote(x)
z = f.remote(y)
ray.get(z) # 3
```
组合任务的能力使得表达有趣的依赖关系变得容易。考虑以下实现的树减少
```python
import numpy as np
import ray

@ray.remote
def generate_data():
    return np.random.normal(size=1000)

@ray.remote
def aggregate_data(x, y):
    return x + y

# Generate some random data. This launches 100 tasks that will be scheduled on
# various nodes. The resulting data will be distributed around the cluster.
data = [generate_data.remote() for _ in range(100)]

# Perform a tree reduce.
while len(data) > 1:
    data.append(aggregate_data.remote(data.pop(0), data.pop(0)))

# Fetch the result.
ray.get(data)
```

## 远程功能中的远程功能
到目前为止，我们只从驱动程序调用远程函数。但是工作进程也可以调用远程函数。为了说明这一点，请考虑以下示例。
```python
import ray

@ray.remote
def sub_experiment(i, j):
    # Run the jth sub-experiment for the ith experiment.
    return i + j

@ray.remote
def run_experiment(i):
    sub_results = []
    # Launch tasks to perform 10 sub-experiments in parallel.
    for j in range(10):
        sub_results.append(sub_experiment.remote(i, j))
    # Return the sum of the results of the sub-experiments.
    return sum(ray.get(sub_results))

results = [run_experiment.remote(i) for i in range(5)]
ray.get(results) # [45, 55, 65, 75, 85]
```
在run_experiment工作人员上执行远程功能时，它会sub_experiment多次调用远程功能。这是一个例子，说明多个实验如何在内部利用并行性，都可以并行运行

## ray api
```python
ray.init(redis_address=None, num_cpus=None, num_gpus=None, 
resources=None, object_store_memory=None, node_ip_address=None, 
object_id_seed=None, num_workers=None, driver_mode=0, 
redirect_worker_output=False, redirect_output=True, 
ignore_reinit_error=False, num_custom_resource=None, 
num_redis_shards=None, redis_max_clients=None, 
plasma_directory=None, huge_pages=False, include_webui=True, use_raylet=None)
```
连接到现有的Ray群集或启动它并连接到群集。

此方法处理两种情况。Ray集群已经存在，我们只是将此驱动程序附加到它，或者我们启动与Ray集群关联的所有进程并附加到新启动的集群。

要启动Ray和所有相关进程，请按如下方式使用：
```python
ray.init()
```
要连接到现有的Ray群集，请按以下方式使用此方法（替换为适当的地址）：
```python
ray.init(redis_address="123.45.67.89:6379")
```
参数：	
- redis_address（str） - 要连接的Redis服务器的地址。如果未提供此地址，则此命令将启动Redis，全局调度程序，本地调度程序，等离子存储，等离子管理器和一些工作程序。当Python退出时，它也会杀死这些进程。
- num_cpus（int） - 用户希望配置所有本地调度程序的cpu数。
- num_gpus（int） - 用户希望配置所有本地调度程序的gpus数。
- resources - 将资源名称映射到可用资源数量的字典。
- object_store_memory - 用于启动对象存储的内存量（以字节为单位）。
- node_ip_address（str） - 我们所在节点的IP地址。
- object_id_seed（int） - 用于为对象ID的确定性生成设定种子。可以在同一作业的多次运行中使用相同的值，以便以一致的方式生成对象ID。但是，不应将相同的ID用于不同的作业。
- num_workers（int） - 要启动的工作者数量。仅在未提供redis_address时才提供此选项。
- driver_mode（bool） - 启动驱动程序的模式。这应该是ray.SCRIPT_MODE，ray.LOCAL_MODE和ray.SILENT_MODE之一。
- redirect_worker_output - 如果应将工作进程的stdout和stderr重定向到文件，则为True。
- redirect_output（bool） - 如果非工作进程的stdout和stderr应重定向到文件，则为True，否则为false。
- ignore_reinit_error - 如果我们应该第二次调用错误来调用ray.init（），则为 True。
- num_redis_shards - 除主Redis分片外还要启动的Redis分片数。
- redis_max_clients - 如果提供，尝试使用此maxclients编号配置Redis。
- plasma_directory - 将创建Plasma内存映射文件的目录。
- huge_pages - 布尔标志，指示是否使用hugetlbfs支持启动Object Store。需要plasma_directory。
- include_webui - 布尔标志，指示是否启动Web UI，这是一个Jupyter笔记本。
- use_raylet - 如果应该使用新的raylet代码路径，则为 True。

返回：	有关已启动进程的地址信息。

```python
ray.remote(*args，**kwargs)
```
定义远程函数或actor类。

这可以在没有参数的情况下用于定义远程函数或actor，如下所示：
```python
@ray.remote
def f():
    return 1

@ray.remote
class Foo(object):
    def method(self):
        return 1
```
它也可以与特定的关键字参数一起使用：
- num_return_vals：这仅适用于远程功能。它指定远程函数调用返回的对象ID数。
- num_cpus：为此任务或actor的生命周期保留的CPU核心数量。
- num_gpus：为此任务或actor的生命周期保留的GPU数量。
- resources：为此任务或actor的生命周期保留的各种自定义资源的数量。这是一个将字符串（资源名称）映射到数字的字典。
- max_calls：仅用于远程功能。这指定了给定工作程序在必须退出之前可以执行给定远程函数的最大次数（这可用于解决第三方库中的内存泄漏或回收无法轻松释放的资源，例如GPU内存被TensorFlow收购）。默认情况下，这是无限的。

这可以按如下方式完成：
```python
@ray.remote(num_gpus=1, max_calls=1, num_return_vals=2)
def f():
    return 1, 2

@ray.remote(num_cpus=2, resources={"CustomResource": 1})
class Foo(object):
    def method(self):
        return 1
```

```python
ray.get(object_ids，worker = <ray.worker.Worker object> )
```
从对象库中获取远程对象或远程对象列表。

此方法将阻塞，直到对象ID对应的对象在本地对象库中可用。如果此对象不在本地对象库中，则它将从具有该对象的对象库中发送（一旦创建了该对象）。如果object_ids是列表，则将返回与列表中的每个对象对应的对象。

参数：	object_ids - 要获取的对象的对象ID或要获取的对象ID列表。

返回：	Python对象或Python对象列表。

举：	Exception - 如果创建对象的任务或创建其中一个对象的任务引发异常，则会引发异常。

```python
ray.wait(object_ids，num_returns = 1，timeout = None，worker = <ray.worker.Worker object> )
```
返回已准备好的ID列表以及不是的ID列表。

如果设置了超时，则函数将在请求的ID数量准备就绪或达到超时时返回，以先发生者为准。如果未设置，则该函数只是等待，直到该数量的对象准备就绪并返回该确切数量的对象ID。

此方法返回两个列表。第一个列表由对象ID组成，这些对象ID对应于对象库中可用的对象。第二个列表对应于其余的对象ID（可能已准备就绪或未准备好）。

保留对象ID的输入列表的排序。也就是说，如果A在输入列表中位于B之前，并且两者都在就绪列表中，则A将位于就绪列表中的B之前。如果A和B都在剩余列表中，这也适用。

参数：	
- object_ids（List [ ObjectID ]） - 可能已准备好但可能未准备好的对象的对象ID列表。请注意，这些ID必须是唯一的。
- num_returns（int） - 应返回的对象ID数。
- timeout（int） - 返回之前等待的最长时间（以毫秒为单位）。

返回：	准备好的对象ID列表以及剩余对象ID的列表。

```python
ray.put(value，worker = <ray.worker.Worker object>)
```
将对象存储在对象库中。

参数：	value - 要存储的Python对象。

返回：	分配给此值的对象ID。

```python
ray.get_gpu_ids()
```
获取工作人员可用的GPU的ID。

返回：	GPU ID列表。

```python
ray.get_resource_ids()
```
获取工作人员可用的资源的ID。

此函数仅在raylet代码路径中受支持。

返回：	将资源名称映射到对列表的字典，其中每对由资源的ID和为该worker保留的资源的分数组成。

```python
ray.shutdown(worker = <ray.worker.Worker object> )
```
断开worker的连接，并终止ray.init()启动的进程。

当使用Ray的Python进程退出时，这将自动运行。可以连续两次运行它。此函数的主要用例是清除测试之间的状态。

请注意，这将清除所有远程函数定义，actor定义和现有actor，因此如果您希望在调用ray.shutdown()之后使用任何先前定义的远程函数或actor，则需要重新定义它们。如果它们是在导入的模块中定义的，那么您将需要重新加载模块。

```python
ray.method(* args，** kwargs )
```
注释actor方法。
```python
@ray.remote
class Foo(object):
    @ray.method(num_return_vals=2)
    def bar(self):
        return 1, 2

f = Foo.remote()

_, _ = f.bar.remote()
```
参数：	num_return_vals - 调用此actor方法应返回的对象ID数。

