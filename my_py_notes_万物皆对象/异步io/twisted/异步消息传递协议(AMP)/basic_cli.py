# coding:utf-8

'''
@author = super_fazai
@File    : basic_cli.py
@connect : superonesfazai@gmail.com
'''

"""
连接到amp服务器
"""

from sys import stdout

from twisted.python.log import startLogging, err
from twisted.protocols.amp import AMP
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ClientEndpoint

def connect():
    endpoint = TCP4ClientEndpoint(reactor, "127.0.0.1", 8750)
    return endpoint.connect(Factory.forProtocol(AMP))

def main():
    startLogging(stdout)

    d = connect()
    d.addErrback(err, "Connection failed")
    def done(ignored):
        reactor.stop()
    d.addCallback(done)

    reactor.run()

if __name__ == '__main__':
    import basic_cli
    raise SystemExit(basic_cli.main())