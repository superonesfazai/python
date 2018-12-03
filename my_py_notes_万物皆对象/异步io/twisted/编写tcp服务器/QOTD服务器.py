# coding:utf-8

'''
@author = super_fazai
@File    : QOTD服务器.py
@connect : superonesfazai@gmail.com
'''

from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from twisted.internet.protocol import Protocol

class QOTD(Protocol):
    def connectionMade(self):
        self.transport.write("An apple a day keeps the doctor away\r\n")
        self.transport.loseConnection()

class QOTDFactory(Factory):
    def buildProtocol(self, addr):
        '''
        创建了一个协议Factory。它的工作是构建QOTD协议实例
        :param addr:
        :return:
        '''
        return QOTD()

# 8007 is the port you want to run under. Choose something >1024
# 然后，我想听一个TCP端口，所以我创建一个TCP4ServerEndpoint来识别我想要绑定的端口，然后将我刚刚创建的工厂传递给它的listen方法。
endpoint = TCP4ServerEndpoint(reactor, 8007)
# endpoint.listen()告诉反应堆使用特定协议处理到端点地址的连接，但是反应器需要运行才能使它做任何事情。
endpoint.listen(QOTDFactory())
# 启动反应堆
reactor.run()