# coding:utf-8

'''
@author = super_fazai
@File    : 设置.py
@connect : superonesfazai@gmail.com
'''

"""
设置监听amp服务器

AMP运行在面向流的基于连接的协议上，例如TCP或SSL。在使用AMP协议的任何功能之前，您需要连接。用于建立AMP连接的协议类是AMP。连接设置与Twisted中几乎所有协议的工作方式相同。
"""

from twisted.protocols.amp import AMP
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.application.service import Application
from twisted.application.internet import StreamServerEndpointService

application = Application("basic AMP server")

endpoint = TCP4ServerEndpoint(reactor, 8750)
factory = Factory()
factory.protocol = AMP
service = StreamServerEndpointService(endpoint, factory)
service.setServiceParent(application)