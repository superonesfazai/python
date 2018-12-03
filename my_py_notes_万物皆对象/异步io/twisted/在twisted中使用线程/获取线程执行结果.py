# coding:utf-8

'''
@author = super_fazai
@File    : 获取线程执行结果.py
@connect : superonesfazai@gmail.com
'''

# 为此，Twisted提供了两种方法：deferToThread和blockingCallFromThread，在twisted.internet.threads模块中定义。
#为了将一些阻塞代码的结果返回到反应器线程中，我们可以使用deferToThread来执行它而不是callFromThread。

from __future__ import print_function
from twisted.internet import reactor, threads, defer
from twisted.web.client import Agent
from twisted.web.error import Error

def doLongCalculation():
    # .... do long calculation here ...
    return 3

def printResult(x):
    print(x)

# 管理Reactor线程池
# 修改线程池的大小，增加或减少使用中的线程数
reactor.suggestThreadPoolSize(30)
# run method in thread and get result as defer.Deferred
d = threads.deferToThread(doLongCalculation)
d.addCallback(printResult)
reactor.run()

# 同样，您希望在非反应器线程中运行的某些代码想要在reactor线程中调用一些代码并获得其结果，您可以使用blockingCallFromThread
# def inThread():
#     agent = Agent(reactor)
#     try:
#         result = threads.blockingCallFromThread(reactor, agent.request, "GET", "http://twistedmatrix.com/"))
#     except Error as exc:
#         print(exc)
#     else:
#         print(result)
#     reactor.callFromThread(reactor.stop)
#
# reactor.callInThread(inThread)
# reactor.run()
# blockingCallFromThread将返回该对象或引发传递给它的函数返回或引发的异常。如果传递给它的函数返回Deferred，它将返回Deferred被回调的值，或者引发它被错误回复的异常。