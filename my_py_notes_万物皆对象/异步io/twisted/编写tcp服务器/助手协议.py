# coding:utf-8

'''
@author = super_fazai
@File    : 助手协议.py
@connect : superonesfazai@gmail.com
'''

"""
许多协议建立在类似的低级抽象上。

例如，许多流行的互联网协议是基于行的，包含由换行符（通常是CR-LF）终止的文本数据，而不是包含直接的原始数据。
但是，相当多的协议是混合的 - 它们具有基于行的部分，然后是原始数据部分。示例包括HTTP / 1.1和Freenet协议。

对于这些情况，有LineReceiver协议。该协议分派给两个不同的事件处理程序 - lineReceived和rawDataReceived。
默认情况下，只会lineReceived为每一行调用一次。但是，如果setRawMode被调用，协议将调用，rawDataReceived直到setLineMode被调用，然后将其返回使用lineReceived。
它还提供了一种方法，sendLine它将数据与类用于拆分行的分隔符一起写入传输（默认情况下\r\n）。
"""

from twisted.protocols.basic import LineReceiver

class Answer(LineReceiver):
    # 简单使用线路接收器
    answers = {'How are you?': 'Fine', None: "I don't know what you mean"}

    def lineReceived(self, line):
        '''
        :param line:
        :return:
        '''
        # 请注意，分隔符不是该行的一部分。
        if line in self.answers:
            self.sendLine(self.answers[line])
        else:
            self.sendLine(self.answers[None])
