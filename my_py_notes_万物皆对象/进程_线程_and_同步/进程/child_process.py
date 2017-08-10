#!/usr/bin/python3.5
#coding: utf-8

import subprocess

print('$ nslookup www.python.org')
r = subprocess.call(['nslookup', 'www.python.org'])
print('Exit code:', r)

print('')
print('下面是有输入的子进程')
import subprocess

print('$ nslookup')
p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
print(output.decode('utf-8'))
print('Exit code:', p.returncode)


'''
测试结果:
$ nslookup www.python.org
Server:		119.29.29.29
Address:	119.29.29.29#53

Non-authoritative answer:
www.python.org	canonical name = python.map.fastly.net.
Name:	python.map.fastly.net
Address: 151.101.72.223

Exit code: 0

下面是有输入的子进程
$ nslookup
Server:		119.29.29.29
Address:	119.29.29.29#53

Non-authoritative answer:
python.org	mail exchanger = 50 mail.python.org.

Authoritative answers can be found from:
python.org	nameserver = ns1.p11.dynect.net.
python.org	nameserver = ns4.p11.dynect.net.
python.org	nameserver = ns2.p11.dynect.net.
python.org	nameserver = ns3.p11.dynect.net.
mail.python.org	internet address = 188.166.95.178
mail.python.org	has AAAA address 2a03:b0c0:2:d0::71:1
ns3.p11.dynect.net	internet address = 208.78.71.11
ns3.p11.dynect.net	has AAAA address 2001:500:94:1::11


Exit code: 0
'''