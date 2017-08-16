import socket

from multiprocessing import Process


# 指明服务器的端口号
PORT = 9000

# 创建socket套接字对象，用于进行通讯
# socket.SOCK_STREAM 指明使用tcp传输层协议，流式协议
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 为socket对象添加reuseaddr选项，保证程序重新启动的时候可以使用相同端口号
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 为服务器端绑定一个固定的地址
address = ("", PORT)
server_sock.bind(address)

# 让服务器开启监听，意思是让服务器能够接收到客户端发送过来的连接请求
# listen参数的意思指明监听队列的容器有多大
# 监听队列中保存的是还未完成三次握手的客户端信息
server_sock.listen(128)
print("服务器已开启监听")


def handle_client(c_sock, c_addr):
    """子进程处理客户端的逻辑"""
    # 这个while循环表示跟同一个客户端循环多次进行数据传输
    while True:
        # 通过跟客户端通讯对应的socket，接收数据
        # 如果客户端先关闭了连接，recv方法也会返回，但是返回的数据是空数据，或者说数据的长度为0
        recv_data = c_sock.recv(1024)

        if recv_data:
            # 表示recv_data不是空数据，即客户端没有关闭连接，而是发送过来的数据
            print("接收到了客户端 %s 传来的数据 %s" % (c_addr, recv_data.decode()))

            # 使用send方法向客户端发送数据， bytes类型
            c_sock.send(recv_data)

        else:
            # 表示recv_data是空数据，即客户端已经主动关闭了连接，
            print("客户端 %s 已经关闭了连接" % (c_addr,))
            # 如果不想发送数据给客户端，可以关闭socket，表示关闭了与客户端的tcp连接
            c_sock.close()
            break


# 表示让服务器可以在处理完一个客户端之后，能够再接收新的客户端的连接请求，并与新的客户端进行数据传输
while True:
    # 接收客户端的连接请求，与客户端完成三次握手
    # 默认是阻塞的，意思是如果监听队列中没有客户端发起的连接请求，则阻塞等待，直到有客户端连接
    # accept()方法有两个返回值
    # client_sock 是用来跟客户端进行一对一通讯用的socket对象
    # client_addr 表示接受了连接请求的客户端的地址信息（客户端ip和端口）元祖
    client_sock, client_addr = server_sock.accept()

    print("客户端 %s 已连接" % (client_addr, ))
    # print("客户端 %s 已连接" % str(client_addr))

    # 创建一个子进程，由子进程负责数据传输
    p = Process(target=handle_client, args=(client_sock, client_addr))
    p.start()

    # 因为负责与客户端通信使用的client_sock是由子进程使用维护，所以主进程中持有的client_sock没有利用价值
    # 主进程中可以通过close方式，释放这个资源
    client_sock.close()



