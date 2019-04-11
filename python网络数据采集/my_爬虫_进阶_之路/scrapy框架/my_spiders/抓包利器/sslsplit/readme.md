# sslsplit
mitmproxy对https连接的数据抓取很完美。但是，它不能理解其他基于TLS/SSL的流量，比如FTPS, SMTP over SSL, IMAP over SSL等。

SSLsplit是针对SSL / TLS加密网络连接的中间人攻击的工具。它旨在用于网络取证，应用程序安全性分析和渗透测试。

SSLsplit旨在透明地终止使用网络地址转换引擎重定向到它的连接。然后SSLsplit终止SSL / TLS并启动到原始目标地址的新SSL / TLS连接，同时记录所有传输的数据。除了基于NAT的操作，SSLsplit还支持静态目的地并使用SNI指示的服务器名称作为上游目的地。SSLsplit纯粹是一个透明的代理，不能充当浏览器中配置的HTTP或SOCKS代理。

SSLsplit支持IPv4和IPv6上的纯TCP，纯SSL，HTTP和HTTPS连接。它还能够动态地将普通TCP升级到SSL，以便一般性地支持SMTP STARTTLS和类似的升级机制。SSLsplit完全支持服务器名称指示（SNI），并且能够使用RSA，DSA和ECDSA密钥以及DHE和ECDHE密码套件。根据构建的OpenSSL版本，SSLsplit还支持SSL 3.0，TLS 1.0，TLS 1.1和TLS 1.2，以及可选的SSL 2.0。

对于SSL和HTTPS连接，SSLsplit即时生成并签署伪造的X509v3证书，模仿原始服务器证书的主题DN，subjectAltName扩展名和其他特征。SSLsplit能够使用私钥可用的现有证书，而不是生成伪造的证书。SSLsplit支持NULL前缀CN证书，但不会对SSL / TLS堆栈中的特定证书验证漏洞实施漏洞利用。

## 安装
mac
```bash
$ brew install sslsplit
```

## 生成ca证书
```bash
$ openssl genrsa -out ca.key 4096
$ openssl req -new -x509 -days 1826 -key ca.key -out ca.crt
```
第1个命令，生成 4096位的RSA私钥（以pem格式保存) ca.key

第2个命令， 使用这个刚生成的私钥，来生成一个 自签名的 root CA 证书(ca.crt)
这两个文件在后面都会用到。只有ca.crt这个证书文件，需要安装 到浏览器，或者受害者的机器上。
```bash
afa@appledeiMac-2:~/Desktop|⇒  openssl req -new -x509 -days 1826 -key ca.key -out ca.crt
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) []:fz
State or Province Name (full name) []:fzhook
Locality Name (eg, city) []:hangzhou
Organization Name (eg, company) []:zy
Organizational Unit Name (eg, section) []:unit
Common Name (eg, fully qualified host name) []:fzhost
Email Address []:superonesfazai@gmail.com
```

## 启用IP转发和NAT引擎
假设SSLsplit运行在两个端口 8080用作非SSL的TCP连接，比如 http, smtp, ftp
8443 用作SSL的连接，比如SMTP over SSL, HTTPS等
为了转发 到达攻击者机器的IP到 互联网上的端口，可以这么设置

```bash
sysctl -w net.inet.ip.forwarding=1
iptables -t nat -F
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080
iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-ports 8443
iptables -t nat -A PREROUTING -p tcp --dport 587 -j REDIRECT --to-ports 8443
iptables -t nat -A PREROUTING -p tcp --dport 465 -j REDIRECT --to-ports 8443
iptables -t nat -A PREROUTING -p tcp --dport 993 -j REDIRECT --to-ports 8443
iptables -t nat -A PREROUTING -p tcp --dport 5222 -j REDIRECT --to-ports 8080
```

## 运行SSLsplit
```bash
$ ./sslsplit
  -D
  -l connections.log
  -j /tmp/sslsplit/
  -S logdir/
  -k ca.key
  -c ca.cer
   ssl 0.0.0.0 8443
   tcp 0.0.0.0 8080
```
-D 调试模式(运行于前台, 详细输出信息)
-l 日志文件
-j 连接的内容保存目录
-S