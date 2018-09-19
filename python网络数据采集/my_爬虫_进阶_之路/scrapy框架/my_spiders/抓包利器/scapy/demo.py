# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

from scapy.all import (
    IP,
    TCP,
    sr1,
    conf,
    RastaTheme,
    sniff,
    srloop,
)

# 配置保存在名为conf的变量中, 该变量保存在会话中
conf.verb = 0
conf.color_theme=RastaTheme()
# print(conf)

# 实现一个ip层
a = IP(dst="172.16.1.40")
print(str(a))

p = IP(dst="github.com")/TCP()
r = sr1(p)
print(r.summary())

# 我们可以轻松捕获一些数据包甚至克隆tcpdump或tethereal
# 如果没有给出接口，则会在每个接口上进行嗅探
# a = sniff(filter="icmp and host 119.75.216.20", count=2)
# a.nsummary()
# print(a[1])

# 以下是类似ping的函数的示例：您始终发送相同的数据包集以查看是否存在更改
# print(srloop(IP(dst='www.baidu.com')/TCP()))
