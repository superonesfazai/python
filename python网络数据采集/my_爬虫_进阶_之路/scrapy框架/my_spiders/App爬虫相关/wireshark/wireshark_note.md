# wireshark抓包ios(世界清静了!!)
- $ sudo wireshark
- wifi
    - 用mac连接有线，在“设置”中选择“共享”，共享wifi给手机
- usb 
    - 安装xcode
    - 查看iphone uuid, 使用itunes
    - 创建一个Remote Virtual Interface(RVI、远程虚拟接口), 这个接口就代表iOS设备的网络栈了，对这个接口抓包即可
    - $ rvictl -s [your_iphone的uuid] (即可在电脑上监听所有的iphone网络通信)
    - 查询新创建好的rvi接口，一般是rvi0
    - 不需要使用之后，要把这个接口去掉 $ rvictl -x [uuid]

## tcp包分析
1. TCP数据包中，seq表示这个包的序号，注意，这个序号不是按1递增的，而是按tcp包内数据字节长度加上，如包内数据是21字节，而当前IP1发到IP2的包的seq是10的话，那下个IP1发到IP2的包的seq就是10+21=31
2. 每个tcp包都带有win、ack，这些是告诉对方，我还可以接收数据的滑动窗口是多少，如果A发到B的包的win为0，就是A告诉B说我现在滑动窗口为0了，饱了，你不要再发给我了，就说明A端环境有压力（如带宽满了等）
3. ack可以理解为应答。A发给B的ack是告诉B，我已收到你发的数据包，收到ack号这里了，你下次要发seq为ack号的给我
4. 在网络不堵即滑动窗口一点都不堵的情况下，第一个包的ack号就是第二个包的seq号，如果堵了，由于是滑动窗口缓存处理队列，所以这个值会错开
5. 注意我们分析tcp包时，要以一个会话做为一个完整对象，即通讯只发生在两个IP之间，两个固定的端口之间，如果端口变化了，那链接就不是同一条了，不同的链接之间的seq是没有关联的

#### tcp三次握手
比较重要的TCP三次握手问题，首先按下面方法（edit——find packet）查找到请求连接的包，（捕获的包少的话，直接观察查找就行）
```bash
# 手机被监听的ip
ip.addr == 192.168.3.2 && tcp.flags.syn == 1        
# 第一次握手：序号：seq=0；无确认号；ACK=0（not set）;SYN=1
# 第二次握手：序号：seq=0；确认号：ack=1；ACK=1;SYN=1
# 第三次握手：序号：seq=1；确认号：ack=1；ACK=1；SYN=0（not set）
```

## dns报文
dns有两条报文, 一条是query报文, 一条是response报文

## wireshark相关
在Wireshark中关于数据包的叫法有三个术语，分别是帧、包、段。
- Frame：物理层的数据帧概况。
- Ethernet II：数据链路层以太网帧头部信息。
- Internet Protocol Version 4：互联网层IP包头部信息。
- Transmission Control Protocol：传输层的数据段头部信息，此处是TCP协议。
- Hypertext Transfer Protocol：应用层的信息，此处是HTTP协议

(1)物理层的数据帧概况
```
    Frame 5: 268 bytes on wire (2144 bits), 268 bytes captured (2144 bits) on interface 0               #5号帧，线路268字节，实际捕获268字节
    Interface id: 0                                                     #接口id
    Encapsulation type: Ethernet (1)                                    #封装类型
    Arrival Time: Jun 11, 2015 05:12:18.469086000 中国标准时间            #捕获日期和时间
    [Time shift for this packet: 0.000000000 seconds]
    Epoch Time: 1402449138.469086000 seconds
    [Time delta from previous captured frame: 0.025257000 seconds]      #此包与前一包的时间间隔
    [Time since reference or first frame: 0.537138000 seconds]          #此包与第一帧的时间间隔
    Frame Number: 5                                                     #帧序号
    Frame Length: 268 bytes (2144 bits)                                 #帧长度
    Capture Length: 268 bytes (2144 bits)                               #捕获长度
    [Frame is marked: False]                                            #此帧是否做了标记：否
    [Frame is ignored: False]                                           #此帧是否被忽略：否
    [Protocols in frame: eth:ip:tcp:http]                               #帧内封装的协议层次结构
    [Number of per-protocol-data: 2]                                    
    [Hypertext Transfer Protocol, key 0]
    [Transmission Control Protocol, key 0]
    [Coloring Rule Name: HTTP]                                          #着色标记的协议名称
[Coloring Rule String: http || tcp.port == 80]                          #着色规则显示的字符串
```
(2)数据链路层以太网帧头部信息
```
    Ethernet II, Src: Giga-Byt_c8:4c:89 (1c:6f:65:c8:4c:89), Dst: Tp-LinkT_f9:3c:c0 (6c:e8:73:f9:3c:c0)
    Destination: Tp-LinkT_f9:3c:c0 (6c:e8:73:f9:3c:c0)                                   #目标MAC地址
    Source: Giga-Byt_c8:4c:89 (1c:6f:65:c8:4c:89)                                        #源MAC地址
    Type: IP (0x0800)
```
(3)互联网层IP包头部信息
```
    Internet Protocol Version 4, Src: 192.168.0.104 (192.168.0.104), Dst: 61.182.140.146 (61.182.140.146)
    Version: 4                                                                                                                          #互联网协议IPv4
    Header length: 20 bytes                                                                               #IP包头部长度
    Differentiated Services Field: 0x00 (DSCP 0x00: Default; ECN: 0x00: Not-ECT (Not ECN-Capable Transport))                                                                                                                                   #差分服务字段
    Total Length: 254                                                                                     #IP包的总长度
    Identification: 0x5bb5 (23477)                                                                        #标志字段
    Flags: 0x02 (Don't Fragment)                                                                          #标记字段
    Fragment offset: 0                                                                                    #分的偏移量
    Time to live: 64                                                                                      #生存期TTL
    Protocol: TCP (6)                                                                                     #此包内封装的上层协议为TCP
    Header checksum: 0x52ec [validation disabled]                                                         #头部数据的校验和
    Source: 192.168.0.104 (192.168.0.104)                                                                 #源IP地址
    Destination: 61.182.140.146 (61.182.140.146)                                                          #目标IP地址
```
（4）传输层TCP数据段头部信息
```
    Transmission Control Protocol, Src Port: 51833 (51833), Dst Port: http (80), Seq: 1, Ack: 1, Len: 214
    Source port: 51833 (51833)                                                                                 #源端口号
    Destination port: http (80)                                                                             #目标端口号
    Sequence number: 1    (relative sequence number)                                   #序列号（相对序列号）
    [Next sequence number: 215    (relative sequence number)]           #下一个序列号
    Acknowledgment number: 1    (relative ack number)                         #确认序列号
    Header length: 20 bytes                                                                               #头部长度
    Flags: 0x018 (PSH, ACK)                                                                             #TCP标记字段
    Window size value: 64800                                                                                    #流量控制的窗口大小
    Checksum: 0x677e [validation disabled]                                                  #TCP数据段的校验和
```