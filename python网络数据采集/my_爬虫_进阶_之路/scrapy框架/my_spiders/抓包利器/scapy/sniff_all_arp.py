# coding:utf-8

'''
@author = super_fazai
@File    : sniff_all_arp.py
@connect : superonesfazai@gmail.com
'''

"""
监控en0所有arp请求
"""

from scapy.all import (
    ARP,
    sniff
)

def arp_monitor_callback(pkt):
    '''
    arp监控回调函数
    :param pkt:
    :return:
    '''
    if ARP in pkt and pkt[ARP].op in (1, 2): # who-has or is-at
        return pkt.sprintf('%ARP.hwsrc% %ARP.psrc%')

# store = 0 以避免将所有的数据包存储在内存中
sniff(iface='en0', filter='arp', prn=arp_monitor_callback, store=0)