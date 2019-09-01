## 数据属性
```bash
AF_UNIX, AF_INET, AF_INET6      python支持的套接字地址家族
SO_STREAM, SO_DGRAM             套接字类型(TCP = 流, UDP = 数据报)
has_ipv6                        表示是否支持ipv6的布尔型标志
```

### 异常
```bash
error       # 套接字相关错误
herror      # 主机和地址相关错误
gaierror    # 地址相关错误
timeout     # 超时
```

### 函数
```bash
socket()                                    # 用指定的地址家族,套接字类型和协议类型创建一个套接字对象
socketpair()                                # 用指定的地址家族,套接字类型和协议类型创建一对套接字对象
fromfd()                                    # 用一个已经打开的文件描述符创建一个套接字对象
ssl()                                       # 在套接字上发起一个安全套接字层(SSL), 不做证书验证
getaddrinfo()                               # 得到地址信息
getfqdn()                                   # 返回完整的域的名字
gethostname()                               # 得到当前主机
gethostbyname()                             # 由主机名得到对应的ip地址
gethostbyname_ex()                          # gethostbyname()的扩展版本,返回主机名,主机所有别名和ip列表
gethostbyaddr()                             # 由ip得到dns信息, 返回一个类似gethostbyname_ex()的3元组
getprotobyname()                            # 由协议名(eg:'tcp')得到对应的号码
getservbyname()/getservbyport()             # 由服务名得到对应的端口号或反之; 两个函数中协议名都是可选的
ntohl()/ntohs()                             # 把一个整型由网络字节序转换为主机字节序
htonl()/htons()                             # 把一个整型由主机字节序转换为网络字节序
inet_aton()/inet_ntoa()                     # 把ip转换为32位整型,或反之(仅对ipv4地址有效)
inet_pton()/inet_ntop()                     # 把ip地址转换为二进制格式,或反之(对ipv4和ipv6地址都有效)
getdefaulttimeout()/setdefaulttimeout()     # 得到/设置默认的套接字超时时间,单位秒(浮点型)
```