# encoding: utf-8

import socket

port = 8081
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(b'hello,this is a 避免死锁 info !', (host, port))