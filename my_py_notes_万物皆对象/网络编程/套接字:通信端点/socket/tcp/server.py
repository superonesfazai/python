# encoding: utf-8

if __name__ == '__main__':
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 8001))
    sock.listen(5)
    while True:
        # 使用accept方法接收客户端的连接请求
        # 如果有新的客户端来连接服务器，那么就产生一个新的套接字专门为这个客户端服务
        # connection用来为这个客户端服务，与客户端形成一对一的连接
        # 而sock就可以省下来专门等待其他新客户端的连接请求
        # address是请求连接的客户端的地址信息，为元祖，包含用户的IP和端口
        connection, address = sock.accept()
        try:
            connection.settimeout(5)
            buf = connection.recv(1024)
            if buf == '1':
                connection.send('welcome to server!')
            else:
                connection.send('please go out!')
        except socket.timeout:
            print('time out')
        # 关闭与客户端连接的socket
        # 只要关闭了，就意味着为不能再为这个客户端服务了，如果还需要服务，只能再次重新连接
        connection.close()
    # 关闭服务端的监听socket
    # 要这个套接字关闭了，就意味着整个程序不能再接收任何新的客户端的连接
    # sock.close()
