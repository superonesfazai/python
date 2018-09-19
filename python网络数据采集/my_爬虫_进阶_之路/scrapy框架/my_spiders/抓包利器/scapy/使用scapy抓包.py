# coding:utf-8

'''
@author = super_fazai
@File    : 使用scapy抓包.py
@connect : superonesfazai@gmail.com
'''

"""
抓包mac
"""

from scapy.all import (
    sniff,
    TCP,
    UDP,
    Ether,
    DNS,
    IP,
    ls,
    wrpcap,
    rdpcap,
)

# 抓包
pcap = sniff(iface='en0', count = 50)
print(str(pcap))        # <Sniffed: TCP:44 UDP:4 ICMP:0 Other:2> 总共抓获44个tcp, 4个udp

'''
数据包的结构:
    scapy的包是按照 TCP/IP 四层参考模型，即：链路层，网络层，传输层，应用层
而我也可以直接只获取指定层的数据
'''
try:
    # 获取抓包到的数据包
    # 类似访问 list 的方式直接通过序号访问数据包
    print(str(pcap[1]))
    print(pcap[1].show())

    # 通过指定 TCP/UDP 等数据包类型来访问指定协议的数据包
    print(str(pcap[UDP][1]))
    print(pcap[UDP][1].show())
    print('-' * 20)

    print(pcap[UDP][1][Ether])
    print(pcap[UDP][1][Ether].dst)      # eg: 98:10:e8:ef:a3:f7

    print(pcap[UDP][1][IP])
    print(pcap[UDP][1][IP].dst)         # eg: '192.168.199.1'

    print(pcap[UDP][1][UDP])
    print(pcap[UDP][1][UDP].dport)      # eg: 1900

    print(pcap[UDP][1][DNS])
    print(pcap[UDP][1][DNS].qd)         # eg: b'\rzb-center-acs\x01m\x06taobao\x03com\x03gds\nalibabadns\x03com\x00\x00\x01\x00\x01'
    print(pcap[UDP][1][DNS].qd.qname)   # eg: b'zb-center-acs.m.taobao.com.gds.alibabadns.com.'
except Exception as e:
    print('遇到错误: ', e, end='\n跳过!')

# 我们可以在ipython 中 使用ls(xxx)进行查看
# print(ls(TCP))
# print(ls(UDP))
# print(ls(Ether))
# print(ls(DNS))

# 包捕获后的存储为pcap格式的文件
wrpcap('./tmp.pcap', pcap)

# 下次重新使用数据包
# pcap_saved = sniff(offline='demo.pcap')
# 或者
# pcap_saved = rdpcap('demo.pcap')

'''过滤'''
# 如果我们想抓指定类型的数据包，就需要使用 filter 进行过滤
# 而 filter 使用的是 Berkeley Packet Filter (BPF)语法
# 也就是我们在 wireshark 中可以使用的过滤语法，如果你不清楚，可以参看这篇文章(https://gist.github.com/Akagi201/10230435)

# 在进行抓包过滤前，我们先来看结合 prn 参数输出抓取到的数据包，并使用 sprintf() 函数进行格式化输出的
tmp = sniff(prn=lambda x:x.sprintf("{IP:%IP.src% -> %IP.dst%\n}{Raw:%Raw.load%\n}"))
# print(tmp)
tmp2 = sniff(prn=lambda x: x.summary())
# print(tmp2)

'''结合上面的格式化输出演示如何抓取指定类型的数据包'''
# 比如我们想抓取 ICMP 数据包
icmp = sniff(filter="icmp", count=4, prn=lambda x:x.sprintf("{IP:%IP.src% -> %IP.dst%\n}{Raw:%Raw.load%\n}"))
# print(icmp)
