# coding = utf-8

'''
@author = super_fazai
@File    : 进程池中的Queue.py
@Time    : 2017/8/9 11:56
@connect : superonesfazai@gmail.com
'''

'''
注意:
    如果要使⽤Pool创建进程, 就需要使⽤multiprocessing.Manager()中的
    Queue(), ⽽不是multiprocessing.Queue(), 否则会得到⼀条如下的错误信息：
    RuntimeError: Queue objects should only be shared between processes
    through inheritance
'''

# 修改import中的Queue为Manager
from multiprocessing import Manager, Pool
import os, time, random

def reader(q):
    print("reader启动(%s),⽗进程为(%s)" % (os.getpid(),os.getppid()))
    for i in range(q.qsize()):
        print("reader从Queue获取到消息： %s" % q.get(True))

def writer(q):
    print("writer启动(%s),⽗进程为(%s)" % (os.getpid(),os.getppid()))
    for i in "dongGe":
        q.put(i)

if __name__=="__main__":
    print("(%s) start" % os.getpid())
    q=Manager().Queue() # 使⽤Manager中的Queue来初始化
    po=Pool()
    # 使⽤阻塞模式创建进程, 这样就不需要在reader中使⽤死循环了
    # 可以让writer完全执⾏完成后, 再⽤reader去读取
    po.apply(writer,(q,))
    po.apply(reader,(q,))
    po.close()
    po.join()
    print("(%s) End" % os.getpid())

'''
测试结果:
(6373) start
writer启动(6375),⽗进程为(6373)
reader启动(6376),⽗进程为(6373)
reader从Queue获取到消息： d
reader从Queue获取到消息： o
reader从Queue获取到消息： n
reader从Queue获取到消息： g
reader从Queue获取到消息： G
reader从Queue获取到消息： e
(6373) End
'''