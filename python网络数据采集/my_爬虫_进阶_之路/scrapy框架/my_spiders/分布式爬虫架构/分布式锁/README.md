# 分布式锁
在实际应用场景中，我们可能有多个worker，可能在一台机器，也可能分布在不同的机器，但只有一个worker可以同时持有一把锁，这个时候我们就需要用到分布式锁了。

正常情况下，worker获得锁后，处理自己的任务，完成后自动释放持有的锁，是不是感觉有点熟悉，很容易想到我们的上下文管理器，这里我们简单的用装饰器实现 with...as... 语法。

[python实现推荐python-redis-lock](https://github.com/ionelmc/python-redis-lock) 可进行快速集成!