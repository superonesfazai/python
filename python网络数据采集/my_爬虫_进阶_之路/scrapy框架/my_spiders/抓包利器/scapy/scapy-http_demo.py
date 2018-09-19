# coding:utf-8

'''
@author = super_fazai
@File    : scapy-http_demo.py
@connect : superonesfazai@gmail.com
'''

import scapy_http.http as HTTP
from scapy.all import (
    IP,
    TCP,
    sniff,
)
from scapy.error import Scapy_Exception

count = 0

def handle_tcp_pkt(pkt):
    global count
    count = count + 1
    print(count)

    try:
        src = pkt[IP].src
        src_port = pkt[IP].sport
    except (AttributeError, IndexError) as e:
        print(e.args[0])
        return False

    if HTTP.HTTPRequest or HTTP.HTTPResponse in pkt:
        try:
            dst_port = pkt[IP].dport
            tcp_flags = pkt[TCP].flags
            dst = pkt[IP].dst
            test = pkt[TCP].payload
        except IndexError as e:
            print(e.args[0])
            return False

        if HTTP.HTTPRequest in pkt:
            print("HTTP Request:")
            # print(test)
            print("=" * 100)

        if HTTP.HTTPResponse in pkt:
            print("HTTP Response:")
            try:
                headers, body = str(test).split("\r\n\r\n", 1)
                print(test)
            except Exception as e:
                print(e)
            print("=" * 100)

    else:
        # print('{} {} -> {}'.format(src, src_port, tcp_flags))
        print('other')

    return True

phone_ip = '192.168.3.2'
_filter = '(host {})'.format(phone_ip)
sniff(iface='bridge100', filter=_filter, prn=lambda pkt: handle_tcp_pkt(pkt))
