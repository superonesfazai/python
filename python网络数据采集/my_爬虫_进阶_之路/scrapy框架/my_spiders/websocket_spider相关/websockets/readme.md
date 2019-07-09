# websockets
websockets是一个用于在Python中构建WebSocket 服务器和客户端的库，重点是正确性和简单性。

它构建于asyncioPython的标准异步I / O框架之上，提供了一个优雅的基于协程的API。

[github](https://github.com/aaugustin/websockets)

[doc](https://websockets.readthedocs.io/en/stable/)

## python环境
python >= 3.4

## 安装
```shell
$ pip3 install websockets
```

## API


## 生命周期
### 状态
WebSocket连接通过一个简单的状态机：
- CONNECTING：初始状态，
- OPEN：当开始握手完成时，
- CLOSING：当结束握手开始时，
- CLOSED：TCP连接关闭时。

过渡发生在以下地方：
- CONNECTING -> OPEN：在 connection_open()其中，当所述运行开口握手完成并且WebSocket连接被建立-不与混淆 connection_made()其中当建立了TCP连接运行;
- OPEN -> CLOSING：在 write_frame()发送关闭帧之前立即; 因为接收一个关闭帧触发发送一个关闭帧，无论哪一方开始收盘握手，这都是正确的 ; 还 fail_connection()复制了几行代码来自write_close_frame（）和write_frame（） ;
- * -> CLOSED：connection_lost()当TCP连接关闭时， 其中始终只调用一次。

### 协同程序
下图显示了客户端连接生命周期的每个阶段正在运行的协同程序。

![](https://websockets.readthedocs.io/en/stable/_images/lifecycle.svg)

服务器端的生命周期是相同的，除了控制的反转使得等效于connect()隐式。

应用程序调用以绿色显示的协同程序。多个协同程序可以同时与WebSocket连接进行交互。

以灰色显示的协同程序管理连接。当打开握手成功时，connection_open()启动两个任务：

- transfer_data_task运行 transfer_data()处理传入数据并recv() 让它消耗它。可以取消它以终止连接。除了以外的例外，它永远不会退出CancelledError。请参阅下面的数据传输
- keepalive_ping_task运行 keepalive_ping()以固定间隔发送Ping帧并确保接收相应的Pong帧。连接终止时取消。除了以外的例外，它永远不会退出CancelledError。
- close_connection_task运行 close_connection()它等待数据传输终止，则需要关闭所述TCP连接的护理。一定不能取消。它永远不会以例外的形式退出。请参阅 下面的连接终止

此外，在打开握手失败时fail_connection()启动相同close_connection_task的操作，以便关闭TCP连接。

拆分两个任务之间的职责可以更容易地保证websockets可以终止连接：

- 在固定的超时内，
- 没有泄漏待处理的任务，
- 没有泄漏开放的TCP连接，

无论连接是正常终止还是异常终止。

transfer_data_task在连接上不再接收数据时完成。在正常情况下，它会在交换闭帧后退出。

close_connection_task TCP连接关闭时完成。

## 打开握手
websockets在建立WebSocket连接时执行打开握手。在客户端，connect()在将协议返回给调用者之前执行它。在服务器端，它在将协议传递给ws_handler处理连接的协程之前执行。

虽然打开握手是不对称的 - 客户端发送HTTP升级请求，服务器回复HTTP切换协议响应 - websockets旨在保持双方的实现彼此一致。

在客户端，handshake()：
- 根据uri传递给的参数 构建HTTP请求connect();
- 将HTTP请求写入网络;
- 从网络读取HTTP响应;
- 检查HTTP响应，验证extensions和subprotocol，并相应地配置协议;
- 搬到OPEN州。

在服务器端，handshake()：
- 从网络读取HTTP请求;
- 调用process_request()可能会中止WebSocket握手并返回HTTP响应; 这个钩子只在服务器端有意义;
- 检查该HTTP请求，协商extensions和subprotocol，并相应地配置协议;
- 根据以上内容和传递给的参数构建HTTP响应 serve();
- 将HTTP响应写入网络;
- 搬到OPEN州;
- 返回path部分uri。

开放握手双方之间最显着的不对称性在于扩展的协商，以及在较小程度上的子协议的协商。服务器知道双方的所有内容，并决定连接的参数。客户只是应用它们。

如果在打开握手期间出现任何问题，websockets 则连接失败。

## 数据传输
### 对称性
一旦打开握手完成，WebSocket协议就进入数据传输阶段。这部分几乎是对称的。服务器和客户端之间只有两个区别：

- 客户端到服务器屏蔽：客户端屏蔽外发帧; 服务器取消屏蔽传入的帧;
- 关闭TCP连接：服务器立即关闭连接; 客户端等待服务器执行此操作。

这些差异非常小，以至于数据成帧， 发送和接收数据以及关闭连接的所有逻辑都在同一个类中实现，WebSocketCommonProtocol。

该is_client属性告诉协议实例正在管理哪一方。此属性在WebSocketServerProtocol和 WebSocketClientProtocol类上定义 。

### 数据流
下图显示了数据如何在构建于顶部的应用程序websockets和远程端点之间流动。无论服务器或客户端是哪一方，它都适用。
![](https://websockets.readthedocs.io/en/stable/_images/protocol.svg)
公共方法以绿色显示，私有方法显示为黄色，缓冲区显示为橙色。省略了与连接终止有关的方法; 连接终止在下面的另一节中讨论。

### 接收数据
图的左侧显示了如何websockets接收数据。

将输入数据写入a StreamReader以实现流控制并在TCP连接上提供背压。

transfer_data_task，在建立WebSocket连接时启动，处理此数据。

当它接收数据帧时，它会重新组合片段并将生成的消息放入messages队列中。

遇到控制框时：

- 如果它是一个接近的框架，它会启动结束握手;
- 如果它是一个ping帧，它用一个乒乓框架回答;
- 如果它是一个乒乓球框架，它会确认相应的ping（除非它是一个未经请求的乒乓球）。

在任务中运行此过程可确保快速处理控制帧。没有这样的任务，websockets将取决于应用程序通过recv()在任何时间只有一个协程等待驱动连接 。虽然这在许多用例中自然发生，但不能依赖它。

然后recv()从messages队列中提取下一条消息，添加一些复杂性以正确处理终止。

### 发送数据
图的右侧显示了如何websockets发送数据。

send()写入包含该消息的单个数据帧。目前不支持碎片。

ping()写一个ping帧并产生一个Future在接收到匹配的pong帧时将完成的帧。

pong() 写一个乒乓球框架。

close() 写一个关闭帧并等待TCP连接终止。

将传出数据写入a StreamWriter以实现流控制并从TCP连接提供背压。

### 结束握手
当连接的另一端启动关闭握手时， read_message()在该OPEN状态下接收关闭帧。它移动到CLOSING状态，发送一个关闭帧，然后返回None，导致 transfer_data_task终止。

当连接的这一侧启动闭合握手时 close()，它将移动到CLOSING 状态并发送一个关闭帧。当另一方发送一个关闭帧时， read_message()在该CLOSING状态下接收它 并返回None，也导致 transfer_data_task终止。

如果另一方未在连接关闭超时内发送关闭帧，则连接websockets 失败。

结束握手可以占用：一个 用于写入关闭帧，另一个用于接收关闭帧。2 * close_timeoutclose_timeoutclose_timeout

然后websockets终止TCP连接。

## 连接终止
close_connection_task，在建立WebSocket连接时启动，负责最终关闭TCP连接。

首先close_connection_task等待transfer_data_task终止，这可能是由于：

- 成功的结束握手：如上所述，这将退出无限循环transfer_data_task;
- 等待结束握手完成时超时：取消 transfer_data_task;
- 协议错误，包括连接错误：取决于异常， transfer_data_task 无法使用合适的代码连接并退出。

close_connection_task是分开的，transfer_data_task以便在结束握手时更容易实现超时。取消 transfer_data_task不会产生取消close_connection_task 和无法关闭TCP连接的风险，从而导致资源泄漏。

然后close_connection_task取消 keepalive_ping。此任务没有协议合规性职责。终止它以避免泄漏是唯一的问题。

终止TCP连接可以在服务器端和客户端进行。客户端从等待服务器关闭连接开始，因此额外 。然后双方将执行以下步骤，直到TCP连接丢失：半关闭连接（仅适用于非TLS连接），关闭连接，中止连接。此时，无论网络上发生什么，连接都会丢失。2 * close_timeout3 * close_timeoutclose_timeout

## 连接失败
如果打开握手未成功完成，websockets则通过关闭TCP连接来使连接失败。

一旦打开握手完成，websockets通过取消transfer_data_task并在适当时发送关闭帧来使连接失败。

transfer_data_task退出，取消阻止 close_connection_task，关闭TCP连接。

## 服务器关闭
WebSocketServer像异步一样关闭 asyncio.Server。关机分两步进行：

1. 停止聆听并接受新的联系;
2. 使用关闭代码1001（离开）关闭已建立的连接，或者，如果打开握手仍在进行中，则使用HTTP状态代码503（服务不可用）关闭已建立的连接。

第一次调用close启动执行此序列的任务。进一步的通话被忽略。这是制作close和 wait_closed幂等的最简单方法。

## 取消
### 用户代码
websockets提供WebSocket应用程序服务器。它管理连接并将它们传递给用户提供的连接处理程序。这是控制场景的反转：库代码调用用户代码。

如果连接断开，则相应的处理程序应终止。如果服务器关闭，则所有连接处理程序都必须终止。取消连接处理程序将终止它们。

但是，为此目的使用取消将需要所有连接处理程序正确处理它。例如，如果连接处理程序启动某些任务，它应该捕获CancelledError，终止或取消这些任务，然后重新引发异常。

在asyncio应用程序中取消是很棘手的，特别是当它与终结逻辑交互时。在上面的例子中，如果处理程序CancelledError在检测到连接丢失后最终确定它启动的任务时被中断了怎么办？

websockets认为取消只能由协程的调用者触发，因为它不再关心该协程的结果。（资料来源：Guido van Rossum）。由于连接处理程序运行任意用户代码，websockets因此无法确定该代码是否仍在执行值得关注的操作。

出于这些原因，websockets永远不要取消连接处理程序。相反，它希望它们检测连接何时关闭，如果需要则执行终结逻辑，然后退出。

相反，取消不是WebSocket客户端关注的问题，因为它们不涉及控制反转。

## 并发
调用的任意组合recv()， send()， ，或 同时是安全的，包括多次调用相同的方法。close() ping()pong()

如上所示，接收帧独立于发送帧。recv()从发送帧的其他方法中隔离接收帧的帧。

发送帧的方法也支持并发调用。连接打开时，每个帧都通过一次写入发送。结合并发模型asyncio，这将强制执行序列化。连接关闭后，发送帧会上升ConnectionClosed。