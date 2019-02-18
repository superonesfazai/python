# coding:utf-8

'''
@author = super_fazai
@File    : 优化之使用uvloop代替asyncio默认事件循环_可进一步加快异步IO速度.py
@connect : superonesfazai@gmail.com
'''

from asyncio import set_event_loop_policy
from uvloop import EventLoopPolicy

# github(https://github.com/MagicStack/uvloop) : uvloop是内置asyncio默认事件循环的快速替代品，可以进一步加快异步I/O操作的速度。uvloop在Cython中实现，并在引擎盖下使用libuv。
# uvloop的使用非常简单，只要在获取事件循环前，调用如下方法，将asyncio的事件循环策略设置为uvloop的事件循环策略。
# 有了 uvloop，我们可以写出每秒每 CPU 核心可以推送上万次请求的 Python 网络互连代码。在一个多核心系统上，用上进程池，也许还可以进一步地提高性能。
set_event_loop_policy(EventLoopPolicy())