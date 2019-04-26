# SSL
SSL协议分为SSL记录协议层和SSL握手协议层。SSL握手协议建立在SSL记录协议之上，用于在实际的数据传输开始前，通讯双方进行身份认证、协商加密算
法、交换加密密钥等。

SSL记录协议将数据块进行拆分压缩，计算消息验证码，加密，封装记录头然后进行传输。如下图显示
![](https://i.loli.net/2019/01/19/5c42940d21ddd.jpg)

## python 模拟ssl请求
[ssl_client.py](https://github.com/BeginMan/pytool/blob/master/unp/ssl_demo/ssl_client.py)
