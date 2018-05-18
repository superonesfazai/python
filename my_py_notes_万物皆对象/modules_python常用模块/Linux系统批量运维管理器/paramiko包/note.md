# 系统批量运维管理器paramiko详解
paramiko是基于ssh2远程安全连接, 支持认证及密钥方式，相对于pexpect封装层次更高, 更接近于ssh协议功能

```html
paramiko的两个核心组件:
1. SSHClient类
2. SFTPClient类
```