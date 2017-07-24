# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-24 下午4:46
# @File    : twisted_reactor_tcp_时间戳_server.py

from twisted.internet import protocol, reactor
from time import ctime

port = 21567

class TSServProtocol(protocol.Protocol):
    def connectionMade(self):
        clnt = self.clnt = self.transport.getPeer().host
        print('...connected from :', clnt)
    def dataReceived(self, data):
        self.transport.write('[%s] %s' %
                             (ctime(), data))

factory = protocol.Factory()
factory.protocol = TSServProtocol
print('waiting for connection...')
reactor.listenTCP(port, factory)
reactor.run()