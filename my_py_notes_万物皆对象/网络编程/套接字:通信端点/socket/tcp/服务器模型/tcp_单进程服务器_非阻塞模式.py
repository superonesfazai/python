# coding = utf-8

'''
@author = super_fazai
@File    : tcp_单进程服务器_非阻塞模式.py
@Time    : 2017/8/18 09:01
@connect : superonesfazai@gmail.com
'''

"""
原理: 通过对服务器的每个socket 连接都改为非阻塞, 并将每个已连接的客户端的socket和addr用list保存
    然后通过循环遍历list, 进行处理每个客户端, 从而实现单进程, 同时实现多处理多个客户端
"""

import socket

# 用来存储所有的新连接的客户端的socket与addr
client_list = []

'''
[(client_socket, client_addr),
 (client_socket, client_addr),
 ...
]
'''

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    address = ('', 8000)
    server_sock.bind(address)
    server_sock.listen(128)

    # 将套接字设置为非堵塞
    # 设置为非堵塞后,如果accept时,恰巧没有客户端connect,那么accept会产生一个异常,所以需要try来进行处理
    server_sock.setblocking(False)

    while True:
        try:
            # 注意: client_info = (client_sock, client_addr)
            # 如果有客户端连接,则返回2个正常值
            client_info = server_sock.accept()
        except BlockingIOError:     # 表示没有客户端发起连接
            pass
        else:         # 表示有客户端发起来连接, 并完成了3次握手, 连接已建立好
            print("客户端%s 已连接" % str(client_info))
            client_info[0].setblocking(False)   # 将套接字设置为非堵塞
            client_list.append(client_info)     # 添加这个成功连接的客户端到list, 等待处理

        # 用来存储需要删除的客户端信息(即记录已关闭连接的客户端)
        need_del_client_info_list = []

        for client_socket, client_addr in client_list:
            try:
                recv_data = client_socket.recv(1024)
                if len(recv_data) > 0:
                    print('recv[%s]:%s' % (str(client_addr), recv_data.decode()))
                else:
                    print('[%s]客户端已经关闭' % str(client_addr))
                    client_socket.close()
                    need_del_client_info_list.append((client_socket, client_addr))
            except BlockingIOError:
                pass

        for client in need_del_client_info_list:    # 单独删除处理, 避免边遍历边循环时出错
            client_list.remove(client)

if __name__ == '__main__':
    main()