# coding:utf-8

'''
@author = super_fazai
@File    : 通过协程实现动态console.py
@Time    : 2018/2/8 11:01
@connect : superonesfazai@gmail.com
'''

'''
Python 3.5添加了async和await这两个关键字
分别用来替换asyncio.coroutine和yield from
自此，协程成为新的语法，而不再是一种生成器类型了
事件循环与协程的引入，可以极大提高高负载下程序的I/O性能。
除此之外还增加了async with(异步上下文管理)、async for(异步迭代器)语法
'''

import asyncio
import itertools
import sys

@asyncio.coroutine      # 打算交给asyncio 处理的协程要使用 @asyncio.coroutine 装饰
def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    status = ''
    for char in itertools.cycle('|/-\\'):  # itertools.cycle 函数从指定的序列中反复不断地生成元素
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))  # 使用退格符把光标移回行首
        try:
            yield from asyncio.sleep(0.1)  # 使用 yield from asyncio.sleep(0.1) 代替 time.sleep(.1), 这样的休眠不会阻塞事件循环
        except asyncio.CancelledError:  # 如果 spin 函数苏醒后抛出 asyncio.CancelledError 异常，其原因是发出了取消请求
            break

    write(' ' * len(status) + '\x08' * len(status))  # 使用空格清除状态消息，把光标移回开头

@asyncio.coroutine
def slow_function():  # 5 现在此函数是协程，使用休眠假装进行I/O 操作时，使用 yield from 继续执行事件循环
    # 假装等待I/O一段时间
    yield from asyncio.sleep(3)  # 此表达式把控制权交给主循环，在休眠结束后回复这个协程
    return 42

@asyncio.coroutine
def supervisor():  #这个函数也是协程，因此可以使用 yield from 驱动 slow_function
    spinner = asyncio.async(spin('thinking!'))  # asyncio.async() 函数排定协程的运行时间，使用一个 Task 对象包装spin 协程，并立即返回
    print('spinner object:', spinner)  # Task 对象，输出类似 spinner object: <Task pending coro=<spin() running at spinner_asyncio.py:6>>
    # 驱动slow_function() 函数，结束后，获取返回值。同时事件循环继续运行，
    # 因为slow_function 函数最后使用yield from asyncio.sleep(3) 表达式把控制权交给主循环
    result = yield from slow_function()
    # Task 对象可以取消；取消后会在协程当前暂停的yield处抛出 asyncio.CancelledError 异常
    # 协程可以捕获这个异常，也可以延迟取消，甚至拒绝取消
    spinner.cancel()

    return result

def main():
    loop = asyncio.get_event_loop()  # 获取事件循环引用
    # 驱动supervisor 协程，让它运行完毕；这个协程的返回值是这次调用的返回值
    result = loop.run_until_complete(supervisor())
    loop.close()
    print('Answer:', result)

if __name__ == '__main__':
    main()
