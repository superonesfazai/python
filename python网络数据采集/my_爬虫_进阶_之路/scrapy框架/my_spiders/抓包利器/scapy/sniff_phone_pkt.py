# coding:utf-8

'''
@author = super_fazai
@File    : sniff_phone_pkt.py
@connect : superonesfazai@gmail.com
'''

"""
嗅探手机数据包
"""

from scapy_http.http import HTTPRequest, HTTPResponse
from scapy.all import (
    sniff,
    Ether,
    ls,
    hexdump,
    IP,
)

from fzutils.sniff_utils import get_hex_res_of_pkt
from fzutils.data.binary_utils import (
    hex_2_str,
    str_2_hex,)

# 指定抓包监视的接口
iface = 'bridge100'
# 抓取数
crawl_count = 300
phone_ip = '192.168.3.2'
# 过滤包
# * 遇到错误(表示过滤器语法错误): tcpdump: syntax error in filter expression: syntax error
# (ip[2:2] >= 606)                              表示仅匹配长度>=606字节的IP数据包
# (portrange 2000-3000)                         表示仅其端口号在2000到3000范围内
# ((tcp[tcpflags] & tcp-ack) != 0)              表示仅匹配ACK数据包
# ((tcp[tcpflags] & tcp-ack) = 0)               表示仅匹配非 -ACK数据包
# src host hostnameA or src host hostnameB      表示仅匹配来自主机hostnameA 或 来自主机的数据包hostnameB
_filter = '(host {}) and (ip[2:2] >= 606) and (tcp)'.format(phone_ip)

# pcap = sniff(iface=iface, count=crawl_count, filter=_filter)
# for i in range(crawl_count):
#     print(pcap[i].show())

def handle_data_packet(pkt):
    '''
    数据包处理
    :param data_packet: 数据包
    :return:
    '''
    print('-' * 100)
    '''获取包命令'''
    # print(pkt.command())
    # print(ls(pkt))

    '''十六进制转储'''
    # # 包原始数据
    try:
        pkt_load = pkt.load
    except AttributeError:
        return False
    # pkt_payload = pkt.payload
    # print(pkt_payload)
    # hex_pkt_load = hexdump(pkt_load)
    # print(hex_pkt_load)

    # 一行输出16进制
    hex_pkt_load = get_hex_res_of_pkt(pkt=pkt)
    # print(hex_pkt_load)
    hex_pkt_load_str = hex_2_str(hex_pkt_load)
    headers = None
    body = hex_pkt_load_str
    try:
        headers, body = hex_pkt_load_str.split(b'\r\n\r\n')
        print('headers: ', headers)
    except Exception:
        pass
    # print(body)
    '''切记: 要存储某个原数据得先删除头部跟尾部'''
    if HTTPRequest in pkt:
        print('HTTP Request:')
        print(hex_pkt_load)
        print(headers)
        print(body)

    elif HTTPResponse in pkt:
        print('HTTP Response:')
        print(hex_pkt_load)
        print(headers)
        print(body)

    else:
        print('other')

    # 下面两行是无实际用途的转码
    # hex_pkt_load_str = hex_2_str(hex_pkt_load).decode('latin-1')
    # print(hex_pkt_load_str)

    '''格式化输出'''
    # ip_src = pkt[IP].src
    # ip_dst = pkt[IP].dst
    # raw_load = pkt.load
    # print('{} -> {}'.format(ip_src, ip_dst))
    # print(raw_load)
    # res = pkt.sprintf("{IP:%IP.src% -> %IP.dst%\n}{Raw:%Raw.load%\n}")
    # print(res)

    # recombine = Ether(pkt)
    # print(str(recombine))

    return True

pcap = sniff(iface=iface, count=crawl_count, filter=_filter, prn=lambda pkt: handle_data_packet(pkt))