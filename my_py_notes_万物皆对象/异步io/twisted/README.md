# Twisted
Twisted是一个基于事件驱动的网络框架 

Twisted支持所有主要系统事件循环 - select（所有平台），poll（大多数POSIX平台），epoll（Linux），kqueue（FreeBSD，macOS），IOCP（Windows）和各种GUI事件循环（GTK + 2/3，Qt，wxWidgets ）。第三方反应堆可插入Twisted，并为其他事件循环提供支持。

Twisted协议以异步方式处理数据。当协议从网络到达时，协议响应事件，并且事件作为对协议上的方法的调用而到达。

Twisted协议以异步方式处理数据。这意味着协议永远不会等待事件，而是响应从网络到达的事件。

- twisted.web：HTTP客户端和服务器，HTML模板和WSGI服务器
- twisted.conch：SSHv2和Telnet客户端以及服务器和终端仿真程序
- twisted.words：IRC，XMPP和其他IM协议的客户端和服务器
- twisted.mail：IMAPv4，POP3，SMTP客户端和服务器
- twisted.positioning：用于与NMEA兼容的GPS接收器通信的工具
- twisted.names：DNS客户端和用于制作自己的DNS服务器的工具
- twisted.trial：一个单元测试框架，可以很好地与基于Twisted的代码集成。

[Docs](https://twistedmatrix.com/documents/current/)

[github](https://github.com/twisted/twisted)

## 安装
```bash
$ pip3 install twisted
```

## 主要内容
twisted的核心部分是deferred，主要内容如下：

1. 讲解了单线程，异步和多线程怎样解决IO问题的缺点和优点。
2. 讲解了阻塞客服端，和非阻塞客服端的实现，引入了reactor
3. reactor的基本操作
4. 使用twisted改写异步客服端，手动控制异步Reader（说明如果在Reader中同步调用的话，reactor没有优势）
5. 抽象出Transports,Protocols,Protocol Factories并手动管理异步操作结果。
6. 引入callback, errback机制
7. 引入Deferred，异步操作和同步操作对比，deferred调用栈.
8. 修改客服端
9. 深入Deferred讨论了同步调用栈， 异步调用栈。划分Deffered的层次调用，层次间的交错调用。
10. 修改客服端
11. 修改服务器
12. 实现服务器和客户端的双向通信
13. 在Deferred中加入了Deferred实现异步中异步
14. 引入了proxy服务器， 在proxy中决定是否引入Deferred。
15. 测试
16. 编写服务
17. 引入了yield,inlineCallbacks,原先需要以异步的异步编写变成了写个单独的函数即可。
18. 引入了DeferredList，这样就可以控制一组Deferred了。
19. 加入了cancel Deferred. 可以异步取消掉一个操作
20. reactor中的大循环然后转化为每个Protocols小循环。从而引入了Erlang.
21. 从函数语言Haskell的惰性来简化了异步操作。

