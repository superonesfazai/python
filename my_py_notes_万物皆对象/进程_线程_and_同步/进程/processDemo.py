#!/usr/bin/python3.5
#coding: utf-8

import os

print('Process (%s) start...' % os.getpid())
# Only works on Unix/Linux/Mac, windows not work:
pid = os.fork()     # 使用fork轻松创建新进程(子进程), 然后复制父进程的所有信息到子进程中
                    # 然后⽗进程和⼦进程都会从fork()函数中得到⼀个返回值,
                    # 在⼦进程中这个值⼀定是0, ⽽⽗进程中是⼦进程的 id号
if pid < 0:
    print('fork调用失败!')
elif pid == 0:  # 子进程返回0, 通过os.getpid()获取当前进程的pid号, 通过os.getppid()获取父进程能得pid
    print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
else:           # 父进程则os.fork()返回子进程的pid
    print('I (%s) just created a child process (%s).' % (os.getpid(), pid))

# fork()创建出来的子进程和父进程谁先运行?
# 答: 父进程、子进程执行顺序没有规律，完全取决于操作系统的调度算法

'''
普通的函数调⽤, 调⽤⼀次, 返回⼀次 
但是fork()调⽤⼀次, 返回两次, 
因为操作系统⾃动把当前进程(称为⽗进程) 复制了⼀份 (称为⼦进程) 
然后, 分别在⽗进程和⼦进程内返回。
⼦进程永远返回0， ⽽⽗进程返回⼦进程的ID。
这样做的理由是， ⼀个⽗进程可以fork出很多⼦进程， 所以， ⽗进程要记下
每个⼦进程的ID， ⽽⼦进程只需要调⽤getppid()就可以拿到⽗进程的ID
'''

'''
测试结果:
Process (4692) start...
I (4692) just created a child process (4693).
I am child process (4693) and my parent is 4692.
'''
