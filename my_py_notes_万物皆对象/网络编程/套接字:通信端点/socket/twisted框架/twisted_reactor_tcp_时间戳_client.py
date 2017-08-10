# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-24 下午4:54
# @File    : twisted_reactor_tcp_时间戳_client.py

from twisted.internet import protocol, reactor

host = ' localhost '
port = 21567

class TSClntProtocol(protocol.Protocol):
    def send_data(self):
        data = input('> ')
        if data:
            print('...sending %s...' % data)
            self.transport.write(data)
        else:
            self.transport.loseConnection()

    def connectionMade(self):
        self.send_data()

    def dataReceived(self, data):
        print(data)
        self.send_data()

# 下面报错未解决先注释掉
# class TSClntFactory(protocol.ClientFactory):
#     protocol = TSClntProtocol
#     client_connection_lost = client_connection_faied = \
#         lambda: self, connector, reason: reactor.stop()

reactor.connecTCP(host, port, TSClntFactory)
reactor.run()