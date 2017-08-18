# coding = utf-8

'''
@author = super_fazai
@File    : tcp_单进程服务器_epoll版.py
@Time    : 2017/8/18 09:15
@connect : superonesfazai@gmail.com
'''

# 无法运行, 平台限制

"""
epoll的优点：
    1. 没有最大并发连接的限制，能打开的FD(指的是文件描述符，通俗的理解就是套接字对应的数字编号)的上限远大于1024
    2. 效率提升,不是轮询的方式,不会随着FD数目的增加效率下降.只有活跃可用的FD才会调用callback函数;
       即epoll最大的优点就在于它只管你“活跃”的连接，而跟连接总数无关，
       因此在实际的网络环境中，epoll的效率就会远远高于select。
"""

import socket
import select
import queue

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", 8080))
s.listen(128)

# 创建一个epoll对象(或者理解为一个epoll容器)
epoll = select.epoll()

# 向epoll中添加需要epoll进行监视管理的socket（通过socket文件编号--fileno()的返回值--进行注册）
# EPOLLIN表示要进行input监控，即监视什么时候能够执行recv或者accept操作
epoll.register(s.fileno(), select.EPOLLIN)

# 用来保存文件编号与socket对应的关系
client_socks = {}
# 用来保存文件编号与客户端地址的对应关系
client_addrs = {}
# 用来保存要发送给客户端的消息数据
msg_queue = {}

while True:
    # 询问epoll有无可以操作的socket，返回的epoll_list中包含可以进行处理的socket对应的文件编号
    epoll_list = epoll.poll()

    # 遍历能够处理的socket文件编号列表，依次进行处理
    # fd表示文件的编号
    # events表示是可以进行读取recv/accept操作还是可以进行写send操作
    for fd, events in epoll_list:
        # 如果是监听的socket文件
        if fd == s.fileno():
            # 接收客户端的请求
            conn, addr = s.accept()
            # 将连接的客户端的socket与地址保存
            client_socks[conn.fileno()] = conn
            client_addrs[conn.fileno()] = addr
            # 创建对应 该客户端的发送消息的队列
            msg_queue[conn.fileno()] = queue.Queue()
            print("%s已连接" % str(addr))
            # 将新的客户端的socket添加到epoll中进行监视管理
            epoll.register(conn.fileno(), select.EPOLLIN)

        elif events == select.EPOLLIN:  # 如果是可以进行读取数据accept/recv的套接字
            recv_data = client_socks[fd].recv(1024)
            if recv_data:
                print("%s传来数据%s" % (str(client_addrs[fd]), recv_data.decode()))
                # 将要发送给客户端的数据放到消息队列中
                msg_queue[fd].put(recv_data)
                # 将这个与客户端进行通信的socket在epoll中的监视行为改为监视可否发送数据
                epoll.modify(fd, select.EPOLLOUT)
            else:
                # 客户端关闭了连接
                print("%s已关闭" % str(client_addrs[fd]))
                epoll.unregister(fd)    # 将socket从epoll中删除
                # 删除与该socket对应的消息队列
                del msg_queue[fd]
                # 关闭该socket
                client_socks[fd].close()
                # 删除socket在cliet_socks和client_addrs中保存的数据
                del client_socks[fd]
                del client_addrs[fd]
                # 如果是可以进行发送数据send的套接字
        elif events == select.EPOLLOUT:
            # 消息队列中不为空，就取出数据发送
            if not msg_queue[fd].empty():
                msg = msg_queue[fd].get()
                client_socks[fd].send(msg)
            # 没有消息数据了，就将对该socket的监视行为改为监视是否有数据从客户端发送过来
            else:
                epoll.modify(fd, select.EPOLLIN)

"""
说明
    * 平台的限制(Linux2.6即以上才实现了epoll机制, unix也不行, windows也不行)
    EPOLLIN （可读）
    EPOLLOUT （可写）
    EPOLLET （ET模式）
    epoll对文件描述符的操作有两种模式：LT（level trigger）和ET（edge trigger）。LT模式是默认模式，LT模式与ET模式的区别如下：
    
    LT模式：当epoll检测到描述符事件发生并将此事件通知应用程序，应用程序可以不立即处理该事件。下次调用epoll时，会再次响应应用程序并通知此事件。
    
    ET模式：当epoll检测到描述符事件发生并将此事件通知应用程序，应用程序必须立即处理该事件。如果不处理，下次调用epoll时，不会再次响应应用程序并通知此事件。
"""