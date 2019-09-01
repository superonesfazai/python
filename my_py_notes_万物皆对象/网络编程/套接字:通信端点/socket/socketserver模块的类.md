```bash
BaseServer                              # 包含服务器的核心功能和混合(mix-in)类挂钩;
                                        # 这个类只用于派生,所以不会生成这个类的实例
                                        # 可以考虑使用TCPServer和UDPServer
TCPServer/UDPServer                     # 基本的网络同步TCP/UDP服务器
UnixStreamServer/UnixDatagramServer     # 基本的基于文件同步的TCP/UDP服务器
ForkingMixIn/ThreadingMixIn             # 实现核心的进程化或线程化的功能;
                                        # 作为混合类,与服务类一并使用以提供一些异步特性; 这个类不会直接实例化
ForkingTCPServer/ForkingUDPServer       # ForkingMixIn和TCPServer/UDPServer的组合
ThreadingTCPServer/ThreadingUDPServer   # ThreadingMixIn和TCPServer/UDPServer的组合
BaseRequestHandler                      # 包含处理服务请求的核心功能,这个类只用于派生
                                        # 所以不会生成这个类的实例可以考虑使用StreamRequestHandler或DatagramRequestHandler
StreamRequestHandler/DatagramRequestHandler     # 用于TCP/UDP服务器处理的工具
```
