# 常见的网络IO模型(多路复用模型)

## select模型原理
select是监听触发机制，监听可读和可写队列。当有事件发生时，进行遍历轮询事件发生的对象然后返回。

比如在服务端启动之后把服务端添加到select的可读监听队列中，当有客户端请求连接服务端时，select函数会返回一个可读事件再让服务端接受客户端的连接。 

select的返回方式可以是阻塞或者是非阻塞，非阻塞式的select处理方式是轮询的，会不断询问占用Cpu太多的资源和时间，所以建议使用阻塞等待返回的方式去使用select

利用select函数，判断套接字上是否存在数据，或者能否向一个套接字写入数据。目的是防止应用程序在套接字处于锁定模式时，调用recv(或send)从没有数据的套接字上接收数据, 被迫进入阻塞状态 

### 优点:
- 没有了多线程的创建、销毁、切换带来的效率和内存上的消耗 

### 缺点: 
- select存在一个最大可监听文件描述符数量，所以会收到最大连接监听的限制 
- select在事件发生以后也是需要遍历监听对象，并不能直接定位到哪个对象，这个操作在对象数量庞大的情况下是个效率的瓶颈。

所以后来有了epoll

select参数和返回值意义如下：
```bash
int select (
 IN int nfds,                           //0,无意义
 IN OUT fd_set* readfds,      //检查可读性
 IN OUT fd_set* writefds,     //检查可写性
 IN OUT fd_set* exceptfds,  //例外数据
 IN const struct timeval* timeout);    //函数的返回时间

struct  timeval {
        long    tv_sec;        //秒
        long    tv_usec;     //毫秒
};
```
select返回fd_set中可用的套接字个数。

fd_set是一个SOCKET队列，以下宏可以对该队列进行操作：
FD_CLR( s, *set) 从队列set删除句柄s;
FD_ISSET( s, *set) 检查句柄s是否存在与队列set中;
FD_SET( s, *set )把句柄s添加到队列set中;
FD_ZERO( *set ) 把set队列初始化成空队列.

### Select工作流程
1: 用FD_ZERO宏来初始化我们感兴趣的fd_set。
也就是select函数的第二三四个参数。

2: 用FD_SET宏来将套接字句柄分配给相应的fd_set。
如果想要检查一个套接字是否有数据需要接收，可以用FD_SET宏把套接接字句柄加入可读性检查队列中

3: 调用select函数。
如果该套接字没有数据需要接收，select函数会把该套接字从可读性检查队列中删除掉，

4: 用FD_ISSET对套接字句柄进行检查。
如果我们所关注的那个套接字句柄仍然在开始分配的那个fd_set里，那么说明马上可以进行相应的IO操 作。比如一个分配给select第一个参数的套接字句柄在select返回后仍然在select第一个参数的fd_set里，那么说明当前数据已经来了， 马上可以读取成功而不会被阻塞。

## poll
select 确实是一个简明好用的模型。可是现在的服务器却越来越少采取这样的模型，原因之一就是它的性能让人担忧。虽然后来升级了poll模型，本质上还是和select模型类似。

## epoll
没错，还有比select/poll模型更好的网络IO模型，就是今天介绍的主角—Epoll。

在很多地方，epoll都是高性能代名词，准确的说epoll是Linux内核升级的多路复用IO模型，在Unix和MacOS上类似的则是 Kqueue。

select的缺点之一就是在网络IO流到来的时候，线程会轮询监控文件数组，并且是线性扫描，还有最大值的限制。相比select，epoll则无需如此。服务器主线程创建了epoll对象，并且注册socket和文件事件即可。当数据抵达的时候，也就是对于事件发生，则会调用此前注册的那个io文件。

epoll例子
```python
import socket
import select
 
EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
response = b'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
response += b'Content-Type: text/plain\r\nContent-Length: 13\r\n\r\n'
response += b'Hello, world!'
 
# 创建套接字对象并绑定监听端口
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', 8080))
serversocket.listen(1)
serversocket.setblocking(0)
 
# 创建epoll对象，并注册socket对象的 epoll可读事件
epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN)
 
try:
    connections = {}
    requests = {}
    responses = {}
    while True:
        # 主循环，epoll的系统调用，一旦有网络IO事件发生，poll调用返回。这是和select系统调用的关键区别
        events = epoll.poll(1)
        # 通过事件通知获得监听的文件描述符，进而处理
        for fileno, event in events:
            # 注册监听的socket对象可读，获取连接，并注册连接的可读事件
            if fileno == serversocket.fileno():
                connection, address = serversocket.accept()
                connection.setblocking(0)
                epoll.register(connection.fileno(), select.EPOLLIN)
                connections[connection.fileno()] = connection
                requests[connection.fileno()] = b''
                responses[connection.fileno()] = response
            elif event & select.EPOLLIN:
                # 连接对象可读，处理客户端发生的信息，并注册连接对象可写
                requests[fileno] += connections[fileno].recv(1024)
                if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
                    epoll.modify(fileno, select.EPOLLOUT)
                    print('-' * 40 + '\n' + requests[fileno].decode()[:-2])
            elif event & select.EPOLLOUT:
                # 连接对象可写事件发生，发送数据到客户端
                byteswritten = connections[fileno].send(responses[fileno])
                responses[fileno] = responses[fileno][byteswritten:]
                if len(responses[fileno]) == 0:
                    epoll.modify(fileno, 0)
                    connections[fileno].shutdown(socket.SHUT_RDWR)
            elif event & select.EPOLLHUP:
                epoll.unregister(fileno)
                connections[fileno].close()
                del connections[fileno]
finally:
    epoll.unregister(serversocket.fileno())
    epoll.close()
    serversocket.close()
```
可见epoll使用也很简单，并没有过多复杂的逻辑，当然主要是在系统层面封装的好。

### epoll与tornado
既然epoll是一种高性能的网络io模型，很多web框架也采取epoll模型。大名鼎鼎tornado是python框架中一个高性能的异步框架，其底层也是来者epoll的IO模型。
当然，tornado是跨平台的，因此他的网络io，在linux下是epoll，unix下则是kqueue。

幸好tornado都做了封装，对于开发者及其友好，下面看一个tornado写的回显例子。
```python
import errno
import functools
import tornado.ioloop
import socket
 
def handle_connection(connection, address):
    """ 处理请求，返回数据给客户端 """
    data = connection.recv(2014)
    print(data)
    connection.send(data)
 
def connection_ready(sock, fd, events):
    """ 事件回调函数，主要用于socket可读事件，用于获取socket的链接 """
    while True:
        try:
            connection, address = sock.accept()
        except socket.error as e:
            if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                raise
            return
        connection.setblocking(0)
        handle_connection(connection, address)
 
if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    sock.bind(("", 5000))
    sock.listen(128)
    # 使用tornado封装好的epoll接口，即IOLoop对象
    io_loop = tornado.ioloop.IOLoop.current()
    callback = functools.partial(connection_ready, sock)
    # io_loop对象注册网络io文件描述符和回调函数与io事件的绑定
    io_loop.add_handler(sock.fileno(), callback, io_loop.READ)
    io_loop.start()
```