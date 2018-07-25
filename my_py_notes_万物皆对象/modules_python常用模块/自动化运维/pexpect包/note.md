# 系统批量运维管理器pexpect
pexpect可以理解为Linux下的expect的python封装, 

通过pexpect我们可以实现对ssh, ftp, passwd, telnet等命令行进行自动化交互, 而达到自动化的目的

```html
pexpect的几个核心组件:
1. spawn类(func: 启动和控制子应用程序)
2. run函数(func: 调用外部命令的函数, 类似于os.system, 不同的是: run()可同时获得命令的输出结果及命令的退出状态)
3. 派生类pxssh(func: 针对ssh回话操作的进一步封装)
```