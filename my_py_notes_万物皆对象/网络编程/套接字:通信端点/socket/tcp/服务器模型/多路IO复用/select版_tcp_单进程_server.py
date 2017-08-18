# coding = utf-8

'''
@author = super_fazai
@File    : tcp_单进程服务器_select版.py
@Time    : 2017/8/18 09:08
@connect : superonesfazai@gmail.com
'''

"""
select 原理:
    在多路复用的模型中,比较常用的有select模型和epoll模型. 这两个都是系统接口,由操作系统提供. 当然,Python的select模块进行了更高级的封装.
    将需要判断有数据传来的(可读的)socket,可以向外发送数据的(可写的)socket及发生异常状态的socket交给select,select会帮助我们从中遍历找出有事件发生的socket,并返回给我们,我们可以直接处理这些发生事件的socket.
"""

'''
下面演示的是select回显服务器
'''

import queue
import socket
import select

listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serv_addr = ('', 8080)
listen_sock.bind(serv_addr)

listen_sock.listen(128)

# 在该list中保存, 让select进行判断是否能recv/accept 数据的套接字, 而不会阻塞
input_list = [listen_sock]

# 在该list中保存, 让select进行判断是否能发送数据的套接字
output_list = []

'''
# 消息容器队列
{
    "client1_sock":queue(msg1, msg2),
    "clietn2_sock":...
}
'''
message_queue = {}

while True:
    # 将input_list 与 output_list交给select进行遍历监视
    # 返回的recv_sock_list 中保存了能够立即接收数据的socket
    # 返回的send_sock_list 中保存了能够立即发送数据的socket
    recv_sock_list, send_sock_list, exception_sock_list = \
        select.select(input_list, output_list, [])

    # 遍历处理可以进行 recv 和 accept 的套接字列表recv_sock_list
    for sock in recv_sock_list:
        if sock is listen_sock:     # 如果是监听的socket(未建立连接的socket, 先建立连接, 然后添加到input_list, 并创建一个消息队列)
            client_sock, client_addr = sock.accept()
            print("客户端%s进行了连接" % str(client_addr))
            input_list.append(client_sock)      # 将对接该客户端的socket添加到input_list的任务中，让select判断什么时候有数据出来
            # 创建跟该客户端对应的队列，用于保存对应该客户端socket可能发送的数据
            message_queue[client_sock] = queue.Queue()
        else:   # 如果不是监听的socket, 而是新添加到input_list中刚建立好连接能够用于与客户端进行数据传输的socket
            recv_data = sock.recv(1024)
            if recv_data:
                print("客户端传来数据: %s" % recv_data.decode())
                # 因为send操作默认会阻塞，所以现将socket放到监视的队列中(output_list),由select来监视什么时候能够发送数据
                output_list.append(sock)
                # 将要发送的数据先保存到message_queue中
                message_queue[sock].put(recv_data)
            else:
                # 客户端关闭连接
                # 清除掉与该客户端对应的消息容器
                del message_queue[sock]
                # 从input_list中移除掉该关闭的socket
                input_list.remove(sock)
                if sock in output_list:   # 如果在output_list中也存在该socket，则也将其移除
                    output_list.remove(sock)
                sock.close()    # 关闭服务端与客户端通信的套接字
                print("客户端关闭了连接")

    # 遍历处理返回的可以发送数据的套接字列表
    for sock in send_sock_list:
        # 如果与套接字对应的消息队列中的数据不为空, 则取 消息数据
        if not message_queue[sock].empty():
            msg = message_queue[sock].get()
            # 向客户端发送数据
            sock.send(msg)
        else:
            # 如果消息队列中的数据为空，则表示数据已经发送完成，将sock从需要监视的output_list移除
            output_list.remove(sock)

"""
总结:
    1. 优点
        select目前几乎在所有的平台上支持，其良好跨平台支持也是它的一个优点。
    2. 缺点
        select的一个缺点在于单个进程能够监视的文件描述符的数量存在最大限制,
        在Linux上一般为1024, 可以通过修改宏定义甚至重新编译内核的方式提升这一限制,
        但是这样也会造成效率的降低。
        一般来说这个数目和系统内存关系很大,具体数目可以cat /proc/sys/fs/file-max察看。32位机默认是1024个。64位机默认是2048.
        对socket进行扫描时是依次扫描的，即采用轮询的方法，效率较低。
        当套接字比较多的时候，每次select()都要通过遍历FD_SETSIZE个Socket来完成调度，不管哪个Socket是活跃的，都遍历一遍。这会浪费很多CPU时间。
"""