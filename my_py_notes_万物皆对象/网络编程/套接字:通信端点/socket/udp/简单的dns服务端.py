# coding = utf-8

'''
@author = super_fazai
@File    : 简单的dns服务端.py
@Time    : 2017/8/11 10:52
@connect : superonesfazai@gmail.com
'''

import socket

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_addr = ('', 8053)
server_sock.bind(server_addr)

# 用来存放域名与ip对应关系的字典
domain_ip = {
    "www.itcast.cn": "192.168.1.2",
    "www.itheima.com": "192.168.1.3",
    "www.google.com": "192.168.1.4",
}

while True:
    # 接收用户要查询的域名
    receive_data, client_addr = server_sock.recvfrom(1024)
    domain = receive_data.decode("utf-8")
    print(client_addr, ": ", domain)
    # 从字典中获取对应域名的ip地址
    # get()的第二个参数表示如果键值不存在, 则返回第二个参数
    ip = domain_ip.get(domain, "i do not know")
    # 将ip地址返回给客户端
    server_sock.sendto(ip.encode("utf-8"), client_addr)