# coding:utf-8

'''
@author = super_fazai
@File    : 简单的聊天服务器.py
@connect : superonesfazai@gmail.com
'''

"""
简单的聊天服务器

允许用户选择用户名，然后与其他用户通信。

它演示了工厂中共享状态的使用, 每个协议的状态机以及不同协议之间的通信
"""

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class Chat(LineReceiver):
    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "GETNAME"

    def connectionMade(self):
        msg = "What's your name?".encode()
        self.sendLine(line=msg)

    def connectionLost(self, reason):
        if self.name in self.users:
            del self.users[self.name]

    def lineReceived(self, line):
        if self.state == "GETNAME":
            self.handle_GETNAME(line)
        else:
            self.handle_CHAT(line)

    def handle_GETNAME(self, name):
        if name in self.users:
            msg = "Name taken, please choose another.".encode()
            self.sendLine(line=msg)
            return

        msg = "Welcome, {}!".format(name).encode()
        self.sendLine(line=msg)
        self.name = name
        self.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        message = "<{}> {}".format(self.name, message).encode()
        for name, protocol in self.users.items():
            if protocol != self:
                protocol.sendLine(message)

class ChatFactory(Factory):
    def __init__(self):
        self.users = {} # maps user names to Chat instances

    def buildProtocol(self, addr):
        return Chat(self.users)

# listenTCP是连接Factory网络的方法。这是端点为您包装的低级API
reactor.listenTCP(8123, ChatFactory())
reactor.run()

'''
shell
$ telnet 127.0.0.1 8123
 Trying 127.0.0.1...
 Connected to 127.0.0.1.
 Escape character is '^]'.
 What's your name?
 test
 Name taken, please choose another.
 bob
 Welcome, bob!
 hello
 <alice> hi bob
 twisted makes writing servers so easy!
 <alice> I couldn't agree more
 <carrol> yeah, it's great
'''