# coding:utf-8

'''
@author = super_fazai
@File    : 通过线程实现动态console.py
@Time    : 2018/2/8 10:40
@connect : superonesfazai@gmail.com
'''

'''
动画形式的console输出
'''

import itertools
import threading
import sys
from time import sleep

class Signal:
    go = True

def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    status = ''
    for char in itertools.cycle('|/-\\'):   # itertools.cycle 函数从指定的序列中反复不断地生成元素
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))     # 使用退格符把光标移回行首
        sleep(.1)       # 每.1秒刷新一次
        if not signal.go:
            break

    write(' ' * len(status) + '\x08' * len(status))

def slow_function():  # 模拟耗时操作
    # 假装等待I/O一段时间
    sleep(5)  # 调用sleep 会阻塞主线程，这么做事为了释放GIL，创建从属线程
    return 42

def supervisor():   # 这个函数设置从属线程，显示线程对象，运行耗时计算，最后杀死进程
    signal = Signal()
    msg = 'thinking!'
    spinner = threading.Thread(target=spin, args=(msg, signal))
    print('spinner object:', spinner)  # 显示线程对象 输出 spinner object: <Thread(Thread-1, initial)>
    spinner.start()  # 启动从属进程
    result = slow_function()  # 运行slow_function 行数，阻塞主线程。同时丛书线程以动画形式旋转指针
    signal.go = False
    spinner.join()  # 等待spinner 线程结束

    return result

def main():
    result = supervisor()
    print('Answer:', result)

if __name__ == '__main__':
    main()