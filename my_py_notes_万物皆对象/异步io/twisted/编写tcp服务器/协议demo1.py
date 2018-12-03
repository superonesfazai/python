# coding:utf-8

'''
@author = super_fazai
@File    : 协议demo1.py
@connect : superonesfazai@gmail.com
'''

from twisted.internet.protocol import Protocol

class Echo(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.numProtocols = self.factory.numProtocols + 1
        self.transport.write(
            "Welcome! There are currently %d open connections.\n" %
            (self.factory.numProtocols,))

    def connectionLost(self, reason):
        self.factory.numProtocols = self.factory.numProtocols - 1

    def dataReceived(self, data):
        self.transport.write(data)

# 在这里connectionMade并connectionLost合作以保持共享对象（工厂）中活动协议的计数。
# 工厂用于共享在任何给定连接的生命周期之外存在的状态。
'''
在上面的代码中，loseConnection在写入传输后立即调用。
loseConnection只有当所有数据都被Twisted写入操作系统时，该调用才会关闭连接，因此在这种情况下使用它是安全的，而不必担心传输写入丢失。
如果生产者与传输一起使用，loseConnection则只有在生产者未注册后才会关闭连接。

在某些情况下，等待所有数据写出来都不是我们想要的。
由于网络故障，或连接另一端的错误或恶意，写入传输的数据可能无法传送，因此即使loseConnection被称为连接也不会丢失。
在这些情况下，abortConnection可以使用：它会立即关闭连接，无论传输中仍未写入的缓冲数据，还是仍然注册的生成器。
请注意，abortConnection仅在Twisted 11.1及更高版本中可用。
'''