# TLS
TLS是以建立在SSL V3.0的基础上，两者的加密算法和MAC算法都不一样，而协议本身差异性不大。

TLS协议也是由两层组成： TLS 记录协议（TLS Record）和 TLS 握手协议（TLS Handshake）。较低的层为 TLS 记录协议。忽略协议的差异性，后面会拿TLS来解密。

一般来说，我们用WireShark来抓取包进行分析是没有多大问题的。但这里有个问题是，如果你碰到的是用SSL/TLS等加密手段加密过的网络数据的时候，往往我们只能束手无策。

在过去的话，如果我们拥有的该传输会话的私钥的话我们还是可以将它提供给WireShark来让其对这些加密数据包进行解密的，但这已经是想当年还用RSA进行网络数据加密的年代的事情了。

当今大家都已经逐渐拥抱前向加密技术PFS 的时代了，所以该方法就不再适用了。因为前向加密技术的目的就是让每个数据交互都使用的是不同的私钥，所以你像以前RSA时代一样想只用一个私钥就能把整个session会话的网络数据包都破解出来的话是不可能的了。

在讲解密之前先来看下HTTPS与HTTP的不同之处，HTTPS是在TCP/IP与HTTP之间，增加一个安全传输层协议，而这个安全传输层协议一般用SSL或TLS，类似于下图。即我们所说的HTTPS=HTTP+SSL/TLS。

![](https://i.loli.net/2019/01/19/5c42939443507.jpg)

为了分析首先要捕获 TLS 流量，考虑到 TLS 流量是加密的，Wireshark 是如何解密这些流量的呢？

为了解密流量，通常有两种方法：

- 在 Wireshark 中配置服务器的私钥，该私钥和证书中包含的公钥是一对密钥。
- 通过 WSSLKEYLOGFILE 方式。(推荐)

使用第一种方法解密 TLS 流量的原因很简单，但有局限性。对于 RSA 密钥协商算法，通过私钥 Wireshark 能够解密会话密钥（Master Secret），从而能够解密 TLS 流量；而对于 DH 密钥协商算法（支持前向安全的密码套件），服务器的私钥并不是用于协商会话密钥的，而就是说会话密钥由客户端和服务器内部运算出来的，通过分析纯粹的 TLS 流量，Wireshark 是无法获取获取会话密钥的，从而也就无法解密 TLS 流量。

而第二种方法能够比较完美的解密 TLS 流量，WSSLKEYLOGFILE 是 Mozilla 的 NSS 底层密码库提出的一种技术，所有基于 NSS 的应用程序在运行期间可以将通信过程中的会话密钥导出到一个文件中，一旦有了这个密码文件，Wireshark 就能够解密所有的 TLS 流量了。

现在 OpenSSL 等其他的 TLS 实现也能支持这种方式，通过 Chrome 和 Firefox 浏览器捕获 TLS 流量，Wireshark 就能够解密了。

那么如何配置 WSSLKEYLOGFILE 呢？主要包含两个步骤：

- 设置环境变量 WSSLKEYLOGFILE（在 Windows 中设置非常简单），定义一个文件目录（Chrome 和 Firefox 浏览器就是将会话密钥导入到这个文件中），比如文件是 c:\ssl.log。

- 在 Wireshark 中打开【编辑】-【首选项】-【Protocols】->【SSL】，然后设置 【Pre-Master-Secret log filename】，具体见下图。

## TLS协议原理
![](https://i.loli.net/2019/01/19/5c42a15668ce1.png)

## TLS的握手
整个握手阶段如下，可分为5步：

第1步，浏览器给出协议版本号、一个客户端生成的随机数，以及客户端支持的加密方法。

第2步，服务器确认双方使用的加密方法，使用的tls版本号和一个随机数。

第3步，并给出数字证书、以及一个服务器运行Diffie-Hellman算法生成的参数，比如pubkey。

第4步，浏览器获取服务器发来的pubkey，计算出另一个pubkey，发给服务器。

第5步，服务器发给浏览器一个session ticket。

![](https://i.loli.net/2019/01/19/5c4294c4a2798.jpg)

## TLS解密
我们现在获取到的Wireshark抓包数据在握手完成之后，还是各种TLSv1.2的东东，都是加密后的数据。

![](https://i.loli.net/2019/01/19/5c42951c4a9a7.jpg)

解密方式有好几种，介绍我觉得最简单的，通过浏览器保存的TLS 会话中使用的对称密钥来进行数据解密。

在浏览器接收到数据之后，会使用秘钥对数据进行解密，部分浏览器会在某个地方会存储这个密钥，我们只要获取浏览器中的会话密钥就能解密数据。

### windows配置sslkeylog.log到wireshark

以windows系统+Chrome浏览器为例，首先要导出浏览器存储的密钥，通过计算机属性—>高级系统设置—>环境变量，新建一个变量名“SSLKEYLOGFILE”的变量，变量值是导出的密钥具体文件地址。

![](https://i.loli.net/2019/01/19/5c4295b3d6ad8.jpg)

设置后可以通过Chrome浏览器打开任意一个HTTPS网址，此时查看变量值对应路径，已经生成sslkey.log

![](https://i.loli.net/2019/01/19/5c4295d425b4b.jpg)

### mac配置sslkeylog.log到wireshark
```bash
# mac 获取sslkeylog.log
1. 查找浏览器所在位置
# 可以找到binary所在路径为/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
$ sudo find / -iname "Google Chrome"
2. 运行chrome并指定sslkey logfile, 来获取sslkeylog文件
$ sudo /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --ssl-key-log-file=/Users/afa/sslkeylog.log
3. 启动wireshark，并配置sslkey文档
菜单栏 -> Wireshark -> Preferences -> Protocols -> SSL
在(Pre)-Master-Secret log filename填入刚才启动时指定的文档路径，如图

# 跟踪ssl stream
访问https站点， 然后在wireshark中过滤栏输入ssl，随便找个包
右键 -> Follow -> SSL Stream
即可看到解密后的http请求。
```
![](https://i.loli.net/2019/01/19/5c429bed621fe.png)

### 重点抓手机tls包并解密
```bash
# 重点抓手机tls包
1. 可以先用charles抓取待抓取站点的单个https的url
2. 然后复制, 并放置mac chrome上(刚刚打开的制定sslkeylog路径的chrome)进行请求以获取对应的sslkeylog.log文件
```
![](https://i.loli.net/2019/01/19/5c42a0c2b5dd8.png)

然后就会有相对应的SSLKEY数据保存下来了，可以去看看这个信息：

![](https://i.loli.net/2019/01/19/5c42a0d79d34c.png)

密钥成功导出到本地啦。

现在可以将密钥应用到Wireshark了。

具体路径如下：菜单栏Edit—>Preferences—>Protocols—>SSL（注意，不论是SSL还是TLS这里都是SSL，没有单独的TLS选项），在(Pre)-Master-Secretlog filename中选择刚才设置的变量值。

![](https://i.loli.net/2019/01/19/5c429618238e9.jpg)

配置完成，看下效果：

![](https://i.loli.net/2019/01/19/5c42963fdda15.jpg)

看到有HTTP了，之前都是TLSv1.2。同时，WireShark下面会有一个“Decrypted SSL data”即已解密的SSL Data的标签，点击之后你就可以如上图所示的看到已经解密的TLS数据包的相信信息了。

觉得这样太难看了？OK，也可以像HTTP一样，通过鼠标右键在菜单栏中选择“Follow SSL Stream”，查看完整的HTTPS解密之后的请求数据哦。

![](https://i.loli.net/2019/01/19/5c42969cc62fa.jpg)

![](https://i.loli.net/2019/01/19/5c4296a711aba.jpg)

除此之外，上面还有很多TLSv1.2的东东，比如：client_key_exchange、Session Ticket，这是最初提到过的TLS握手过程的第四步和第五步，并不是请求数据包的内容，因此看到其中像是没有解密的内容也不要奇怪哦。

![](https://i.loli.net/2019/01/19/5c4296c8af3cd.jpg)




