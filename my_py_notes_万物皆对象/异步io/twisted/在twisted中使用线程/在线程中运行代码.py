# coding:utf-8

'''
@author = super_fazai
@File    : 在线程中运行代码.py
@connect : superonesfazai@gmail.com
'''

from __future__ import print_function
from time import sleep
from twisted.internet import reactor

def aSillyBlockingMethod(x):
    sleep(2)
    print(x)

# callInThread和callFromThread允许您分别将代码的执行移出反应器线程，但这并不总是足够的。
# callInThread将你的代码放入队列中，由反应堆线程池中的下一个可用线程运行。
# 这意味着，根据提交给池的其他工作，您的方法可能无法立即运行。
reactor.callInThread(aSillyBlockingMethod, "2 seconds have passed")
reactor.run()

'''
注意:
请记住，callInThread只能同时运行固定的最大数量的任务，并且反应堆的所有用户都在共享该限制。
因此，您不应该提交依赖于其他任务的任务以完成执行callInThread。

这样的任务的一个例子是这样的：
from __future__ import print_function

q = Queue()
def blocker():
    print(q.get() + q.get())
def unblocker(a, b):
    q.put(a)
    q.put(b)
    
在这种情况下，除非可以成功运行以提供输入，否则blocker将永久阻止unblocker; 同样，unblocker如果blocker不运行消耗其输出，可能永远阻止。因此，如果您有一个最大大小为X的线程池，并且您运行了，则反应堆线程池将永远被楔入，无法处理更多工作甚至关闭。for each in range(X): reactor.callInThread(blocker)
'''