#!/usr/bin/python2.7
#coding: utf-8

from socket import *

#通过IP+port 找到互联网中的唯一进程
myhost = ''  #它会绑定本地每个IP和每个网卡
mypost = 9091

#AF_INET IPv4协议 SOCK_STREAM 流式协议默认为TCP/IP协议
sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((myhost, mypost))
sockobj.listen(128)  #设置同时有128个连接
while True:
    connection, address = sockobj.accept() 
    print('connect by', address)
    while True:
        data = connection.recv(1024)  #一次接收1024个字节
        if not data:
            break
        connection.send('echo:' + data)
    connection.close()
